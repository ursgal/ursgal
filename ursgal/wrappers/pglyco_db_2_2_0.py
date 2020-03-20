#!/usr/bin/env python
import ursgal
import os
from collections import defaultdict as ddict
import csv
import itertools
import sys

class pglyco_db_2_2_0(ursgal.UNode):
    """
    Unode for pGlyco 2.2.0
    For furhter information see: https://github.com/pFindStudio/pGlyco2

    Note:
        Please download pGlyco 2.2.0 manually from
        https://github.com/pFindStudio/pGlyco2

    Reference:
    Liu MQ, Zeng WF,, Fang P, Cao WQ, Liu C, Yan GQ, Zhang Y, Peng C, Wu JQ,
    Zhang XJ, Tu HJ, Chi H, Sun RX, Cao Y, Dong MQ, Jiang BY, Huang JM, Shen HL,
    Wong CCL, He SM, Yang PY. (2017) pGlyco 2.0 enables precision N-glycoproteomics
    with comprehensive quality control and one-step mass spectrometry
    for intact glycopeptide identification.
    Nat Commun 8(1)
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'pGlyco',
        'version': '2.2.0',
        'release_date': '2019-01-01',
        'utranslation_style': 'pglyco_db_style_1',
        'input_extensions': ['.mgf'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': True,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'engine': {
            'win32' : {
                '64bit' : {
                    'exe'            : 'pGlycoDB.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation':
        'Liu MQ, Zeng WF,, Fang P, Cao WQ, Liu C, Yan GQ, Zhang Y, Peng C, Wu JQ,'
            'Zhang XJ, Tu HJ, Chi H, Sun RX, Cao Y, Dong MQ, Jiang BY, Huang JM, Shen HL,'
            'Wong CCL, He SM, Yang PY. (2017) pGlyco 2.0 enables precision N-glycoproteomics '
            'with comprehensive quality control and one-step mass spectrometry'
            'for intact glycopeptide identification.'
            'Nat Commun 8(1)'
    }

    def __init__(self, *args, **kwargs):
        super(pglyco_db_2_2_0, self).__init__(*args, **kwargs)
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
            + '_pGlyco.cfg'
        )
        # self.created_tmp_files.append(self.param_file_name)

        # pprint.pprint(self.params['translations']['_grouped_by_translated_key'])
        # pprint.pprint(self.params)
        # sys.exit(1)
        self.params_to_write = {
            'output_dir_path' : self.params['output_dir_path'],
            'input_file' : self.params['translations']['mgf_input_file'],
        }

        precursor_tolerance = []
        opt_mods = []
        fix_mods = []
        for pglyco_param_name in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][pglyco_param_name].items():
                # if pglyco_param_name in write_exclusion_list:
                #     continue
                if pglyco_param_name == 'search_precursor_tolerance':
                    precursor_tolerance.append(param_value)
                elif pglyco_param_name == 'modifications':
                    # fix_total=
                    # fix1=Carbamidomethyl[C]
                    # var_total=
                    # var1=Oxidation[M]
                    # var2=Acetyl[ProteinN-term]
                    sum_opt_mods = 0
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
                            mod_dict['pos'] = 'ProteinN-term'
                        elif mod_dict['pos'] == 'Prot-C-term':
                            mod_dict['pos'] = 'ProteinC-term'
                        elif mod_dict['pos'] == 'N-term':
                            mod_dict['pos'] = 'AnyN-term'
                        elif mod_dict['pos'] == 'C-term':
                            mod_dict['pos'] = 'AnyC-term'
                        elif mod_dict['pos'] == 'any':
                            pass
                        else:
                            print(
                                '''
                            Unknown positional argument for given modification:
                            {0}
                            pGlyco (or Ursgal) cannot deal with this, please use one of the follwing:
                            any, Prot-N-term, Prot-C-term, N-term, C-term
                            '''.format(mod_dict['org'])
                            )
                            sys.exit(1)
                        sum_opt_mods += 1
                        if 'term' in mod_dict['pos']:
                            if mod_dict['aa'] == '*':
                                mod_dict['aa'] = ''
                            opt_mods.append('var{0}={1}[{2}{3}]'.format(
                                sum_opt_mods,
                                mod_dict['name'],
                                mod_dict['pos'],
                                mod_dict['aa'],
                            ))
                        else:
                            if mod_dict['aa'] == '*':
                                print('''
                                Not sure how to handle this modification in pGlyco:
                                {0}
                                '''.format(mod_dict['org']))
                                sys.exit(1)
                            opt_mods.append('var{0}={1}[{2}]'.format(
                                sum_opt_mods,
                                mod_dict['name'],
                                mod_dict['aa'],
                            ))

                    sum_fix_mods = 0
                    for mod_dict in self.params['mods']['fix']:
                        if mod_dict['pos'] == 'Prot-N-term':
                            mod_dict['pos'] = 'ProteinN-term'
                        elif mod_dict['pos'] == 'Prot-C-term':
                            mod_dict['pos'] = 'ProteinC-term'
                        elif mod_dict['pos'] == 'N-term':
                            mod_dict['pos'] = 'AnyN-term'
                        elif mod_dict['pos'] == 'C-term':
                            mod_dict['pos'] = 'AnyC-term'
                        elif mod_dict['pos'] == 'any':
                            pass
                        else:
                            print(
                                '''
                            Unknown positional argument for given modification:
                            {0}
                            pGlyco (or Ursgal) cannot deal with this, please use one of the follwing:
                            any, Prot-N-term, Prot-C-term, N-term, C-term
                            '''.format(mod_dict['org'])
                            )
                            sys.exit(1)
                        sum_fix_mods += 1
                        if 'term' in mod_dict['pos']:
                            if mod_dict['aa'] == '*':
                                mod_dict['aa'] = ''
                            fix_mods.append('fix{0}={1}[{2}{3}]'.format(
                                sum_fix_mods,
                                mod_dict['name'],
                                mod_dict['pos'],
                                mod_dict['aa'],
                            ))
                        else:
                            if mod_dict['aa'] == '*':
                                print('''
                                Not sure how to handle this modification in pGlyco:
                                {0}
                                '''.format(mod_dict['org']))
                                sys.exit(1)
                            fix_mods.append('fix{0}={1}[{2}]'.format(
                                sum_fix_mods,
                                mod_dict['name'],
                                mod_dict['aa'],
                            ))
                else:
                    self.params_to_write[pglyco_param_name] = param_value
        assert len(precursor_tolerance) == 2, '''
        Both, precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
        need to be given. Received: {0}
        '''.format(precursor_tolerance)
        self.params_to_write['precursor_tolerance'] = sum(precursor_tolerance) / 2.0
        self.params_to_write['sum_fixed_mods'] = sum_fix_mods
        self.params_to_write['sum_opt_mods'] = sum_opt_mods
        self.params_to_write['fix_mods'] = '\n'.join(fix_mods)
        self.params_to_write['opt_mods'] = '\n'.join(opt_mods)
        
        self.write_params_file()

        self.params['command_list'] = [
            self.exe,
            self.param_file_name,
        ]

        return self.params

    def postflight(self):
        # '''
        # Reads pGlyco txt output and write final csv output file.

        # Adds:
        #     * Raw data location, since this can not be added later

        # '''
        pglyco_header = [
            'GlySpec',
            'PepSpec',
            'RawName',
            'Scan',
            'RT',
            'PrecursorMH',
            'PrecursorMZ',
            'Charge',
            'Rank',
            'Peptide',
            'Mod',
            'PeptideMH',
            'Glycan(H,N,A,G,F)',
            'PlausibleStruct',
            'GlyID',
            'GlyFrag',
            'GlyMass',
            'GlySite',
            'TotalScore',
            'PepScore',
            'GlyScore',
            'CoreMatched',
            'CoreFuc',
            'MassDeviation',
            'PPM',
            'GlyIonRatio',
            'PepIonRatio',
            'GlyDecoy',
            'PepDecoy',
        ]

        translated_headers = []
        header_translations = self.UNODE_UPARAMS[
            'header_translations']['uvalue_style_translation']
        for original_header_key in pglyco_header:
            ursgal_header_key = header_translations[original_header_key]
            if ursgal_header_key not in translated_headers:
                translated_headers.append(ursgal_header_key)

        translated_headers += [
            'Raw data location',
        ]

        csv_kwargs = {}
        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'
        csv_writer = csv.DictWriter(
            open(self.params['translations']['output_file_incl_path'], 'w'),
            fieldnames=translated_headers,
            **csv_kwargs
        )

        pglyco_output = os.path.join(
            self.params['output_dir_path'],
            'pGlycoDB-GP.txt'
        )
        translated_headers.insert(0, 'Spectrum Title')
        translated_headers.insert(0, 'Spectrum Title')
        csv_reader = csv.DictReader(
            open(pglyco_output, 'r'),
            fieldnames=translated_headers,
            delimiter='\t',
        )
        # self.created_tmp_files.append(pglyco_output)

        csv_writer.writeheader()
        for n, line_dict in enumerate(csv_reader):
            if n == 0:
                continue
            line_dict['Raw data location'] = os.path.abspath(
                self.params['translations']['mgf_input_file']
            )
            csv_writer.writerow(line_dict)
        return

    def write_params_file(self):
        with open(self.param_file_name, 'w') as io:
            print('''[version]
pGlyco_version=pGlyco_Tag20190101
[flow]
glyco_type=N-Glyco
glycandb=pGlyco.gdb
process={process}
output_dir={output_dir_path}
[protein]
fasta={fasta}
enzyme={enzyme}
digestion=not_support_in_cur_version
max_miss_cleave={max_miss_cleave}
max_peptide_len={max_peptide_len}
min_peptide_len={min_peptide_len}
max_peptide_weight={max_peptide_weight}
min_peptide_weight={min_peptide_weight}
[modification]
fix_total={sum_fixed_mods}
{fix_mods}
max_var_modify_num={max_var_modify_num}
var_total={sum_opt_mods}
{opt_mods}
[search]
search_precursor_tolerance={precursor_tolerance}
search_precursor_tolerance_type={search_precursor_tolerance_type}
search_fragment_tolerance={search_fragment_tolerance}
search_fragment_tolerance_type={search_fragment_tolerance_type}
spec_file_type=mgf
spectrum_total=1
file1={input_file}
'''.format(
                **self.params_to_write),
                file=io
            )
        return
