#!/usr/bin/env python3.4
import ursgal
import os
from collections import defaultdict as ddict
import csv
import itertools
import sys
import re

class pnovo_3_1_3(ursgal.UNode):
    """
    Unode for pNovo 3.1.3
    For furhter information see: http://pfind.ict.ac.cn/software/pNovo/
 
    Note:
        Please download pNovo 3.1.3 manually from
        http://pfind.ict.ac.cn/software/pNovo/#Downloads

    Reference:
    Yang, H; Chi, H; Zhou, W; Zeng, WF; He, K; Liu, C; Sun, RX; He, SM. (2017)
    Open-pNovo: De Novo Peptide Sequencing with Thousands of Protein Modifications.
    J Proteome Res. 16(2)
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'pNovo',
        'version': '3.1.3',
        'release_date': '2018-12-30',
        'utranslation_style': 'pnovo_style_1',
        'input_extensions': ['.mgf'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'de_novo_search_engine': True,
        },
        'engine': {
            'win32' : {
                '64bit' : {
                    'exe'            : 'pNovo3.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation':
        'Yang, H; Chi, H; Zhou, W; Zeng, WF; He, K; Liu, C; Sun, RX; He, SM. (2017)'
            'Open-pNovo: De Novo Peptide Sequencing with Thousands of Protein Modifications.'
            'J Proteome Res. 16(2)'
    }

    def __init__(self, *args, **kwargs):
        super(pnovo_3_1_3, self).__init__(*args, **kwargs)
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
            + '_pnovo.param'
        )
        # self.created_tmp_files.append(self.param_file_name)

        self.params_to_write = {
            'output_dir_path' : self.params['output_dir_path'],
            'input_file' : self.params['translations']['mgf_input_file'],
        }

        print(
            '''
            [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
            [ WARNING ] need to be combined for pNovo (use of symmetric tolerance window).
            [ WARNING ] The arithmetic mean is used.
            '''
        )
        self.params['translations']['_grouped_by_translated_key'][
            'pep_tol'] = {
                'precursor_mass_tolerance': ( float(self.params['precursor_mass_tolerance_plus']) + \
                                            float(self.params['precursor_mass_tolerance_minus']) ) \
                                            / 2.0
            }
        opt_mods = []
        fix_mods = []
        self.mod_lookup = {}
        for pnovo_param_name in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][pnovo_param_name].items():
                if pnovo_param_name == 'spec_path1':
                    self.params_to_write[pnovo_param_name] =  self.params['translations']['mgf_input_file'].replace('.mgf', '.ms2')
                    self.params_to_write['out_path'] =  os.path.dirname(
                        self.params['translations']['output_file_incl_path']
                    )
                elif pnovo_param_name == 'modifications':
                    #If you want to add a variable modification, 
                    #please use a letter from (a-z) instead.
                    #For example, if M+Oxidation is to be added,
                    #you can add the line below(without '#'), 
                    #in which 147.0354 = mass(M) + mass(Oxidation)

                    #a=147.0354
                    #b=160.030654
                    #N- or C- terminal variable modifications can be added as follows (using 0-9)

                    #c-term=0.984016

                    #A fixed modification can be added like (without '#'):

                    #C=160.030654
                    #in which 160.030654 = mass(C) + mass(Carbamidomethyl)

                    #FixMod Carbamidomethyl[C]  C
                    # C=160.030654 Carbamidomethyl[C]
                    #VarMod Oxidation[M]    M
                    # a=147.035405 Oxidation[M]
                    import string
                    alphabet = [x for x in string.ascii_lowercase]
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
                        if 'Prot' in mod_dict['pos']:
                            print(
                                '''
                            Protein N/C-terminal modifications are not supported by pNovo
                            Please change or delete the following modification:
                            {0}
                            '''.format(mod_dict['org'])
                            )
                            sys.exit(1)
                        elif mod_dict['pos'] == 'N-term':
                            mod_dict['pos'] = 'n-term'
                        elif mod_dict['pos'] == 'C-term':
                            mod_dict['pos'] = 'c-term'
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
                        cc = ursgal.ChemicalComposition()
                        if 'term' in mod_dict['pos']:
                            if mod_dict['aa'] != '*':
                                print('''
                                    Specific amino acids are not supported with terminal modifications
                                    in pNovo. Please change or delete the following modification:
                                    {0}
                                    '''.format(mod_dict['org'])
                                )
                                sys.exit(1)
                            opt_mods.append('{0}={1}'.format(
                                mod_dict['pos'],
                                mod_dict['mass'],
                            ))
                        else:
                            if mod_dict['aa'] == '*':
                                print('''
                                Not sure how to handle this modification in pNovo:
                                {0}
                                '''.format(mod_dict['org']))
                                sys.exit(1)
                            cc.use('{0}#{1}:1'.format(
                                mod_dict['aa'],
                                mod_dict['name']
                            ))
                            mod_dict['mass'] = cc._mass()
                            opt_mods.append('{0}={1} {2}[{3}]'.format(
                                alphabet[sum_opt_mods],
                                mod_dict['mass'],
                                mod_dict['name'],
                                mod_dict['aa'],
                            ))
                            self.mod_lookup[alphabet[sum_opt_mods]] = (mod_dict['name'], mod_dict['aa'])
                            sum_opt_mods += 1

                    for mod_dict in self.params['mods']['fix']:
                        if 'term' in mod_dict['pos']:
                            print(
                                '''
                            Fixed N/C-terminal modifications are not supported by pNovo
                            Please change or delete the following modification:
                            {0}
                            '''.format(mod_dict['org'])
                            )
                            sys.exit(1)
                        else:
                            cc = ursgal.ChemicalComposition()
                            cc.use('{0}#{1}:1'.format(
                                mod_dict['aa'],
                                mod_dict['name']
                            ))
                            mod_dict['mass'] = cc._mass()
                            opt_mods.append('{0}={1} {2}[{3}]'.format(
                                mod_dict['aa'],
                                mod_dict['mass'],
                                mod_dict['name'],
                                mod_dict['aa'],
                            ))
                else:
                    self.params_to_write[pnovo_param_name] = param_value
        self.params_to_write['FixMod'] = '\n'.join(fix_mods)
        self.params_to_write['VarMod'] = '\n'.join(opt_mods)
        
        self.write_params_file()

        self.params['command_list'] = [
            self.exe,
            self.param_file_name,
        ]
        print(' '.join(self.params['command_list']))
        return self.params

    def postflight(self):
        # '''
        # Reads pGlyco txt output and write final csv output file.

        # Adds:
        #     * Raw data location, since this can not be added later

        # '''
        pnovo_header = [
            'Rank',
            'Sequence',
            'pNovo:Score',
            'pNovo:Modification Abundance',
            'Mass Difference',
            'pNovo:Path Rank',
            'pNovo:Score main ions',
            'pNovo:Score internal ions',
            'pNovo:Continuity b ions',
            'pNovo:Continuity y ions',
            'pNovo:Enzyme score',
            'pNovo:Std. fragment mass deviations',
            'pNovo:Max. fragment mass deviations',
            'pNovo:Charge feature',
            'pNovo:Raw score',
            'pNovo:Spearman correlation of intensities',
            'pNovo:Gap feature',
            'pNovo:Gap feature N-term',
        ]

        new_header = pnovo_header + [
            'Raw data location',
            'Spectrum Title',
            'Exp m/z',
            'Modifications',
            'Charge',
            'Spectrum ID',
        ]

        csv_kwargs = {}
        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'
        csv_writer = csv.DictWriter(
            open(self.params['translations']['output_file_incl_path'], 'w'),
            fieldnames=new_header,
            **csv_kwargs
        )

        pnovo_output = os.path.join(
            self.params['output_dir_path'],
            'pnovo+',
            self.params['input_file'].replace('.mgf', '.txt')
        )
        csv_reader = csv.DictReader(
            open(pnovo_output, 'r'),
            fieldnames=pnovo_header,
            delimiter='\t',
        )
        # self.created_tmp_files.append(pnovo_output)
        

        csv_writer.writeheader()
        spec_title = None
        exp_mz = None
        for n, line_dict in enumerate(csv_reader):
            # if n == 0:
            #     continue
            if line_dict['Rank'] == '' or line_dict['Rank'] == 'time:':
                continue
            elif line_dict['Rank'].startswith('S'):
                spec_title = line_dict['Sequence']
                exp_mz = line_dict['pNovo:Score']
            else:
                line_dict['Spectrum Title'] = spec_title
                line_dict['Exp m/z'] = exp_mz
                line_dict['Raw data location'] = os.path.abspath(
                    self.params['translations']['mgf_input_file']
                )
                new_sequence = ''
                modifications = []
                for pos, aa in enumerate(line_dict['Sequence']):
                    if aa in self.mod_lookup.keys():
                        name, aa = self.mod_lookup[aa]
                        modifications.append('{0}:{1}'.format(
                            name,
                            pos+1
                        ))
                    else:
                        assert aa in ursgal.chemical_composition_kb.aa_compositions.keys(), '''
                        [ERROR] Unknown amino acid when trying to parse through pNovo output:
                        {0}
                        '''.format(aa)
                    new_sequence += aa
                line_dict['Sequence'] = new_sequence
                line_dict['Modifications'] = ';'.join(modifications)
                csv_writer.writerow(line_dict)
        return

    def write_params_file(self):
        with open(self.param_file_name, 'w') as io:
            print('''[meta]
#If you want to use Open search, you can set OpenModification 'true'
OpenModification=false
MergeResult=false

#The lines below show the basic ion types of HCD and ETD data.
HCDIONTYPE=4
HCDIONTYPE1=b   1 1 1 0.0
HCDIONTYPE2=y   1 0 1 18.0105647
HCDIONTYPE3=b   2 1 1 0.0
HCDIONTYPE4=y   2 0 1 18.0105647
ETDIONTYPE=6
ETDIONTYPE1=c 1 1 1 17.026549105
ETDIONTYPE2=z 1 0 1 1.99129206512
ETDIONTYPE3=c-1 1 1 0 16.01872407
ETDIONTYPE4=z+1 1 0 1 2.999665665
ETDIONTYPE5=c 2 1 0 17.026549105
ETDIONTYPE6=z 2 0 0 1.99129206512

#[IMPORTANT]
#An enzyme can be set as: 
#[EnzymeName] [CleavageSites] [N/C] (Cleave at N- or C- terminal)
enzyme={enzyme}

#if you want to use multi-threads, please set the number of threads below (1 ~ 8):
thread={thread}

#Mass ranges of precursors
#Only the spectra whose precursors are in the specified mass range will be sequenced.
mass_lower_bound={mass_lower_bound}
mass_upper_bound={mass_upper_bound}

#[HCD, CID, ETD]
activation_type={activation_type}

#[IMPORTANT]
#Tolerance of precursors. 
#If you want to use Daltons, please set 'pep_tol_type_ppm' as 0
pep_tol={pep_tol}
pep_tol_type_ppm={pep_tol_type_ppm}

#[IMPORTANT]
#Tolerance of fragment ions. 
#If you want to use Daltons, please set 'frag_tol_type_ppm' as 0
frag_tol={frag_tol}
frag_tol_type_ppm={frag_tol_type_ppm},

[file]

#DTA/MS2/MGF are valid options.if DTA is specified, 
#please set the following path(s) as the folder containing the DTA file(s)
spec_type=MS2

#1:means only one activation type, CID/HCD/ETD, is used
#       spec_path1 should be set as the path of the data
#2:(HCD + ETD) is used. In this case, activation_type is ignored.
#       spec_path1 should be set as the path of the HCD data,
#       and spec_path2 should be set as the path of the ETD data.
spec_path=1
spec_path1={spec_path1}

#If only one activation type of spectra is used (spec_path=1),
#you can specify a folder containing several MS2 or MGF files.
#Set spec_path1 as the foler,
#and pNovo+ will sequence the MS/MS data files one by one. 
#if folder=no, then the value of 'spec_path1' above must be a MS/MS file path. 
folder=no

#The folder where the result files are to be output
out_path={out_path}

#The number of peptides reported per spectrum
report_pep={report_pep}

report_path=150
report_temp=800
max_node=300
#FixMod Carbamidomethyl[C]  C
{FixMod}
#VarMod Oxidation[M]    M
{VarMod}
'''.format(
                **self.params_to_write),
                file=io
            )
        return
