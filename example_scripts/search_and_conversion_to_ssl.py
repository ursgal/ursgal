#!/usr/bin/env python3.4
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main():
    '''
    Executes a search with XTandem on the BSA1.mzML input_file.
    Results are validated with percolator and exported to .ssl.

    usage:
        ./search_and_conversion_to_ssl.py

    '''
    uc = ursgal.UController(
        profile = 'LTQ XL low res',
        params = {
            'database' : os.path.join(
                os.pardir,
                'example_data',
                'BSA.fasta'
            ),
            'modifications' : [
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

    mzML_file = os.path.join(
        os.pardir,
        'example_data',
        'BSA_simple_example_search',
        'BSA1.mzML'
    )
    if os.path.exists(mzML_file) is False:
        uc.params['http_url'] = 'http://sourceforge.net/p/open-ms/code/HEAD/tree/OpenMS/share/OpenMS/examples/BSA/BSA1.mzML?format=raw'
        uc.params['http_output_folder'] = os.path.dirname(mzML_file)
        uc.fetch_file(
            engine     = 'get_http_files_1_0_0',
        )
        try:
            shutil.move(
                '{0}?format=raw'.format(mzML_file),
                mzML_file
            )
        except:
            shutil.move(
                '{0}format=raw'.format(mzML_file),
                mzML_file
            )

    unified_search_result_file = uc.search(
        input_file = mzML_file,
        engine     = xtandem,
        force      = False
    )

    validated_results = uc.validate(
        input_file = unified_search_result_file,
        engine = 'percolator_2_08',
    )

    uc.params['ssl_score_column_name'] = 'q-value'
    uc.params['ssl_score_type'] = 'PERCOLATOR QVALUE' 

    ssl_file = uc.visualize(
        input_files    = validated_results,
        engine         = 'csv2ssl',
    )
    return


if __name__ == '__main__':
    main()
