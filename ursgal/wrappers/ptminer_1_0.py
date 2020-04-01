#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import pickle
import shutil
import csv
from ursgal import ukb

class ptminer_1_0(ursgal.UNode):
    """ptminer_1_0 used for mass shifts localization and peptides anotation"""
    META_INFO = {
        'edit_version': 1.0,
        'name': 'PTMiner',
        'version': '1.0',
        'release_date': '2017-07',
        'utranslation_style': 'ptminer_style_1',
        'input_extensions': ['.mgf', '.csv'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        #'distributable': True,
        'engine_type': {
            'misc_engine' : True,
        },
        'engine': {
            'win32': {
                '64bit': {
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
        self.params['translations']['csv_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        mgf_input_file = self.params['translations']['mgf_input_file']
        ptminer_input = self.params['translations']['csv_input_file'].strip('.csv') + '.txt'
        tmp_csv = self.params['translations']['csv_input_file'].strip('.csv')  + '_tmp.csv'
        selected_columns = []
        #convert csv file into PTMiner input file
        with open(self.params['translations']['csv_input_file'], 'r') as csv_file:
        	csv_reader = csv.DictReader(csv_file)
        	for row in csv_reader:
        		tmp_dict = {}
        		tmp_dict['Dataset Name'] = mgf_input_file
        		tmp_dict['Spectrum Name'] = row['Spectrum Title']
        		tmp_dict['Sequence'] = row['Sequence']
        		tmp_dict['Charge'] = row['Charge']
        		tmp_dict['ObsMH'] = (float(row['Exp m/z']) * float(row['Charge'])) - (ukb.PROTON * (float(row['Charge']) - 1))
        		tmp_dict['Mass Shift'] = row['Mass Difference']
        		tmp_dict['Main Score'] = self.params['translations']['validation_score_field']
        		tmp_dict['High Score Better'] = self.params['translations']['bigger_scores_better']

        		#taking into account cases where there are multiple modifications:positions
        		tmp_dict['Identified Mod Name'] = ''
        		tmp_dict['Identified Mod Position'] = ''
        		mods = row['Modifications'].split(';')

        		for mod in mods:
        			if mod != '':
        				tmp_dict['Identified Mod Name'] += mod.split(':')[0] + ';'
        				tmp_dict['Identified Mod Position'] += mod.split(':')[1] + ';'
        		tmp_dict['Identified Mod Position'] = tmp_dict['Identified Mod Position'].strip(';')
        		tmp_dict['Identified Mod Name'] = tmp_dict['Identified Mod Name'].strip(';')
        		
        		tmp_dict['Protein Access'] = row['Protein ID']
        		tmp_dict['Before AA'] = row['Sequence Pre AA'] 
        		tmp_dict['After AA'] = row['Sequence Post AA']
        		selected_columns.append(tmp_dict)

        fieldnames_list = [	'Dataset Name', 
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

        with open(tmp_csv, 'w', newline='') as new_csvfile:
            writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames_list)
            writer.writeheader()
            for row in selected_columns:
            	writer.writerow(row)

        with open(tmp_csv, 'r') as csvfile:
        	reader = csv.reader(csvfile)
	        for line in reader:
	        	with open(ptminer_input, 'a') as txt:
	        		txt_writer = csv.writer(txt, delimiter='\t')
	        		txt_writer.writerow(line)

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
        self.params_to_write['precursor_matching_tolerance'] = self.params['translations']['max_mod_size']
        self.params_to_write['fragment_tol'] = self.params['translations']['frag_mass_tolerance']
        self.params_to_write['fragment_tol_type'] = self.params['translations']['frag_mass_tolerance_unit']
        self.params_to_write['dataset'] = mgf_input_file
        self.params_to_write['input_file'] = ptminer_input
        self.params_to_write['is_fdr_control'] = self.params['translations']['is_fdr_control']
        self.params_to_write['decoy_tag'] = self.params['translations']['decoy_tag']
        self.params_to_write['fdr_threshold'] = self.params['translations']['fdr_cutoff']
        self.params_to_write['fdr_method'] = self.params['translations']['fdr_method']
        self.params_to_write['is_localized'] = self.params['translations']['is_localized']
        self.params_to_write['min_mod_number'] = self.params['translations']['min_num_mods']
        self.params_to_write['use_prior'] = self.params['translations']['use_prior']
        self.params_to_write['is_annotated'] = self.params['translations']['is_annotated']
        self.params_to_write['protein_database'] = self.params['translations']['database']
        self.params_to_write['output'] = self.params['translations']['output_file_incl_path']
        self.params_to_write['fixed_modifications'] = ''
        self.params_to_write['fixed_mod_number'] = 0
        self.params_to_write['variable_modifications'] = ''
        self.params_to_write['var_mod_number'] = 0

        for modification in self.params['modifications']:
            modList = modification.split(',')
            if modList[1] == 'fix':
                self.params_to_write['fixed_mod_number'] += 1
                self.params_to_write['fixed_modifications'] += 'fixed_mod_%s = %s (%s)\n' % (self.params_to_write['fixed_mod_number'], modList[3], modList[0])
            if modList[1] == 'opt':
                self.params_to_write['var_mod_number'] += 1
                self.params_to_write['variable_modifications'] += 'var_mod_%s = %s (%s)\n' % (self.params_to_write['var_mod_number'], modList[3], modList[0])

        #create param file
        self.write_params_file()

        self.created_tmp_files.append(tmp_csv)
        #self.created_tmp_files.append(self.param_file_name)

        #command line
        self.params['command_list'] = [
            self.exe,
            self.param_file_name,
        ]
        return self.params
    def postflight(self):
        #fields from anno_result
        #Posterior Probability; Position; AA; SDP Score; Annotation Type; New Sequence; New Mod; New Mod Position; # Mass, Mod; 
        #Annotated Mass; Annotated Mod; Annotated Mod Site; Annotated Mod Term Spec; Annotated Mod Classification;

        #write new CSV to merge back into results
        anno_result = os.path.join(
            self.params['output_dir_path'],
            'anno_result.txt'
        )
        csv_input = self.params['translations']['csv_input_file']
        rows = {}
        fieldnames = []
        #read from orginal input csv file
        with open(csv_input, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            for row in reader:
                if (row['Spectrum Title'], row['Sequence']) not in rows:
                    rows[(row['Spectrum Title'], row['Sequence'])] = row
                else:
                    raise KeyError('The search engine reported more than one row for same PSM')

        #convert anno_result.txt into csv file
        anno_result_csv = os.path.join(self.params['output_dir_path'], 'anno_result.csv')
        input_txt = csv.reader(open(anno_result, 'rb'), delimiter = '\t')
        output_csv = csv.writer(open(anno_result_csv, 'wb'))
        output_csv.writerows(input_txt)

        #read from annotated results csv file
        with open(anno_result_csv, 'r') as anno_file:
            reader = csv.DictWriter(anno_file)
            for row in reader:
                if (row['Spectrum Name'], row['Sequence']) not in rows:
                    rows[(row['Spectrum Name'], row['Sequence'])] = {}
                    rows[(row['Spectrum Name'], row['Sequence'])]['Spectrum Title'] = row['Spectrum Name']
                    rows[(row['Spectrum Name'], row['Sequence'])]['Sequence'] = row['Sequence']
                    rows[(row['Spectrum Name'], row['Sequence'])]['Charge'] = row['Charge']
                    rows[(row['Spectrum Name'], row['Sequence'])]['Mass Difference'] = row['Mass Shift']
                    rows[(row['Spectrum Name'], row['Sequence'])]['Exp m/z'] = (float(row['ObsMH']) + (ukb.PROTON * (float(row['Charge']) - 1)))/float(row['Charge'])

                    pos = row['Identified Mod Position'].split(';')
                    mod_pos = ''
                    for p in pos:
                        mod_pos += row['Identified Mod Name']+':'+p+';'
                    mod_pos.strip(';')
                    rows[(row['Spectrum Name'], row['Sequence'])]['Modifications'] = mod_pos
                    rows[(row['Spectrum Name'], row['Sequence'])]['Protein ID'] = row['Protein Access']
                    rows[(row['Spectrum Name'], row['Sequence'])]['Sequence Pre AA'] = row['Before AA']
                    rows[(row['Spectrum Name'], row['Sequence'])]['Sequence Post AA'] = row['After AA']

                rows[(row['Spectrum Name'], row['Sequence'])]['Posterior Probability'] = row['Posterior Probability']
                rows[(row['Spectrum Name'], row['Sequence'])]['Position'] = row['Position']
                rows[(row['Spectrum Name'], row['Sequence'])]['AA'] = row['AA']
                rows[(row['Spectrum Name'], row['Sequence'])]['SDP Score'] = row['SDP Score']
                rows[(row['Spectrum Name'], row['Sequence'])]['Annotation Type'] = row['Annotation Type']
                rows[(row['Spectrum Name'], row['Sequence'])]['New Sequence'] = row['New Sequence']
                rows[(row['Spectrum Name'], row['Sequence'])]['New Mod'] = row['New Mod']
                rows[(row['Spectrum Name'], row['Sequence'])]['New Mod Position'] = row['New Mod Position']
                rows[(row['Spectrum Name'], row['Sequence'])]['# Mass, Mod'] = row['# Mass, Mod']
                rows[(row['Spectrum Name'], row['Sequence'])]['Annotated Mass'] = row['Annotated Mass']
                rows[(row['Spectrum Name'], row['Sequence'])]['Annotated Mod'] = row['Annotated Mod']
                rows[(row['Spectrum Name'], row['Sequence'])]['Annotated Mod Site'] = row['Annotated Mod Site']
                rows[(row['Spectrum Name'], row['Sequence'])]['Annotated Mod Term Spec'] = row['Annotated Mod Term Spec']
                rows[(row['Spectrum Name'], row['Sequence'])]['Annotated Mod Classification'] = row['Annotated Mod Classification']

        #write merged final csv
        merged_results_csv = csv_input.strip('.csv')+'_annotated.csv'

        fieldnames.extend([
            'Posterior Probability', 
            'Position', 
            'AA', 
            'SDP Score', 
            'Annotation Type', 
            'New Sequence', 
            'New Mod', 
            'New Mod Position', 
            '# Mass, Mod', 
            'Annotated Mass', 
            'Annotated Mod', 
            'Annotated Mod Site', 
            'Annotated Mod Term Spec', 
            'Annotated Mod Classification',
        ])

        with open(merged_results_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(rows[row])

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
precursor_tol = 5
precursor_tol_type = 1
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