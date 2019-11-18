#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main():
    '''

    '''
    uc = ursgal.UController(
        profile='LTQ XL low res',
        params={
            'database': os.path.join(
                os.pardir,
                'example_data',
                'BSA.fasta'
            ),
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
            ],
        }
    )

    mzML_file = os.path.join(
        os.pardir,
        'example_data',
        'mzid_lib_comparison',
        'BSA1.mzML'
    )
    if os.path.exists(mzML_file) is False:
        uc.params[
            'http_url'] = 'http://sourceforge.net/p/open-ms/code/HEAD/tree/OpenMS/share/OpenMS/examples/BSA/BSA1.mzML?format=raw'
        uc.params['http_output_folder'] = os.path.dirname(mzML_file)
        uc.fetch_file(
            engine='get_http_files_1_0_0',
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

    converter_engine_list = [
        'mzidentml_lib_1_7',
        'mzidentml_lib_1_6_10',
        'mzidentml_lib_1_6_11',
    ]

    unified_file_list = []
    uc.params['visualization_label_positions'] = {}
    for n, conveter_engine in enumerate(converter_engine_list):
        uc.params['visualization_label_positions'][str(n)] = conveter_engine
        uc.params['mzidentml_converter_version'] = conveter_engine
        uc.params['prefix'] = conveter_engine
        unified_search_result_file = uc.search(
            input_file=mzML_file,
            engine='msgfplus_v9979',
            force=False
        )
        unified_file_list.append(unified_search_result_file)
    uc.params['prefix'] = None
    uc.visualize(
        input_files=unified_file_list,
        engine='venndiagram_1_1_0',
    )

    return


if __name__ == '__main__':
    main()
