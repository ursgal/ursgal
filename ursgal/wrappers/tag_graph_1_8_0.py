#!/usr/bin/env python3.4
import ursgal
import os
import csv
import sys
import pprint
import re
import shutil


class tag_graph_1_8_0(ursgal.UNode):
    """
    TagGraph unode
    For further information see https://sourceforge.net/projects/taggraph/

    Note:
        Please download and install MSFragger manually from
        http://www.nesvilab.org/software.html

    Reference:
    Devabhaktuni, A.; Lin, S.; Zhang, L.; Swaminathan, K.; Gonzalez, CG.; Olsson, N.; Pearlman, SM.; Rawson, K.; Elias, JE.
    (2019) TagGraph reveals vast protein modification landscapes from large tandem mass spectrometry datasets.
    Nat Biotechnol. 37(4)
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'TagGraph',
        'version'                     : '1.8.0',
        'release_date'                : '2019-10-13',
        'utranslation_style'          : 'tag_graph_style_1',
        'input_extensions'            : ['.mzML', '.mzXML'],
        'output_extensions'           : ['.csv', '.pepXML'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'               : False,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'engine'                      : {
            'platform_independent'    : {
                'arc_independent' : {
                    'exe'            : 'readme.txt',
                    'url'            : 'https://sourceforge.net/projects/taggraph/',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation' :
        'Devabhaktuni, A.; Lin, S.; Zhang, L.; Swaminathan, K.; Gonzalez, CG.; Olsson, N.; Pearlman, SM.; Rawson, K.; Elias, JE.'
            '(2019) TagGraph reveals vast protein modification landscapes from large tandem mass spectrometry datasets.'
            'Nat Biotechnol. 37(4)'
    }

    def __init__(self, *args, **kwargs):
        super(tag_graph_1_8_0, self).__init__(*args, **kwargs)
        pass

    def reformat_de_novo_file(self, unified_de_novo_results=None, mod2mass=None):
        reformatted_inputs = []

        for i, unified_de_novo_result in enumerate(unified_de_novo_results):
            reformatted_input = os.path.join(
                self.tag_graph_tmp_dir,
                os.path.basename(unified_de_novo_result).replace('.csv', '_tmp.csv')
            )
            reformatted_inputs.append(reformatted_input)
            header_translations = {
                'Fraction': i+1,  # start with fraction 1
                'Scan': 'Spectrum ID',
                'Source File': 'Raw data location',
                'Peptide': 'Sequence', # add modificaions
                'Tag Length': '', # len(Sequence)
                'ALC (%)': 'Average Score or Confidence',
                'length': '', # len(Sequence)
                'm/z': 'Exp m/z',
                'z': 'Charge',
                'RT': 'Retention Time (s)', # convert to min
                'Area': '',
                'Mass': 'uCalc Mass',
                'ppm': 'Accuracy (ppm)',
                'PTM': 'Modifications', # reformat
                'local confidence (%)': 'Local Score or Confidence',
                'tag (>=0%)': 'Sequence', # add modificaions
                'mode': '',
            }
            mod_pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )
            new_header = sorted(header_translations.keys())
            with open(unified_de_novo_result, 'r') as in_file, open(reformatted_input, 'w') as out_file:
                csv_reader = csv.DictReader(in_file)
                csv_writer = csv.DictWriter(
                    out_file,
                    fieldnames=new_header
                )
                csv_writer.writeheader()
                for line_dict in csv_reader:
                    new_line_dict = {}
                    for translated_header in header_translations.keys():
                        if translated_header in [
                            'Fraction',
                            'Area',
                            'mode',
                        ]:
                            new_line_dict[translated_header] = ''
                        elif translated_header == 'Source File':
                            new_line_dict[translated_header] = os.path.basename(
                                line_dict[header_translations[translated_header]]
                            )
                        elif translated_header in ['Peptide', 'tag (>=0%)', 'PTM']:
                            mods = {}
                            for mod in line_dict['Modifications'].split(';'):
                                for occ, match in enumerate(mod_pattern.finditer(mod)):
                                    unimod = mod[:match.start()]
                                    pos = int(mod[match.start()+1:])
                                    if pos in mods.keys():
                                        print('''
                                        [ERROR] Multiple mods at the same position.
                                        [ERROR] Check de novo result file or reformatting.
                                        ''')
                                        sys.exit(1)
                                    mods[pos] = unimod
                            mod_list = []
                            new_sequence = ''
                            for n, aa in enumerate(line_dict['Sequence']):
                                # Does not work for terminal mods yet
                                # not sure how terminal mods are formatted in PEAKS
                                if n+1 in mods.keys():
                                    add_plus = ''
                                    name = mods[n+1]
                                    mass = mod2mass[name]
                                    if mass >= 0:
                                        add_plus = '+'
                                    new_sequence += '{0}({1}{2})'.format(
                                        aa,
                                        add_plus,
                                        round(mass, 2)
                                    )
                                    mod_list.append(
                                        '{0} ({1})'.format(name, aa)
                                    )
                                else:
                                    new_sequence += aa
                            new_line_dict['Peptide'] = new_sequence
                            # new_line_dict['Peptide'] = line_dict['Sequence']
                            new_line_dict['tag (>=0%)'] = new_sequence
                            new_line_dict['PTM'] = '; '.join(mod_list)
                        elif translated_header in ['Tag Length', 'length']:
                            new_line_dict[translated_header] = len(line_dict['Sequence'])
                        elif translated_header == 'RT':
                            new_line_dict[translated_header] = float(
                                line_dict[header_translations[translated_header]])/60
                        else:
                            new_line_dict[translated_header] = line_dict[header_translations[translated_header]]
                    csv_writer.writerow(new_line_dict)

        return reformatted_inputs

    def preflight(self):
        '''
        Formatting the command line and writing two param input files
        via self.params

        Returns:
                dict: self.params
        '''
        self.input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        breakpoint()
        multi_input = False
        if self.input_file.lower().endswith('.mzml') or \
                self.input_file.lower().endswith('.mzml.gz'):
            self.params['translations']['mzml_input_file'] = [self.input_file]
            self.input_file = [self.input_file]
        elif self.input_file.lower().endswith('.mgf'):
            self.params['translations']['mzml_input_file'] = \
                [self.meta_unodes['ucontroller'].get_mzml_that_corresponds_to_mgf(
                                    self.input_file
                                )]
            self.input_file = [self.input_file]
        elif self.input_file.lower().endswith('.json'):
            multi_input = True
            self.input_file = [os.path.join(d['dir'], d['file']) for d in self.params['input_file_dicts']]
            self.params['translations']['mzml_input_file'] = self.input_file
        else:
            raise Exception(
                'TagGraph input spectrum file must be in mzML format!')
        self.tag_graph_tmp_dir = os.path.join(
            self.params['output_dir_path'],
            'tag_graph_tmp',
        )
        if os.path.exists(self.tag_graph_tmp_dir) is False:
            os.mkdir(self.tag_graph_tmp_dir)
        # self.created_tmp_files.append(self.tag_graph_tmp_dir)
        input_file = []
        for i, f in enumerate(self.input_file):
            stem, ext = os.path.splitext(f)
            new_f = '{stem}_F{i:02d}{ext}'.format(stem=stem, i=i+1, ext=ext)
            input_file.append(new_f)
        self.input_file = input_file

        if isinstance(self.params['translations']['mzml_input_file'], list):
            for i, f in enumerate(self.params['translations']['mzml_input_file']):
                # add fraction here
                # stem, ext = os.path.splitext(os.path.basename(f))
                # new_f = f'{stem}_F{i+1:02d}{ext}'
                # shutil.copy(f, os.path.join(self.tag_graph_tmp_dir, new_f))
                shutil.copy(f, self.tag_graph_tmp_dir)
        else:
            shutil.copy(self.params['translations']['mzml_input_file'], self.tag_graph_tmp_dir)

        self.docker_dir_path = '/mnt/ursgal_taggraph/'
        self.docker_mount = '{0}:{1}'.format(
            self.tag_graph_tmp_dir,
            self.docker_dir_path
        )

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        self.param_file_name = os.path.join(
            self.tag_graph_tmp_dir,
            'tag_graph_input_params.params'
        )
        # self.created_tmp_files.append(self.param_file_name)
        self.ini_file_name = os.path.join(
            self.tag_graph_tmp_dir,
            'tag_graph_input_ini.ini'
        )
        # self.created_tmp_files.append(self.ini_file_name)

        self.params_to_write = {
            'mzml_file': [os.path.basename(x).replace('.mzML', '') for x in self.input_file],
            'output' : os.path.join(self.docker_dir_path, 'EM_output'),
            'dataDirectory' : self.docker_dir_path,
            'init': os.path.join(self.docker_dir_path, os.path.basename(self.ini_file_name)),
            'ExperimentName': self.params['output_file'].replace('.csv', '')
        }
        self.ini_to_write = {}

        file_locations = {
            'unimoddict' : '/opt/bio/tools/taggraph/TagGraph.1.8/resources/unimodDict_noLabels_20160724.pck',
            'model' : '/opt/bio/tools/taggraph/TagGraph.1.8/resources/AllChargeDist_posOnlyDependence_20150808_HumanProt500000.pck',
            'config' : '/opt/bio/tools/taggraph/TagGraph.1.8/resources/AllChargeDist_posOnlyDependence_20150808.txt',
        }

        mod2mass = {}
        for taggraph_param_name in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params[
                'translations']['_grouped_by_translated_key'][taggraph_param_name].items():
                if type(taggraph_param_name) is tuple:
                    for tg_name in taggraph_param_name:
                        self.params_to_write[tg_name] = param_value
                elif taggraph_param_name == 'ppmstd':
                    if self.params['translations']['frag_mass_tolerance_unit'] == 'da':
                        self.params_to_write[taggraph_param_name] = ursgal.ucore.convert_dalton_to_ppm(
                            param_value,
                            base_mz=self.params['translations']['base_mz']
                        )
                    else:
                        self.params_to_write[taggraph_param_name] = param_value
                elif taggraph_param_name in file_locations.keys():
                    if param_value == 'default':
                        self.params_to_write[taggraph_param_name] = file_locations[taggraph_param_name]
                    else:
                        self.params_to_write[taggraph_param_name] = param_value
                elif taggraph_param_name == 'fmindex':
                    shutil.copy(param_value, self.tag_graph_tmp_dir)
                    self.params_to_write[taggraph_param_name] = os.path.basename(param_value).replace('.fasta', '.fm')
                    self.database = os.path.basename(param_value)
                    # shutil.copy(param_value.replace('.fm','.fasta'), self.tag_graph_tmp_dir)
                    # shutil.copy(param_value.replace('.fm','.offset'), self.tag_graph_tmp_dir)
                    # shutil.copy(param_value.replace('.fm','.seqnames.1'), self.tag_graph_tmp_dir)
                elif taggraph_param_name == 'Amino Acids':
                    aa_list = []
                    for aa in param_value.keys():
                        if 'monoisotopic_mass' not in param_value[aa].keys():
                            continue
                        aa_list.append('{0}: {1} {2} {3} {4} {5}'.format(
                            param_value[aa]['name'],
                            aa,
                            param_value[aa]['3_letter_code'],
                            param_value[aa]['chemical_composition'],
                            param_value[aa]['monoisotopic_mass'],
                            param_value[aa]['avg_mass'],
                        ))
                    self.ini_to_write['Amino_Acids'] = '\n'.join(aa_list)
                elif taggraph_param_name == 'Enzyme':
                    self.ini_to_write['Name'] = self.params['enzyme']
                    self.ini_to_write['Specificity'] = param_value
                elif taggraph_param_name == 'modifications':
                    '''
                    ; mod_name: AA mod_mass
                    ; use N-Term for N-terminus and C-Term for C-terminus
                    [Static Mods]
                    Carbamidomethylated Cysteine: C 57.021464

                    ; mod_name: AA(can be list of AAs such as STY, etc.) mod_mass overide_static_mod mod_symbol
                    ; mod_symbol optional and will be chosen automatically if not given
                    ; override_static_mod is either 0 or 1, 1 means add mod_mass to original AA mass, not statically modified mass
                    [Diff Mods]
                    Oxidation: M 15.994915 0 #
                    '''
                    opt_mods = {}
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
                        if 'term' in mod_dict['pos']:
                            print('''
                                [ ERROR ] It is unclear how terminal modifications are set in TagGraph.
                                [ ERROR ] please remove terminal modifications and try again
                                {0}
                            '''.format(mod_dict))
                        # if mod_dict['pos'] == 'Prot-N-term':
                        #     pos_modifier = 'N-Term'
                        # elif mod_dict['pos'] == 'Prot-C-term':
                        #     pos_modifier = 'C-Term'
                        # elif mod_dict['pos'] == 'N-term':
                        #     pos_modifier = 'N-Term'
                        # elif mod_dict['pos'] == 'C-term':
                        #     pos_modifier = 'C-Term'
                        # elif mod_dict['pos'] == 'any':
                        #     pass
                        # else:
                        #     print(
                        #         '''
                        #     Unknown positional argument for given modification:
                        #     {0}
                        #     MSFragger cannot deal with this, please use one of the follwing:
                        #     any, Prot-N-term, Prot-C-term, N-term, C-term
                        #     '''.format(mod_dict['org'])
                        #     )
                        #     sys.exit(1)
                        if mod_dict['name'] not in opt_mods.keys():
                            opt_mods[mod_dict['name']] = {
                                'aa_list' : [],
                                'mass' : mod_dict['mass']
                            }
                        opt_mods[mod_dict['name']]['aa_list'].append(mod_dict['aa'])
                        mod2mass[mod_dict['name']] = mod_dict['mass']
                    opt_mod_list = []
                    for unimod in opt_mods.keys():
                        if len(opt_mods[unimod]['aa_list']) == 1:
                            opt_mod_list.append('{0}: {1} {2} 0'.format(
                                unimod,
                                opt_mods[unimod]['aa_list'][0],
                                opt_mods[unimod]['mass'],
                            ))
                        else:
                            for aa in opt_mods[unimod]['aa_list']:
                                opt_mod_list.append('{0}_{1}: {2} {3} 0'.format(
                                    unimod,
                                    aa,
                                    aa,
                                    opt_mods[unimod]['mass'],
                                ))
                    self.ini_to_write['Diff_Mods'] = '\n'.join(opt_mod_list)

                    fix_mods = {}
                    for mod_dict in self.params['mods']['fix']:
                        # if mod_dict['pos'] == 'Prot-N-term':
                        #     mod_key = 'add_Nterm_protein'
                        # elif mod_dict['pos'] == 'Prot-C-term':
                        #     mod_key = 'add_Cterm_protein'
                        # elif mod_dict['pos'] == 'N-term':
                        #     mod_key = 'add_Nterm_peptide'
                        # elif mod_dict['pos'] == 'C-term':
                        #     mod_key = 'add_Cterm_peptide'
                        if 'term' in mod_dict['pos']:
                            print('''
                                [ ERROR ] It is unclear how terminal modifications are set in TagGraph.
                                [ ERROR ] please remove terminal modifications and try again
                                {0}
                            '''.format(mod_dict))
                        if mod_dict['name'] not in fix_mods.keys():
                            fix_mods[mod_dict['name']] = {
                                'aa_list' : [],
                                'mass' : mod_dict['mass']
                            }
                        fix_mods[mod_dict['name']]['aa_list'].append(mod_dict['aa'])
                        mod2mass[mod_dict['name']] = mod_dict['mass']
                    fix_mod_list = []
                    for unimod in fix_mods.keys():
                        if len(fix_mods[unimod]['aa_list']) == 1:
                            fix_mod_list.append('{0}: {1} {2}'.format(
                                unimod,
                                fix_mods[unimod]['aa_list'][0],
                                fix_mods[unimod]['mass'],
                            ))
                        else:
                            for aa in fix_mods[unimod]['aa_list']:
                                fix_mod_list.append('{0}_{1}: {2} {3}'.format(
                                    unimod,
                                    aa,
                                    aa,
                                    fix_mods[unimod]['mass'],
                                ))
                    self.ini_to_write['Static_Mods'] = '\n'.join(fix_mod_list)
                else:
                    self.params_to_write[taggraph_param_name] = param_value

        reformatted_inputs = self.reformat_de_novo_file(
            unified_de_novo_results = self.params_to_write['de_novo'],
            mod2mass = mod2mass,
        )
        # print(reformatted_inputs)
        # self.created_tmp_files.append(reformatted_input)
        self.params_to_write['de_novo'] = [os.path.basename(reformatted_input) for reformatted_input in reformatted_inputs]
        print(self.params_to_write['de_novo'])
        self.write_params_file()
        self.write_ini_file()

        if os.path.exists(os.path.join(self.tag_graph_tmp_dir, 'EM_output')):
            rm_str = '&& rm -r {0}/EM_output'.format(self.docker_dir_path)
        else:
            rm_str = ''

        self.params['command_list'] = [
            'docker',
            'run',
            # '--rm',
            '-v', self.docker_mount,
            '-i', '-t',
            'inf/taggraph:v1_debug',
            'bash', '-c',
            'cd {0} && python /opt/bio/tools/taggraph/TagGraph.1.8/scripts/BuildFMIndex.py -f {1}\
             {2} && python /opt/bio/tools/taggraph/TagGraph.1.8/runTG.py {3}'.format(
                self.docker_dir_path,
                self.database,
                rm_str,
                os.path.basename(self.param_file_name)
            )
        ]
        print(' '.join(self.params['command_list']))
        # breakpoint()
        return self.params

    def postflight(self):
        '''
        Reads TagGraph tdv output and write final csv output file.
        '''
        taggraph_header = [
            'ScanF',
            'Charge',
            'Retention Time',
            'Obs M+H',
            'Theo M+H',
            'PPM',
            'EM Probability',
            '1-lg10 EM',
            'Spectrum Score',
            'Alignment Score',
            'Composite Score',
            'Unique Siblings',
            'Context Mod Variants',
            'Num Mod Occurrences',
            'Context',
            # 'Mod Context',
            'Mods',
            'Mod Ambig Edges',
            'Mod Ranges',
            'Proteins',
            'De Novo Peptide',
            'De Novo Score',
            'Matching Tag Length',
            'Num Matches',
        ]

        translated_headers = []
        header_translations = self.UNODE_UPARAMS[
            'header_translations']['uvalue_style_translation']
        for original_header_key in taggraph_header:
            ursgal_header_key = header_translations[original_header_key]
            translated_headers.append(ursgal_header_key)
        translated_headers += [
            'Spectrum Title',
            'Raw data location',
            'Calc m/z',
        ]

        taggrapg_output_tdv = os.path.join(
            self.tag_graph_tmp_dir,
            'EM_output',
            # '{0}_TopResults.tdv'.format(
            #     self.params['output_file'].replace('.csv', '')
            # )
            '{0}_TopResults.txt'.format(
                self.params['output_file'].replace('.csv', '')
            )

        )

        csv_out_fobject = open(
            self.params['translations']['output_file_incl_path'],
            'w'
        )
        csv_writer = csv.DictWriter(
            csv_out_fobject,
            fieldnames=translated_headers
        )
        csv_writer.writeheader()

        with open(taggrapg_output_tdv, 'r') as temp_tsv:
            csv_reader = csv.DictReader(
                temp_tsv,
                delimiter='\t'
            )
            for line_dict in csv_reader:
                out_line_dict = {}

                ############################################
                # all fixing here has to go into unify csv! #
                ############################################

                for column in taggraph_header:
                    if column == 'ScanF':
                        out_line_dict[header_translations[column]] = line_dict[column].split(':')[1]
                    elif column == 'Context':
                        out_line_dict[header_translations[column]] = line_dict[column].split('.')[1]
                    else:
                        out_line_dict[header_translations[column]] = line_dict[column]
                from pprint import pprint
                pprint(line_dict)
                breakpoint()
                out_line_dict['Raw data location'] = os.path.abspath(
                    os.path.join(os.path.dirname(self.params['translations']['mzml_input_file'][0]),
                    line_dict['ScanF'].split(':')[0]+'.mzML')
                )
                csv_writer.writerow(out_line_dict)

        csv_out_fobject.close()
        return

    def write_params_file(self):
        with open(self.param_file_name, 'w') as io:
            assert len(self.params_to_write['de_novo']) == len(self.params_to_write['mzml_file']), 'Must have same number of denovo results as input files'

            file_input_lines = []
            for denovo, mzml in zip(self.params_to_write['de_novo'], self.params_to_write['mzml_file']):
                file_input_lines.append('{denovo}|{mzml}'.format(denovo=denovo, mzml=mzml))

            with open(os.path.join(self.tag_graph_tmp_dir, self.params_to_write['de_novo'][0])) as fin:
                fn = fin.readline().strip().split(',')

            new_name = os.path.splitext(self.params['output_file'])[0] + 'deepnovo_pointnovo_unified_tmp_denovo_merged.csv'

            merged_path = os.path.join(self.tag_graph_tmp_dir, new_name)
            # with open(merged_path, 'w') as fout:
            #     writer = csv.DictWriter(fout, fieldnames=['Source File', 'Fraction'])
            #     writer.writeheader()
            #     for i, f in enumerate(self.input_file):
            #         writer.writerow({'Source File': os.path.basename(f), 'Fraction': i+1})

            with open(merged_path, 'w') as fout:
                writer = csv.DictWriter(fout, fieldnames=['Fraction'] + fn)
                writer.writeheader()
                for i, denovo_file in enumerate(self.params_to_write['de_novo']):
                    with open(os.path.join(self.tag_graph_tmp_dir, denovo_file)) as fin:
                        reader = csv.DictReader(fin)
                        for line in reader:
                            frac = i + 1
                            line['Fraction'] = frac
                            writer.writerow(line)
            # breakpoint()
            self.params_to_write['denovo_mzml_input_line'] = ';'.join(file_input_lines)
            # self.params_to_write['denovo_mzml_input_line'] = ''
            # self.params_to_write['de_novo_tag_graph'] = self.params_to_write['de_novo'][0]
            # self.params_to_write['de_novo'] = merged_path
            self.params_to_write['de_novo'] = self.tag_graph_tmp_dir
            # self.params_to_write['de_novo_tag_graph'] = ';'.join(file_input_lines)
            # should be a csv with column Source File and Fraction
            mapping_file = os.path.join(self.params_to_write['dataDirectory'], os.path.basename(merged_path))
            # print(mapping_file)
            breakpoint()
            self.params_to_write['de_novo_tag_graph'] = mapping_file

            # TODO rewrite denovo files to to file and include fraction column!


            print('''##### General Settings #####
[General]
# Not used at this time, place-holder for the capabilities to only run the TG step, or the EM step if TG was run previously
runTG = True
runEM = True
nonPEAKS = False

# If set to True the copies of the input mzML/mzXML input files are removed from the output tree when the run has finished.
cleanInputDataFilesFromOutput = {cleanInputDataFilesFromOutput}
cleanIntermediateFiles = {cleanIntermediateFiles}

# output file
generatePepXML = {generatePepXML}
outputPerFraction = False
FDRCutoff = {FDRCutoff}
logEMCutoff = {logEMCutoff}
DisplayProteinNum = {DisplayProtNum}
##### END General Settings #####



##### De Novo Settings #####
[DeNovo]
# File mapping:
# If de novo sequencing program creates a single output text file, simply enter that text file;
# Otherwise, if de novo sequencing program generates one text output per input raw data file and there are multiple raw data input files, enter the folder which contains all de novo files: e.g.:
# de_novo= /project_folder/de_novo_results/denovo_output.csv OR de_novo=/project_folder/de_novo_results/
de_novo        = {dataDirectory}

# If de novo sequencing program generates one text output per input file, enter mapping here, linking each de novo file to the root name of the corresponding input raw data file via a pipe (|) separating each de novo / raw file pair by semicolons, e.g.: denovoMZML =216.csv|ath017216;217.csv|ath017217, otherwise, leave blank.
denovoMZML      = {denovo_mzml_input_line}

# De novo output file parsing
# De novo output file parsing: Header lines to ignore
# Enter number lines in de novo input file which contains descriptive information (e.g., column headers) to ignore.  e.g.,:Ignore rows= 1
ignoreRows       =1

#delimiter for the denovo file. eg: a tab, a commma, etc
denovoFileDelimiter=,

# Column assignment
# Column assignment: Multiple raw file / Fraction designation:
# When searching multiple input raw files in one batch, does the de novo software assign a unique identifier to each input raw file (e.g., a fraction number)?  If so, enter the column number which contains this information (left-most column = 1) e.g.,:fractionID= 1
fractionID      =

# Column assignment: Scan designation
# Enter column number which contains scan mapping information for given peptide (left-most column = 1) if it's multiple scan IDs, then include the scanSplitter (eg: deepnovo sequences) e.g.,scan= 10
scan            =8

# De novo output file parsing: Scan parsing:
#If de novo sequencing program aggregates multiple scans which contributed to a peptide identification (e.g., "2333;2567;2673"), enter the character which delimits each scan (i.e., "/"). e.g., scanSplitter= ;
scanSplitter    =

# Column assignment: Charge designation
# Enter column number which contains charge assignment information for given peptide (left-most column = 1) e.g.,charge= 7
charge          =17

# Column assignment: Peptide sequence
# Enter column number which contains peptide sequence (left-most column = 1) e.g., : peptide = 3
peptide         =6

# De novo output file parsing: Peptide parsing:
# If de novo sequencing program enters a character between each returned amino acid (e.g., "P.E.P.T.I.D.E"), enter that character (i.e., ".").  TagGraph will ignore this character in the peptide sequence: e.g.,denovoDelimeter= .
peptideDelimiter=

#optional parameters:
rt              =7
precursor_mz    =13
ALCinPCT        =1
LC              =1
##### End De Novo Settings #####


##### TagGraph Settings #####
[TagGraph]
# An integer number of data files to be used as fractions, and the path to each (mz[X]ML) data file with 2-digit counter appended to 'fraction' as key
dataDirectory  = {dataDirectory}

# Name to be used for this experiment and its output files and directories. Must not contain spaces.
ExperimentName = {ExperimentName}

# Location of input de novo search results exported from de novo sequencing program in .csv or .pepXML format. See README for format requirements/examples or more details.
de_novo        = {de_novo_tag_graph}

# Path to folder TagGraph will create to store output. Should not already exist.
output         = {output}

# Initialization file used to configure TAG-GRAPH. See README for detailed information.
init           = {init}

# Location and name of fmindex to search.  This fmindex location should include multiple related files as described in the README.
fmindex        = {fmindex}

# Expected standard deviation in ppm error distributions of fragment ions. Recommend 5 for HCD 30,000 resolution
ppmstd         = {ppmstd}

# Maximum absolute deviation (Da) between experimental and database modification mass for TagGraph to consider modification as a candidate match. Recommend 0.1.
modtolerance   = {modtolerance}

# Maximum number of times a de novo-produced substring can occur in the protein sequence database for TagGraph to consider it as an unmodified peptide match.
# Recommend less than 1,000 for single organism database (i.e., human uniprot) and 5,000 for nr or 6-frame translations
maxcounts      = {maxcounts}

# Maximum number of times a de novo-produced substring can occur in the protein sequence database for TagGraph to consider it as a modified peptide match.
# Recommend 200 for single organism database (i.e. human uniprot) and 1,000 for nr or 6-frame translations
modmaxcounts   = {modmaxcounts}

# Location of pickled (python-serialized) unimod dictionary
unimoddict     = {unimoddict}

# Path to pickled (python-serialized) probabilistic model file.
model          = {model}

# Path to pickled (python-serialized) model configuration file.
config         = {config}

##### End TagGraph Settings #####


##### EM Settings #####
[EM]
# Number of iterations in initial EM over all results. Recommend 20 iterations.
initIterations = {initIterations}

# Maximum number of expectation maximization iterations for FDR assignment. Recommend 100 iterations.
maxIterations = {maxIterations}

# Filename Prefix to use for the output EM results files. Must not contain spaces.
resultsPrefix = EM_Results
##### End EM Settings #####

'''.format(
                **self.params_to_write),
                file=io
            )


    def write_ini_file(self):
        with open(self.ini_file_name, 'w') as io:
            print('''[Parameters]

; Add enzyme info here
; Specificity is regular expression with a semicolon used to indicate cleavage site
[Enzyme]
Name: {Name}
Specificity: {Specificity}

; AA_name: AA_1_letter_abbrev AA_3_letter_abbrev AA_Elemental_Comp AA_monoisotopic_mass AA_avg_mass
; Add any additional amino acids other than the twenty original ones here
[Amino Acids]
{Amino_Acids}

; mod_name: AA mod_mass
; use N-Term for N-terminus and C-Term for C-terminus
[Static Mods]
{Static_Mods}

; mod_name: AA(can be list of AAs such as STY, etc.) mod_mass overide_static_mod mod_symbol
; mod_symbol optional and will be chosen automatically if not given
; override_static_mod is either 0 or 1, 1 means add mod_mass to original AA mass, not statically modified mass
[Diff Mods]
{Diff_Mods}
'''.format(
                **self.ini_to_write),
                file=io
            )
