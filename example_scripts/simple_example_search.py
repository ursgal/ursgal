#!/usr/bin/env python3.4
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
    params = {
        'database' : os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'modifications' : [
            'M,opt,any,Oxidation',        # Met oxidation
            'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
            '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
        ],
        'http_url': 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/misc/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta' ,
        'http_output_folder' : os.path.join(
            os.pardir,
            'example_data'
        ),
        'ftp_url'       : 'ftp.peptideatlas.org',
        'ftp_login'         : 'PASS00269',
        'ftp_password'      : 'FI4645a',
        'ftp_include_ext'   : [
            'JB_FASP_pH8_2-3_28122012.mzML',
        ],
        'ftp_output_folder' : os.path.join(
            os.pardir,
            'example_data',
            'simple_search'
    ),
        # 'peptide_mapper_class_version' : 'UPeptideMapper_v2',
    }
    uc = ursgal.UController(
        profile = 'LTQ XL low res',
        params = params
    )

    if sys.maxsize > 2 ** 32:
        xtandem = 'xtandem_vengeance'
    else:
        xtandem = 'xtandem_sledgehammer'

    engine_list = [
        'msgfplus_v2016_09_16',
        'omssa',
        xtandem,
    ]

    mzML_file = os.path.join(
        params['ftp_output_folder'],
        params['ftp_include_ext'][0]
    )
    if os.path.exists(mzML_file) is False:
        uc.fetch_file(
            engine     = 'get_ftp_files_1_0_0'
        )
    if os.path.exists(params['database']) is False:
        uc.fetch_file(
            engine     = 'get_http_files_1_0_0'
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

    unified_file_list = []

    for engine in engine_list:
        unified_search_result_file = uc.search(
            input_file = mzML_file,
            engine     = engine,
            force      = False
        )
        uc.params['infere_proteins'] = True
        val = uc.validate(
            input_file=unified_search_result_file,
            engine    = 'percolator_3_0'
        )
        unified_file_list.append(val)
    
    uc.visualize(
        input_files    = unified_file_list,
        engine         = 'venndiagram',
    )
    return


if __name__ == '__main__':
    main()
