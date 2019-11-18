#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main():
    '''
    Executes a search with OMSSA, XTandem and MS-GF+ on the BSA1.mzML
    input_file

    usage:
        ./simple_example_search.py

    Note:
        Myrimatch does not work with this file.
        To use MSAmanda on unix platforms, please install mono 
        (http://www.mono-project.com/download)

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
                '*,opt,Prot-N-term,Acetyl',    # N-Acteylation
            ],
            # 'peptide_mapper_class_version' : 'UPeptideMapper_v2',
        }
    )

    if sys.maxsize > 2 ** 32:
        xtandem = 'xtandem_vengeance'
    else:
        xtandem = 'xtandem_sledgehammer'

    engine_list = [
        'omssa',
        xtandem,
        'msgfplus_v2016_09_16',
    ]

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