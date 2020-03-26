#!/usr/bin/env python
import ursgal
import os
import json
import sys


class peptide_forest_1_0_0( ursgal.UNode ):
    """PeptideForest 1_0_0 UNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'PeptideForest',
        'version'            : '1.0.0',
        'release_date'       : '20206-3-4',
        'engine_type' : {
            'validation_engine' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'peptide_forest_1_0_0_validated',
        'include_in_git'     : False,
        'in_development'     : False,
        'distributable'      : False,
        'utranslation_style' : 'peptide_forest_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'peptide_forest_1_0_0.py',
                },
            },
        },
        'citation' : \
            '',
    }

    def __init__(self, *args, **kwargs):
        super(peptide_forest_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        import engine from source

        write config file and format parameters
        '''
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        input_file_dicts = self.params['input_file_dicts']
        ursgal_path_dict = {}
        if self.params['translations']['peptide_forest_file_params'] == {}:
            for result_pos, result_file_dict in enumerate(input_file_dicts):
                last_search_engine = result_file_dict.get('last_engine', False)
                if last_search_engine is False:
                    print('''
                        [ERROR] Cannot determine last search engine for file
                        {0}
                        Please specify "peptide_forest_file_params" for this file.
                    '''.format(result_file_dict['file']))
                    sys.exit(1)
                else:
                    score_bigger_better = self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][last_search_engine]
                    score_col = self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][last_search_engine]

                file_path = os.path.join(
                    result_file_dict['dir'],
                    result_file_dict['file']
                )
                ursgal_path_dict[file_path] = {
                    'engine': last_search_engine,
                    'score_col': score_col,
                    'score_bigger_better': score_bigger_better
                }
        else:
            for result_pos, result_file_dict in enumerate(input_file_dicts):
                file_path = os.path.join(
                    result_file_dict['dir'],
                    result_file_dict['file']
                )
                if result_pos not in self.params['translations']['peptide_forest_file_params'].keys():
                    print('''
                        [ERROR] File specific parameters not defined for all input files.
                        Please add parameters for file number {0}
                        to "peptide_forest_file_params".
                    '''.format(result_pos))
                    sys.exit(1)
                ursgal_path_dict[file_path] = {}
                for k, v in self.params['translations']['peptide_forest_file_params'][result_pos].items():
                    ursgal_path_dict[file_path][k] = v

        self.write_input_file_json(ursgal_path_dict)

        kwargs = {}
        translations = self.params['translations']['_grouped_by_translated_key']
        for translated_key, translation_dict in translations.items():
            if translated_key in ['score_bigger_better', 'score_col', 'ursgal_path_dict']:
                continue
            elif len(translation_dict.keys()) == 1:
                ukey, translated_value = list(translation_dict.items())[0]
                if ukey == 'peptide_forest_general_params':
                    for k, v in translated_value.items():
                        kwargs[k] = v
                else:
                    kwargs[translated_key] = translated_value
            else:
                print('''
                    [ERROR] translated key maps on several ukeys but it is not specified
                    how to handle this:
                    {0}
                '''.format(translated_key))

        peptide_forest_main = self.import_engine_as_python_function()
        peptide_forest_output_path = peptide_forest_main(
            output_file=self.params['translations']['output_file_incl_path'],
            **kwargs
        )
        # self.print_execution_time(tag='execution')
        return peptide_forest_output_path

    def write_input_file_json(self, param_dict):
        json_file_location = os.path.join(
            os.path.dirname(self.exe),
            'config',
            'ursgal_path_dict.json'
        )
        with open(json_file_location, 'w') as param_json:
            json.dump(
                param_dict,
                param_json,
                indent=2,
            )