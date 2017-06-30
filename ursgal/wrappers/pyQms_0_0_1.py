#!/usr/bin/env python3
'''
'''
import os
import ursgal

class pyQms_0_0_1(ursgal.UNode):
    '''
    '''
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'pyQms',
        'version'                     : '0.0.1',
        'input_multi_file'          : False,
        'release_date'                : None,
        'engine_type'        : {
            'quantitation_engine' : True
        },
        'utranslation_style' : 'pyQms_style_1',
        'citation'           : 'pyQms, Leufken et. al.',
        'input_extensions'   : ['.mzML', '.csv'],
        # 'input_types'        : None,#['.mzML', ',csv'],
        'output_extensions'   : ['.csv'],
        'create_own_folder'  : True,
        'in_development'     : False,
        'include_in_git'     : False,
        # Download Information
        'engine'             : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'pyQms_0_0_1.py',
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """."""
        super(pyQms_0_0_1, self).__init__(*args, **kwargs)

    def _execute(self):
        """run."""
        from pprint import pprint
        # pprint(self.params)
        print('[ -ENGINE- ] Executing quantitation ..')
        self.time_point(tag = 'execution')

        main = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        pickle_file = os.path.join(
            self.params['output_dir_path'],
            self.params['translations']['pyQms_pickle_name']
        )
        # multiple input mzML files
        if self.params['input_file'].endswith('.json'):
            mzml_files = []
            for fdict in self.params['input_file_dicts']:
                mzml_files.append(fdict['full'])
        else:  # sing mzML file
            mzml_files = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        # pyqms_params = {
        #   'PERCENTILE_FORMAT_STRING'                :
        #       self.params['PERCENTILE_FORMAT_STRING'],
        #    'M_SCORE_THRESHOLD'                       :
        #        self.params['M_SCORE_THRESHOLD'],
        #    'ELEMENT_MIN_ABUNDANCE'                   :
        #        self.params['ELEMENT_MIN_ABUNDANCE'],
        #    'MIN_REL_PEAK_INTENSITY_FOR_MATCHING'     :
        #        self.params['MIN_REL_PEAK_INTENSITY_FOR_MATCHING'],
        #    'REQUIRED_PERCENTILE_PEAK_OVERLAP'        :
        #        self.params['REQUIRED_PERCENTILE_PEAK_OVERLAP'],
        #    'MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES' :
        #        self.params['MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES'],
        #    'INTENSITY_TRANSFORMATION_FACTOR'         :
        #        self.params['INTENSITY_TRANSFORMATION_FACTOR'],
        #    'UPPER_MZ_LIMIT'                          :
        #        self.params['UPPER_MZ_LIMIT'],
        #    'LOWER_MZ_LIMIT'                          :
        #        self.params['LOWER_MZ_LIMIT'],
        #    'MZ_TRANSFORMATION_FACTOR'                :
        #        self.params['MZ_TRANSFORMATION_FACTOR'],
        #    'REL_MZ_RANGE'                            :
        #        self.params['REL_MZ_RANGE'],
        #    'REL_I_RANGE'                             :
        #        self.params['REL_I_RANGE'],
        #    'INTERNAL_PRECISION'                      :
        #        self.params['INTERNAL_PRECISION'],
        #    'MAX_MOLECULES_PER_MATCH_BIN'             :
        #        self.params['MAX_MOLECULES_PER_MATCH_BIN'],
        #    'SILAC_AAS_LOCKED_IN_EXPERIMENT'          :
        #        self.params['SILAC_AAS_LOCKED_IN_EXPERIMENT'],
        #    'BUILD_RESULT_INDEX'                      :
        #        self.params['BUILD_RESULT_INDEX'],
        #    'MACHINE_OFFSET_IN_PPM'                   :
        #        self.params['MACHINE_OFFSET_IN_PPM'],
        #    'FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS'   :
        #        self.params['FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS'],
        #    'COLORS'                                  :
        #        self.params['COLORS'],
        # }

        fixed_labels = {}
        for fixed_mod in self.params['mods']['fix']:
            aa = fixed_mod['aa']
            comp = fixed_mod['composition']
            name = fixed_mod['name']
            if not fixed_labels.get(aa, False):
                fixed_labels[aa] = []
            fixed_labels[aa].append(
                {
                    'element_composition' : comp,
                    'evidence_mod_name'   : name
                }
            )
        out = main(
            mzml_file           = mzml_files,
            output_file         = output_file,
            pickle_name         = pickle_file,
            fixed_labels        = fixed_labels, #fixed_labels,
            evidence_files      = self.params['quantitation_evidences'],
            molecules           = self.params['molecules_to_quantify'],
            rt_border_tolerance = self.params['rt_border_tolerance'],
            label               = self.params['label'],
            label_percentile    = self.params['label_percentile'],
            min_charge          = self.params['precursor_min_charge'],
            max_charge          = self.params['precursor_max_charge'],
            evidence_score_field= self.params['evidence_score_field'],
            ms_level            = self.params['quant_ms_level'],
            # mz_score_percentile = self.params['mz_score_percentile'],
            trivial_names       = self.params['pyQms_trivial_names'],
            #fragment_peptide    = self.params['translations']['fragment_peptide'],
            #fragments_to_match  = self.params['translations']['fragments_to_match'],
            #pyQms_params        = pyqms_params,
            write_rt_info_file  = self.params['write_pyQms_rt_info']

        )

        self.print_execution_time(tag='execution')
        return out
