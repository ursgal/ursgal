#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Script to compare Percolator versions 2.08 and 3.2 using MSFragger as
    search engine
    '''

    engine_list = [
        'xtandem_vengeance',
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
            'percolator_version_comparison'
        ),
        'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data'
        ),
        'infer_proteins': False,
        'percolator_post_processing': 'tdc',
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

    validation_engine_list = [
        'percolator_2_08',
        'percolator_3_2_1'
    ]
    uc.params['visualization_label_positions'] = {}
    for n, vce in enumerate(validation_engine_list):
        uc.params['visualization_label_positions'][str(n)] = vce
    for engine in engine_list:
        unified_search_results = uc.search(
            input_file=mzML_file,
            engine=engine,
        )

        validated_and_filtered_files_list = []
        for pc_version in validation_engine_list:
            uc.params['prefix'] = pc_version
            validated_file = uc.validate(
                input_file=unified_search_results,
                engine=pc_version,
            )
            filtered_file = uc.execute_misc_engine(
                input_file=validated_file,
                engine='filter_csv'
            )
            validated_and_filtered_files_list.append(
                filtered_file
            )
        uc.visualize(
            input_files=validated_and_filtered_files_list,
            engine='venndiagram_1_1_0',
        )

    return

if __name__ == '__main__':
    main()
