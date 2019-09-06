#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Executes a search with 5 versions of X!Tandem on an example file from the
    data from Barth et al. 2014.

    usage:
        ./xtandem_version_comparison.py


    This is a simple example file to show the straightforward comparison of
    different program versions of X!Tandem

    Creates a Venn diagram with the peptides obtained by the different versions.

    Note:
        At the moment in total 6 XTandem versions are incorporated in Ursgal.

    '''
    engine_list = [
        # 'xtandem_cyclone',
        'xtandem_jackhammer',
        'xtandem_sledgehammer',
        'xtandem_piledriver',
        'xtandem_vengeance',
        'xtandem_alanine',

    ]

    params = {
        'database': os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'modifications': [],
        'csv_filter_rules': [
            ['PEP', 'lte', 0.01],
            ['Is decoy', 'equals', 'false']
        ],
        'ftp_url': 'ftp.peptideatlas.org',
        'ftp_login': 'PASS00269',
        'ftp_password': 'FI4645a',
        'ftp_include_ext': [
            'JB_FASP_pH8_2-3_28122012.mzML',
        ],
        'ftp_output_folder': os.path.join(
            os.pardir,
            'example_data',
            'xtandem_version_comparison'
        ),
        'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data'
        )
    }

    if os.path.exists(params['ftp_output_folder']) is False:
        os.mkdir(params['ftp_output_folder'])

    uc = ursgal.UController(
        profile='LTQ XL low res',
        params=params
    )
    mzML_file = os.path.join(
        params['ftp_output_folder'],
        params['ftp_include_ext'][0]
    )
    if os.path.exists(mzML_file) is False:
        uc.fetch_file(
            engine='get_ftp_files_1_0_0'
        )
    if os.path.exists(params['database']) is False:
        uc.fetch_file(
            engine='get_http_files_1_0_0'
        )

    filtered_files_list = []
    for engine in engine_list:
        unified_result_file = uc.search(
            input_file=mzML_file,
            engine=engine,
        )

        validated_file = uc.validate(
            input_file=unified_result_file,
            engine='percolator_2_08',
        )

        filtered_file = uc.execute_misc_engine(
            input_file=validated_file,
            engine='filter_csv_1_0_0',
        )

        filtered_files_list.append(filtered_file)

    uc.visualize(
        input_files=filtered_files_list,
        engine='venndiagram_1_1_0',
    )
    return

if __name__ == '__main__':
    main()
