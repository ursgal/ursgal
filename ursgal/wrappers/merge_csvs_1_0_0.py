#!/usr/bin/env python
import ursgal
import os


class merge_csvs_1_0_0( ursgal.UNode ):
    """Merge CSVS 1_0_0 UNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Merge CSVs',
        'version'            : '1.0.0',
        'release_date'       : '2016-3-4',
        'engine_type' : {
            'misc_engine' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'merged',
        'include_in_git'     : True,
        'in_development'     : False,
        'distributable'      : True,
        'utranslation_style' : 'merge_csvs_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'merge_csvs_1_0_0.py',
                },
            },
        },
        'citation' : \
            'Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. & '\
            'Fufezan, C. (2016) Ursgal, Universal Python Module Combining '\
            'Common Bottom-Up Proteomics Tools for Large-Scale Analysis. J. '\
            'Proteome res. 15, 788-794.',
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
        # self.time_point(tag = 'execution')
        csv_files = []

        for input_file_dict in self.params['input_file_dicts']:
            csv_files.append(
                os.path.join(
                    input_file_dict['dir'],
                    input_file_dict['file']
                )
            )

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        merge_csv_main = self.import_engine_as_python_function()
        merged_csv_output_path = merge_csv_main(
            csv_files = csv_files,
            output    = self.params['translations']['output_file_incl_path'],
        )
        # self.print_execution_time(tag='execution')
        return merged_csv_output_path
