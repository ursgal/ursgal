#!/usr/bin/env python3
'''
'''
import os
import ursgal
import sys
import importlib


class glycopeptide_fragmentor_1_0_0(ursgal.UNode):
    """
    SugarPy - discovery-driven analysis of glycan compositions from IS-CID of intact glycopeptides.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Glycopeptide Fragmentor',
        'version'            : '1.0.0',
        'release_date'       : None,
        'engine_type'        : {
            'misc_engine' : True
        },
        'utranslation_style' : 'glycopeptide_fragmentor_style_1',
        'citation'           : '',
        'input_extensions'   : ['.mzML', '.csv', '.idx.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'glycofrag_ions',
        'create_own_folder'  : False,
        'in_development'     : False,
        'include_in_git'     : False,
        'distributable'      : False,
        'engine'             : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe': 'glycopeptide_fragmentor_1_0_0.py',
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """."""
        super(glycopeptide_fragmentor_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        """
        Import the main function from Glycopeptide Fragmentor.
        Translated Ursgal parameters are passed to the Glycopeptide Fragmentor main function.
        """

        self.time_point(tag='execution')

        main = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        translations = self.params['translations'][
            '_grouped_by_translated_key']

        glycopep_params = {}
        glycopep_params['frag_mass_tolerance'] = self.params['translations']['frag_mass_tolerance']
        if self.params['translations']['frag_mass_tolerance_unit'] == 'da':
            glycopep_params['frag_mass_tolerance'] = \
                ursgal.ucore.convert_dalton_to_ppm(
                    glycopep_params['frag_mass_tolerance'],
                    base_mz=self.params['translations']['base_mz']
                        )
        glycopep_params['glycopep_ident_file'] = input_file
        glycopep_params['output_file'] = output_file
        glycopep_params['mzml_file_list'] = self.params['translations']['mzml_input_files']
        glycopep_params['internal_precision'] = self.params['translations']['internal_precision']
        glycopep_params['decoy_glycan'] = self.params['translations']['sugarpy_decoy_glycan']
        glycopep_params['min_Y_ions'] = self.params['translations']['min_y_ions']
        glycopep_params['min_oxonium_ions'] = self.params['translations']['min_oxonium_ions']

        out = main(**glycopep_params)

        self.print_execution_time(tag='execution')
        return out
