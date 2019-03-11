#!/usr/bin/env python3
import ursgal
import os


def main():
    """."""
    params = {
        'csv_filter_rules': [
            ['combined PEP', 'lte', 0.05],
            ['Is decoy', 'equals', 'false']
        ],
        'compress_raw_search_results_if_possible': False,
        'database': os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'ftp_url': 'ftp.peptideatlas.org',
        'ftp_login': 'PASS00269',
        'ftp_password': 'FI4645a',
        'ftp_include_ext': [
            'JB_FASP_pH8_2-3_28122012.mzML',
        ],
        'ftp_output_folder': os.path.join(
            os.pardir,
            'example_data',
            'quantify_JB_example'
        ),
        'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data'
        )
    }
    if os.path.exists(params['ftp_output_folder']) is False:
        os.mkdir(params['ftp_output_folder'])

    engines = [
        'msgfplus_v2019_01_22',
        'xtandem_vengeance',
        # 'msfragger_20170103'
    ]

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

    mgf = uc.convert(
        input_file=mzML_file,
        engine='mzml2mgf_1_0_0'
    )

    all_res = []
    for label in ['14N', '15N']:
        uc.params['label'] = label
        uc.params['prefix'] = label
        results = []
        for engine in engines:
            res = uc.search(
                input_file=mgf,
                engine=engine
            )
            val = uc.validate(
                input_file=res,
                engine='percolator_2_08'
            )
            results.append(val)

        combined_results = uc.combine_search_results(
            input_files=results,
            engine='combine_PEP_1_0_0',
        )

        fil = uc.filter_csv(
            input_file=combined_results
        )
        all_res.append(fil)

    uc.params['quantification_evidences'] = all_res
    uc.params['label'] = '15N'
    uc.params['label_percentile'] = [0, 0.99]
    uc.params['evidence_score_field'] = 'combined PEP'
    uc.params['ms_level'] = 1

    uc.quantify(
        input_file=mzML_file,
        engine='pyqms_1_0_0',
        force=False
    )

if __name__ == '__main__':
    main()
