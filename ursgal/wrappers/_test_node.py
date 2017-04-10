#!/usr/bin/env python3.4
import ursgal
import os


class _test_node( ursgal.UNode ):
    """_test_node UNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'test node',
        'version'            : 'alpha',
        'release_date'       : None,
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'   : ['.txt', '.csv', '.fasta', '.mzML'],
        'input_multi_file'   : False,
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'test_node',
        'in_development'     : True,  # do not show in UNode overview
        'include_in_git'     : True,
        'utranslation_style' : '_test_node_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'test_node_exe.py',
                },
            },
        },
        'citation' : \
            'TEST/DEBUG: Internal Ursgal UNode for debugging nd testing.',
    }

    def __init__(self, *args, **kwargs):
        super(_test_node, self).__init__(*args, **kwargs)

    def preflight(self):

        in_path = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        out_path = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        # python3.4 _test_node.py -i x -o test.txt -t1 a -t2 3
        self.params['command_list'] = [
            'python3.4',
            self.exe,
            '-i',
            in_path,
            '-o',
            out_path,
            '-t1',
            '{test_param1}'.format(**self.params['translations']),
            '-t2',
            '{test_param2}'.format(**self.params['translations']),
        ]
        print("\nTest UNode: preflight() was executed!\n")

    def postflight(self):
        print("\nTest UNode: postflight() was executed!\n")
