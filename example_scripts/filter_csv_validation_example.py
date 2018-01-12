#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Examples script for filtering validated results for a PEP <= 0.01 and
    remove all decoys.

    usage:
        ./filter_csv_validation_example.py


    Will produce a file with only target sequences with a posterior error
    probability of lower or equal to 1 percent
    '''
    params = {
        'csv_filter_rules': [
            ['PEP', 'lte', 0.01],
            ['Is decoy', 'equals', 'false']
        ]
    }

    csv_file_to_filter = os.path.join(
        os.pardir,
        'example_data',
        'misc',
        'filter_csv_for_mods_example_omssa_2_1_9_pmap_unified_percolator_2_08_validated.csv'
    )
    uc = ursgal.UController(
        params=params
    )

    filtered_csv = uc.execute_misc_engine(
        input_file=csv_file_to_filter,
        engine='filter_csv_1_0_0',
    )


if __name__ == '__main__':
    main()
