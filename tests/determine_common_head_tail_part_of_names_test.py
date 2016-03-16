#!/usr/bin/env python3
# encoding: utf-8
import ursgal
R = ursgal.UController()

TESTS = [
    {
        'input' : {
            'input_files' : [
                'uSearch_OSX',
                'uSearch_WINDOWS',
            ],
        },
        'output' : ('uSearch_' , '')
    },
    {
        'input' : {
            'input_files' : [
                'uSearch_OSX__ROCKS',
                'uSearch_WINDOWS__ROCKS',
            ],
        },
        'output' : ('uSearch_' , '__ROCKS')
    },
    {
        'input' : {
            'input_files' : [
                'uSearch__ROCKS',
                'not_only_uSearch__ROCKS',
            ],
        },
        'output' : ('' , 'uSearch__ROCKS')
    }

]


def determine_common_common_head_tail_part_of_names_test():
    for test_id, test_dict in enumerate(TESTS):
        yield determine_common_common_head_tail_part_of_names, test_dict


def determine_common_common_head_tail_part_of_names( test_dict ):
    out_put = R.determine_common_head_tail_part_of_names(
        **test_dict['input']
    )
    print('Results', out_put , test_dict)
    assert out_put == test_dict['output'], '''
    determine_common_name {0} failed'''.format(
        test_dict
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        determine_common_common_head_tail_part_of_names( test_dict )
