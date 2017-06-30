#!/usr/bin/env python3
import ursgal
import os


def main():
    """."""
    mzml = os.path.join(
        os.pardir,
        'example_data',
        'BSA1.mzML'
    )

    params = {
        'csv_filter_rules': [
            ['estimated_FDR', 'lte', 0.06],
            ['Is decoy', 'equals', 'false']
        ],
        'compress_raw_search_results_if_possible' : False,
        'database': os.path.join(
            os.pardir,
            'example_data',
            'BSA.fasta'
        )
    }

    engines = [
        'msgfplus_v9979'
    ]

    uc = ursgal.UController(
        profile='LTQ XL low res',
        params =params
    )

    mgf = uc.convert_to_mgf_and_update_rt_lookup(
        input_file=mzml
    )
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
        fil = uc.filter_csv(
            input_file=val
        )
        results.append(file)

    quant = uc.execute_unode(
        input_file=mzml,
        engine='pyQms_0_0_1'
    )

if __name__ == '__main__':
    main()
