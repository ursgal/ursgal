#!/usr/bin/env python
import ursgal
import os
import tempfile
import time


class _test_node( ursgal.UNode ):
    """_test_node UNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'test node',
        'version'            : 'alpha',
        'release_date'       : None,
        'engine_type' : {
            '_test'  : True
        },
        'input_extensions'   : ['.txt', '.csv', '.fasta', '.mzML'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'test_node',
        'in_development'     : True,  # do not show in UNode overview
        'include_in_git'     : True,
        'distributable'      : True,
        'utranslation_style' : '_test_node_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'test_node.py',
                },
            },
        },
        'citation' : \
            'TEST/DEBUG: Internal Ursgal UNode for debugging nd testing.',
    }

    def __init__(self, *args, **kwargs):
        super(_test_node, self).__init__(*args, **kwargs)

    def preflight(self):
        self.params['command_list'] = ['sleep', '1']


        # in_path = os.path.join(
        #     self.params['input_dir_path'],
        #     self.params['input_file']
        # )

        out_path = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        with open( out_path, 'w') as oof:
            print('Testing 1,2,3 ...', file = oof)
        # # python _test_node.py -i x -o test.txt -t1 a -t2 3
        # self.params['command_list'] = [
        #     'python',
        #     self.exe,
        #     '-i',
        #     in_path,
        #     '-o',
        #     out_path,
        #     '-t1',
        #     '{test_param1}'.format(**self.params['translations']),
        #     '-t2',
        #     '{test_param2}'.format(**self.params['translations']),
        # ]
        time.sleep(2)
        self.print_info(
            'Test UNode: preflight() was executed, slept for 2 seconds!'
        )
        self.print_info(
            'Scheduled command: {command_list}'.format(**self.params )
        )

    def postflight(self):
        time.sleep(1)
        self.print_info("Test UNode: postflight() was executed, slept for 1 second")
