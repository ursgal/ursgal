#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


R = ursgal.UController()

TESTS = [
    {
        'input' : {
            'input_files' : [
                os.path.join( os.sep, 'Volumes', '_', '_', '_', '1') + os.sep,
                os.path.join( os.sep, 'Volumes', '_', '_', '_', '1') + os.sep
            ],
        },
        'output' : os.path.join( os.path.abspath( os.sep ), 'Volumes', '_', '_', '_', '1') + os.sep
    },
    {
        'input' : {
            'input_files' : [
                os.path.join( os.sep, 'Volumes', '_', '_', '_') + os.sep,
                os.path.join( os.sep, 'Volumes', '_', '_', '_', '1') + os.sep
            ],
        },
        'output' : os.path.join( os.path.abspath( os.sep ), 'Volumes', '_', '_', '_') + os.sep,
    },
    {
        'input' : {
            'input_files' : [
                os.path.join( os.sep, 'Volumes') + os.sep,
                os.path.join( os.sep, 'Volumes', '_', '_', '_', '1') + os.sep,
            ],
        },
        'output' : os.path.join( os.path.abspath( os.sep ), 'Volumes') + os.sep
    },

]


def determine_common_top_level_folder_test():
    for test_id, test_dict in enumerate(TESTS):
        yield determine_common_top_level_folder, test_dict


def determine_common_top_level_folder( test_dict ):
    out_put = R.determine_common_top_level_folder(
        **test_dict['input']
    )
    print( out_put , test_dict)
    assert out_put == test_dict['output'], '''
    determine_common_top_level_folder failed with
        test:
        {0}
        output
        {1}'''.format(
        test_dict,
        out_put
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        determine_common_top_level_folder( test_dict )
