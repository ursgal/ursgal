#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Executes a search with a current maximum of 3 versions of MSGF+ on an
    example file from the data from Barth et al. (2014)

    usage:
        ./msgf_version_comparison.py


    This is a simple example file to show the straightforward comparison of
    different program versions of MSGF+

    Creates a Venn diagram with the peptides obtained by the different
    versions.

    An example plot can be found in the online documentation.

    Note:
        Uses the new MS-GF+ C# mzid converter if available

    '''

    params = {
        'database': os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
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
            'msgf_version_comparison'
        ),
        'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data'
        ),
        'remove_temporary_files': False,

    }

    if os.path.exists(params['ftp_output_folder']) is False:
        os.mkdir(params['ftp_output_folder'])

    uc = ursgal.UController(
        profile='LTQ XL low res',
        params=params
    )

    engine_list = [
        'msgfplus_v9979',
        'msgfplus_v2016_09_16',
    ]
    if 'msgfplus_v2017_01_27' in uc.unodes.keys():
        if uc.unodes['msgfplus_v2017_01_27']['available']:
            engine_list.append('msgfplus_v2017_01_27')
    if 'msgfplus_v2018_01_30' in uc.unodes.keys():
        if uc.unodes['msgfplus_v2018_01_30']['available']:
            engine_list.append('msgfplus_v2018_01_30')

    if 'msgfplus_C_mzid2csv_v2017_07_04' in uc.unodes.keys():
        if uc.unodes['msgfplus_C_mzid2csv_v2017_07_04']['available']:
            uc.params['msgfplus_mzid_converter_version'] = 'msgfplus_C_mzid2csv_v2017_07_04'

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
