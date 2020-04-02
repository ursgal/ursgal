#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import sys
import glob
import os


def main(folder=None, profile=None, target_decoy_database=None, validated_file=None):

    # define folder with mzML_files as sys.argv[1]
    mzML_files = []
    for mzml in glob.glob(os.path.join('{0}'.format(folder), '*.mzML')):
        mzML_files.append(mzml)
    mass_spectrometer = profile

    # We specify all search engines and validation engines that we want to use in a list
    # (version numbers might differ on windows or mac):
    search_engines = [
        'msfragger_20171106',
    ]

    validation_engine = 'percolator_3_2_1'

    # Initializing the Ursgal UController class with
    # our specified mass spectrometer
    params = {
        'database': target_decoy_database,
        'modifications' : ['C,fix,any,Carbamidomethyl'],
        'csv_filter_rules': [
            ['Is decoy', 'equals', 'false'],
            ['PEP', 'lte', 0.01],
        ],
        'enzyme' : 'trypsin',
        'frag_mass_tolerance_unit' : 'ppm',
        'frag_mass_tolerance' : 10,
        'precursor_mass_tolerance_unit' : 'da',
        'precursor_mass_tolerance_plus' : 4000,
        'precursor_mass_tolerance_minus' : -200,
        'precursor_true_units' : 'ppm',
        'precursor_true_tolerance' : 10,
    }

    uc = ursgal.UController(
        profile=mass_spectrometer,
        params=params,
    )

    # complete workflow:
    # every spectrum file is searched with every search engine,
    # results are validated and filtrated for targets and PEP <= 0.01 (for each engine seperately).
    # In the end, all filtered results from all spectrum files are merged
    for search_engine in search_engines :
        result_all_files_each_engine = []
        mgf_files = [] 
        for spec_file in mzML_files:

            #1. convert to MGF
            mgf_file = uc.convert(
                input_file=spec_file,
                engine = 'mzml2mgf_2_0_0',
                )

            mgf_files.append(mgf_file)

            #2. do the actual search
            raw_search_results=uc.search_mgf(
                input_file = mgf_file,
                engine = search_engine,
                )

            #3. convert files to csv
            csv_search_results= uc.convert(
                input_file=raw_search_results,
                engine = None,
                guess_engine = True,
                )

            #4. protein mapping. 
            mapped_csv_search_results = uc.execute_misc_engine(
                input_file       = csv_search_results,
                #output_file_name = output_file_name,
                engine           = 'upeptide_mapper_1_0_0',
            )

            #5. Convert csv to unified ursgal csv format:
            unified_search_results = uc.execute_misc_engine(
                input_file       = mapped_csv_search_results,
                #output_file_name = output_file_name,
                engine           = 'unify_csv_1_0_0',
                merge_duplicates = False,
            )

            validated_csv = uc.validate(
                input_file=unified_search_results,
                engine=validation_engine,
                )

            filtered_validated_results = uc.execute_misc_engine(
                input_file=validated_csv,
                engine='filter_csv_1_0_0',
                )

            result_all_files_each_engine.append(filtered_validated_results)

        
        merged_results = uc.execute_misc_engine(
            input_file=result_all_files_each_engine,
            engine='merge_csvs_1_0_0',
        )

        uc.params.update({
            'mgf_input_files_list' : mgf_files,
        })

        #you can give a merged file or a file from a single mgf file as input_file
        ptminer_results = uc.execute_misc_engine(
            input_file=merged_results,
            engine='ptminer',
            force=True,
            #output_file_name='ptminer_test'
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
