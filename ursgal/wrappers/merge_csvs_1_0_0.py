#!/usr/bin/env python3.4
import ursgal
import os


class merge_csvs_1_0_0( ursgal.UNode ):
    """Merge CSVS 1_0_0 UNode"""
    META_INFO = {
        'engine_type'            : {
            'converter'         : True,
        },
        'output_extension'       : '.csv',
        'output_suffix'          : 'merged',
        'input_types'            : ['.csv'],
        'include_in_git'            : True,
        'in_development'            : True,
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'merge_csvs_1_0_0.py',
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        super(merge_csvs_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Merges .csv files

        for same header, new rows are appended

        for different header, new columns are appended
        '''
        print('[ -ENGINE- ] Merging csv files...')
        self.time_point(tag = 'execution')
        csv_files = []

        for input_file_dict in self.params['input_file_dicts']:
            csv_files.append(
                os.path.join(
                    input_file_dict['dir'],
                    input_file_dict['file']
                )
            )

        self.params['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        merge_csv_main = self.import_engine_as_python_function()
        merged_csv_output_path = merge_csv_main(
            csv_files = csv_files,
            output    = self.params['output_file_incl_path'],
        )
        self.print_execution_time(tag='execution')
        return merged_csv_output_path
