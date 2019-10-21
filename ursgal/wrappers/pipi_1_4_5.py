#!/usr/bin/env python
import ursgal
import os
from collections import defaultdict as ddict
import csv
import itertools
import sys

class pipi_1_4_5(ursgal.UNode):
    """
    Unode for PIPI: PTM-Invariant Peptide Identification
    For furhter information see: http://bioinformatics.ust.hk/pipi.html

    Note:
        Please download and extract PIPI manually from 
        http://bioinformatics.ust.hk/pipi.html

    Reference:
    Yu, F., Li, N., Yu, W. (2016) PIPI: PTM-Invariant Peptide Identification 
    Using Coding Method. J Prot Res 15(12)
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'PIPI',
        'version': '1.4.5',
        'release_date': '2018-06-20',
        'utranslation_style': 'pipi_style_1',
        'input_extensions': ['.mgf', '.mzML', '.mzXML'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': True,
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'engine': {
            'platform_independent': {
                'arc_independent': {
                    'exe': 'PIPI-1.4.5.jar',
                    'url': 'http://bioinformatics.ust.hk/pipi.html',
                    'zip_md5' : 'f28bf201a1d71da257e0035cf3a95823',
                    'additional_exe': [],
                },
            },
        },
        'citation':
        'Yu, F., Li, N., Yu, W. (2016) PIPI: PTM-Invariant '
            'Peptide Identification Using Coding Method. '
            'J Prot Res 15(12)'
    }

    def __init__(self, *args, **kwargs):
        super(pipi_1_4_5, self).__init__(*args, **kwargs)
        pass

    def preflight(self):
        '''
        Formatting the command line and writing the param input file via 
        self.params

        Returns:
                dict: self.params
        '''
        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        self.param_file_name = os.path.join(
            self.params['translations']['output_file_incl_path'].strip('.csv')
            + 'pipi_params.def'
        )
        self.created_tmp_files.append(self.param_file_name)

        # pprint.pprint(self.params['translations']['_grouped_by_translated_key'])
        # pprint.pprint(self.params)
        # sys.exit(1)
        self.params_to_write = {
            'version': self.META_INFO['version'],
            'output_percolator_input': 1,
            'mod10': '0.0@X?',
            'pepNterm': 0.0,
            'pepCterm': 0.0,
            'proNterm': 0.0,
            'proCterm': 0.0,
        }
        symbols = ['~', '!', '%', '^', '&', '*', '+', '<', '>']
        for x, element in enumerate(symbols):
            self.params_to_write[
                'mod0{0}'.format(x + 1)
            ] = '0.0@X{0}'.format(element)
        for aa in 'ACDEFGHIKLMNOPQRSTUVWYnc':
            self.params_to_write[aa] = 0

        write_exclusion_list = [
            # 'label',
            '-Xmx',
            'frag_mass_tolerance_unit',
            'base_mz',
            # 'header_translations',
            # 'validation_score_field'
        ]

        # additional_15N_modifications = []
        # if self.params['translations']['label'] == '15N':
        #     for aminoacid, N15_Diff in ursgal.ukb.DICT_15N_DIFF.items():
        #         existing = False
        #         for mod_dict in self.params['mods']['fix']:
        #             if aminoacid == mod_dict['aa']:
        #                 mod_dict['mass'] += N15_Diff
        #                 mod_dict['name'] += '_15N_{0}'.format(aminoacid)
        #                 existing = True
        #         if existing == True:
        #             continue
        #         else:
        #             self.params['mods']['fix'].append(
        #                 {
        #                     'aa': aminoacid,
        #                     'mass': N15_Diff,
        #                     'name': '_15N_{0}'.format(aminoacid),
        #                     'pos': 'any',
        #                 }
        #             )

        if self.params['translations']['frag_mass_tolerance_unit'] == 'ppm':
            self.params['translations']['_grouped_by_translated_key']['ms2_tolerance'] = {
                'frag_mass_tolerance': ursgal.ucore.convert_ppm_to_dalton(
                    self.params['translations']['frag_mass_tolerance'],
                    base_mz=self.params['base_mz']
                )
            }

        for pipi_param_name in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][pipi_param_name].items():
                if pipi_param_name in write_exclusion_list:
                    continue
                elif pipi_param_name == 'frag_clear_mz_range':
                    min_mz, max_mz = param_value
                    self.params_to_write['min_clear_mz'] = min_mz
                    self.params_to_write['max_clear_mz'] = max_mz
                elif type(pipi_param_name) is tuple:
                    for pn in pipi_param_name:
                        self.params_to_write[pn] = param_value
                elif pipi_param_name == 'enzyme':
                    enz, site, aa, inh = param_value.split(';')
                    self.params_to_write['enzyme'] = '{0} {1} {2} {3}'.format(
                        enz,
                        site,
                        aa,
                        inh
                    )
                elif pipi_param_name == 'modifications':
                    '''
                    # specify additional mass and amino acid. DO NOT change the last character.
                    # maximum number is 10
                    # empty entries must start with 0.0
                    mod01 = 79.966331@S~ # Phosphorylation
                    mod02 = 79.966331@T! # Phosphorylation
                    mod03 = 79.966331@Y% # Phosphorylation
                    mod04 = 42.010565@K^ # Acetylation
                    mod05 = 15.994915@M& # Oxidation
                    mod06 = 14.015650@K* # Methylation
                    mod07 = 0.0@X+
                    mod08 = 0.0@X<
                    mod09 = 0.0@X>
                    mod10 = 0.0@X?
                    '''
                    n = 0
                    for mod_dict in self.params['mods']['opt']:
                        '''
                        {'_id': 0,
                          'aa': '*',
                          'composition': {'C': 2, 'H': 2, 'O': 1},
                          'id': '1',
                          'mass': 42.010565,
                          'name': 'Acetyl',
                          'org': '*,opt,Prot-N-term,Acetyl',
                          'pos': 'Prot-N-term',
                          'unimod': True},
                        '''
                        if mod_dict['pos'] == 'Prot-N-term':
                            self.params_to_write['proNterm'] = mod_dict['mass']
                            continue
                        elif mod_dict['pos'] == 'Prot-C-term':
                            self.params_to_write['proCterm'] = mod_dict['mass']
                            continue
                        elif mod_dict['pos'] == 'N-term':
                            self.params_to_write['pepNterm'] = mod_dict['mass']
                            continue
                        elif mod_dict['pos'] == 'C-term':
                            self.params_to_write['pepCterm'] = mod_dict['mass']
                            continue
                        elif mod_dict['pos'] == 'any':
                            pass
                        else:
                            print(
                                '''
                            Unknown positional argument for given modification:
                            {0}
                            PIPI cannot deal with this, please use one of the follwing:
                            any, Prot-N-term, Prot-C-term, N-term, C-term
                            '''.format(mod_dict['org'])
                            )
                            sys.exit(1)
                        n += 1
                        assert n <= 10, '''
                        A maximum of 10 optional modifications is allowed in PIPI.
                        You specified more than 10.
                        '''
                        if n < 10:
                            mod_n = 'mod0{0}'.format(n)
                        elif n == 10:
                            mod_n = 'mod{0}'.format(n)
                        else:
                            print('''
                                A maximum of 10 optional modifications is allowed in PIPI.
                                You specified more than 10.
                            ''')
                            sys.exit(1)
                        self.params_to_write[mod_n] = '{0}@{1}{2}'.format(
                            mod_dict['mass'],
                            mod_dict['aa'],
                            symbols[n - 1]
                        )

                    for mod_dict in self.params['mods']['fix']:
                        if 'N-term' in mod_dict['pos']:
                            self.params_to_write['n'] = mod_dict['mass']
                        elif 'C-term' in mod_dict['pos']:
                            self.params_to_write['c'] = mod_dict['mass']
                        else:
                            self.params_to_write[
                                mod_dict['aa']] = mod_dict['mass']
                else:
                    self.params_to_write[pipi_param_name] = param_value
        self.write_params_file()

        self.params['command_list'] = [
            'java',
            '-Xmx{0}'.format(self.params['translations']
                             ['_grouped_by_translated_key']['-Xmx']['-xmx']),
            '-jar',
            self.exe,
            self.param_file_name,
            self.params['translations']['mgf_input_file']
        ]

        return self.params

    def postflight(self):
        # '''
        # Reads PIPI csv output and write final csv output file.

        # Adds:
        #     * Raw data location, since this can not be added later

        # '''
        pipi_fragger_header = [
            'scan_num',
            'peptide',
            'charge',
            'theo_mass',
            'exp_mass',
            'abs_ppm',
            'A_score',
            'protein_ID',
            'score',
            'delta_C_n',
            'other_PTM_patterns',
            'MGF_title',
            'labelling',
            'isotope_correction',
            'MS1_pearson_correlation_coefficient',
            # 'ptm_delta_score',
            # 'naive_q_value',
            # 'percolator_score',
            # 'posterior_error_prob',
            # 'percolator_q_value',
        ]

        translated_headers = []
        header_translations = self.UNODE_UPARAMS[
            'header_translations']['uvalue_style_translation']
        for original_header_key in pipi_fragger_header:
            ursgal_header_key = header_translations[original_header_key]
            translated_headers.append(ursgal_header_key)

        translated_headers += [
            'Raw data location',
            'Modifications',
            'Mass Difference',
        ]

        csv_writer = csv.DictWriter(
            open(self.params['translations']['output_file_incl_path'], 'w'),
            fieldnames=translated_headers
        )
        new_label = ""
        if self.params['label'] == '14N':
            new_label = 'N14'

        if self.params['label'] == '15N':
            new_label = 'N15'

        pipi_output = self.params['translations'][
            'mgf_input_file'] + '.{0}.pipi.csv'.format(new_label)
        csv_reader = csv.DictReader(
            open(pipi_output, 'r'),
            fieldnames=translated_headers,
        )
        # self.created_tmp_files.append(pipi_output)
        # self.created_tmp_files.append(pipi_output.replace('.pipi.csv', '.pipi.pep.xml'))
        # self.created_tmp_files.append(pipi_output.replace('.pipi.csv', '.input.temp'))

        csv_writer.writeheader()
        for n, line_dict in enumerate(csv_reader):
            if n == 0:
                continue
            # try:
            #     float(line_dict['PIPI:score'])
            # except:
            #     line_dict['Protein ID'] += line_dict['PIPI:score']
            #     line_dict['PIPI:score'] = line_dict['PIPI:delta_C_n']
            #     line_dict['PIPI:delta_C_n'] = line_dict['PIPI:other_PTM_patterns']
            #     line_dict['PIPI:other_PTM_patterns'] = line_dict['Spectrum Title']
            #     line_dict['Spectrum Title'] = line_dict['label']
            #     line_dict['label'] = line_dict['PIPI:isotope_correction']
            #     line_dict['PIPI:isotope_correction'] = line_dict['PIPI:MS1_pearson_correlation_coefficient']
            #     line_dict['PIPI:MS1_pearson_correlation_coefficient'] = line_dict['Raw data location']
            line_dict['Raw data location'] = os.path.abspath(
                self.params['translations']['mgf_input_file']
            )

        #     ############################################
        #     # all fixing here has to go into unify csv! #
        #     ############################################

            tmp_seq = ''
            tmp_mods = []
            line_dict['Sequence'] = line_dict['Sequence'].replace('n', '')
            for part in line_dict['Sequence'].split('('):
                if ')' in part:
                    mod, seq = part.split(')')
                    tmp_mods.append(
                        '{0}:{1}'.format(mod, len(tmp_seq))
                    )
                    tmp_seq += seq
                else:
                    tmp_seq += part
            tmp_seq = tmp_seq.replace('c', '')
            line_dict['Sequence'] = tmp_seq
            line_dict['Modifications'] = ';'.join(tmp_mods)
            csv_writer.writerow(line_dict)
        return

    def write_params_file(self):
        with open(self.param_file_name, 'w') as io:
            print('''# {version}
# First line is the parameter file version. Don't change it.
thread_num = {thread_num}
percolator_path = ursgal/resources/darwin/64bit/percolator_2_08/percolator_2_08

# Database
db = {db}
database_type = Others # Different types have different fasta header patterns. Available values: UniProt, SwissProt, TAIR, ITAG, RefSeq, Others
missed_cleavage = {missed_cleavage}
min_peptide_length = {min_peptide_length}
max_peptide_length = {max_peptide_length}
add_decoy = {add_decoy} # 0 = don't generate and search decoy sequences automatically; 1 = generate and search decoy sequences
add_contaminant = {add_contaminant} # 0 = don't add contaminant proteins automatically; 1 = add contaminant proteins

# Spectrum
ms_level = {ms_level}

# Tolerance
ms1_tolerance_unit = {ms1_tolerance_unit}
ms1_tolerance = {ms1_tolerance}
ms2_tolerance = {ms2_tolerance}
mz_bin_offset = {mz_bin_offset}
min_clear_mz = {min_clear_mz}
max_clear_mz = {max_clear_mz}

# Modification related
min_ptm_mass = {min_ptm_mass}
max_ptm_mass = {max_ptm_mass}

# Isotopic labelling strategy
15N = {15N} # 1: 15N. 0: 14N.

# considered modifications in generating tags
# specify additional mass and amino acid. DO NOT change the last character.
# maximum number is 10
# empty entries must start with 0.0
mod01 = {mod01}
mod02 = {mod02}
mod03 = {mod03}
mod04 = {mod04}
mod05 = {mod05}
mod06 = {mod06}
mod07 = {mod07}
mod08 = {mod08}
mod09 = {mod09}
mod10 = {mod10}

# considered peptide/protein N/C-terminal modifications in generating tags
# empty ones must with value 0.0
# the maximum number for each terminal is 9
Nterm = {pepNterm}
Cterm = {pepCterm}

# Fix modification
G = {G}
A = {A}
S = {S}
P = {P}
V = {V}
T = {T}
C = {C}
I = {I}
L = {L}
N = {N}
D = {D}
Q = {Q}
K = {K}
E = {E}
M = {M}
H = {H}
F = {F}
R = {R}
Y = {Y}
W = {W}
O = {O}
U = {U}
n = {n}
c = {c}

# Enzyme digestion specificities
# enzyme name    is cut from C-term      cleavage site   protection site
{enzyme}

# Do not change the following
output_percolator_input = 1
'''.format(
                **self.params_to_write),
                file=io
            )
        return
