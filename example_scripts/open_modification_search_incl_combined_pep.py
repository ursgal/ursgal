#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import sys
import glob
import os
import pprint


def main(folder=None, database=None, enzyme=None):
    '''
    Example workflow to perform a open modification search with three independent search engines
    across all mzML files of a given folder and to statistically post-process and combine the
    results of all searches.

    Usage:
        ./open_modification_search_incl_combined_pep.py <mzML_folder> <database> <enzyme>
    '''
    #For this particular dataset, two enzymes were used, namely gluc and trypsin.
    mzml_files = []
    for mzml in glob.glob(os.path.join(folder, '*.mzML')):
        mzml_files.append(mzml)

    mass_spectrometer = 'QExactive+'
    validation_engine = 'percolator_3_4_0'
    search_engines = ['msfragger_2_3', 'pipi_1_4_6', 'moda_v1_61']

    params = {
        'modifications' : ['C,fix,any,Carbamidomethyl'],
        'csv_filter_rules': [
            ['Is decoy', 'equals', 'false'],
            ['PEP', 'lte', 0.01],
        ],
        'frag_mass_tolerance_unit' : 'ppm',
        'frag_mass_tolerance' : 20,
        'precursor_mass_tolerance_unit' : 'ppm',
        'precursor_mass_tolerance_plus' : 5,
        'precursor_mass_tolerance_minus' : 5,
        'moda_high_res' : False,
        'max_mod_size' : 4000,
        'min_mod_size' : -200,
        'precursor_true_units' : 'ppm',
        'precursor_true_tolerance' : 5,
        'percolator_post_processing': 'mix-max',
        'psm_defining_colnames': [
            'Spectrum Title',
            'Sequence',
            'Modifications',
            'Charge',
            'Is decoy',
            'Mass Difference'
        ],
        'database': database,
        'enzyme': enzyme,
    }

    uc = ursgal.UController(
        profile=mass_spectrometer,
        params=params,
    )

    # This will hold input to combined PEP engine
    combined_pep_input = defaultdict(list)
    
    # This dictionary will help organize which results to merge
    all_merged_results = defaultdict(list)

    for search_engine in search_engines:

        #The modification size for MSFragger is configured through precursor mass tolerance
        if search_engine == 'msfragger_2_3':
            uc.params.update({
                'precursor_mass_tolerance_unit' : 'da',
                'precursor_mass_tolerance_plus' : 4000, 
                'precursor_mass_tolerance_minus' : 200,
            })

        for n, spec_file in enumerate(mzml_files):
            #1. convert to MGF
            mgf_file = uc.convert(
                input_file=spec_file,
                engine = 'mzml2mgf_2_0_0',
                )

            #2. do the actual search
            raw_search_results=uc.search_mgf(
                input_file = mgf_file,
                engine = search_engine,
                )

            #reset precursor mass tolerance just in case it was previously changed
            uc.params.update(
                {
                    'precursor_mass_tolerance_unit': 'ppm', 
                    'precursor_mass_tolerance_plus': 5, 
                    'precursor_mass_tolerance_minus': 5
                }
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
                engine           = 'upeptide_mapper_1_0_0',
            )

            # 5. Convert csv to unified ursgal csv format:
            unified_search_results = uc.execute_misc_engine(
                input_file       = mapped_csv_search_results,
                engine           = 'unify_csv_1_0_0',
                merge_duplicates = False,
            )

            # 6. Validate the results
            validated_csv = uc.validate(
                input_file=unified_search_results,
                engine=validation_engine,
            )

            #save the validated input for combined pep
            #Eventually, each sample will have 3 files correpsonding to the 3 search engines
            combined_pep_input['sample_{0}'.format(n)].append(validated_csv)

            filtered_validated_results = uc.execute_misc_engine(
                input_file=validated_csv,
                engine='filter_csv_1_0_0',
                merge_duplicates=False,
            )

            all_merged_results['percolator_only'].append(filtered_validated_results)

    #combined pep
    uc.params.update({
        'csv_filter_rules': [
            ['Is decoy', 'equals', 'false'],
            ['combined PEP', 'lte', 0.01],
        ],
        'psm_defining_colnames': [
            'Spectrum Title',
            'Sequence',
            'Modifications',
            'Charge',
            'Is decoy',
        ],
    })
    for sample in combined_pep_input.keys():
        combine_results = uc.execute_misc_engine(
            input_file=combined_pep_input[sample],
            engine='combine_pep_1_0_0',
        )

        filtered_validated_results = uc.execute_misc_engine(
                input_file=combine_results,
                engine='filter_csv_1_0_0',
            )
        all_merged_results['combined_pep'].append(filtered_validated_results)

    #separately merge results from the two types of validation techniques
    #We also add back "Mass Difference" to columns defining a PSM to avoid merging mass differences
    uc.params.update({   
        'psm_defining_colnames': [
            'Spectrum Title',
            'Sequence',
            'Modifications',
            'Charge',
            'Is decoy',
            'Mass Difference'
        ],
    })

    for validation_type in all_merged_results.keys():
        if validation_type == 'percolator_only':
            uc.params['psm_colnames_to_merge_multiple_values'] = {
                'PEP': 'min_value',
            }
        else:
            uc.params['psm_colnames_to_merge_multiple_values'] = {
                'combined PEP': 'min_value',
                'Bayes PEP': 'min_value',
            }

        uc.params['prefix'] = 'All_{0}'.format(validation_type) #helps recognize files easily
        
        merged_results_one_rep = uc.execute_misc_engine(
            input_file=all_merged_results[validation_type],
            engine='merge_csvs_1_0_0',
            merge_duplicates=True,
        )
        uc.params['prefix'] = ''

if __name__ == '__main__':
    main(
        folder=sys.argv[1],
        database=sys.argv[2],
        enzyme=sys.argv[3],
    )
