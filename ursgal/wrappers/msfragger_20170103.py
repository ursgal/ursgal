#!/usr/bin/env python
import ursgal
import os
import pprint
from collections import defaultdict as ddict
import csv
import itertools
import sys


class msfragger_20170103(ursgal.UNode):
    """
    MSFragger unode

    Note:
        Please download and install MSFragger manually from
        http://www.nesvilab.org/software.html

    Reference:
    Kong, A. T., Leprevost, F. V, Avtonomov, D. M., Mellacheruvu, D., and Nesvizhskii, A. I. (2017)
    MSFragger: ultrafast and comprehensive peptide identification in mass spectrometry–based
    proteomics. Nature Methods 14

    Note:
        Addition of user amino acids not implemented yet. Only mzML search
        possible at the moment. The mgf file can still be passed to the node,
        but the mzML has to be in the same folder as the mgf.

    Warning:
        Still in testing phase!
        Metabolic labeling based 15N search may still be errorprone. Use with
        care!

    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'MSFragger',
        'version'                     : '20170103',
        'release_date'                : '2017-01-03',
        'utranslation_style'          : 'msfragger_style_1',
        'input_extensions'            : ['.mgf', '.mzML', '.mzXML'],
        'output_extensions'           : ['.csv'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'           : False,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'engine'                      : {
            'platform_independent'    : {
                'arc_independent' : {
                    'exe'            : 'MSFragger.jar',
                    'url'            : 'http://www.nesvilab.org/software.html',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation'                   :
        'Kong, A. T., Leprevost, F. V, Avtonomov, '
            'D. M., Mellacheruvu, D., and Nesvizhskii, A. I. (2017) MSFragger: '
            'ultrafast and comprehensive peptide identification in mass '
            'spectrometry-based proteomics. Nature Methods 14'
    }

    def __init__(self, *args, **kwargs):
        super(msfragger_20170103, self).__init__(*args, **kwargs)
        pass

    def write_params_file(self):
        with open(self.param_file_name , 'w') as io:
            for msfragger_param_name, param_value in sorted(self.params_to_write.items()):
                print(
                    '{0} = {1}'.format(
                        msfragger_param_name,
                        param_value
                    ),
                    file=io
                )

        return

    def preflight(self):
        '''
        Formatting the command line and writing the param input file via 
        self.params

        Returns:
                dict: self.params
        '''
        self.param_file_name = os.path.join(
            self.params['output_dir_path'],
            'msfragger.params'
        )
        # further prepare and translate params

        # pprint.pprint(self.params['translations']['_grouped_by_translated_key'])
        # pprint.pprint(self.params)
        # exit()
        self.params_to_write = {
            'output_file_extension' : 'tsv',  # tsv or pepXML we fix it...
            'output_format'         : 'tsv',  # pepXML or tsv
            'digest_mass_range' : '{0} {1}'.format(
                self.params['translations']['_grouped_by_translated_key'][
                    'precursor_min_mass']['precursor_min_mass'],
                self.params['translations']['_grouped_by_translated_key'][
                    'precursor_max_mass']['precursor_max_mass']
            )
        }

        write_exclusion_list = [
            'precursor_min_mass',
            'precursor_max_mass',
            'precursor_min_charge',
            'precursor_max_charge',
            'label',
            '-Xmx',
            'header_translations',
            'validation_score_field'
        ]

        additional_15N_modifications = []
        if self.params['translations']['_grouped_by_translated_key']['label']['label'] == '15N':
            self.print_info(
                'Search with label=15N may still be errorprone. Evaluate with care!',
                caller='WARNING'
            )
            for aminoacid, N15_Diff in ursgal.ukb.DICT_15N_DIFF.items():
                existing = False
                for mod_dict in self.params['mods']['fix']:
                    if aminoacid == mod_dict['aa']:
                        mod_dict['mass'] += N15_Diff
                        mod_dict['name'] += '_15N_{0}'.format(aminoacid)
                        existing = True
                if existing == True:
                    continue
                else:
                    mod_key = 'add_{0}_{1}'.format(
                        aminoacid,
                        ursgal.chemical_composition_kb.aa_names[aminoacid]
                    )
                    self.params_to_write[mod_key] = N15_Diff

        for msfragger_param_name in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][msfragger_param_name].items():
                if msfragger_param_name in write_exclusion_list:
                    continue
                elif msfragger_param_name == 'enzyme':
                    '''
                    search_enzyme_name = Trypsin
                    search_enzyme_cutafter = KR
                    search_enzyme_butnotafter = P
                    '''
                    aa_site, term, inhibitor = param_value.split(';')
                    self.params_to_write[
                        'search_enzyme_name'] = self.params['enzyme']
                    self.params_to_write['search_enzyme_cutafter'] = aa_site
                    self.params_to_write[
                        'search_enzyme_butnotafter'] = inhibitor
                elif msfragger_param_name == 'num_enzyme_termini':
                    # num_enzyme_termini = 2 # 2 for enzymatic, 1 for
                    # semi-enzymatic, 0 for nonspecific digestion

                    if self.params['translations']['_grouped_by_translated_key']['enzyme']['enzyme'] == 'nonspecific':
                        self.params_to_write[msfragger_param_name] = 0
                    else:
                        self.params_to_write[
                            msfragger_param_name] = param_value
                elif msfragger_param_name == 'clear_mz_range':
                    min_mz, max_mz = param_value
                    self.params_to_write[
                        msfragger_param_name] = '{0} {1}'.format(min_mz, max_mz)
                elif msfragger_param_name == 'modifications':
                    '''
                    #maximum of 7 mods - amino acid codes, * for any amino acid, [ and ] specifies protein termini, n and c specifies peptide termini
                    variable_mod_01 = 15.9949 M
                    variable_mod_02 = 42.0106 [*
                    #variable_mod_03 = 79.96633 STY
                    #variable_mod_03 = -17.0265 nQnC
                    #variable_mod_04 = -18.0106 nE
                    '''
                    # print(self.params['translations']['_grouped_by_translated_key'][msfragger_param_name])
                    # pprint.pprint(self.params[ 'mods' ])
                    # exit()
                    mass_to_mod_aa = ddict(list)
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
                        aa_to_append = mod_dict['aa']
                        pos_modifier = None
                        if mod_dict['pos'] == 'Prot-N-term':
                            pos_modifier = '['
                        elif mod_dict['pos'] == 'Prot-C-term':
                            pos_modifier = ']'
                        elif mod_dict['pos'] == 'N-term':
                            pos_modifier = 'n'
                        elif mod_dict['pos'] == 'C-term':
                            pos_modifier = 'c'
                        elif mod_dict['pos'] == 'any':
                            pass
                        else:
                            print(
                                '''
                            Unknown positional argument for given modification:
                            {0}
                            MSFragger cannot deal with this, please use one of the follwing:
                            any, Prot-N-term, Prot-C-term, N-term, C-term
                            '''.format(mod_dict['org'])
                            )
                            sys.exit(1)
                        if pos_modifier is not None:
                            aa_to_append = '{0}{1}'.format(
                                pos_modifier, aa_to_append)
                        mass_to_mod_aa[mod_dict['mass']].append(aa_to_append)
                    for pos, (mass, aa_list) in enumerate(mass_to_mod_aa.items()):
                        self.params_to_write['variable_mod_0{0}'.format(pos + 1)] = '{0} {1}'.format(
                            mass,
                            ''.join(aa_list)
                        )
                    for mod_dict in self.params['mods']['fix']:
                        '''
                        add_C_cysteine = 57.021464             # added to C - avg. 103.1429, mono. 103.00918
                        '''
                        if mod_dict['pos'] == 'Prot-N-term':
                            mod_key = 'add_Nterm_protein'
                        elif mod_dict['pos'] == 'Prot-C-term':
                            mod_key = 'add_Cterm_protein'
                        elif mod_dict['pos'] == 'N-term':
                            mod_key = 'add_Nterm_peptide'
                        elif mod_dict['pos'] == 'C-term':
                            mod_key = 'add_Cterm_peptide'
                        else:
                            mod_key = 'add_{0}_{1}'.format(
                                mod_dict['aa'],
                                ursgal.chemical_composition_kb.aa_names[
                                    mod_dict['aa']]
                            )
                        self.params_to_write[mod_key] = mod_dict['mass']

                elif msfragger_param_name == 'override_charge':
                    self.params_to_write[msfragger_param_name] = param_value
                    if param_value == 1:
                        self.params_to_write['precursor_charge'] = '{0} {1}'.format(
                            self.params['translations']['_grouped_by_translated_key'][
                                'precursor_min_charge']['precursor_min_charge'],
                            self.params['translations']['_grouped_by_translated_key'][
                                'precursor_max_charge']['precursor_max_charge']
                        )

                else:
                    self.params_to_write[msfragger_param_name] = param_value
        self.write_params_file()

        self.input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        if self.input_file.lower().endswith('.mzml') or \
                self.input_file.lower().endswith('.mzml.gz') or \
                self.input_file.lower().endswith('.mgf'):
            self.params['translations']['mzml_input_file'] = self.input_file
        # elif self.input_file.lower().endswith('.mgf'):
        #     self.params['translations']['mzml_input_file'] = \
        #         self.meta_unodes['ucontroller'].get_mzml_that_corresponds_to_mgf( self.input_file )
        #     self.print_info(
        #         'MSFragger can only read Proteowizard MGF input files,'
        #         'the corresponding mzML file {0} will be used instead.'.format(
        #             os.path.abspath(self.params['translations']['mzml_input_file'])
        #         ),
        #         caller = "INFO"
            # )
        else:
            raise Exception(
                'MSFragger input spectrum file must be in mzML or MGF format!')

        # pprint.pprint(self.params['translations'])
        # exit()
        self.params['command_list'] = [
            'java',
            '-Xmx{0}'.format(
                self.params['translations'][
                    '_grouped_by_translated_key']['-Xmx']['-xmx']
            ),
            '-jar',
            self.exe,
            self.param_file_name,
            self.params['translations']['mzml_input_file']
        ]

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        return self.params

    def postflight(self):
        '''
        Reads MSFragger tsv output and write final csv output file.

        Adds:
            * Raw data location, since this can not be added later
            * Converts masses in Da to m/z (could be done in unify_csv)


        '''
        ms_fragger_header = [
            'ScanID',
            'Precursor neutral mass (Da)',
            'Retention time (minutes)',
            'Precursor charge',
            'Hit rank',
            'Peptide Sequence',
            'Upstream Amino Acid',
            'Downstream Amino Acid',
            'Protein',
            'Matched fragment ions',
            'Total possible number of matched theoretical fragment ions',
            # (including any variable modifications) (Da)
            'Neutral mass of peptide',
            'Mass difference',
            'Number of tryptic termini',
            'Number of missed cleavages',
            # '(starts with M, separated by |, formated as position,mass)
            'Variable modifications detected',
            'Hyperscore',
            'Next score',
            'Intercept of expectation model (expectation in log space)',
            'Slope of expectation model (expectation in log space)',
        ]

        translated_headers = []
        header_translations = self.UNODE_UPARAMS[
            'header_translations']['uvalue_style_translation']
        for original_header_key in ms_fragger_header:
            ursgal_header_key = header_translations[original_header_key]
            translated_headers.append(ursgal_header_key)

        translated_headers += [
            'Spectrum Title',
            'Raw data location',
            'Exp m/z',
            'Calc m/z',

        ]

        msfragger_output_tsv = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '.tsv'
        )

        if os.path.exists(msfragger_output_tsv) is False:
            msfragger_output_tsv = os.path.join(
                self.params['input_dir_path'],
                self.params['file_root'][len(self.params['prefix'])+1:] + '.tsv'
            )    
            if os.path.exists(msfragger_output_tsv) is False:
                msfragger_output_tsv = os.path.join(
                    self.params['input_dir_path'],
                    '_'.join(self.params['file_root'].split('_')[1:]) + '.tsv'
                )
                if os.path.exists(msfragger_output_tsv) is False:
                    print('[ERROR]: MSFragger could not find the correct output tsv file')

        csv_out_fobject = open(self.params['translations'][
                               'output_file_incl_path'], 'w')
        csv_writer = csv.DictWriter(
            csv_out_fobject,
            fieldnames=translated_headers
        )
        csv_writer.writeheader()

        with open(msfragger_output_tsv) as temp_tsv:
            csv_reader = csv.DictReader(
                temp_tsv,
                fieldnames=translated_headers,
                delimiter='\t'
            )
            for line_dict in csv_reader:
                line_dict['Raw data location'] = os.path.abspath(
                    self.params['translations']['mzml_input_file']
                )

                ############################################
                # all fixing here has to go into unify csv! #
                ############################################

                # 'Precursor neutral mass (Da)' : '',
                # 'Neutral mass of peptide' : 'Calc m/z',# (including any variable modifications) (Da)
                line_dict['Exp m/z'] = ursgal.ucore.calculate_mz(
                    line_dict['MSFragger:Precursor neutral mass (Da)'],
                    line_dict['Charge']
                )
                line_dict['Calc m/z'] = ursgal.ucore.calculate_mz(
                    line_dict['MSFragger:Neutral mass of peptide'],
                    line_dict['Charge']
                )
                csv_writer.writerow(line_dict)

        csv_out_fobject.close()
        if msfragger_output_tsv.endswith('.tsv'):
            os.remove(msfragger_output_tsv)
        return
