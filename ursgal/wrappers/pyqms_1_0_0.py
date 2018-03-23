#!/usr/bin/env python3
'''
'''
import os
import ursgal


class pyqms_1_0_0(ursgal.UNode):
    """
    pyQms- molecule qunatification node.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'pyqms',
        'version'            : '1.0.0',
        'release_date'       : None,
        'engine_type'        : {
            'quantitation_engine' : True
        },
        'utranslation_style' : 'pyqms_style_1',
        'citation'           : 'Leufken J, Niehues A, Sarin LP, Wessel F, Hippler M, Leidel SA, Fufezan C (2017) pyQms enables universal and accurate quantification of mass spectrometry data',
        'input_extensions'   : ['.mzML'],
        'output_extensions'  : ['.csv'],
        'create_own_folder'  : True,
        'in_development'     : False,
        'include_in_git'     : False,
        'distributable'      : False,
        # Download Information
        'engine'             : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe': 'pyqms_1_0_0.py',
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """."""
        super(pyqms_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        """run."""
        print('[ -ENGINE- ] Executing quantitation ..')
        self.time_point(tag='execution')

        main = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        pickle_file = os.path.join(
            self.params['output_dir_path'],
            os.path.splitext(self.params['output_file'])[0] + '_quant.pkl' ,
        )
        # multiple input mzML files
        if self.params['input_file'].endswith('.json'):
            mzml_files = []
            for fdict in self.params['input_file_dicts']:
                mzml_files.append(fdict['full'])
        else:  # single mzML file
            mzml_files = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        pyqms_params = {
            'PERCENTILE_FORMAT_STRING'                :
                self.params['label_percentile_format_string'],
            'M_SCORE_THRESHOLD'                       :
                self.params['m_score_cutoff'],
            'ELEMENT_MIN_ABUNDANCE'                   :
                self.params['min_element_abundance'],
            'MIN_REL_PEAK_INTENSITY_FOR_MATCHING'     :
                self.params['min_rel_peak_intensity_for_matching'],
            'REQUIRED_PERCENTILE_PEAK_OVERLAP'        :
                self.params['required_percentile_peak_overlap'],
            'MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES' :
                self.params['min_number_of_matched_isotopologues'],
            'INTENSITY_TRANSFORMATION_FACTOR'         :
                self.params['intensity_transformation_factor'],
            'UPPER_MZ_LIMIT'                          :
                self.params['upper_mz_limit'],
            'LOWER_MZ_LIMIT'                          :
                self.params['lower_mz_limit'],
            'MZ_TRANSFORMATION_FACTOR'                :
                self.params['mz_transformation_factor'],
            'REL_MZ_RANGE'                            :
                self.params['rel_mz_range'],
            'REL_I_RANGE'                             :
                self.params['rel_intensity_range'],
            'INTERNAL_PRECISION'                      :
                self.params['internal_precision'],
            'MAX_MOLECULES_PER_MATCH_BIN'             :
                self.params['max_molecules_per_match_bin'],
            'SILAC_AAS_LOCKED_IN_EXPERIMENT'          :
                self.params['silac_aas_locked_in_experiment'],
            'BUILD_RESULT_INDEX'                      :
                self.params['build_pyqms_result_index'],
            'MACHINE_OFFSET_IN_PPM'                   :
                self.params['machine_offset_in_ppm'],
            'FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS'   :
                self.params['fixed_label_isotope_enrichment_levels'],
            # 'COLORS'                                  :
            #     self.params['pyQms_colors'],
        }

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
            mzml_file=mzml_files,
            output_file=output_file,
            fixed_labels=fixed_labels,
            evidence_files=self.params['quantitation_evidences'],
            molecules=self.params['molecules_to_quantify'],
            rt_border_tolerance=self.params['rt_border_tolerance'],
            label=self.params['label'],
            label_percentile=self.params['label_percentile'],
            min_charge=self.params['precursor_min_charge'],
            max_charge=self.params['precursor_max_charge'],
            evidence_score_field=self.params['evidence_score_field'],
            ms_level=self.params['ms_level'],
            trivial_names=self.params['pyqms_trivial_names'],
            pyqms_params=pyqms_params,
            verbose=self.params['pyqms_verbosity'],
            pickle_name = pickle_file
        )

        self.print_execution_time(tag='execution')
        return out
