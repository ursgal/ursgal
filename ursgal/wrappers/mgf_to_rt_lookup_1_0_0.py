#!/usr/bin/env python
import ursgal
import os


class mgf_to_rt_lookup_1_0_0(ursgal.UNode):
    """Write RT lookup from mgf file
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'mgf_to_rt_lookup',
        'version'                     : '1.0.0',
        'engine_type': {
            'converter': True
        },
        'output_extensions'           : ['.txt'],
        'create_own_folder'           : False,
        'utranslation_style'          : 'mgf_to_rt_lookup_style_1',
        'citation'                    : '',
        'in_development'              : False,
        'include_in_git'              : True,
        'input_extensions'            : ['.mgf'],
        'release_date'                : None,
        'engine': {
            'platform_independent': {
                'arc_independent': {
                    'exe': 'mgf_to_rt_lookup_1_0_0.py',
                },
            },
        },
        'citation': '',
    }

    def __init__(self, *args, **kwargs):
        super(mgf_to_rt_lookup_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        print('[ -ENGINE- ] Executing conversion ..')
        self.time_point(tag='execution')
        main = self.import_engine_as_python_function()
        if self.params['input_file'].lower().endswith('.mgf') is False:
            raise ValueError('Trying to convert a non-mgf file')

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        input_file = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        main(
            input_file=input_file,
            output_file=output_file,
            rt_pickle_name=self.params['rt_pickle_name'],
            spec_id_regex=r'\w+.(\d+).\d+.\d',
            run_id_regex=r'(\w+).\d+.\d+.\d'
        )
        # TODO add spec_id_regex and run_id_regex as uparams, could also be used in unify_csv etc
        self.print_execution_time(tag='execution')
        return output_file
