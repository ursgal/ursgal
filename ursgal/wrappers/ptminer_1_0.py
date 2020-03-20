#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import pickle
import shutil
import csv
import copy
import re
from ursgal import ukb
import pprint

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
        merged_mgf_file = mgf_input_files[0].strip('.mgf') + '_merged.mgf'
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
                last_search_engine_colname = self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][last_engine]

            if last_engine_bigger_scores_better is None:
                last_engine = self.get_last_search_engine(
                    history = self.stats['history'],
                )
                if type(last_engine) is list:
                    raise Exception('''
                        You need to specify bigger_scores_better param.
                        Each of these engines %s may define that param differently
                        ''' % last_engine)
                last_engine_bigger_scores_better = self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][last_engine]

    
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
                tmp_dict['Protein Access'] = row['Protein ID']
                tmp_dict['Before AA'] = row['Sequence Pre AA'] 
                tmp_dict['After AA'] = row['Sequence Post AA']
                selected_columns.append(tmp_dict)

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

        if os.path.exists(ptminer_input):
            os.remove(ptminer_input)
        with open(ptminer_input, 'w', newline='') as new_csvfile:
            writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames_list, delimiter='\t')
            writer.writeheader()
            for row in selected_columns:
                writer.writerow(row)

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
        self.created_tmp_files.append(self.param_file_name)
        self.created_tmp_files.append(merged_mgf_file)
        return self.params
    def postflight(self, anno_result=None, csv_input=None, merged_results_csv=None):
        #fields from anno_result
        #Posterior Probability; Position; AA; SDP Score; Annotation Type; New Sequence; New Mod; New Mod Position; # Mass, Mod; 
        #Annotated Mass; Annotated Mod; Annotated Mod Site; Annotated Mod Term Spec; Annotated Mod Classification;

        filtered_result = os.path.join(self.params_to_write['output'],'filtered_result.txt')
        loc_result = os.path.join(self.params_to_write['output'],'loc_result.txt')
        prior_probability = os.path.join(self.params_to_write['output'],'prior_probability.txt')
        if anno_result is None:
            anno_result = os.path.join(self.params_to_write['output'],'anno_result.txt')

        if csv_input is None:
            csv_input = self.params['translations']['csv_input_file']
        original_rows = {}
        fieldnames = []
        #read from original input csv file
        with open(csv_input, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            for row in reader:
                psm_identifier = '#'.join([row['Spectrum Title'], row['Sequence'], row['Modifications']])
                if psm_identifier not in original_rows:
                    original_rows[psm_identifier] = [row]
                else:
                    original_rows[psm_identifier].append(row)

        #convert anno_result.txt into csv file
        anno_result_csv = os.path.join(self.params['output_dir_path'], 'anno_result.csv')
        input_txt = csv.reader(open(anno_result, 'r'), delimiter = '\t')
        output_csv = csv.writer(open(anno_result_csv, 'w'))
        output_csv.writerows(input_txt)

        second_row_translations = { 'Dataset Name': '# Mass, Mod', 
                                    'Spectrum Name': 'Annotated Mass',
                                    'Sequence': 'Annotated Mod',
                                    'Charge': 'Annotated Mod Site',
                                    'ObsMH': 'Annotated Mod Term Spec',
                                    'Mass Shift': 'Annotated Mod Classification',
                                }
        annotated_rows = {}
        #read from annotated results csv file
        with open(anno_result_csv, 'r') as anno_file:
            reader = csv.DictReader(anno_file)
            previous_row = {}
            added_annotation_columns = True
            for row in reader:
                #skip the second line, which is part of the headers
                if row['Dataset Name'] == '# Mass, Mod':
                    continue
               
                if row['#'] == '*':
                    copy_prev_row = copy.deepcopy(previous_row)
                    for k, v in second_row_translations.items():
                        copy_prev_row[v] = row[k]
                    psm_identifier = '#'.join([copy_prev_row['Spectrum Title'], copy_prev_row['Sequence'], copy_prev_row['Modifications']])
                    annotated_rows[psm_identifier].append(copy_prev_row)
                    added_annotation_columns = True

                else:
                    if not added_annotation_columns:
                        annotated_rows['#'.join([previous_row['Spectrum Title'], previous_row['Sequence'], previous_row['Modifications']])].append(previous_row)
                    added_annotation_columns = False

                    subrow = {}
                    subrow['Spectrum Title'] = row['Spectrum Name']
                    subrow['Sequence'] = row['Sequence']
                    subrow['Charge'] = row['Charge']
                    subrow['Mass Shift'] = row['Mass Shift']
                    subrow['Exp m/z'] = (float(row['ObsMH']) + (ukb.PROTON * (float(row['Charge']) - 1)))/float(row['Charge'])

                    pos = row['Identified Mod Position'].split(';')
                    mod = row['Identified Mod Name'].split(';')
                    mod_pos_list = []
                    for m, p in zip(mod, pos):
                        if m == '':
                            continue
                        mod_pos_list.append(m+':'+p)
                    mod_pos = ';'.join(mod_pos_list)

                    subrow['Modifications'] = mod_pos
                    subrow['Protein ID'] = row['Protein Access']
                    subrow['Sequence Pre AA'] = row['Before AA']
                    subrow['Sequence Post AA'] = row['After AA']
                    subrow['Posterior Probability'] = row['Posterior Probability']
                    subrow['Position'] = row['Position']
                    subrow['AA'] = row['AA']
                    subrow['SDP Score'] = row['SDP Score']
                    subrow['Annotation Type'] = row['Annotation Type']
                    subrow['New Sequence'] = row['New Sequence']
                    subrow['New Mod'] = row['New Mod']
                    subrow['New Mod Position'] = row['New Mod Position']

                    psm_identifier = '#'.join([subrow['Spectrum Title'], subrow['Sequence'], subrow['Modifications']])
                    if psm_identifier not in annotated_rows:
                        annotated_rows[psm_identifier] = []

                    #check if there is new sequence, and if so create a new row for it
                    if str(row['New Sequence']).strip() != '' and row['New Sequence'] is not None:
                        new_row = copy.deepcopy(subrow)
                        subrow['New Sequence'] = ''
                        subrow['New Mod'] = ''
                        subrow['New Mod Position'] = ''
                        annotated_rows[psm_identifier].append(new_row)

                    previous_row = subrow

        self.created_tmp_files.append(anno_result_csv)
        self.created_tmp_files.append(anno_result)
        self.created_tmp_files.append(filtered_result)
        self.created_tmp_files.append(loc_result)
        self.created_tmp_files.append(prior_probability)

        #merge the two dictionaries
        rows = []
        keys_from_annotated_file_and_ursgal_results = set()
        for key in original_rows.keys():
            if key not in annotated_rows.keys():
                #add the row anyways
                for subrow in original_rows[key]:
                    rows.append(subrow)
                continue
            keys_from_annotated_file_and_ursgal_results.add(key)
            #the same row in the original results file can generate multiple rows after annotation by PTMiner 
            for row in annotated_rows[key]:
                #add missing keys from the search engine's results to the annotated results
                for column_name in original_rows[key][0].keys():
                    if column_name in row.keys():
                        continue
                    row[column_name] = original_rows[key][0][column_name]
                #deal with new modification from new sequence
                if str(row['New Sequence']).strip() != '' and row['New Sequence'] is not None:
                    #we assume there is only one position for the new modification
                    #we first separate AA from modification
                    row['AA'] = str(row['New Mod']).split(' ', 2)[1][1:-1]
                    row['New Modification'] = '%s:%s' % (str(row['New Mod']).split(' ', 2)[0], row['New Mod Position'])
                    row['Mass Difference'] = ''
                    row.pop('Position', None)
                    row.pop('New Mod Position', None)
                    row.pop('Mass Shift', None)
                    row.pop('New Mod', None)
                    rows.append(row)
                else:
                    #merge old modifications with annotated modifications
                    #AA to position correspondance
                    positions = str(row['Position']).split(';')
                    AAs = row['AA'].split(';')
                    aa_pos = {}
                    for p,aa in zip(positions, AAs):
                        if aa in aa_pos:
                            aa_pos[aa].append(p)
                        else:
                            aa_pos[aa] = [p]

                    #create a new row for each possible positions for an aa
                    if 'Annotated Mod' not in row: #this is the case where there is no annotation nor annotated mass
                        for aa in aa_pos.keys():
                            for p in aa_pos[aa]:
                                new_row = copy.deepcopy(row)
                                new_row['Mass Difference'] = '%s:%s' % (row['Mass Shift'], p)
                                new_row['AA'] = aa
                                new_row.pop('Position', None)
                                new_row.pop('New Sequence', None)
                                new_row.pop('New Mod', None)
                                new_row.pop('New Mod Position', None)
                                new_row.pop('Mass Shift', None)
                                rows.append(new_row)
                    else:
                        if row['Annotated Mod'] is None:#this is the case where only annotated mass is given without further identification
                            # for aa in aa_pos.keys():
                            #     for p in aa_pos[aa]:
                            #         new_row = copy.deepcopy(row)
                            #         new_row['Mass Difference'] = '%s:%s' % (row['Annotated Mass'], p)
                            #         new_row['AA'] = aa
                            #         new_row.pop('Position', None)
                            #         new_row.pop('New Mod Position', None)
                            #         new_row.pop('Annotated Mod', None)
                            #         new_row.pop('Annotated Mass', None)
                            #         new_row.pop('New Sequence', None)
                            #         new_row.pop('New Mod', None)
                            #         new_row.pop('Mass Shift', None)
                            #         new_row.pop('Annotated Mod Site', None)
                            #         rows.append(new_row)
                            continue
                        else:
                            aa = str(row['Annotated Mod']).split(' ', 2)[1][1:-1]
                            for p in aa_pos[aa]:
                                new_row = copy.deepcopy(row)
                                new_row['Modifications'] = '%s;%s:%s' % (row['Modifications'], str(row['Annotated Mod']).split(' ', 2)[0], p)
                                if str(row['Modifications']) == '':
                                    new_row['Modifications'] = new_row['Modifications'][1:]
                                new_row['Modifications'].strip(';')
                                new_row['Mass Difference'] = '%s:%s' % (row['Annotated Mass'], p)
                                new_row['AA'] = aa
                                new_row.pop('Position', None)
                                new_row.pop('New Mod Position', None)
                                new_row.pop('Annotated Mod', None)
                                new_row.pop('Annotated Mass', None)
                                new_row.pop('New Sequence', None)
                                new_row.pop('New Mod', None)
                                new_row.pop('New Mod Position', None)
                                new_row.pop('Mass Shift', None)
                                new_row.pop('Annotated Mod Site', None)
                                rows.append(new_row)
                    
        for key in annotated_rows:
            if key not in keys_from_annotated_file_and_ursgal_results:
                #this case should never happen
                raise KeyError('For some reason, PTMiner created this PSM: %s' % key)

        #write merged final csv
        if merged_results_csv is None:
            merged_results_csv = os.path.join(
                self.params['translations']['output_file_incl_path']
            )
        print(merged_results_csv)
        fieldnames.extend([
            'New Sequence',
            'New Modification',
            'Annotation Type', 
            '# Mass, Mod',  
            'Annotated Mod Term Spec', 
            'Annotated Mod Classification',
            'AA',
            'Posterior Probability',
            'SDP Score',
        ])

        with open(merged_results_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return merged_results_csv
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