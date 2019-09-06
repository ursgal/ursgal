#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Executes a search with 3 different search engines on an example file from
    the data from Barth et al. Two searches are performed pe engine for each
    14N (unlabeled) and 15N labeling. The overlap of identified peptides
    for the 14N and 15N searches between the engines is visualized as well as 
    the overlap between all 14N and 15N identified peptides.

    usage:
        ./search_with_label_15N.py

    Note:
        It is important to convert the mgf file outside of (and before :) ) the 
        search loop to avoid mgf file redundancy and to assure correct retention
        time mapping in the unify_csv node.

    '''

    engine_list = [
        'omssa_2_1_9',
        'xtandem_piledriver',
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
            'search_with_label_15N'
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

    mgf_file = uc.convert(
        input_file=mzML_file,
        engine='mzml2mgf_1_0_0',
    )
    files_2_merge = {}
    label_list = ['14N', '15N']
    for label in label_list:
        validated_and_filtered_files_list = []
        uc.params['label'] = label
        uc.params['prefix'] = label
        for engine in engine_list:
            search_result = uc.search_mgf(
                input_file=mgf_file,
                engine=engine,
            )
            converted_result = uc.convert(
                input_file=search_result,
                guess_engine=True,
            )
            mapped_results = uc.execute_misc_engine(
                input_file=converted_result,
                engine='upeptide_mapper',
            )
            unified_search_results = uc.execute_misc_engine(
                input_file=mapped_results,
                engine='unify_csv'
            )
            validated_file = uc.validate(
                input_file=unified_search_results,
                engine='percolator_2_08',
            )
            filtered_file = uc.execute_misc_engine(
                input_file=validated_file,
                engine='filter_csv'
            )
            validated_and_filtered_files_list.append(filtered_file)
        files_2_merge[label] = validated_and_filtered_files_list
        uc.visualize(
            input_files=validated_and_filtered_files_list,
            engine='venndiagram_1_1_0',
        )
    uc.params['prefix'] = None
    uc.params['label'] = ''
    uc.params['visualization_label_positions'] = {}
    label_comparison_file_list = []
    for n, label in enumerate(label_list):
        uc.params['visualization_label_positions'][str(n)] = label
        label_comparison_file_list.append(
            uc.execute_misc_engine(
                input_file=files_2_merge[label],
                engine='merge_csvs'
            )
        )
    uc.visualize(
        input_files=label_comparison_file_list,
        engine='venndiagram_1_1_0',
    )

    return

if __name__ == '__main__':
    main()
