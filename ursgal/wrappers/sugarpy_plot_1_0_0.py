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
        'input_extensions'   : ['.mzML', '.csv'],
        'output_extensions'  : ['.txt'],
        'output_suffix'      : 'created_files',
        'create_own_folder'  : True,
        'in_development'     : True,
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

        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        translations = self.params['translations'][
            '_grouped_by_translated_key']

        pyqms_params = {
            'PERCENTILE_FORMAT_STRING': None,
            'M_SCORE_THRESHOLD': None,
            'ELEMENT_MIN_ABUNDANCE': None,
            'MIN_REL_PEAK_INTENSITY_FOR_MATCHING': None,
            'REQUIRED_PERCENTILE_PEAK_OVERLAP': None,
            'MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES': None,
            'INTENSITY_TRANSFORMATION_FACTOR': None,
            'UPPER_MZ_LIMIT': None,
            'LOWER_MZ_LIMIT': None,
            'MZ_TRANSFORMATION_FACTOR': None,
            'REL_MZ_RANGE': None,
            'REL_I_RANGE': None,
            'INTERNAL_PRECISION': None,
            'MAX_MOLECULES_PER_MATCH_BIN': None,
            'SILAC_AAS_LOCKED_IN_EXPERIMENT': None,
            'BUILD_RESULT_INDEX': None,
            'MACHINE_OFFSET_IN_PPM': None,
            'FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS': None,
            'MZ_SCORE_PERCENTILE': None,
        }
        sugarpy_params = {}
        sugarpy_params['charges'] = list(range(
            self.params['translations']['precursor_min_charge'],
            self.params['translations']['precursor_max_charge'] + 1
        ))

        for translated_key, translation_dict in translations.items():
            if translated_key == 'REL_MZ_RANGE':
                if self.params['translations']['ms_level'] == 1:
                    print(
                        '''
                        [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
                        [ WARNING ] need to be combined for SugarPy (use of symmetric tolerance window).
                        [ WARNING ] The arithmetic mean is used.
                        '''
                    )
                    pyqms_params['REL_MZ_RANGE'] = (
                        float(self.params['translations']['precursor_mass_tolerance_plus']) +
                        float(self.params['translations'][
                              'precursor_mass_tolerance_minus'])) / 2.0
                    if self.params['translations']['precursor_mass_tolerance_unit'] == 'da':
                        pyqms_params['REL_MZ_RANGE'] = \
                            ursgal.ucore.convert_dalton_to_ppm(
                                pyqms_params['REL_MZ_RANGE'],
                                base_mz=self.params['translations']['base_mz']
                        )
                else:
                    pyqms_params['REL_MZ_RANGE'] = \
                        self.params['translations']['frag_mass_tolerance']
                    if self.params['translations']['frag_mass_tolerance_unit'] == 'da':
                        pyqms_params['REL_MZ_RANGE'] = \
                            ursgal.ucore.convert_dalton_to_ppm(
                                pyqms_params['REL_MZ_RANGE'],
                                base_mz=self.params['translations']['base_mz']
                        )
                pyqms_params['REL_MZ_RANGE'] = pyqms_params['REL_MZ_RANGE'] * 1e-6
                sugarpy_params['frag_mass_tolerance'] = self.params['translations']['frag_mass_tolerance']
                if self.params['translations']['frag_mass_tolerance_unit'] == 'da':
                    sugarpy_params['frag_mass_tolerance'] = \
                        ursgal.ucore.convert_dalton_to_ppm(
                            sugarpy_params['frag_mass_tolerance'],
                            base_mz=self.params['translations']['base_mz']
                        )
            elif translated_key in pyqms_params.keys():
                pyqms_params[translated_key] = list(
                    translation_dict.values())[0]
            elif 'charge' in translated_key:
                continue
            elif len(translation_dict) == 1:
                sugarpy_params[translated_key] = list(
                    translation_dict.values())[0]
            else:
                print('The translated key ', translated_key,
                      ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                sys.exit(1)
        sugarpy_params['pyqms_params'] = pyqms_params
        sugarpy_params['mzml_file'] = input_file
        sugarpy_params['output_file'] = output_file

        out = main(**sugarpy_params)

        self.print_execution_time(tag='execution')
        return out
