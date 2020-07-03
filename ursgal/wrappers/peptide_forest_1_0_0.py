#!/usr/bin/env python
import ursgal
import os
import json
import sys
import csv


class peptide_forest_1_0_0( ursgal.UNode ):
    """PeptideForest 1_0_0 UNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'PeptideForest',
        'version'            : '1.0.0',
        'release_date'       : '2020-3-4',
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
        self.params['translations']['tmp_output_file'] = self.params[
            'translations']['output_file_incl_path'].replace('.csv', '_tmp.csv')

        self.created_tmp_files.append(
            self.params['translations']['tmp_output_file']
        )

        input_file_dicts = self.params['input_file_dicts']
        self.params['ursgal_path_dict'] = {}
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
                self.params['ursgal_path_dict'][file_path] = {
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
                self.params['ursgal_path_dict'][file_path] = {}
                for k, v in self.params['translations']['peptide_forest_file_params'][result_pos].items():
                    self.params['ursgal_path_dict'][file_path][k] = v

        self.write_input_file_json(self.params['ursgal_path_dict'])

        kwargs = {}
        translations = self.params['translations']['_grouped_by_translated_key']
        for translated_key, translation_dict in translations.items():
            if translated_key in [
                'score_bigger_better',
                'score_col',
                'ursgal_path_dict',
                'psm_defining_colnames',
                'psm_colnames_to_merge_multiple_values',
            ]:
                continue
            elif translated_key == 'initial_engine':
                ukey, translated_value = list(translation_dict.items())[0]
                if translated_value == '':
                    last_search_engine = self.get_last_search_engine(
                        history=self.stats['history']
                    )
                    if type(last_search_engine) is list:
                        print('''
                            [ERROR] Cannot automatically determine last search engine
                            Please specify which engine should be used for initial scoring
                            (i.e. "peptide_forest_initial_engine"). E.g., choose one of these:
                            {0}
                        '''.format(last_search_engine))
                        sys.exit(1)
                    kwargs[translated_key] = last_search_engine
                else:
                    kwargs[translated_key] = translated_value
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

        peptide_forest_main = self.import_engine_as_python_function(function_name='run_peptide_forest')
        peptide_forest_output_path = peptide_forest_main(
            output_file=self.params['translations']['tmp_output_file'],
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

    def postflight(self):
        '''
        map input file line dicts to output file PSMs
        '''
        output_file = self.params['translations']['output_file_incl_path']
        tmp_output_file = self.params['translations']['tmp_output_file']
        psm_colnames = self.params['translations']['psm_defining_colnames']

        out_fieldnames = []
        remove_columns = [
            'Mass',
            'dM',
            'enzN',
            'enzC',
            'enzInt',
            'PepLen',
            'CountProt',
        ]
        out_tmp_psm_dicts = {}
        with open(tmp_output_file, 'r') as out_tmp:
            csv_reader = csv.DictReader(out_tmp)
            out_tmp_fieldnames = csv_reader.fieldnames
            for fn in out_tmp_fieldnames:
                if fn not in remove_columns and fn.startswith('top_target') is False:
                    out_fieldnames.append(fn)
            for line_dict in csv_reader:
                reduced_line_dict = {}
                for k, v in line_dict.items():
                    if k not in out_fieldnames:
                        continue
                    reduced_line_dict[k] = v
                if reduced_line_dict['Modifications'] == 'None':
                    reduced_line_dict['Modifications'] = ''
                if reduced_line_dict['Is decoy'] == 'True':
                    reduced_line_dict['Is decoy'] = 'true'
                elif reduced_line_dict['Is decoy'] == 'False':
                    reduced_line_dict['Is decoy'] = 'false'
                else:
                    print(reduced_line_dict['Is decoy'])
                psm_id = []
                for colname in psm_colnames:
                    psm_id.append(reduced_line_dict[colname])
                psm_id = '||'.join(psm_id)
                if psm_id in out_tmp_psm_dicts.keys():
                    # out_tmp_psm_dicts[psm_id] = []
                    print('''
                        [ ERROR ] Multiple lines for the same PSM in PeptideForest output
                        [ ERROR ] This should never happen.
                        [ ERROR ] PSM-ID: {0}
                    '''.format(psm_id))
                out_tmp_psm_dicts[psm_id] = [reduced_line_dict]            

        input_file_dicts = self.params['input_file_dicts']
        for result_file_dict in input_file_dicts:
            input_file_path = os.path.join(
                result_file_dict['dir'],
                result_file_dict['file']
            )
            with open(input_file_path, 'r') as in_file:
                csv_reader = csv.DictReader(in_file)
                in_fieldnames = csv_reader.fieldnames
                for fn in in_fieldnames:
                    if fn not in out_fieldnames:
                        out_fieldnames.append(fn)
                for line_dict in csv_reader:
                    psm_id = []
                    for colname in psm_colnames:
                        psm_id.append(line_dict[colname])
                    psm_id = '||'.join(psm_id)
                    if psm_id not in out_tmp_psm_dicts.keys():
                        out_tmp_psm_dicts[psm_id] = []
                    out_tmp_psm_dicts[psm_id].append(line_dict)

        if sys.platform == 'win32':
            lineterminator = '\n'
        else:
            lineterminator = '\r\n'
        with open(output_file, 'w') as out_file:
            csv_writer = csv.DictWriter(
                out_file,
                fieldnames=out_fieldnames,
                lineterminator=lineterminator
            ) 
            csv_writer.writeheader()
            # import pprint
            for psm_id in out_tmp_psm_dicts.keys():
                # if 'TN_CSF_062617_02.10.10.3' in psm_id:
                    # pprint.pprint(out_tmp_psm_dicts[psm_id])
                    # print('===================================')
                if len(out_tmp_psm_dicts[psm_id]) > 1:
                    merged_row_dict = ursgal.ucore.merge_rowdicts(
                        out_tmp_psm_dicts[psm_id], 
                        self.params['translations']['psm_colnames_to_merge_multiple_values'],
                        joinchar=';',
                    )
                    csv_writer.writerow(merged_row_dict)
                    # if 'TN_CSF_062617_02.10.10.3' in psm_id:
                        # pprint.pprint(merged_row_dict)
                        # print('------------------------')
                else:
                    csv_writer.writerow(out_tmp_psm_dicts[psm_id][0])
                    # if 'TN_CSF_062617_02.10.10.3' in psm_id:
                        # pprint.pprint(out_tmp_psm_dicts[psm_id][0])
                        # print('______________________________')
                # exit()
        return