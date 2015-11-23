#!/usr/bin/env python3
# encoding: utf-8

import ursgal
R = ursgal.UController()

TESTS = [
    {
        'input' : {
            'input_files' : [
                '/Volumes/_/_/_/1/',
                '/Volumes/_/_/_/1/'
            ],
        },
        'output' : '/Volumes/_/_/_/1/'
    },
    {
        'input' : {
            'input_files' : [
                '/Volumes/_/_/_/',
                '/Volumes/_/_/_/1'
            ],
        },
        'output' : '/Volumes/_/_/_/'
    },
    {
        'input' : {
            'input_files' : [
                '/Volumes/',
                '/Volumes/_/_/_/1',
            ],
        },
        'output' : '/Volumes/'
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
