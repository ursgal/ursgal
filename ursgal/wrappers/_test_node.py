#!/usr/bin/env python3.4
import ursgal
import os


class _test_node( ursgal.UNode ):
    """_test_node UNode"""
    META_INFO = {
        'edit_version'     : 1.00,                                              # flot, inclease number if something is changed (kaz)
        'name'             : 'test node',                                       # str, Software name (kaz)
        'version'          : 'alpha',                                           # str, Software version name (kaz)
        'release_date'     : None,                                              # None, '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' (kaz)
        'in_development'   : True,  # do not show in UNode overview
        'engine_type' : {
            'converter' : True
        },
        'input_types'      : ['txt', 'csv', 'fasta', 'mzml'],                   # list, extensions without a dot (kaz)
        'multiple_files'   : False,                                             # bool, fill true up if multiple files input is MUST like venn-diagram (kaz)
        'output_extension' : ['csv'],                                           # list, extensions without a dot (kaz)
        'output_suffix'    : 'test_node',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'test_node_exe.py',
                },
            },
        },
        'citation'         : \
            'TEST/DEBUG: Internal Ursgal UNode for debugging nd testing.',
        'include_in_git'   : True,
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
