#!/usr/bin/env python
import ursgal
import importlib
import os
import sys


class mzml2mgf_2_0_0(ursgal.UNode):
    """
    mzml2mgf_2_0_0 UNode

    Version two works only with pymzML version 2.0.0 or higher!

    Converts .mzML files into .mgf files
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'mzml2mgf',
        'version'            : '2.0.0',
        'release_date'       : '2018-03-26',
        'engine_type' : {
            'converter' : True,
        },
        'input_extensions'   : ['.mzML', '.mzML.gz', '.idx.gz'],
        'output_extensions'  : ['.mgf'],
        'output_suffix'      : None,
        'in_development'     : False,
        'include_in_git'     : True,
        'distributable'      : True,
        'utranslation_style' : 'mzml2mgf_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'mzml2mgf_2_0_0.py',
                },
            },
        },
        'citation' :
            'Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. & '
            'Fufezan, C. (2016) Ursgal, Universal Python Module Combining '
            'Common Bottom-Up Proteomics Tools for Large-Scale Analysis. J. '
            'Proteome res. 15, 788-794.',
    }

    def __init__(self, *args, **kwargs):
        super(mzml2mgf_2_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        print('[ -ENGINE- ] Executing conversion ..')
        # self.time_point(tag = 'execution')
        mzml2mgf_main = self.import_engine_as_python_function()

        tmp = mzml2mgf_main(
            mzml=os.path.join(
                self.io['input']['finfo']['dir'],
                self.io['input']['finfo']['file']
            ),
            mgf=os.path.join(
                self.io['output']['finfo']['dir'],
                self.io['output']['finfo']['file']
            ),
            i_decimals=self.params['translations']['num_i_decimals'],
            mz_decimals=self.params['translations']['num_mz_decimals'],
            machine_offset_in_ppm=self.params[
                'translations']['machine_offset_in_ppm'],
            scan_exclusion_list=self.params[
                'translations']['scan_exclusion_list'],
            scan_inclusion_list=self.params[
                'translations']['scan_inclusion_list'],
            prefix=self.params.get('prefix', None),
            scan_skip_modulo_step=self.params[
                'translations']['scan_skip_modulo_step'],
            ms_level=self.params['translations']['ms_level'],
            precursor_min_charge=self.params[
                'translations']['precursor_min_charge'],
            precursor_max_charge=self.params[
                'translations']['precursor_max_charge'],
            ion_mode=self.params['translations']['ion_mode'],
            spec_id_attribute=self.params['translations']['pymzml_spec_id_attribute'],
        )
        return tmp
