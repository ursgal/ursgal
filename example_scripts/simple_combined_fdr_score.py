#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Executes a search with 3 different search engines on an example file from the
    data from Barth et al. (The same file that is used in the XTandem version
    comparison example.)

    usage:
        ./simple_combined_fdr_score.py


    This is a simple example script to show how results from multiple search engines
    can be combined using the Combined FDR Score approach of Jones et al. (2009).
    '''

    engine_list = [
        'omssa_2_1_9',
        'xtandem_piledriver',
        # 'myrimatch_2_1_138',
        'msgfplus_v9979',
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

    validated_files_list = []
    for engine in engine_list:

        unified_result_file = uc.search(
            input_file=mzML_file,
            engine=engine,
        )

        validated_file = uc.validate(
            input_file=unified_result_file,
            engine='percolator_2_08',
        )

        validated_files_list.append(validated_file)

    combined_results = uc.combine_search_results(
        input_files=validated_files_list,
        engine='combine_FDR_0_1',
        # use combine_pep_1_0_0 for combined PEP :)
    )
    print('\tCombined results can be found here:')
    print(combined_results)
    return

if __name__ == '__main__':
    main()
