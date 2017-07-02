#!/usr/bin/env python3
import ursgal
import os


def main():
    """."""
    mzml = os.path.join(
        os.pardir,
        'example_data',
        'simple_search',
        'JB_FASP_pH8_2-3_28122012.mzML'
    )

    params = {
        'csv_filter_rules': [
            ['combined PEP', 'lte', 0.06],
            ['Is decoy', 'equals', 'false']
        ],
        'compress_raw_search_results_if_possible' : False,
        'database': os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        )
    }

    engines = [
        'msgfplus_v9979',
        'msfragger_20170103'
    ]

    uc = ursgal.UController(
        profile='LTQ XL low res',
        params =params
    )

    mgf = uc.convert_to_mgf_and_update_rt_lookup(
        input_file=mzml
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
            input_files     = results,
            engine          = 'combine_PEP_1_0_0',
        )

        fil = uc.filter_csv(
            input_file=combined_results
        )
        all_res.append(fil)

    uc.params['quantitation_evidences'] = all_res
    uc.params['label']                  = '15N'
    uc.params['label_percentile']       = [0, 0.99]
    uc.params['evidence_score_field']   = 'combined PEP'

    quant = uc.execute_unode(
        input_file=mzml,
        engine='pyQms_0_0_1',
        force=True
    )

if __name__ == '__main__':
    main()
