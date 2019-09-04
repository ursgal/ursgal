#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys


def main(folder):
    '''
    Executes a search with different versions of msgf+ m on an example file from the
    data from Bruderer et al.

    usage:
        ./msgf_plus_version_comparison_qexactive.py <folder containing B_D140314_SGSDSsample1_R01_MSG_T0.mzML.gz>


    Creates a Venn diagram with the peptides obtained by the different versions.


    '''

    required_example_file = 'B_D140314_SGSDSsample1_R01_MSG_T0.mzML.gz'
    full_path = os.path.join(folder, required_example_file)

    if os.path.exists(full_path) is False:

        print(
            '''
            Your specified folder does not contain the required example file:
            {0}
            The RAW data from peptideatlas.org (PASS00589, password: WF6554orn)
            will be downloaded.
            Please convert to mzML after the download has finished and run this
            script again.
            '''.format(required_example_file)
        )

        ftp_get_params = {
            'ftp_url': 'ftp.peptideatlas.org',
            'ftp_login': 'PASS00589',
            'ftp_password': 'WF6554orn',
            'ftp_include_ext': [
                required_example_file.replace(
                    '.mzML',
                    '.raw'
                )
            ],
            'ftp_output_folder': folder,
        }
        uc = ursgal.UController(
            params=ftp_get_params
        )
        uc.fetch_file(
            engine='get_ftp_files_1_0_0'
        )
        sys.exit(1)

    engine_list = [
        'msgfplus_v9979',
        'msgfplus_v2016_09_16',
        'msgfplus_v2018_01_30',
        'msgfplus_v2018_06_28',
        'msgfplus_v2018_09_12',
    ]

    params = {
        'database': os.path.join(
            os.pardir,
            'example_data',
            'hs_201303_qs_sip_target_decoy.fasta'
        ),
        'modifications': ['C,fix,any,Carbamidomethyl'],
        'csv_filter_rules': [
            ['PEP', 'lte', 0.01],
            ['Is decoy', 'equals', 'false']
        ],
        'http_url': 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/misc/hs_201303_qs_sip_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data'
        ),
        'machine_offset_in_ppm': -5e-6,
        'remove_temporary_files': False
    }

    uc = ursgal.UController(
        profile='QExactive+',
        params=params
    )

    if os.path.exists(params['database']) is False:
        uc.fetch_file(
            engine='get_http_files_1_0_0'
        )

    mzML_file = os.path.join(folder, required_example_file)

    filtered_files_list = []
    for engine in engine_list:

        unified_result_file = uc.search(
            input_file=mzML_file,
            engine=engine,
            force=False,
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
    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)
    main(sys.argv[1])
