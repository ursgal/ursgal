#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import pprint
import ursgal.resources.platform_independent.arc_independent.combine_pep_1_0_0.combine_pep_1_0_0 as cpep


TESTS = [
    {
        'iterable': [1,2,3,4,5],
        'window_len': 3,
        'out_windows': [
            (1, [1, 2]),
            (2, [1, 2, 3]),
            (3, [2, 3, 4]),
            (4, [3, 4, 5]),
            (5, [4, 5]),
        ],
    },

    {

        'iterable': [1,0,0,1,1],
        'window_len': 3,
        'out_windows': [
            (1, [1, 0]),
            (0, [1, 0, 0]),
            (0, [0, 0, 1]),
            (1, [0, 1, 1]),
            (1, [1, 1]),
        ],
    },

    {
        'iterable': [1,2,3,4,5],
        'window_len': 2,
        'out_windows': [
            (1, [1, 2]),
            (2, [1, 2, 3]),
            (3, [2, 3, 4]),
            (4, [3, 4, 5]),
            (5, [4, 5]),
        ],
    },

    {
        'iterable': [1,2,3,4,5],
        'window_len': 5,
        'out_windows': [
            (1, [1, 2, 3]),
            (2, [1, 2, 3, 4]),
            (3, [1, 2, 3, 4, 5]),
            (4, [2, 3, 4, 5]),
            (5, [3, 4, 5]),
        ],
    },

    {
        'iterable': [1,2,3,4,5],
        'window_len': 7,
        'out_windows': [
            (1, [1, 2, 3, 4]),
            (2, [1, 2, 3, 4, 5]),
            (3, [1, 2, 3, 4, 5]),
            (4, [1, 2, 3, 4, 5]),
            (5, [2, 3, 4, 5]),
        ],
    },

    {
        'iterable': [1,2,3,4,5],
        'window_len': 99999,
        'out_windows': [
            (1, [1, 2, 3, 4, 5]),
            (2, [1, 2, 3, 4, 5]),
            (3, [1, 2, 3, 4, 5]),
            (4, [1, 2, 3, 4, 5]),
            (5, [1, 2, 3, 4, 5]),
        ],
    },

    {
        'iterable': [1,2,3,4,5],
        'window_len': 1,
        'out_windows': [
            (1, [1]),
            (2, [2]),
            (3, [3]),
            (4, [4]),
            (5, [5]),
        ],
    },

    {
        'iterable': [1,2,3,4,5,6,7],
        'window_len': 11,
        'out_windows': [
            (1, [1, 2, 3, 4, 5, 6]),
            (2, [1, 2, 3, 4, 5, 6, 7]),
            (3, [1, 2, 3, 4, 5, 6, 7]),
            (4, [1, 2, 3, 4, 5, 6, 7]),
            (5, [1, 2, 3, 4, 5, 6, 7]),
            (6, [1, 2, 3, 4, 5, 6, 7]),
            (7, [2, 3, 4, 5, 6, 7]),
        ],
    },

    {
        'iterable': [1],
        'window_len': 999,
        'out_windows': [
            (1, [1]),
        ],
    },

]


def check_sliding_window_test():
    for test_id, test_dict in enumerate(TESTS):
        yield check_sliding_window, test_dict


def check_sliding_window( test_dict ):

    print('\nInput list:', str(test_dict['iterable']), '; win_size:', test_dict['window_len'])

    window_slider = cpep.sliding_window(
        test_dict['iterable'],
        test_dict['window_len'],
        flexible=False,
    )
    expected_results = test_dict['out_windows']
    i = -1
    for i, win_center_tuple in enumerate(window_slider):

        windowsum = win_center_tuple[0]

        center = win_center_tuple[1]
        expected_window = expected_results[i][1]
        expected_center = expected_results[i][0]


        error_str = '\n  Expected:\n\t{0}\t{1}\t{2}\n  Got:\n\t{3}\t{4}'.format(
            expected_center, sum(expected_window), expected_window,
            center, windowsum
        )
        assert center == expected_center, error_str
        assert windowsum == sum(expected_window), error_str
        print(center, windowsum)

    assert i+1 == len(expected_results), '''\n
    Sliding window yielded {0} iterations,
    but {1} iterations were expected.\n
    Test case:\n{2}
    '''.format(i+1, len(expected_results),
               pprint.pformat(test_dict))

if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        check_sliding_window( test_dict )
