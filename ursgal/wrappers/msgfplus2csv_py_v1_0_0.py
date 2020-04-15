#!/usr/bin/env python
import ursgal
import os


class msgfplus2csv_py_v1_0_0(ursgal.UNode):
    """
    msgfplus2csv_py v1.0.0 UNode
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'msgfplus_py_mzid2csv',
        'version'            : 'v1.0.0',
        'release_date'       : '2018-08-28',
        'engine_type' : {
            'converter'     : True
        },
        'input_extensions'   : ['.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : None,
        'include_in_git'     : True,
        'in_development'     : False,
        'distributable'      : True,
        'utranslation_style' : 'msgfplus_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'msgfplus2csv_py_v1_0_0.py'
                },
            },
        },
        'citation' : ''
    }

    def __init__(self, *args, **kwargs):
        super(msgfplus2csv_py_v1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        msgf_mzid2csv = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        msgf_mzid2csv(input_file, output_file)
        return output_file
