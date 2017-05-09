#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import pickle

class add_estimated_fdr_1_0_0( ursgal.UNode ):
    """add_estimated_fdr_1_0_0 UNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Add Estimated FDR',
        'version'            : '1.0.0',
        'release_date'       : '2008-1-1',
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'   : ['.csv'],
        'input_multi_file'   : False,
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'withFDR',
        'in_development'     : False,
        'include_in_git'     : True,
        'utranslation_style' : 'add_estimated_fdr_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'add_estimated_fdr_1_0_0.py',
                },
            },
        },
        'citation' : \
            'An implementation of the target/decoy FDR estimation method '\
            'described in: Lukas Kall, John D. Storey, Michael J. MacCoss and '\
            'William Stafford Noble (2008) Assigning significance to peptides '\
            'identified by tandem mass spectrometry using decoy databases.' ,
    }

    def __init__(self, *args, **kwargs):
        super(add_estimated_fdr_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        '''
        print('[ -ENGINE- ] Executing conversion ..')
        # self.time_point(tag = 'execution')
        add_fdr_main = self.import_engine_as_python_function()
        if self.params['input_file'].lower().endswith('.csv') is False:
            raise ValueError('add_estimated_fdr_1_0_0 input file must be a CSV file!')

        # if the user specified a specific score to use for FDR estimation, use that:
        if self.params['validation_score_field'] is not None and self.params['bigger_scores_better'] is not None:
            score_field = self.params['validation_score_field']
            bigger_is_better = self.params['bigger_scores_better']
        # otherwise, estimate the FDR based on the score of the last search engine:
        else:
            last_search_engine = self.get_last_search_engine(
                history = self.stats['history']
            )
            assert last_search_engine, '''
  Could not detect which search engine produced the input file.
  "add_estimated_fdr" requires a quality criterion (score) to calculate estimated FDRs.
  Please make sure your input file has a proper ursgal u.json file, or define the
  column name of that score using this syntax:
  >>> uc.params['validation_score_field'] = 'my_score_column'
  >>> uc.params['bigger_scores_better'] = False  # or True!
        '''
            print('Estimating FDR based on the raw "{}" scores since '
                '"validation_score_field" and "bigger_scores_better" '
                'were not manually specified in the UController.params.'.format(
                    last_search_engine))
            score_field = self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][last_search_engine]
            bigger_is_better = self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][last_search_engine]

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

        # self.print_execution_time(tag='execution')
        return output_file
