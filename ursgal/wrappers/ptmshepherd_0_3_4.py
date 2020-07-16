#!/usr/bin/env python3.4
import ursgal
import os
import sys
import shutil
import csv
import copy
import re
from ursgal import ukb
import pprint
import re

class ptmshepherd_0_3_4(ursgal.UNode):
    """
    ptmshepherd_0_3_4 for validation and annotation of mass sifts from
    open modeification search results
    """
    META_INFO = {
        'edit_version': 1.0,
        'name': 'PTM-Shepherd',
        'version': '1.0',
        'release_date': '2020-07-10',
        'utranslation_style': 'ptmshepherd_style_1',
        'input_extensions': ['.csv'],
        'output_extensions': ['.csv'],
        'create_own_folder': False,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'validation_engine' : True,
        },
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'ptmshepherd-0.3.4.jar',
                    'url'            : 'https://github.com/Nesvilab/PTM-Shepherd/releases/download/v0.3.4/ptmshepherd-0.3.4.jar',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation':
            'Geiszler DJ, Kong AT, Avtonomov DM, Yu F, Leprevost FV, Nesvizhski AI.'\
            'PTM-Shepherd: analysis and summarization of post-translational and chemical modifications from open search results.'\
            'doi: https://doi.org/10.1101/2020.07.08.192583.',
    }

    def __init__(self, *args, **kwargs):
        super(ptmshepherd_0_3_4, self).__init__(*args, **kwargs)
        self.params_to_write = {}
        pass

    def preflight(self):
        self.params['translations']['csv_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        n = 0
        while os.path.exists(os.path.join(
            self.params['input_dir_path'],
            'ptmshephered_tmp_{0}'.format(n)
        )):
            n += 1
        self.tmp_dir = os.path.join(
            self.params['input_dir_path'],
            'ptmshephered_tmp_{0}'.format(n)
        )
        os.mkdir(self.tmp_dir)

        tmp_input_file = self.write_input_tsv(self.params['translations']['csv_input_file'], self.tmp_dir)

        write_exclusion_list = [
            'base_mz',
        ]
        for ptmshep_param in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][ptmshep_param].items():
                if ptmshep_param in write_exclusion_list:
                    continue
                elif ptmshep_param == 'dataset':
                    print('[ PREFLGHT ] copying mzML files into tmp folder ...')
                    for mzml in param_value:
                        shutil.copyfile(
                            mzml,
                            os.path.join(
                                self.tmp_dir,
                                os.path.basename(mzml)
                            )
                        )
                    self.params_to_write['dataset'] = '01 {0} {1}'.format(
                        tmp_input_file,
                        self.tmp_dir
                    )
                elif ursgal_param_name == 'ptmshepherd_peak_picking_params':
                    for k, v in param_value.items():
                        self.params_to_write[k] = v
                elif ptmshep_param == 'precursor_tol':
                    self.params_to_write['precursor_tol'] = \
                        self.params['translations']['precursor_mass_tolerance_plus'] +\
                        self.params['translations']['precursor_mass_tolerance_minus']
                elif ptmshep_param == 'spectra_ppmtol':
                    if self.params['translations']['frag_mass_tolerance_unit'] == 'da':
                        self.params_to_write['spectra_ppmtol'] = \
                            ursgal.ucore.convert_ppm_to_dalton(
                                self.params['translations']['frag_mass_tolerance'],
                                base_mz=self.params['translations']['base_mz']
                        )
                    elif self.params['translations']['frag_mass_tolerance_unit'] == 'ppm':
                        self.params_to_write['spectra_ppmtol'] = self.params['translations']['frag_mass_tolerance']
                    else:
                        print('please add convertion of frag mass tolerance for ptmshepherd for {0}'.format(
                            self.params['translations']['frag_mass_tolerance_unit']
                        ))
                        sys.exit(1)
                elif ptmshep_param == 'varmod_masses':
                    assert len(self.params['mods']['fix']) == 0, '''
                        [ERROR] PTM-Shepherd does not support fixed modifications.
                        [ERROR] Please change the following mods to variable mods:
                        {0}
                    '''.format(self.params['mods']['fix'])
                    mod_list = []
                    for mod_dict in self.params['mods']['opt']:
                        mod_list.append('{0}:{1}'.format(
                            mod_dict['name'],
                            mod_dict['mass']
                        ))
                    self.params_to_write['varmod_masses'] = ','.join(mod_list)
                elif ptmshep_param == 'mass_offsets':
                    self.params_to_write['mass_offsets'] = '/'.join(param_value)
                elif ptmshep_param == '-Xmx':
                    xmx = '-Xmx{0}'.format(param_value)
                else:
                    self.params_to_write[ptmshep_param] = param_value

        #create param file
        self.param_file_name = self.write_params_file(self.tmp_dir)

        #command line
        self.params['command_list'] = [
            'java',
            '-jar',
            xmx,
            self.exe,
            self.param_file_name,
        ]
        print(self.params['command_list'])

        return self.params


    def postflight(self, anno_result=None, csv_input=None, merged_results_csv=None):
        #fields from anno_result
        #Posterior Probability; Position; AA; SDP Score; Annotation Type; New Sequence; New Mod; New Mod Position; # Mass, Mod; 
        #Annotated Mass; Annotated Mod; Annotated Mod Site; Annotated Mod Term Spec; Annotated Mod Classification;

        # print('read original input csv ...')
        # if csv_input is None:
        #     csv_input = self.params['translations']['csv_input_file']
        # original_rows = {}
        # fieldnames = []
        # #read from original input csv file
        # with open(csv_input, 'r') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     fieldnames = reader.fieldnames
        #     for row in reader:
        #         psm_identifier = '||'.join([row['Spectrum Title'], row['Sequence'], row['Modifications']])
        #         if psm_identifier not in original_rows:
        #             original_rows[psm_identifier] = [row]
        #         else:
        #             original_rows[psm_identifier].append(row)

        # #prepare output file and write it on the fly
        # if merged_results_csv is None:
        #     merged_results_csv = os.path.join(
        #         self.params['translations']['output_file_incl_path']
        #     )
        # print('Writing result file:', merged_results_csv)
        # print('While parsing PTMiner annotated results file')
        # fieldnames.extend([
        #     'PTMiner:Result # for PSM',
        #     'PTMiner:Posterior Probability',
        #     'PTMiner:SDP Score',
        #     'PTMiner:Annotation Type', 
        #     'PTMiner:Annotated Mod Pos within Pep or Prot',
        #     'PTMiner:Annotated Mod Classification',
        #     'PTMiner:# Mass, Mod',  
        # ])
        # if sys.platform == 'win32':
        #     lineterminator = '\n'
        # else:
        #     lineterminator = '\r\n'

        # print('read annotated results txt ...')
        # anno_result_csv = anno_result
        # if anno_result is None:
        #     filtered_result = os.path.join(self.params_to_write['output'],'filtered_result.txt')
        #     loc_result = os.path.join(self.params_to_write['output'],'loc_result.txt')
        #     prior_probability = os.path.join(self.params_to_write['output'],'prior_probability.txt')
        #     self.created_tmp_files.append(filtered_result)
        #     self.created_tmp_files.append(loc_result)
        #     self.created_tmp_files.append(prior_probability)
        #     anno_result = os.path.join(self.params_to_write['output'],'anno_result.txt')
        #     self.created_tmp_files.append(anno_result)

        # #read from annotated results csv file
        # new_psms = {}
        # found_psm_identifier = set()
        # with open(anno_result, 'r') as anno_file, open(merged_results_csv, 'w') as out_file:
        #     writer = csv.DictWriter(out_file, fieldnames=fieldnames, lineterminator=lineterminator)
        #     writer.writeheader()
        #     reader = csv.DictReader(anno_file, delimiter = '\t')
        #     previous_row = {}
        #     for row in reader:
        #         #skip the second line, which is part of the headers
        #         if row['Dataset Name'] == '# Mass, Mod':
        #             continue
               
        #         if row['#'] != '*':
        #             n = 0
        #             spectrum_title = row['Spectrum Name']
        #             sequence = row['Sequence']

        #             pos_list = row['Identified Mod Position'].split(';')
        #             mod_list = row['Identified Mod Name'].split(';')
        #             mod_pos_list = []
        #             for m, p in zip(mod_list, pos_list):
        #                 if m == '':
        #                     continue
        #                 mod_pos_list.append('{0}:{1}'.format(m,p))
        #             modifications = ';'.join(mod_pos_list)
        #             psm_identifier = '||'.join([spectrum_title, sequence, modifications])
        #             if psm_identifier not in original_rows.keys():
        #                 if psm_identifier not in new_psms.keys():
        #                     new_psms[psm_identifier] = []
        #                 new_psms[psm_identifier].append(row)
        #                 continue

        #             found_psm_identifier.add(psm_identifier)
        #             mass_shift = float(row['Mass Shift'])
        #             mass_shift_pos = row['Position'].split(';')
        #             ptminer_posterior_probability = row['Posterior Probability']
        #             ptminer_sdp_score = row['SDP Score']
        #             annotation_type = row['Annotation Type']
                    
        #             for line_dict in original_rows[psm_identifier]:
        #                 line_dict['Mass Difference'] = '{0}:{1}'.format(mass_shift, '<|>'.join(mass_shift_pos))
        #                 line_dict['PTMiner:Posterior Probability'] = ptminer_posterior_probability
        #                 line_dict['PTMiner:SDP Score'] = ptminer_sdp_score
        #                 line_dict['PTMiner:Annotation Type'] = annotation_type
        #                 line_dict['PTMiner:Result # for PSM'] = 0
        #                 # line_dict['PTMiner:Annotated Mod Pos within Pep or Prot'] = ''
        #                 # line_dict['PTMiner:Annotated Mod Classification'] = ''
        #                 # line_dict['PTMiner:# Mass, Mod'] = ''
        #                 writer.writerow(line_dict)

        #             #check if there is new sequence, and if so create a new row for it
        #             if str(row['New Sequence']).strip() != '' and row['New Sequence'] is not None:
        #                 for line_dict in original_rows[psm_identifier]:
        #                     new_row = copy.deepcopy(line_dict)
        #                     new_row['Sequence'] = row['New Sequence'].strip()
        #                     new_mod_pos = row['New Mod Position'].split()
        #                     new_mod_name = row['New Mod'].split(' (')[0]
        #                     unimod_id = ursgal.GlobalUnimodMapper.name2id(
        #                         new_mod_name.strip()
        #                     )
        #                     if unimod_id is None:
        #                         new_row['Mass Difference'] = '{0}({1}):{2}'.format(
        #                                 mass_shift,
        #                                 new_mod_name,
        #                                 '<|>'.join(new_mod_pos)
        #                             )
        #                         new_mod_pos_list = mod_pos_list
        #                     else:
        #                         new_row['Mass Difference'] = ''
        #                         new_mod_pos_list = [x for x in mod_pos_list]
        #                         new_mod_pos_list.append(
        #                             '{0}:{1}'.format(new_mod_name, '<|>'.join(new_mod_pos))
        #                         )
        #                     new_row['Modifications'] = self.sort_mods(new_mod_pos_list)
        #                     new_row['PTMiner:Result # for PSM'] = -1
        #                     writer.writerow(new_row)
                    
        #         else:
        #             if psm_identifier not in original_rows.keys():
        #                 if psm_identifier not in new_psms.keys():
        #                     new_psms[psm_identifier] = []
        #                 new_psms[psm_identifier].append(row)
        #                 continue
        #             found_psm_identifier.add(psm_identifier)
        #             n += 1
        #             annotated_mass = row['Spectrum Name']
        #             if row['Sequence'] is not None and row['Sequence'] != '':
        #                 annotated_mod = row['Sequence'].split(' (')[0]
        #             else:
        #                 annotated_mod = ''
        #             if annotated_mod == '':
        #                 unimod_id = None
        #                 unimod_name = annotated_mass
        #             else:
        #                 unimod_id = ursgal.GlobalUnimodMapper.name2id(
        #                     annotated_mod.strip()
        #                 )
        #                 unimod_name = annotated_mod
        #             mass_shift_aa = row['Charge']
        #             if unimod_id is None:
        #                 if mass_shift_aa == '':
        #                     new_mass_shift = '{0}({1}):{2}'.format(
        #                         mass_shift,
        #                         unimod_name,
        #                         '<|>'.join(mass_shift_pos)
        #                     )
        #                     new_modifications = [modifications]
        #                 else:
        #                     new_mass_shift_pos = []
        #                     for pos in mass_shift_pos:
        #                         # try:
        #                         if int(pos) == 0:
        #                             pos = '1'
        #                         elif int(pos) == len(sequence)+1:
        #                             pos = '{0}'.format(len(sequence))
        #                         if sequence[int(pos)-1] == mass_shift_aa:
        #                             new_mass_shift_pos.append(pos)
        #                         # except:
        #                         #     print(pos)
        #                         #     print(psm_identifier)
        #                         #     print(sequence)
        #                         #     print(int(pos)-1)
        #                         #     print(sequence[int(pos)-1])
        #                         #     exit()
        #                     new_mass_shift = '{0}({1}):{2}'.format(
        #                         mass_shift,
        #                         unimod_name,
        #                         '<|>'.join(new_mass_shift_pos)
        #                     )
        #                     new_modifications = [modifications]
        #             else:
        #                 new_mass_shift = ''
        #                 new_mod_pos_list = [x for x in mod_pos_list]
        #                 new_modifications = []
        #                 for pos in mass_shift_pos:
        #                     if int(pos) == 0:
        #                         pos = '1'
        #                     elif int(pos) == len(sequence)+1:
        #                         pos = '{0}'.format(len(sequence))
        #                     if sequence[int(pos)-1] == mass_shift_aa:
        #                         new_modifications.append(
        #                             self.sort_mods(
        #                                 new_mod_pos_list + [
        #                                     '{0}:{1}'.format(unimod_name, pos)
        #                                 ]    
        #                             )
        #                         )
        #             for new_mod in new_modifications:
        #                 for line_dict in original_rows[psm_identifier]:
        #                     line_dict['PTMiner:Posterior Probability'] = ptminer_posterior_probability
        #                     line_dict['PTMiner:SDP Score'] = ptminer_sdp_score
        #                     line_dict['PTMiner:Annotation Type'] = annotation_type
        #                     line_dict['PTMiner:Result # for PSM'] = n
        #                     line_dict['PTMiner:Annotated Mod Pos within Pep or Prot'] = row['ObsMH']
        #                     line_dict['PTMiner:Annotated Mod Classification'] = row['Mass Shift']
        #                     line_dict['PTMiner:# Mass, Mod'] = row['Dataset Name']
        #                     line_dict['Mass Difference'] = new_mass_shift
        #                     line_dict['Modifications'] = new_mod
        #                     writer.writerow(line_dict)

        #     for psm_identifier in set(original_rows.keys()) - found_psm_identifier:
        #         for line_dict in original_rows[psm_identifier]:
        #             writer.writerow(line_dict)

        # new_psms_list = list(new_psms.keys())
        # print('''
        #     [ WARNING ] {0} PSMs from PTMiner results were not present in the original results
        #     [ WARNING ] These have been skipped (truncated to 100):
        #     [ WARNING ] {1}'''.format(
        #         len(new_psms_list),
        #         new_psms_list if len(new_psms_list) <100 else new_psms_list[:99],
        #     )
        # )

        # # lost_psm_identifier = set(original_rows.keys()) - found_psm_identifier
        # # if len(lost_psm_identifier) > 0:
        # #     print('''
        # #         [ WARNING ] {0} PSMs from the original results were not found in the PTMiner results
        # #         [ WARNING ] These have been skipped (truncated to 100):
        # #         [ WARNING ] {1}'''.format(
        # #             len(lost_psm_identifier),
        # #             list(lost_psm_identifier) if len(lost_psm_identifier) <100 else list(lost_psm_identifier)[:99],
        # #         )
        # #     )

        return

        # os.rmdir(self.tmp_dir)

    def write_input_tsv(self, input_csv, tmp_dir):
        '''
        convert ursgal csv into PTM-Shepherd input tsv
        (same format as Philosopher output psms tsv)
        '''
        print('[ PREFLGHT ] writing PTM-Shepherd config file ...')
        ptmshep_input = os.path.join(
            tmp_dir,
            os.path.basename(input_csv).replace('.csv', '.tsv')
        )
        # mod pattern
        mod_pattern = re.compile( r'''(?P<name>.*):(?P<pos>[0-9]*$)''' )
        
        #convert csv file into PTM-Shepherd input file
        fieldnames_list = [ 'Spectrum', 
                            'Peptide', 
                            'Modified Peptide', 
                            'Peptide Length', 
                            'Charge',
                            'Retention',
                            'Calculated Peptide Mass',
                            'Calculated M/Z',
                            'Delta Mass',
                            'Assigned Modifications',
                            'Is Unique',
                        ]
        umama = ursgal.UnimodMapper()

        with open(ptmshep_input, 'w', newline='') as new_csvfile, \
            open(self.params['translations']['csv_input_file'], 'r') as csv_file:
            writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames_list, delimiter='\t')
            writer.writeheader()
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                mass_diffs = row['Mass Difference'].split(';')
                mass_diffs_sum = 0.0
                for mass in mass_diffs:
                    if mass == '':
                        continue
                    mass_diffs_sum += float(mass.split(':')[0])

                if '<|>' in row['Protein ID']:
                    is_unique = 'false'
                else:
                    is_unique = 'true'
                    
                tmp_dict = {}
                tmp_dict['Spectrum'] = row['Spectrum Title']
                tmp_dict['Peptide'] = row['Sequence']
                tmp_dict['Modified Peptide'] = row['Sequence']
                tmp_dict['Peptide Length'] = len(row['Sequence'])
                tmp_dict['Charge'] = row['Charge']
                tmp_dict['Retention'] = row['Retention Time (s)']
                tmp_dict['Calculated Peptide Mass'] = row['uCalc Mass']
                tmp_dict['Calculated M/Z'] = row['uCalc m/z']
                tmp_dict['Delta Mass'] = mass_diffs_sum
                tmp_dict['Is Unique'] = is_unique

                mods = row['Modifications'].split(';')
                new_mod_list = []
                for mod in mods:
                    if mod == '':
                        continue
                    match = mod_pattern.search(mod)
                    pos = int(match.group('pos'))
                    if pos == 0:
                        aa = row['Sequence'][pos]
                    else:
                        aa = row['Sequence'][pos-1]
                    mass = umama.name2mass(match.group('name'))
                    mod_entry = '{0}{1}({2})'.format(
                        pos,
                        aa,
                        mass
                    )
                    new_mod_list.append(mod_entry)
                tmp_dict['Assigned Modifications'] = ', '.join(new_mod_list)
                writer.writerow(tmp_dict)

        return ptmshep_input

    def write_params_file(self, param_dir):
        print('[ PREFLGHT ] writing PTM-Shepherd config file ...')
        param_file_name = os.path.join(
            param_dir,
            'ptmshepherd_config.txt'
        )
        with open(param_file_name, 'w') as io:
            print('''dataset = {dataset}
threads = {threads}
histo_bindivs = {histo_bindivs}
histo_smoothbins = {histo_smoothbins}
peakpicking_promRatio = {peakpicking_promRatio}
peakpicking_mass_units = {peakpicking_mass_units}
peakpicking_width = {peakpicking_width}
peakpicking_topN = {peakpicking_topN}
precursor_mass_units = {precursor_mass_units}
precursor_tol = {precursor_tol}
spectra_ppmtol = {spectra_ppmtol}
spectra_condPeaks = {spectra_condPeaks}
spectra_condRatio = {spectra_condRatio}
varmod_masses = {varmod_masses}
localization_background = {localization_background}
mass_offsets = {mass_offsets}
isotope_error = {isotope_error}
output_extended = true
'''.format(
                **self.params_to_write),
                file=io
            )
        return param_file_name