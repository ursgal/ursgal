#!/usr/bin/env python3.4
import ursgal
import os
import sys
import csv
import copy
import re
from ursgal import ukb
import pprint
import re

class ptminer_1_0(ursgal.UNode):
    """ptminer_1_0 used for mass shifts localization and peptides anotation"""
    META_INFO = {
        'edit_version': 1.0,
        'name': 'PTMiner',
        'version': '1.0',
        'release_date': '2017-07-01',
        'utranslation_style': 'ptminer_style_1',
        'input_extensions': ['.mgf', '.csv'],
        'output_extensions': ['.csv'],
        'create_own_folder': False,
        'in_development': False,
        'include_in_git': False,
        #'distributable': True,
        'engine_type': {
            'validation_engine' : True,
        },
        'engine': {
            'win32': {
                '64bit': {
                    'exe': 'Localization.exe',
                },
                '32bit': {
                    'exe': 'Localization.exe',
                },
            },
        },
        'citation':
        '',
    }

    def __init__(self, *args, **kwargs):
        super(ptminer_1_0, self).__init__(*args, **kwargs)
        self.params_to_write = {}
        pass

    def preflight(self):
        # pprint.pprint(self.params)
        self.params['translations']['csv_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        mgf_input_files = self.params['translations']['mgf_input_files_list']
        #merge the input mgf files
        merged_mgf_file = os.path.join(
            os.path.dirname(mgf_input_files[0]),
            'PTMiner_merged.mgf'
        )
        # if os.path.exists(merged_mgf_file):
        #     pass
        if len(mgf_input_files) == 1:
            merged_mgf_file = mgf_input_files[0]
        else:
            first_file = True
            print('merging mgf files. This may take a while ...')
            with open(merged_mgf_file, 'w') as merged_mgf:
                for mgf_file in mgf_input_files:
                    #avoid empty line at the beginning if this is the first mgf file
                    if not first_file:
                        merged_mgf.write('\n')
                    first_file = False
                    with open(mgf_file) as mgf:
                        for line in mgf:
                            merged_mgf.write(line)

        ptminer_input = self.params['translations']['csv_input_file'].strip('.csv') + '.txt'
        selected_columns = []
        # mod pattern
        mod_pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )
        
        #convert csv file into PTMiner input file
        fieldnames_list = [ 'Dataset Name', 
                            'Spectrum Name', 
                            'Sequence', 
                            'Charge', 
                            'ObsMH', 
                            'Mass Shift', 
                            'Main Score', 
                            'High Score Better', 
                            'Identified Mod Name',
                            'Identified Mod Position',
                            'Protein Access',
                            'Before AA',
                            'After AA',
                        ]
        # self.protein_lookup = {}
        if os.path.exists(ptminer_input):
            os.remove(ptminer_input)
        with open(ptminer_input, 'w', newline='') as new_csvfile:
            writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames_list, delimiter='\t')
            writer.writeheader()
            # for row in selected_columns:
            #     writer.writerow(row)

            with open(self.params['translations']['csv_input_file'], 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                # find the last search/denovo engine:
                # if validation_score_field is None, do as before
                # else use that (user defines this in workflow as well as bigger_score_better)
                # check if last_engine is list and print error

                last_search_engine_colname = self.params['translations']['validation_score_field']
                last_engine_bigger_scores_better = self.params['translations']['bigger_scores_better']

                if last_search_engine_colname is None:
                    last_engine = self.get_last_search_engine(
                        history = self.stats['history'],
                    )
                    if type(last_engine) is list:
                        raise Exception('''
                            You need to specify validation_score_field param.
                            Each of these engines %s may define that param differently
                            ''' % last_engine) 
                    last_search_engine_colname = self.UNODE_UPARAMS[
                        'validation_score_field']['uvalue_style_translation'][last_engine]

                if last_engine_bigger_scores_better is None:
                    last_engine = self.get_last_search_engine(
                        history = self.stats['history'],
                    )
                    if type(last_engine) is list:
                        raise Exception('''
                            You need to specify bigger_scores_better param.
                            Each of these engines %s may define that param differently
                            ''' % last_engine)
                    last_engine_bigger_scores_better = self.UNODE_UPARAMS[
                        'bigger_scores_better']['uvalue_style_translation'][last_engine]

        
                for row in csv_reader:
                    #taking into account cases where there are multiple mass differences:positions for same PSM
                    mass_diffs = row['Mass Difference'].split(';')
                    mass_diffs_sum = 0
                    for mass in mass_diffs:
                        if mass == '':
                            continue
                        mass_diffs_sum += float(mass.split(':')[0])
                    
                    tmp_dict = {}
                    tmp_dict['Mass Shift'] = mass_diffs_sum
                    tmp_dict['Dataset Name'] = merged_mgf_file
                    tmp_dict['Spectrum Name'] = row['Spectrum Title']
                    tmp_dict['Sequence'] = row['Sequence']
                    tmp_dict['Charge'] = row['Charge']
                    tmp_dict['ObsMH'] = (float(row['Exp m/z']) * float(row['Charge'])) - (ukb.PROTON * (float(row['Charge']) - 1))
                    tmp_dict['Main Score'] = row[last_search_engine_colname]
                    tmp_dict['High Score Better'] = last_engine_bigger_scores_better

                    #taking into account cases where there are multiple modifications:positions
                    mods = row['Modifications'].split(';')
                    mod_name_list = []
                    pos_list = []
                    for mod in mods:
                        if mod == '':
                            continue
                        match = mod_pattern.search(mod)
                        pos = match.group('pos')
                        pos_list.append(pos)
                        mod_name = mod[:match.start()]
                        mod_name_list.append(mod_name)
                    tmp_dict['Identified Mod Name'] = ';'.join(mod_name_list)
                    tmp_dict['Identified Mod Position'] = ';'.join(pos_list)
                    #PTMiner uses semicolon as separation between proteins
                    tmp_dict['Protein Access'] = row['Protein ID'].split('<|>')[0].split(' ')[0]
                    # if tmp_dict['Protein Access'] not in self.protein_lookup.keys():
                    #     self.protein_lookup[tmp_dict['Protein Access']] = row['Protein ID']
                    tmp_dict['Before AA'] = row['Sequence Pre AA'].split('<|>')[0].split(';')[0]
                    tmp_dict['After AA'] = row['Sequence Post AA'].split('<|>')[0].split(';')[0]
                    writer.writerow(tmp_dict)

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        self.param_file_name = os.path.join(
            self.params['translations']['output_file_incl_path'].strip('.csv')
            + '.param'
        )

        #params to write
        self.params_to_write['open_search'] = self.params['translations']['is_open_search']
        self.params_to_write['precursor_matching_tolerance'] = max(abs(self.params['translations']['min_mod_size']), 
            abs(self.params['translations']['max_mod_size']))
        #print a warning
        print(
'''
[ WARNING ] we assume the mass shifts have the following format: mass_shift:position
[ WARNING ] mutliple mass shits for same PSM are summed up; PTMiner does not support multiple masses in one row
[ WARNING ] PTMiner does not take into account the mass shift's positions from input file
[ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
[ WARNING ] need to be combined for PTMiner (use of symmetric tolerance window).
[ WARNING ] the max value is used.
[ WARNING ] the same applies to max_mod_size and min_mod_size
[ WARNING ] PSM is defined as Spectrum Title + Sequence + Modifications
'''
        )
        self.params_to_write['precursor_tol'] = max(abs(self.params['translations']['precursor_mass_tolerance_plus']), 
            abs(self.params['translations']['precursor_mass_tolerance_minus']))
        self.params_to_write['precursor_tol_type'] = self.params['translations']['precursor_mass_tolerance_unit']
        self.params_to_write['fragment_tol'] = self.params['translations']['frag_mass_tolerance']
        self.params_to_write['fragment_tol_type'] = self.params['translations']['frag_mass_tolerance_unit']
        self.params_to_write['dataset'] = merged_mgf_file
        self.params_to_write['input_file'] = ptminer_input
        self.params_to_write['is_fdr_control'] = 1
        self.params_to_write['decoy_tag'] = self.params['translations']['decoy_tag']
        self.params_to_write['fdr_threshold'] = 1
        self.params_to_write['fdr_method'] = self.params['translations']['fdr_method']
        self.params_to_write['is_localized'] = self.params['translations']['determine_localization']
        self.params_to_write['min_mod_number'] = self.params['translations']['min_num_mods']
        self.params_to_write['use_prior'] = self.params['translations']['use_prior_probability']
        self.params_to_write['is_annotated'] = self.params['translations']['determine_unimod_annotation']
        self.params_to_write['protein_database'] = os.path.abspath(self.params['translations']['database'])
        self.params_to_write['output'] = os.path.dirname(self.params['translations']['output_file_incl_path'])+'\\'
        variable_mods = self.params['mods']['opt']
        fixed_mods = self.params['mods']['fix']
        self.params_to_write['fixed_mod_number'] = len(fixed_mods)
        self.params_to_write['var_mod_number'] = len(variable_mods)

        fix_mod_list = []
        for n, fix_mod_dict in enumerate(fixed_mods):
            if fix_mod_dict['pos'] == 'Prot-N-term':
                aa_pos = 'Protein N-term'
            elif fix_mod_dict['pos'] == 'Prot-C-term':
                aa_pos = 'Protein C-term'
            elif fix_mod_dict['pos'] == 'N-term':
                aa_pos = 'Any N-term'
            elif fix_mod_dict['pos'] == 'C-term':
                aa_pos = 'Any C-term'
            elif fix_mod_dict['pos'] == 'any':
                aa_pos = fix_mod_dict['aa']
            fix_mod_str = 'fixed_mod_{0} = {1} ({2})'.format(
                n+1,
                fix_mod_dict['name'],
                aa_pos
            )
            fix_mod_list.append(fix_mod_str)
        self.params_to_write['fixed_modifications'] = '\n'.join(fix_mod_list)
        opt_mod_list = []
        for n, opt_mod_dict in enumerate(variable_mods):
            if opt_mod_dict['pos'] == 'Prot-N-term':
                aa_pos = 'Protein N-term'
            elif opt_mod_dict['pos'] == 'Prot-C-term':
                aa_pos = 'Protein C-term'
            elif opt_mod_dict['pos'] == 'N-term':
                aa_pos = 'Any N-term'
            elif opt_mod_dict['pos'] == 'C-term':
                aa_pos = 'Any C-term'
            elif opt_mod_dict['pos'] == 'any':
                aa_pos = opt_mod_dict['aa']
            opt_mod_str = 'var_mod_{0} = {1} ({2})'.format(
                n+1,
                opt_mod_dict['name'],
                aa_pos
            )
            opt_mod_list.append(opt_mod_str)
        self.params_to_write['variable_modifications'] = '\n'.join(opt_mod_list)

        #create param file
        self.write_params_file()

        #command line
        self.params['command_list'] = [
            self.exe,
            self.param_file_name,
        ]
        print(self.params['command_list'])
        # self.created_tmp_files.append(self.param_file_name)
        # self.created_tmp_files.append(merged_mgf_file)
        # self.created_tmp_files.append(ptminer_input)

        return self.params


    def postflight(self, anno_result=None, csv_input=None, merged_results_csv=None):
        #fields from anno_result
        #Posterior Probability; Position; AA; SDP Score; Annotation Type; New Sequence; New Mod; New Mod Position; # Mass, Mod; 
        #Annotated Mass; Annotated Mod; Annotated Mod Site; Annotated Mod Term Spec; Annotated Mod Classification;

        print('read original input csv ...')
        if csv_input is None:
            csv_input = self.params['translations']['csv_input_file']
        original_rows = {}
        fieldnames = []
        #read from original input csv file
        with open(csv_input, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            for row in reader:
                psm_identifier = '||'.join([row['Spectrum Title'], row['Sequence'], row['Modifications']])
                if psm_identifier not in original_rows:
                    original_rows[psm_identifier] = [row]
                else:
                    original_rows[psm_identifier].append(row)

        #prepare output file and write it on the fly
        if merged_results_csv is None:
            merged_results_csv = os.path.join(
                self.params['translations']['output_file_incl_path']
            )
        print('Writing result file:', merged_results_csv)
        print('While parsing PTMiner annotated results file')
        fieldnames.extend([
            'Mass Difference Annotations',
            'PTMiner:Mass Shift Localization',
            'PTMiner:Result # for PSM',
            'PTMiner:Posterior Probability',
            'PTMiner:SDP Score',
            'PTMiner:Annotation Type', 
            'PTMiner:Annotated Mod Pos within Pep or Prot',
            'PTMiner:Annotated Mod Classification',
            'PTMiner:# Mass, Mod',  
        ])
        if sys.platform == 'win32':
            lineterminator = '\n'
        else:
            lineterminator = '\r\n'

        print('read annotated results txt ...')
        anno_result_csv = anno_result
        if anno_result is None:
            filtered_result = os.path.join(self.params_to_write['output'],'filtered_result.txt')
            loc_result = os.path.join(self.params_to_write['output'],'loc_result.txt')
            prior_probability = os.path.join(self.params_to_write['output'],'prior_probability.txt')
            # self.created_tmp_files.append(filtered_result)
            # self.created_tmp_files.append(loc_result)
            # self.created_tmp_files.append(prior_probability)
            anno_result = os.path.join(self.params_to_write['output'],'anno_result.txt')
            # self.created_tmp_files.append(anno_result)

        #read from annotated results csv file
        new_psms = {}
        found_psm_identifier = set()
        with open(anno_result, 'r') as anno_file, open(merged_results_csv, 'w') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=fieldnames, lineterminator=lineterminator)
            writer.writeheader()
            reader = csv.DictReader(anno_file, delimiter = '\t')
            previous_row = {}
            for row in reader:
                #skip the second line, which is part of the headers
                if row['Dataset Name'] == '# Mass, Mod':
                    continue
                if row['#'] != '*':
                    n = 0
                    spectrum_title = row['Spectrum Name']
                    sequence = row['Sequence']

                    pos_list = row['Identified Mod Position'].split(';')
                    mod_list = row['Identified Mod Name'].split(';')
                    mod_pos_list = []
                    for m, p in zip(mod_list, pos_list):
                        if m == '':
                            continue
                        mod_pos_list.append('{0}:{1}'.format(m,p))
                    modifications = ';'.join(mod_pos_list)
                    psm_identifier = '||'.join([spectrum_title, sequence, modifications])
                    if psm_identifier not in original_rows.keys():
                        if psm_identifier not in new_psms.keys():
                            new_psms[psm_identifier] = []
                        new_psms[psm_identifier].append(row)
                        continue

                    found_psm_identifier.add(psm_identifier)
                    mass_shift = float(row['Mass Shift'])
                    mass_shift_pos = row['Position'].split(';')
                    ptminer_posterior_probability = row['Posterior Probability']
                    ptminer_sdp_score = row['SDP Score']
                    annotation_type = row['Annotation Type']
                    
                    for line_dict in original_rows[psm_identifier]:
                        # line_dict['Mass Difference'] = '{0}:{1}'.format(mass_shift, '<|>'.join(mass_shift_pos))
                        line_dict['PTMiner:Mass Shift Localization'] = ';'.join(mass_shift_pos)
                        line_dict['PTMiner:Posterior Probability'] = ptminer_posterior_probability
                        line_dict['PTMiner:SDP Score'] = ptminer_sdp_score
                        line_dict['PTMiner:Annotation Type'] = annotation_type
                        line_dict['PTMiner:Result # for PSM'] = 0
                        # line_dict['PTMiner:Annotated Mod Pos within Pep or Prot'] = ''
                        # line_dict['PTMiner:Annotated Mod Classification'] = ''
                        # line_dict['PTMiner:# Mass, Mod'] = ''
                        writer.writerow(line_dict)

                    #check if there is new sequence, and if so create a new row for it
                    if str(row['New Sequence']).strip() != '' and row['New Sequence'] is not None:
                        for line_dict in original_rows[psm_identifier]:
                            new_row = copy.deepcopy(line_dict)
                            # new_row['Sequence'] = row['New Sequence'].strip()
                            new_seq = row['New Sequence'].strip()
                            new_mod_pos = row['New Mod Position'].strip()
                            new_mod_name = row['New Mod'].split(' (')[0]
                            # unimod_id = ursgal.GlobalUnimodMapper.name2id(
                            #     new_mod_name.strip()
                            # )
                            if new_mod_name == '':
                                new_row['Mass Difference Annotations'] = new_seq
                            # if unimod_id is None:
                                # new_row['Mass Difference'] = '{0}({1}):{2}'.format(
                                #         mass_shift,
                                #         new_mod_name,
                                #         '<|>'.join(new_mod_pos)
                                #     )
                                # new_mod_pos_list = mod_pos_list
                            else:
                                new_row['Mass Difference Annotations'] = '{0}#{1}:{2}'.format(
                                    new_seq,
                                    new_mod_name,
                                    new_mod_pos,
                                )
                                # new_row['Mass Difference'] = ''
                                # new_mod_pos_list = [x for x in mod_pos_list]
                                # new_mod_pos_list.append(
                                #     '{0}:{1}'.format(new_mod_name, '<|>'.join(new_mod_pos))
                                # )
                            # new_row['Modifications'] = self.sort_mods(new_mod_pos_list)
                            new_row['PTMiner:Result # for PSM'] = -1
                            new_row['PTMiner:Mass Shift Localization'] = ''
                            writer.writerow(new_row)
                    
                else:
                    if psm_identifier not in original_rows.keys():
                        if psm_identifier not in new_psms.keys():
                            new_psms[psm_identifier] = []
                        new_psms[psm_identifier].append(row)
                        continue
                    found_psm_identifier.add(psm_identifier)
                    n += 1
                    annotated_mass = row['Spectrum Name']
                    if row['Sequence'] is not None and row['Sequence'] != '':
                        annotated_mod = row['Sequence'].split(' (')[0]
                    else:
                        annotated_mod = ''
                    if annotated_mod == '':
                        unimod_id = None
                        unimod_name = annotated_mass
                    else:
                        unimod_id = ursgal.GlobalUnimodMapper.name2id(
                            annotated_mod.strip()
                        )
                        unimod_name = annotated_mod
                    mass_shift_aa = row['Charge']
                    # if unimod_id is None:
                    if mass_shift_aa == '':
                        new_mass_shift_pos = mass_shift_pos
                            # new_mass_shift = '{0}({1}):{2}'.format(
                            #     mass_shift,
                            #     unimod_name,
                            #     '<|>'.join(mass_shift_pos)
                            # )
                            # new_modifications = [modifications]
                    else:
                        new_mass_shift_pos = []
                        for pos in mass_shift_pos:
                            # try:
                            if int(pos) == 0:
                                pos = '1'
                            elif int(pos) == len(sequence)+1:
                                pos = '{0}'.format(len(sequence))
                            if sequence[int(pos)-1] == mass_shift_aa:
                                new_mass_shift_pos.append(pos)
                                # except:
                                #     print(pos)
                                #     print(psm_identifier)
                                #     print(sequence)
                                #     print(int(pos)-1)
                                #     print(sequence[int(pos)-1])
                                #     exit()
                            # new_mass_shift = '{0}({1}):{2}'.format(
                            #     mass_shift,
                            #     unimod_name,
                            #     '<|>'.join(new_mass_shift_pos)
                            # )
                            # new_modifications = [modifications]
                    new_mass_shift_pos = ';'.join(new_mass_shift_pos)
                    if unimod_id is None:
                        new_mass_shift_anno = 'Unannotated mass-shift {0}'.format(annotated_mass)
                    else:
                        new_mass_shift_anno = unimod_name
                        # new_mass_shift = ''
                        # new_mod_pos_list = [x for x in mod_pos_list]
                        # new_modifications = []
                        # for pos in mass_shift_pos:
                        #     if int(pos) == 0:
                        #         pos = '1'
                        #     elif int(pos) == len(sequence)+1:
                        #         pos = '{0}'.format(len(sequence))
                        #     if sequence[int(pos)-1] == mass_shift_aa:
                        #         new_modifications.append(
                        #             self.sort_mods(
                        #                 new_mod_pos_list + [
                        #                     '{0}:{1}'.format(unimod_name, pos)
                        #                 ]    
                        #             )
                        #         )
                    # for new_mod in new_modifications:
                    for line_dict in original_rows[psm_identifier]:
                        line_dict['Mass Difference Annotations'] = new_mass_shift_anno
                        line_dict['PTMiner:Mass Shift Localization'] = new_mass_shift_pos
                        line_dict['PTMiner:Posterior Probability'] = ptminer_posterior_probability
                        line_dict['PTMiner:SDP Score'] = ptminer_sdp_score
                        line_dict['PTMiner:Annotation Type'] = annotation_type
                        line_dict['PTMiner:Result # for PSM'] = n
                        line_dict['PTMiner:Annotated Mod Pos within Pep or Prot'] = row['ObsMH']
                        line_dict['PTMiner:Annotated Mod Classification'] = row['Mass Shift']
                        line_dict['PTMiner:# Mass, Mod'] = row['Dataset Name']
                        # line_dict['Mass Difference'] = new_mass_shift
                        # line_dict['Modifications'] = new_mod
                        writer.writerow(line_dict)

            for psm_identifier in set(original_rows.keys()) - found_psm_identifier:
                for line_dict in original_rows[psm_identifier]:
                    writer.writerow(line_dict)

        new_psms_list = list(new_psms.keys())
        print('''
            [ WARNING ] {0} PSMs from PTMiner results were not present in the original results
            [ WARNING ] These have been skipped (truncated to 100):
            [ WARNING ] {1}'''.format(
                len(new_psms_list),
                new_psms_list if len(new_psms_list) <100 else new_psms_list[:99],
            )
        )

        # lost_psm_identifier = set(original_rows.keys()) - found_psm_identifier
        # if len(lost_psm_identifier) > 0:
        #     print('''
        #         [ WARNING ] {0} PSMs from the original results were not found in the PTMiner results
        #         [ WARNING ] These have been skipped (truncated to 100):
        #         [ WARNING ] {1}'''.format(
        #             len(lost_psm_identifier),
        #             list(lost_psm_identifier) if len(lost_psm_identifier) <100 else list(lost_psm_identifier)[:99],
        #         )
        #     )

        return merged_results_csv

    def sort_mods(self, modifications):
        mod_pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )
        tmp = []
        positions = set()
        for e in modifications:
            for occ, match in enumerate(mod_pattern.finditer(e)):
                mod = e[:match.start()]
                mod_pos = e[match.start()+1:]
                m = (int(mod_pos), mod)
                if m not in tmp:
                    tmp.append(m)
                    positions.add(int(mod_pos))
        tmp.sort()
        sorted_modifications = ';'.join(
            [
                '{m}:{p}'.format( m=mod, p=pos) for pos, mod in tmp
            ]
        )
        return sorted_modifications

    def write_params_file(self):
        with open(self.param_file_name, 'w') as io:
            print('''[Search]
# pFind 2.8 (.txt),MSFragger (.pepXML),Sequest (.txt) and PTMiner (.txt)
search_result_format = PTMiner (.txt)
#0 = close search, 1 = open search
open_search = {open_search}

# # peptide_tol and peptide_tol_type
# peptide_tol_type MUST be 0 = Da
precursor_matching_tolerance = {precursor_matching_tolerance}
precursor_matching_tolerance_type = 0

# the four parameters refer to spectrum precision
# 0 = Da, 1 = PPM
precursor_tol = {precursor_tol}
precursor_tol_type = {precursor_tol_type}
fragment_tol = {fragment_tol}
fragment_tol_type = {fragment_tol_type}

# fixed modifications in peptide identification process
fixed_mod_number = {fixed_mod_number}
{fixed_modifications}

# variable modifications in peptide identification process
var_mod_number = {var_mod_number}
{variable_modifications}

# dataset
# now only support mgf format
dataset_format = mgf
dataset_number = 1
dataset_filename_1 = {dataset}

# peptide identification results
pep_ident_format = PTMiner (.txt)
pep_ident_number = 1
pep_ident_filename_1 = {input_file}

[Fdr]
# do fdr control or not. 0=No, 1=Yes
is_fdr_control = {is_fdr_control}

# decoy tag
decoy_tag = {decoy_tag}

# fdr threshold
fdr_threshold = {fdr_threshold}

# fdr method, global=1,separate=2,transferred=3
fdr_method = 3

[Localization]
# do localization or not. 0=No, 1=Yes
is_localized = {is_localized}

# the minimum number of modifications
min_mod_number = {min_mod_number}

# use the prior probability or not.  0=No, 1=Yes
use_prior = {use_prior}

# the method to filter localization results
# 0 = probability, 1 = flr
filter_method = 1

# filter threshold
filter_threshold = 1

[Annotation]
# do annotation or not. 0=No, 1=Yes
is_annotated = {is_annotated}
protein_database = {protein_database}

[Output]
# output path
output = {output}
'''.format(
                **self.params_to_write),
                file=io
            )
        return