#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import pickle

class add_estimated_fdr_1_0_0( ursgal.UNode ):
    """filter_csv_1_0_0 UNode"""
    def __init__(self, *args, **kwargs):
        super(add_estimated_fdr_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        '''
        print('[ -ENGINE- ] Executing conversion ..')
        self.time_point(tag = 'execution')
        add_fdr_main = self.import_engine_as_python_function()
        if self.params['input_file'].lower().endswith('.csv') is False:
            raise ValueError('add_estimated_fdr_1 input file must be a CSV file!')

        assert 'validation_score_field' in self.params and \
            isinstance( self.params['validation_score_field'], str), '''
  add_estimated_fdr requires a quality criterion (score) to calculate estimated FDRs.
  Please define the column name of that score using this syntax:
  >>> uc.params['validation_score_field'] = 'my_score_column'
  >>> uc.params['bigger_scores_better'] = False  # or True!
        '''

        score_field = self.params['validation_score_field']
        if 'bigger_scores_better' not in self.params:
            bigger_is_better = False
            print('''
  WARNING! You did not specify "bigger_scores_better" (True/False)
  in the UController params! By default, add_estimated_fdr assumes
  that small score values indicate PSMs of high quality.
  If you specified a score column where large values are better,
  the following FDR estimation will definitely lead to wrong results!
            ''')
        else:
            bigger_is_better = self.params['bigger_scores_better']

        output_file = os.path.join(
                self.params['output_dir_path'],
                self.params['output_file']
            )
        input_file  = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )
        
        add_fdr_main(
            input_file           = input_file,
            output_file          = output_file,
            score_colname        = score_field,
            bigger_scores_better = bigger_is_better,
        )

        self.print_execution_time(tag='execution')
        return output_file
