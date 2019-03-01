#!/usr/bin/env python3
# encoding: utf-8

import ursgal
R = ursgal.UController()

ways_to_merge = ['max_value']
#,'min_value','avg_value','most_frequent']

TESTS = [
    {
        'input'  : [{'X\!Tandem:hyperscore': '34', 'Spectrum ID': '5' },
        {'X\!Tandem:hyperscore': '1', 'Spectrum ID': '5' }],
        'output' : {'X\!Tandem:hyperscore': 34, 'Spectrum ID': '5'}
    },
]


'''
results = ursgal.ucore.merge_rowdicts(
    list_of_rowdicts=input_csv,
    joinchar=';',
    psm_colnames_to_merge_multiple_values={'X\!Tandem:hyperscore':'most_frequent'},
)
'''

def merge_rowdicts_test():
    for test_id, test_dict in enumerate(TESTS):
        yield merge_fdicts, test_dict


def merge_rowdicts( test_dict ):
    output = ursgal.ucore.merge_rowdicts( 
        list_of_rowdicts=*test_dict['input'],
        joinchar=';',
        psm_colnames_to_merge_multiple_values={'X\!Tandem:hyperscore':ways_to_merge[test_id]}, 
    )
    
    print( output , test_dict)
    assert output == test_dict['output'], '''
        merge_rowdicts {0} failed with output {1}'''.format(
        test_dict,
        output
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        merge_rowdicts( test_dict )
