#!/usr/bin/env python3
'''
'''
import os
import ursgal


class sugarpy_1_0_0(ursgal.UNode):
    """
    SugarPy - discovery-driven analysis of glycan compositions from IS-CID of intact glycopeptides.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'SugarPy',
        'version'            : '1.0.0',
        'release_date'       : None,
        'engine_type'        : {
            'misc_engine' : True
        },
        'utranslation_style' : 'sugarpy_style_1',
        'citation'           : '',
        'input_extensions'   : ['.mzML'],
        'output_extensions'  : ['.csv'],
        'create_own_folder'  : True,
        'in_development'     : False,
        'include_in_git'     : False,
        'distributable'      : True,
        'engine'             : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe': 'SugarPy_1_0_0.py',
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """."""
        super(sugarpy_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        """Run SugarPy on a given list of .mzML files based on identified
        peptides from a evidences.csv

        Translated Ursgal parameters are passed to the SugarPy main function.
        """

        self.time_point(tag='execution')

        main = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        mzml_files = []

        for input_file_dict in self.params['input_file_dicts']:
            mzml_files.append(
                os.path.join(
                    input_file_dict['dir'],
                    input_file_dict['file']
                )
            )

        translations = self.params['translations']['_grouped_by_translated_key']

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
        }
        sugarpy_params[charges] = list(range(
            self.params['translations']['precursor_min_charge'],
            self.params['translations']['precursor_max_charge'] +1
        ))

        sugarpy_params = {}
        for translated_key, translation_dict in translations.items():
            if translated_key in pyqms_params.keys():
                pyqms_params[translated_key] = list(translation_dict.values())[0]
            elif 'charge' in translated_key:
                continue
            elif len(translation_dict) == 1:
                sugarpy_params[translated_key] = list(translation_dict.values())[0]
            else:
                print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                sys.exit(1)
        sugarpy_params['pyqms_params'] = pyqms_params
        sugarpy_params['mzml_files'] = mzml_files
        sugarpy_params['output_file'] = output_file

        out = main(**sugarpy_params)

        self.print_execution_time(tag='execution')
        return out
