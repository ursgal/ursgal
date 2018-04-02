#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Simple example script how to generate a target decoy database.

    Note:
        By default a 'shuffled peptide preserving cleavage sites' database is 
        generated. For this script a 'reverse protein' database is generated.

    usage:

        ./target_decoy_generation_example.py

    '''
    params = {
        'enzyme': 'trypsin',
        'decoy_generation_mode': 'reverse_protein',
    }

    fasta_database_list = [
        os.path.join(
            os.pardir,
            'example_data',
            'BSA.fasta'
        )
    ]

    uc = ursgal.UController(
        params=params
    )

    new_target_decoy_db_name = uc.execute_misc_engine(
        input_file=fasta_database_list,
        engine='generate_target_decoy_1_0_0',
        output_file_name='my_BSA_target_decoy.fasta',
    )
    print('Generated target decoy database: {0}'.format(
        new_target_decoy_db_name))

if __name__ == '__main__':
    main()
