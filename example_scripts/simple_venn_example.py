#!/usr/bin/env python3.4
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Example for plotting a simple Venn diagram with single ursgal csv files.

    usage:
        ./simple_venn_example.py


    '''
    uc = ursgal.UController(
        profile = 'LTQ XL low res',
        params = {
            'visualization_label_list' : [
                'omssa',
                'xtandem'
            ]

        }
    )

    file_list = [
        os.path.join(
            os.pardir,
            'tests',
            'data',
            'omssa_2_1_9',
            'test_BSA1_omssa_2_1_9.csv'
        ),
        os.path.join(
            os.pardir,
            'tests',
            'data',
            'xtandem_sledgehammer',
            'test_BSA1_xtandem_sledgehammer.csv'
        ),
    ]

    uc.visualize(
        input_files    = file_list,
        engine         = 'venndiagram',
    )
    return


if __name__ == '__main__':
    main()
