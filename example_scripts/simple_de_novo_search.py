#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main():
    '''
    Executes a search with Novor and PepNovo on the BSA1.mzML
    input_file

    usage:
        ./simple_de_novo_search.py

    Note:
        PepNovo currently only works for Linux. 
        Novor needs to be downloaded from http://rapidnovor.com/novor/standalone/ and 
        stored at <ursgal_path>/resources/<platform>/<architecture>/novor_1_1beta

    '''
    uc = ursgal.UController(
        profile='LTQ XL low res',
        params={
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
            ],
        }
    )

    engine_list = [
        'novor',
        'pepnovo',
    ]

    mzML_file = os.path.join(
        os.pardir,
        'example_data',
        'BSA_simple_de_novo_search',
        'BSA1.mzML'
    )
    if os.path.exists(mzML_file) is False:
        uc.params['http_url'] = 'http://sourceforge.net/p/open-ms/code/HEAD/tree/OpenMS/share/OpenMS/examples/BSA/BSA1.mzML?format=raw'
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

    unified_file_list = []

    for engine in engine_list:
        unified_search_result_file = uc.search(
            input_file=mzML_file,
            engine=engine,
            force=False
        )
        unified_file_list.append(unified_search_result_file)

    uc.visualize(
        input_files=unified_file_list,
        engine='venndiagram_1_1_0',
    )
    return


if __name__ == '__main__':
    main()
