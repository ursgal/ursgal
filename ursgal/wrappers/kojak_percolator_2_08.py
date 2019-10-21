#!/usr/bin/env python
import ursgal
import math
import csv
import bisect
import os
from collections import defaultdict as ddict
from collections import OrderedDict
import sys
import pprint


class kojak_percolator_2_08( ursgal.UNode ):
    """
    Kojak adjusted Percolator 2_08 UNode

    Kojak provides preformatted Percolator input, this is used direclty as the
    input file for Percolator. In contrast to the original Percolator node, the
    input files are not reformatted or used to write a new input file.

    Note:

        Percolator (2.08) has to be symlinked or copied to engine-folder
        'kojak_percolator_2_08' in order to make this node work.

    Reference:
    Käll L, Canterbury JD, Weston J, Noble WS, MacCoss MJ. (2007) Semi-supervised learning for peptide identification from shotgun proteomics datasets.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Kojak Percolator',
        'version'            : '2.08',
        'release_date'       : '2007-11-1',
        'engine_type' : {
            'validation_engine' : True,
        },
        'input_extensions'   : ['.txt'],
        'output_extensions'  : ['.tsv'],
        'output_suffix'      : 'percolator_2_08_validated',
        'create_own_folder'  : False,
        'distributable'  : False,
        'in_development'     : False,
        'include_in_git'     : None,
        'utranslation_style' : 'kojak_percolator_style_1',
        'engine' : {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'percolator_2_08',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'percolator',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'percolator.exe',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
                '32bit' : {
                    'exe'            : 'percolator.exe',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'K・・ｽ､ll L, Canterbury JD, Weston J, Noble WS, MacCoss MJ. (2007) '\
            'Semi-supervised learning for peptide identification from shotgun '\
            'proteomics datasets.',
    }

    def __init__(self, *args, **kwargs):
        super(kojak_percolator_2_08, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formatting the command line to via self.params
        '''

        self.params['translations']['input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        self.params['command_list'] = [
            # percolator -X pout.xml pin.tab >| yeast-01.psms
            self.exe,
            '--only-psms',
            '{input_file}'.format(**self.params['translations']),
            '--results-psms',
            '{output_file_incl_path}'.format(**self.params['translations']),
        ]


    def postflight( self ):
        '''
        Convert the percolator output .tsv into the .csv format with headers as in the
        unified csv format.
        '''
        new_output_file = self.params['translations']['output_file_incl_path'].replace('.perc.','_').replace('.tsv','.csv')
        percolator_output_dict_reader = csv.DictReader(
            open(
                self.params['translations']['output_file_incl_path'],
                'r'
            ),
            delimiter='\t'
        )
        translated_fieldnames = []
        for old_fieldname in percolator_output_dict_reader.fieldnames:
            new_fieldname = self.UNODE_UPARAMS['header_translations']['uvalue_style_translation'][old_fieldname]
            translated_fieldnames.append( new_fieldname )

        percolator_output_writer = csv.DictWriter(
            open(
                new_output_file,
                'w'
            ),
            fieldnames = translated_fieldnames
        )
        percolator_output_writer.writeheader()

        for pos, line_dict in enumerate(percolator_output_dict_reader):
            dict_2_write = {}
            proteinIds   = []
            for key, value in line_dict.items():
                if key in [ None, 'proteinIds']:
                    if key is None:
                        proteinIds += value
                    else:
                        proteinIds.append(value)
                else:
                    new_key = self.UNODE_UPARAMS['header_translations']['uvalue_style_translation'][key]

                    dict_2_write[new_key] = value
            dict_2_write['Protein ID'] = '__'.join(sorted(proteinIds))
            percolator_output_writer.writerow(dict_2_write)
        self.created_tmp_files += [
           self.params['translations']['output_file_incl_path']
        ]

        return
