#!/usr/bin/env python3
'''
'''
import os
import ursgal


class sugarpy_plot_1_0_0(ursgal.UNode):
    """
    SugarPy - discovery-driven analysis of glycan compositions from IS-CID of intact glycopeptides.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'SugarPy Plot',
        'version'            : '1.0.0',
        'release_date'       : None,
        'engine_type'        : {
            'misc_engine' : True
        },
        'utranslation_style' : 'sugarpy_plot_style_1',
        'citation'           : '',
        'input_extensions'   : ['.mzML'],
        'output_extensions'  : ['.txt'],
        'output_suffix'      : 'created_files',
        'create_own_folder'  : True,
        'in_development'     : False,
        'include_in_git'     : False,
        'distributable'      : False,
        'engine'             : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe': 'sugarpy_plot_1_0_0.py',
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """."""
        super(sugarpy_plot_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        """Run the SugarPy plotting functions on a given .mzML file based on identified
        glycopeptides from SugarPy result .csv or a defined plot_molecule_dict as well as
        the corresponding validated_results_list.pkl

        Translated Ursgal parameters are passed to the SugarPy main function.
        """

        self.time_point(tag='execution')

        main = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        input_file  = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        translations = self.params['translations']['_grouped_by_translated_key']

        sugarpy_params = {}
        for translated_key, translation_dict in translations.items():
            if len(translation_dict) == 1:
                sugarpy_params[translated_key] = list(translation_dict.values())[0]
            else:
                print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                sys.exit(1)
        sugarpy_params['mzml_file'] = input_file
        sugarpy_params['output_file'] = output_file

        out = main(**sugarpy_params)

        self.print_execution_time(tag='execution')
        return out
