#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Examples script for filtering unified results for modification containing
    entries

    usage:
        ./filter_csv_for_mods_example.py


    Will produce a file with only entries which contain Carbamidomethyl as a
    modification.
    '''
    params = {
        'csv_filter_rules': [
            ['Modifications', 'contains', 'Carbamidomethyl'],
        ],
        'write_unfiltered_results': False

    }

    csv_file_to_filter = os.path.join(
        os.pardir,
        'example_data',
        'misc',
        'filter_csv_for_mods_example_omssa_2_1_9_pmap_unified.csv'
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
