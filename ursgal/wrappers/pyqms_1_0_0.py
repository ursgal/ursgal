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
        'edit_version': 1.00,
        'name': 'pyqms',
        'version': '1.0.0',
        'release_date': None,
        'engine_type': {
            'quantification_engine': True
        },
        'utranslation_style': 'pyqms_style_1',
        'citation': 'Leufken J, Niehues A, Sarin LP, Wessel F, Hippler M, Leidel SA, Fufezan C (2017) pyQms enables universal and accurate quantification of mass spectrometry data',
        'input_extensions': ['.mzML'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        # Download Information
        'engine': {
            'platform_independent': {
                'arc_independent': {
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
        print('[ -ENGINE- ] Executing quantification ..')
        self.time_point(tag='execution')

        main = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        pickle_file = os.path.join(
            self.params['output_dir_path'],
            os.path.splitext(self.params['output_file'])[0] + '_quant.pkl',
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
        if self.params['translations']['ms_level'] == 1:
            print(
                '''
                [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
                [ WARNING ] need to be combined for pyQms (use of symmetric tolerance window).
                [ WARNING ] The arithmetic mean is used.
                '''
            )
            self.params['translations']['REL_MZ_RANGE'] = (
                float(self.params['translations']['precursor_mass_tolerance_plus']) +
                float(self.params['translations'][
                      'precursor_mass_tolerance_minus'])) / 2.0
            if self.params['translations']['precursor_mass_tolerance_unit'] == 'da':
                self.params['translations']['REL_MZ_RANGE'] = \
                    ursgal.ucore.convert_dalton_to_ppm(
                        self.params['translations']['REL_MZ_RANGE'],
                        base_mz=self.params['translations']['base_mz']
                )
        else:
            self.params['translations']['REL_MZ_RANGE'] = \
                self.params['translations']['frag_mass_tolerance']
            if self.params['translations']['frag_mass_tolerance_unit'] == 'da':
                self.params['translations']['REL_MZ_RANGE'] = \
                    ursgal.ucore.convert_dalton_to_ppm(
                        self.params['translations']['REL_MZ_RANGE'],
                        base_mz=self.params['translations']['base_mz']
                )
        self.params['translations']['REL_MZ_RANGE'] = self.params[
            'translations']['REL_MZ_RANGE'] * 1e-6

        pyqms_params = {
            'PERCENTILE_FORMAT_STRING':
                self.params['translations']['label_percentile_format_string'],
            'M_SCORE_THRESHOLD':
                self.params['translations']['m_score_cutoff'],
            'ELEMENT_MIN_ABUNDANCE':
                self.params['translations']['min_element_abundance'],
            'MIN_REL_PEAK_INTENSITY_FOR_MATCHING':
                self.params['translations'][
                    'min_rel_peak_intensity_for_matching'],
            'REQUIRED_PERCENTILE_PEAK_OVERLAP':
                self.params['translations'][
                    'required_percentile_peak_overlap'],
            'MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES':
                self.params['translations'][
                    'min_number_of_matched_isotopologues'],
            'INTENSITY_TRANSFORMATION_FACTOR':
                self.params['translations']['intensity_transformation_factor'],
            'UPPER_MZ_LIMIT':
                self.params['translations']['upper_mz_limit'],
            'LOWER_MZ_LIMIT':
                self.params['translations']['lower_mz_limit'],
            'MZ_TRANSFORMATION_FACTOR':
                self.params['translations']['mz_transformation_factor'],
            'REL_MZ_RANGE':
                self.params['translations']['REL_MZ_RANGE'],
            'REL_I_RANGE':
                self.params['translations']['rel_intensity_range'],
            'INTERNAL_PRECISION':
                self.params['translations']['internal_precision'],
            'MAX_MOLECULES_PER_MATCH_BIN':
                self.params['translations']['max_molecules_per_match_bin'],
            'SILAC_AAS_LOCKED_IN_EXPERIMENT':
                self.params['translations']['silac_aas_locked_in_experiment'],
            'BUILD_RESULT_INDEX':
                self.params['translations']['build_pyqms_result_index'],
            'MACHINE_OFFSET_IN_PPM':
                self.params['translations']['machine_offset_in_ppm'],
            'FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS':
                self.params['translations'][
                    'fixed_label_isotope_enrichment_levels'],
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
                    'element_composition': comp,
                    'evidence_mod_name': name
                }
            )

        out = main(
            mzml_file=mzml_files,
            output_file=output_file,
            fixed_labels=fixed_labels,
            evidence_files=self.params['translations'][
                'quantification_evidences'],
            molecules=self.params['translations']['molecules_to_quantify'],
            rt_border_tolerance=self.params[
                'translations']['rt_border_tolerance'],
            label=self.params['translations']['label'],
            label_percentile=self.params['translations']['label_percentile'],
            min_charge=self.params['translations']['precursor_min_charge'],
            max_charge=self.params['translations']['precursor_max_charge'],
            evidence_score_field=self.params[
                'translations']['evidence_score_field'],
            ms_level=self.params['translations']['ms_level'],
            trivial_names=self.params['translations']['pyqms_trivial_names'],
            pyqms_params=pyqms_params,
            verbose=self.params['translations']['pyqms_verbosity'],
            pickle_name=pickle_file
        )

        self.print_execution_time(tag='execution')
        return out
