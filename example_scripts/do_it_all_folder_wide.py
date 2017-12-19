#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import sys
import glob
import os


def main(folder=None, profile=None, target_decoy_database=None):
    '''
    An example test script to search all mzML files which are present in the
    specified folder. The search is currently performed on 4 search engines
    and 2 validation engines.

    The machine profile has to be specified as well as the target-decoy
    database.

    usage:

        ./do_it_all_folder_wide.py <mzML_folder> <profile> <target_decoy_database>


    Current profiles:

        * 'QExactive+'
        * 'LTQ XL low res'
        * 'LTQ XL high res'

    '''
    # define folder with mzML_files as sys.argv[1]
    mzML_files = []
    for mzml in glob.glob(os.path.join('{0}'.format(folder), '*.mzML')):
        mzML_files.append(mzml)

    mass_spectrometer = profile

    # We specify all search engines and validation engines that we want to use in a list
    # (version numbers might differ on windows or mac):
    search_engines = [
        'omssa',
        'xtandem_vengeance',
        'msgfplus_v2016_09_16',
        # 'msamanda_1_0_0_6300',
        # 'myrimatch_2_1_138',
    ]

    validation_engines = [
        'percolator_2_08',
        'qvality',
    ]

    # Modifications that should be included in the search
    all_mods = [
        'C,fix,any,Carbamidomethyl',
        'M,opt,any,Oxidation',
        # 'N,opt,any,Deamidated',
        # 'Q,opt,any,Deamidated',
        # 'E,opt,any,Methyl',
        # 'K,opt,any,Methyl',
        # 'R,opt,any,Methyl',
        '*,opt,Prot-N-term,Acetyl',
        # 'S,opt,any,Phospho',
        # 'T,opt,any,Phospho',
        # 'N,opt,any,HexNAc'
    ]

    # Initializing the Ursgal UController class with
    # our specified modifications and mass spectrometer
    params = {
        'database': target_decoy_database,
        'modifications': all_mods,
        'csv_filter_rules': [
            ['Is decoy', 'equals', 'false'],
            ['PEP', 'lte', 0.01],
        ]
    }

    uc = ursgal.UController(
        profile=mass_spectrometer,
        params=params
    )

    # complete workflow:
    # every spectrum file is searched with every search engine,
    # results are validated (for each engine seperately),
    # validated results are merged and filtered for targets and PEP <= 0.01.
    # In the end, all filtered results from all spectrum files are merged
    for validation_engine in validation_engines:
        result_files = []
        for spec_file in mzML_files:
            validated_results = []
            for search_engine in search_engines:
                unified_search_results = uc.search(
                    input_file=spec_file,
                    engine=search_engine,
                )
                validated_csv = uc.validate(
                    input_file=unified_search_results,
                    engine=validation_engine,
                )
                validated_results.append(validated_csv)

            validated_results_from_all_engines = uc.execute_misc_engine(
                input_file=validated_results,
                engine='merge_csvs_1_0_0',
            )
            filtered_validated_results = uc.execute_misc_engine(
                input_file=validated_results_from_all_engines,
                engine='filter_csv_1_0_0',
            )
            result_files.append(filtered_validated_results)

        results_all_files = uc.execute_misc_engine(
            input_file=result_files,
            engine='merge_csvs_1_0_0',
        )

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(main.__doc__)
        sys.exit(1)
    main(
        folder=sys.argv[1],
        profile=sys.argv[2],
        target_decoy_database=sys.argv[3],
    )
