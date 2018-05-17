#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main(mzML_file=None, profile=None, database=None):
    '''
    Executes a search with XTandem on an mzml_input_file.
    Results are validated with percolator and exported to .ssl.

    usage:
        ./search_and_conversion_to_ssl.py <mzML_file> <profile> <target_decoy_database>

    '''
    uc = ursgal.UController(
        profile=profile,
        params={
            'database': database,
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
            ],
        }
    )

    if sys.maxsize > 2 ** 32:
        xtandem = 'xtandem_vengeance'
    else:
        xtandem = 'xtandem_sledgehammer'

    unified_search_result_file = uc.search(
        input_file=mzML_file,
        engine=xtandem,
        force=False
    )

    validated_results = uc.validate(
        input_file=unified_search_result_file,
        engine='percolator_2_08',
    )

    uc.params['ssl_score_column_name'] = 'q-value'
    uc.params['ssl_score_type'] = 'PERCOLATOR QVALUE'

    ssl_file = uc.convert(
        input_file=validated_results,
        engine='csv2ssl',
    )
    return


if __name__ == '__main__':
    main(
        mzML_file=sys.argv[1],
        profile=sys.argv[2],
        database=sys.argv[3]
    )
