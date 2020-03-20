#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle
import shutil

class sanitize_csv_1_0_0( ursgal.UNode ):
    """sanitize_csv_1_0_0 UNode

    Result files (.csv) are sanitized following defined parameters.
    That means, for each spectrum PSMs are compared and the
    best spectrum (spectra) is (are) chosen.

    The parameters have to be defined in the params. See the engine
    documentation for further information ( :meth:`.sanitize_csv_1_0_0._execute` ).
    """

    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Sanitize CSV',
        'version'            : '1.0.0',
        'release_date'       : None,
        'engine_type' : {
            'misc_engine' : True
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'sanitized',
        'in_development'     : False,
        # 'rejected_output_suffix': 'rejected',
        'include_in_git'     : True,
        'distributable'      : True,
        'group_psms'         : True,
        'utranslation_style' : 'sanitize_csv_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'sanitize_csv_1_0_0.py',
                },
            },
        },
        'citation' : \
            ''
    }


    def __init__(self, *args, **kwargs):
        super(sanitize_csv_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Result files (.csv) are sanitized following defined parameters.
        That means, for each spectrum PSMs are compared and the
        best spectrum (spectra) is (are) chosen

        Input file has to be a .csv

        Creates a _sanitized.csv file and returns its path.

        Note:

            If not specified, the validation_score_field and
            bigger_scores_better parameters are determined from the
            last engine. Therefore, if sanitize_csv_1_0_0 is applied to
            merged or processed result files, both parameters need to be
            specified.


        Available parameters:

            * score_diff_threshold (float): minimum score difference between
                the best PSM and the first rejected PSM of one spectrum
            * threshold_is_log10 (bool): True, if log10 scale has been used for
                score_diff_threshold.
            * accept_conflicting_psms (bool): If True, multiple PSMs for one
                spectrum can be reported if their score difference is below
                the threshold. If False, all PSMs for one spectrum are removed
                if the score difference between the best and secondbest PSM
                is not above the threshold, i.e. if there are conflicting PSMs
                with similar scores.
            * num_compared_psms (int): maximum number of PSMs (sorted by score,
                starting with the best scoring PSM) that are compared
            * remove_redundant_psms (bool): If True, redundant PSMs (e.g.
                the same identification reported by multiple engined) for the
                same spectrum are removed. An identification is defined by the
                combination of 'Sequence', 'Modifications' and 'Charge'.

        '''
        print('[ -ENGINE- ] Executing conversion ..')
        # self.time_point(tag = 'execution')
        sanitize_csv_main = self.import_engine_as_python_function()
        if self.params['output_file'].lower().endswith('.csv') is False:
            raise ValueError('Sanitize_csv only works for csv files.')

        output_file = os.path.join(
                self.params['output_dir_path'],
                self.params['output_file']
            )
        input_file  = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        bigger_scores_better = self.params['translations']['bigger_scores_better']
        validation_score_field = self.params['translations']['validation_score_field']

        if bigger_scores_better is None or validation_score_field is None:
            last_engine = self.get_last_search_engine( history = self.stats['history'] )
            print('''
[ WARNING ] Sanitizing based on the raw "{}" scores since
[ WARNING ] "validation_score_field" and/or "bigger_scores_better"
[ WARNING ] were not manually specified in the UController.params.
            '''.format(last_engine))
            if last_engine is None or type(last_engine) == list:
                print('''
                    Could not determine last_search_engine from input file.
                    Got {0}
                    Please specify parameters validation_score_field and bigger_scores_better
                '''.format(last_engine))
                sys.exit(1)
            else:
                bigger_scores_better = self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][last_engine]
                validation_score_field = self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][last_engine]

        # if self.params['translations']['write_unfiltered_results'] is False:
        #     output_file_unfiltered = None
        # else:
        #     file_extension = self.META_INFO.get(
        #         'output_suffix',
        #         None
        #     )
        #     new_file_extension = self.META_INFO.get(
        #         'rejected_output_suffix',
        #         None
        #     )
        #     output_file_unfiltered = output_file.replace(
        #         file_extension,
        #         new_file_extension
        #     )
        #     shutil.copyfile(
        #         '{0}.u.json'.format(output_file),
        #         '{0}.u.json'.format(output_file_unfiltered)
        #     )

        sanitize_csv_main(
            input_file              = input_file,
            output_file             = output_file,
            grouped_psms            = self.params['grouped_psms'],
            validation_score_field  = validation_score_field,
            bigger_scores_better    = bigger_scores_better,
            log10_threshold         = self.params['translations']['threshold_is_log10'],
            score_diff_threshold    = self.params['translations']['score_diff_threshold'],
            accept_conflicting_psms = self.params['translations']['accept_conflicting_psms'],
            num_compared_psms       = self.params['translations']['num_compared_psms'],
            remove_redundant_psms   = self.params['translations']['remove_redundant_psms'],
        )

        # self.print_execution_time(tag='execution')
        return output_file
