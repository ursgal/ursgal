#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import csv
import os.path

# csv.field_size_limit(sys.maxsize)

class venndiagram_1_0_0( ursgal.UNode ):
    """Venn Diagram uNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Venndiagram',
        'version'            : '1.0.0',
        'release_date'       : None,
        'engine_type' : {
            'visualizer' : True,
        },
        'input_extensions'   : ['.csv'],
        'input_multi_file'   : True,
        'output_extensions'  : ['.svg'],
        'output_suffix'      : 'venndiagram',
        'include_in_git'     : True,
        'in_development'     : False,
        'utranslation_style' : 'venndiagram_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'venndiagram_1_0_0.py',
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
        super(venndiagram_1_0_0, self).__init__(*args, **kwargs)
        pass

    def _execute( self ):
        '''
        Plot Venn Diagramm for a list of .csv result files (2-5)

        Arguments are set in uparams.py but passed to the engine by self.params attribute

        Returns:
            dict: results for the different areas e.g. dict['C-(A|B|D)']['results']

            Output file is written to the common_top_level_dir
        '''
        # Keyword Arguments:
        #     Input files (self.params['_input_file_dicts']): list of dictionaries created by multi_run
        #     column_names (list)     : list of column names (str) used for the comparison
        #                               columns are merged if more than one column name given
        #     header (str)            : header of the produced Venn diagram
        #     label_list (list)       : list of labels in the same order as the input files list
        #                               names of last_search_engine are used if no label_list given
        #     output_file_name (str)  : created by self.magic_name_generator if None
        #     opacity (float)

        print('[ -ENGINE- ] Plotting Venn diagram ..')
        venndiagram_main = self.import_engine_as_python_function()

        venn_params = {}
        translations = self.params['translations']['_grouped_by_translated_key']

        output_file_name = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        if output_file_name == None:
            head, tail = self.determine_common_common_head_tail_part_of_names( input_file_dicts=input_file_dicts)
            output_file_name = head + tail

        translations['output_file']['output_file_incl_path'] = output_file_name

        for translated_key, translation_dict in translations.items():
            if translated_key in [
                'visualization_column_names',
                'visualization_label_list',
            ]:
                continue
            elif translated_key == 'visualization_font':
                venn_params['font'] = translation_dict['visualization_font'][0]
                venn_params['label font-size header'] = translation_dict['visualization_font'][1]
                venn_params['label font-size major'] = translation_dict['visualization_font'][2]
                venn_params['label font-size minor'] = translation_dict['visualization_font'][3]
                venn_params['label font-size venn'] = translation_dict['visualization_font'][3]
            elif translated_key == 'visualization_scaling_factors' :
                venn_params['cx'] = translation_dict['visualization_scaling_factors'][0]
                venn_params['cy'] = translation_dict['visualization_scaling_factors'][1]
            elif translated_key == 'visualization_size' :
                venn_params['width'] = translation_dict['visualization_size'][0]
                venn_params['height'] = translation_dict['visualization_size'][1]
            elif len(translation_dict) == 1:
                venn_params[translated_key] = list(translation_dict.values())[0]
            else:
                print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                exit(1)

        column_sets = {}
        default_label = ['label_A','label_B','label_C','label_D','label_E','label_F']
        input_file_dicts = self.params['input_file_dicts']
        data = []
        for result_pos, result_file in enumerate(input_file_dicts):
            has_last_engine = result_file.get('last_engine', False)
            if has_last_engine is False:
                label_for_venn = '{0}'.format( result_pos )
            else:
                label_for_venn = '{0} ({1})'.format(
                    has_last_engine,
                    result_pos
                )
            data_field = (
                label_for_venn,
                os.path.join(
                    result_file['dir'],
                    result_file['file']
                )
            )
            data.append( data_field )

        all_are_csv = all( [f[1].upper().endswith('.CSV') for f in data] )
        assert all_are_csv == True, "VennDiagram input files all have to be .csv"
        assert len(data) <= 5, '''
            ERROR: input_file_list can only contain two to five result files,
            you can merge files before, if you need.
            Current number of files: {0}'''.format(len(data))

        used_labels = []

        for n, (engine, file_path) in enumerate(data):
            if self.params['translations']['visualization_label_list'] == []:
                label = engine
            else:
                label = self.params['translations']['visualization_label_list'][n]
            venn_params[default_label[n]] = label
            column_sets[ label ]     = set()
            used_labels.append(label)
            print('[ Reading  ] Venn set {0} / file #{1} : {0}'.format(
                n,
                file_path)
            )
            file_object = open(file_path, 'r')
            csv_input = csv.DictReader(
                filter(
                    lambda row: row[0] != '#', file_object
                )
            )
            for line_dict in csv_input:
                value = ''
                for column_name in self.params['translations']['visualization_column_names']:
                    value += '||{0}'.format( line_dict[column_name] )
                column_sets[ label ].add( value )

        in_sets = []
        for label in used_labels:
            in_sets.append( column_sets[label] )

        return_dict = venndiagram_main(
            *in_sets,
            **venn_params
            )

        return return_dict
