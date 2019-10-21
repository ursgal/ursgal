#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import time


def main():
    '''

    Testscript to evaluate the speed of common search engines.

    Usage:
        ./compare_search_engine_speed.py

    Note:
        The complete time for the search including peptide mapping and
        unifying the csv results.

    '''
    engine_list = [
        # 'msfragger_20170103',
        'xtandem_vengeance',
        'omssa',
        'msgfplus_v2016_09_16'
    ]

    params = {
        'database': os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'modifications': [
            '*,opt,Prot-N-term,Acetyl',
            'M,opt,any,Oxidation',
        ],
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
            'xtandem_and_msfragger_comparison'
        ),
        'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data'
        ),
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
    time_collector = {}
    filtered_files_list = []
    mgf_file = uc.convert(
        input_file=mzML_file,
        engine='mzml2mgf_1_0_0',
    )
    for engine in engine_list:
        start_time = time.time()
        unified_result_file = uc.search(
            input_file=mzML_file,
            engine=engine,
        )
        time_collector[engine] = time.time() - start_time
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

    for key, duration in time_collector.items():
        print('Engine {0} took {1:1.2f}s'.format(key, duration))
    return

if __name__ == '__main__':
    main()
