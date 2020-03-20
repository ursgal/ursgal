#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle
import csv
import copy
import re
import pprint
from collections import defaultdict as ddict

class compomics_utilities_4_11_5( ursgal.UNode ):
    """
    compomics_utilities_4_11_5 UNode

    Reference:
        Barsnes, H., Vaudel, M., Colaert, N., Helsens, K., Sickmann, A.,
        Berven, F. S., and Martens, L. (2011) compomics-utilities: an 
        open-source Java library for computational proteomics. BMC\
        Bioinformatics 12, 70

    Warning:
        Implementation still in beta-stage!

    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Compomic Utilities',
        'version'            : '4.11.5',
        'release_date'       : None,
        'engine_type' : {
            'misc_engine'     : True
        },
        'output_suffix'     : 'compomics',
        'input_extensions'  : ['.txt', ],
        'output_extensions' : ['.csv', ],
        'distributable' : False,
        'include_in_git'    : False,
        'in_development'    : False,
        'utranslation_style'    : 'compomics_utilities_style_1',
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'utilities-4.11.5.jar',
                    'url'            : '',
                    'zip_md5'        : '',
                },
            },
        },
        'citation' : \
        'Barsnes, H., Vaudel, M., Colaert, N., Helsens, K., Sickmann, A.,'
        'Berven, F. S., and Martens, L. (2011) compomics-utilities: an '
        'open-source Java library for computational proteomics. BMC'
        'Bioinformatics 12, 70'
    }

    def __init__(self, *args, **kwargs):
        super(compomics_utilities_4_11_5, self).__init__(*args, **kwargs)

    def set_up_command_list(self):
        '''
        java
        -cp
        utilities-4.11.5.jar
        com.compomics.util.experiment.identification.protein_inference.executable.PeptideMapping
        -p /media/plan-f/Shared/databases/Saccharomyces_cerevisiae/uniprot_version_20161016_download_date_20161213/uniprot-proteome%3AUP000002311.fasta
        test.txt
        test_out.txt

        '''

        if self.params['translations']['compomics_utility_name'] == 'com.compomics.util.experiment.identification.protein_inference.executable.PeptideMapping':
            command_list = [
                'java',
                '-cp',
                self.exe,
                self.params['translations']['compomics_utility_name'],
                '-p',
                self.params['translations']['database'],
                self.tmp_peptide_file,
                self.params['translations']['output_file_incl_path'],
            ]
        return command_list

    def preflight( self ):
        '''


        '''
        input_file_incl_path = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        if self.params['translations']['compomics_utility_name'] == 'com.compomics.util.experiment.identification.protein_inference.executable.PeptideMapping':

            # read csv and write txt input file...
            self.tmp_peptide_file = os.path.join(
                self.params['output_dir_path'],
                'peptides.txt'
            )
            with open(self.tmp_peptide_file, 'w') as io:
                peptides = set()
                for line_dict in csv.DictReader(open(input_file_incl_path,'r')):
                    appended = False
                    for aa_to_replace, replace_dict in sorted(self.params['translations']['aa_exception_dict'].items(), reverse=True):
                        if aa_to_replace in line_dict['Sequence']:
                            if aa_to_replace in ['O']:
                                if 'unimod_name' in replace_dict.keys():
                                    for r_pos, aa in enumerate(line_dict['Sequence']):
                                        if aa == aa_to_replace:
                                            index_of_aa = r_pos + 1
                                            unimod_name = replace_dict['unimod_name']
                                            new_mod = '{0}:{1}'.format(
                                                unimod_name,
                                                index_of_aa
                                            )
                                            if line_dict['Modifications'] == '':
                                                line_dict['Modifications'] += new_mod
                                            else:
                                                line_dict['Modifications'] += ';{0}'.format(
                                                    new_mod
                                                )
                                if len(replace_dict['original_aa']) == 1:
                                    line_dict['Sequence'] = line_dict['Sequence'].replace(
                                        aa_to_replace,
                                        replace_dict['original_aa'][0]
                                    )
                            elif aa_to_replace in ['J']:
                                repeat_count = line_dict['Sequence'].count(aa_to_replace)
                                #we need to do all combos for the positions of I and L in the seq...
                                positions = []
                                for index_of_aa, aa in enumerate(line_dict['Sequence']):
                                    if aa == aa_to_replace:
                                        positions.append( index_of_aa )
                                product_combos = []
                                new_peptides = set()
                                for combo_tuple in itertools.product(replace_dict['original_aa'],repeat=repeat_count):
                                    # product_combos.append(n)
                                    for pos, new_aa in enumerate(combo_tuple):
                                        index_of_aa = positions[pos]
                                        # text[:1] + 'Z' + text[2:]
                                        remapped_peptide = '{0}{1}{2}'.format(
                                            line_dict['Sequence'][:index_of_aa],
                                            new_aa,
                                            line_dict['Sequence'][index_of_aa+1:],
                                        )
                                        tmp_peptide_set.add(
                                            remapped_peptide
                                        )
                                        line_dict['Sequence'] = remapped_peptide
                                        csv_file_buffer.append( deepcopy(line_dict) )
                                        appended = True
                            else:
                                print(
                                    '''
                                    [ WARNING ] New not covered case of aa exception for: "{0}"
                                    [ WARNING ] Please adjust upeptide_mapper accordingly
                                    '''.format(aa_to_replace)
                                )
                                sys.exit(1)
                    if appended is False:
                        peptides.add(line_dict['Sequence'])
                for peptide in peptides:
                    print(peptide,file=io)       

        self.params['command_list'] = self.set_up_command_list()
        return self.params['translations']['output_file_incl_path']

    def postflight( self ):
        '''
        add pre and post amino acids to results and extend txt results..
        '''
        # read database and get full name and also the pre and post aa
        short_2_long_name_mapping = {}
        fasta_id_dict = {}
        for fastaID, sequence in ursgal.ucore.parse_fasta( open( self.params['translations']['database'], 'r' ) ):
            fasta_id_dict[fastaID] = sequence
            try:
                short_2_long_name_mapping[ fastaID.split('|')[1] ] = fastaID # uniprot style
            except:
                pass
        all_full_protein_names = list(fasta_id_dict.keys())
        buffered_maps = ddict(list)
        with open(self.params['translations']['output_file_incl_path'],'r') as io:
            for line in io.readlines():
                peptide, protein, start_pos = line.split(',')
                if protein in fasta_id_dict.keys():
                    full_protein_name = protein
                else:
                    #this is slow and inefficient, but we need the full name
                    # use pyahocorasick automaton?? :)))
                    if protein in short_2_long_name_mapping.keys():
                        full_protein_name = short_2_long_name_mapping[protein]
                    else:
                        for full_protein_name in all_full_protein_names:
                            if protein in full_protein_name:
                                short_2_long_name_mapping[protein] = full_protein_name
                                break

                sequence = fasta_id_dict[full_protein_name]
                start_pos = int(start_pos)
                stop_pos = start_pos + len(peptide)
                pre_pos = start_pos - 1
                if pre_pos < 0:
                    pre = '-'
                else:
                    pre = sequence[ pre_pos ]
                try:
                    post = sequence[ stop_pos ]
                except:
                    post = '-'

                buffered_maps[peptide].append(
                    {
                        'start' : start_pos + 1,
                        'end'   : stop_pos,
                        'pre'   : pre,
                        'post'  : post,
                        'id'    : full_protein_name
                    }
                )
        with open(self.params['translations']['output_file_incl_path'],'w') as io:
            for peptide, info_dict_list in buffered_maps.items():
                for info_dict in info_dict_list:
                    print(
                        '{0},{id},{start},{end},{pre},{post}'.format( 
                            peptide,
                            **info_dict
                        ),
                        file =io
                    )
        os.remove(self.tmp_peptide_file)
        return
