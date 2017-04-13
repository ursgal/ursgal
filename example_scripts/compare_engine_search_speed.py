#!/usr/bin/env python3.4
# encoding: utf-8

import ursgal
import os
import time


def main():
    '''
    '''
    engine_list = [
        'msfragger_20170103',
        'xtandem_vengeance',
        'omssa',
        'msgfplus_v2016_09_16'
    ]

    params = {
        'database' : os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'modifications' : [
            '*,opt,Prot-N-term,Acetyl',
            'M,opt,any,Oxidation',
            # 'C,fix,any,Carbamidomethyl',
            # 'T,opt,any,Phospho',
            # 'S,opt,any,Phospho',
            # 'Y,opt,any,Phospho',
        ],
        'csv_filter_rules':[
            ['PEP'      , 'lte'    , 0.01 ]    ,
            ['Is decoy' , 'equals' , 'false']
        ],
        'ftp_url'       : 'ftp.peptideatlas.org',
        'ftp_login'         : 'PASS00269',
        'ftp_password'      : 'FI4645a',
        'ftp_include_ext'   : [
            'JB_FASP_pH8_2-3_28122012.mzML',
        ],
        'ftp_output_folder' : os.path.join(
            os.pardir,
            'example_data',
            'xtandem_and_msfragger_comparison'
        ),
        'http_url': 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/misc/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta' ,
        'http_output_folder' : os.path.join(
            os.pardir,
            'example_data'
        ),
        # 'precursor_max_mass' : 5000,
        # 'precursor_min_mass' : 500,
        # 'frag_max_charge'    : 2,
        # 'min_pep_length'     : 7,
        # 'max_num_per_mod'    : 3,
        # 'num_match_spec'     : 10,
        # 'precursor_true_tolerance' : 20,
        # 'precursor_true_tolerance_units' : 'ppm',
        # 'frag_mass_tolerance' : 500,
        # 'frag_mass_tolerance_unit' : 'ppm',

    }

    if os.path.exists(params['ftp_output_folder']) is False:
        os.mkdir(params['ftp_output_folder'])

    uc = ursgal.UController(
        profile = 'LTQ XL low res' ,
        params = params
    )
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
    time_collector = {}
    filtered_files_list = []
    for engine in engine_list:
        start_time =time.time()
        unified_result_file = uc.search(
            input_file = mzML_file,
            engine     = engine,
        )
        time_collector[ engine ] = time.time()-start_time
        # exit()
        validated_file = uc.validate(
            input_file = unified_result_file,
            engine     = 'percolator_2_08',
        )

        filtered_file = uc.filter_csv(
            input_file = validated_file,
        )

        filtered_files_list.append( filtered_file )

    uc.visualize(
        input_files     = filtered_files_list,
        engine          = 'venndiagram',
    )

    for key, duration in time_collector.items():
        print('Engine {0} took {1:1.2f}s'.format(key,duration))
    return

if __name__ == '__main__':
    main()
