#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys


def main():
    '''
    Simple example script how to generate a target decoy database using one or
    multiple fasta files as input.

    Note:
        A 'shuffled peptide preserving cleavage sites' database is 
        generated.

    usage:

        ./generate_target_decoy_from_fasta.py <fasta_database_1> <fasta_database_2> <fasta_database_n> ...

    '''
    params = {
        'enzyme': 'trypsin',
        # 'decoy_generation_mode': 'reverse_protein',
    }

    fasta_database_list = sys.argv[1:-1]
    target_db_name = sys.argv[-1]

    uc = ursgal.UController(
        params = params
    )

    new_target_decoy_db_name = uc.execute_misc_engine(
        input_file      = fasta_database_list,
        engine           = 'generate_target_decoy_1_0_0',
        output_file_name = target_db_name,
    )
    print(
        'Generated target decoy database: {0}'.format(
            new_target_decoy_db_name
        )
    )

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(main.__doc__)
    main()
