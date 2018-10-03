#!/usr/bin/env python3
# encoding: utf-8


import ursgal
import glob
import os.path
import sys


def main(folder):
    '''

    Example script for reproducing the data for figure 3

    usage:

        ./barth_et_al_large_scale.py <folder>

    The folder determines the target folder where the files will be downloaded

    Chlamydomonas reinhardtii samples

    Three biological replicates of 4 conditions (2_3, 2_4, 3_1, 4_1)

    For more details on the samples please refer to
    Barth, J.; Bergner, S. V.; Jaeger, D.; Niehues, A.; Schulze, S.; Scholz,
    M.; Fufezan, C. The interplay of light and oxygen in the reactive oxygen
    stress response of Chlamydomonas reinhardtii dissected by quantitative mass
    spectrometry. MCP 2014, 13 (4), 969–989.

    Merge all search results (per biological replicate and condition, on folder
    level) on engine level and validate via percolator.

    'LTQ XL high res':

        * repetition 1
        * repetition 2

    'LTQ XL low res':

        * repetition 3

    Database:

        * Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta

    Note:

        The database and the files will be automatically downloaded from our
        webpage and peptideatlas
    '''

    input_params = {
        'database': os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'modifications': [
            'M,opt,any,Oxidation',
            '*,opt,Prot-N-term,Acetyl',  # N-Acetylation
        ],
        'ftp_url': 'ftp.peptideatlas.org',

        'ftp_login': 'PASS00269',
        'ftp_password': 'FI4645a',

        'ftp_output_folder_root': folder,
        'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data'
        )
    }

    uc = ursgal.UController(
        params=input_params
    )

    if os.path.exists(input_params['database']) is False:
        uc.fetch_file(
            engine='get_http_files_1_0_0'
        )

    output_folder_to_file_list = {
        ('rep1_sample_2_3', 'LTQ XL high res'): [
            'CF_07062012_pH8_2_3A.mzML',
            'CF_13062012_pH3_2_3A.mzML',
            'CF_13062012_pH4_2_3A.mzML',
            'CF_13062012_pH5_2_3A.mzML',
            'CF_13062012_pH6_2_3A.mzML',
            'CF_13062012_pH11FT_2_3A.mzML',
        ],
        ('rep1_sample_2_4', 'LTQ XL high res'): [
            'CF_07062012_pH8_2_4A.mzML',
            'CF_13062012_pH3_2_4A_120615113039.mzML',
            'CF_13062012_pH4_2_4A.mzML',
            'CF_13062012_pH5_2_4A.mzML',
            'CF_13062012_pH6_2_4A.mzML',
            'CF_13062012_pH11FT_2_4A.mzML',

        ],
        ('rep1_sample_3_1', 'LTQ XL high res'): [
            'CF_12062012_pH8_1_3A.mzML',
            'CF_13062012_pH3_1_3A.mzML',
            'CF_13062012_pH4_1_3A.mzML',
            'CF_13062012_pH5_1_3A.mzML',
            'CF_13062012_pH6_1_3A.mzML',
            'CF_13062012_pH11FT_1_3A.mzML',
        ],
        ('rep1_sample_4_1', 'LTQ XL high res'): [
            'CF_07062012_pH8_1_4A.mzML',
            'CF_13062012_pH3_1_4A.mzML',
            'CF_13062012_pH4_1_4A.mzML',
            'CF_13062012_pH5_1_4A.mzML',
            'CF_13062012_pH6_1_4A.mzML',
            'CF_13062012_pH11FT_1_4A.mzML',
        ],

        ('rep2_sample_2_3', 'LTQ XL high res'): [
            'JB_18072012_2-3_A_FT.mzML',
            'JB_18072012_2-3_A_pH3.mzML',
            'JB_18072012_2-3_A_pH4.mzML',
            'JB_18072012_2-3_A_pH5.mzML',
            'JB_18072012_2-3_A_pH6.mzML',
            'JB_18072012_2-3_A_pH8.mzML',
        ],
        ('rep2_sample_2_4', 'LTQ XL high res'): [

            'JB_18072012_2-4_A_FT.mzML',
            'JB_18072012_2-4_A_pH3.mzML',
            'JB_18072012_2-4_A_pH4.mzML',
            'JB_18072012_2-4_A_pH5.mzML',
            'JB_18072012_2-4_A_pH6.mzML',
            'JB_18072012_2-4_A_pH8.mzML',

        ],
        ('rep2_sample_3_1', 'LTQ XL high res'): [
            'JB_18072012_3-1_A_FT.mzML',
            'JB_18072012_3-1_A_pH3.mzML',
            'JB_18072012_3-1_A_pH4.mzML',
            'JB_18072012_3-1_A_pH5.mzML',
            'JB_18072012_3-1_A_pH6.mzML',
            'JB_18072012_3-1_A_pH8.mzML',
        ],
        ('rep2_sample_4_1', 'LTQ XL high res'): [
            'JB_18072012_4-1_A_FT.mzML',
            'JB_18072012_4-1_A_pH3.mzML',
            'JB_18072012_4-1_A_pH4.mzML',
            'JB_18072012_4-1_A_pH5.mzML',
            'JB_18072012_4-1_A_pH6.mzML',
            'JB_18072012_4-1_A_pH8.mzML',
        ],

        ('rep3_sample_2_3', 'LTQ XL low res'): [
            'JB_FASP_pH3_2-3_28122012.mzML',
            'JB_FASP_pH4_2-3_28122012.mzML',
            'JB_FASP_pH5_2-3_28122012.mzML',
            'JB_FASP_pH6_2-3_28122012.mzML',
            'JB_FASP_pH8_2-3_28122012.mzML',
            'JB_FASP_pH11-FT_2-3_28122012.mzML',
        ],
        ('rep3_sample_2_4', 'LTQ XL low res'): [
            'JB_FASP_pH3_2-4_28122012.mzML',
            'JB_FASP_pH4_2-4_28122012.mzML',
            'JB_FASP_pH5_2-4_28122012.mzML',
            'JB_FASP_pH6_2-4_28122012.mzML',
            'JB_FASP_pH8_2-4_28122012.mzML',
            'JB_FASP_pH11-FT_2-4_28122012.mzML',
        ],
        ('rep3_sample_3_1', 'LTQ XL low res'): [
            'JB_FASP_pH3_3-1_28122012.mzML',
            'JB_FASP_pH4_3-1_28122012.mzML',
            'JB_FASP_pH5_3-1_28122012.mzML',
            'JB_FASP_pH6_3-1_28122012.mzML',
            'JB_FASP_pH8_3-1_28122012.mzML',
            'JB_FASP_pH11-FT_3-1_28122012.mzML',
        ],
        ('rep3_sample_4_1', 'LTQ XL low res'): [
            'JB_FASP_pH3_4-1_28122012.mzML',
            'JB_FASP_pH4_4-1_28122012.mzML',
            'JB_FASP_pH5_4-1_28122012.mzML',
            'JB_FASP_pH6_4-1_28122012.mzML',
            'JB_FASP_pH8_4-1_28122012.mzML',
            'JB_FASP_pH11-FT_4-1_28122012_130121201449.mzML',
        ],
    }

    for (outfolder, profile), mzML_file_list in sorted(output_folder_to_file_list.items()):
        uc.params['ftp_output_folder'] = os.path.join(
            input_params['ftp_output_folder_root'],
            outfolder
        )
        uc.params['ftp_include_ext'] = mzML_file_list

        if os.path.exists(uc.params['ftp_output_folder']) is False:
            os.makedirs(uc.params['ftp_output_folder'])

        uc.fetch_file(
            engine='get_ftp_files_1_0_0'
        )

    if os.path.exists(input_params['database']) is False:
        uc.fetch_file(
            engine='get_http_files_1_0_0'
        )

    search_engines = [
        'omssa_2_1_9',
        'xtandem_piledriver',
        'myrimatch_2_1_138',
        'msgfplus_v9979',
        'msamanda_1_0_0_5243',
    ]

    # This dict will be populated with the percolator-validated results
    # of each engine ( 3 replicates x4 conditions = 12 files each )
    percolator_results = {
        'omssa_2_1_9': [],
        'xtandem_piledriver': [],
        'msgfplus_v9979': [],
        'myrimatch_2_1_138': [],
        'msamanda_1_0_0_5243': [],
    }

    five_files_for_venn_diagram = []

    for search_engine in search_engines:

        # This list will collect all 12 result files for each engine,
        # after Percolator validation and filtering for PSMs with a
        # FDR <= 0.01
        filtered_results_of_engine = []
        for mzML_dir_ext, mass_spectrometer in output_folder_to_file_list.keys():
            # for mass_spectrometer, replicate_dir in replicates:
            # for condition_dir in conditions:
            uc.set_profile(mass_spectrometer)

            mzML_dir = os.path.join(
                input_params['ftp_output_folder_root'],
                mzML_dir_ext
            )
            # i.e. /media/plan-f/mzML/Christian_Fufezan/ROS_Experiment_2012/Juni_2012/2_3/Tech_A/
            # all files ending with .mzml in that directory will be used!

            unified_results_list = []
            for filename in glob.glob(os.path.join(mzML_dir, '*.mzML')):
                # print(filename)
                if filename.lower().endswith(".mzml"):
                    # print(filename)
                    unified_search_results = uc.search(
                        input_file=filename,
                        engine=search_engine,
                    )
                    unified_results_list.append(
                        unified_search_results
                    )

            # Merging results from the 6 pH-fractions:
            merged_unified = uc.execute_misc_engine(
                input_file=unified_results_list,
                engine='merge_csvs_1_0_0',
            )

            # Validation with Percolator:
            percolator_validated = uc.validate(
                input_file=merged_unified,
                engine='percolator_2_08',  # one could replace this with 'qvality'
            )
            percolator_results[search_engine].append(
                percolator_validated
            )

            # At this point, the analysis is finished. We got
            # Percolator-validated results for each of the 3
            # replicates and 12 conditions.

            # But let's see how well the five search engines
            # performed! To compare, we collect all PSMs with
            # an estimated FDR <= 0.01 for each engine, and
            # plot this information with the VennDiagram UNode.
            # We will also use the Combine FDR Score method
            # to combine the results from all five engines,
            # and increase the number of identified peptides.

    five_large_merged = []
    filtered_final_results = []

    # We will estimate the FDR for all 60 files
    # (5 engines x12 files) when using percolator PEPs as
    # quality score
    uc.params['validation_score_field'] = 'PEP'
    uc.params['bigger_scores_better'] = False

    # To make obtain smaller CSV files (and make plotting
    # less RAM-intensive, we remove all decoys and PSMs above
    # 0.06 FDR
    uc.params['csv_filter_rules'] = [
        ['estimated_FDR', 'lte', 0.06],
        ['Is decoy', 'equals', 'false']
    ]
    for engine, percolator_validated_list in percolator_results.items():

        # unfiltered files for cFDR script
        twelve_merged = uc.execute_misc_engine(
            input_file=percolator_validated_list,
            engine='merge_csvs_1_0_0',
        )

        twelve_filtered = []
        for one_of_12 in percolator_validated_list:
            one_of_12_FDR = uc.validate(
                input_file=one_of_12,
                engine='add_estimated_fdr_1_0_0'
            )
            one_of_12_FDR_filtered = uc.execute_misc_engine(
                input_file=one_of_12_FDR,
                engine='filter_csv_1_0_0'
            )
            twelve_filtered.append(one_of_12_FDR_filtered)

        # For the combined FDR scoring, we merge all 12 files:
        filtered_merged = uc.execute_misc_engine(
            input_file=twelve_filtered,
            engine='merge_csvs_1_0_0'
        )

        five_large_merged.append(twelve_merged)
        filtered_final_results.append(filtered_merged)

    # The five big merged files of each engine are combined:
    cFDR = uc.combine_search_results(
        input_files=five_large_merged,
        engine='combine_FDR_0_1',
    )

    # We estimate the FDR of this combined approach:
    uc.params['validation_score_field'] = 'Combined FDR Score'
    uc.params['bigger_scores_better'] = False

    cFDR_FDR = uc.validate(
        input_file=cFDR,
        engine='add_estimated_fdr_1_0_0'
    )

    # Removing decoys and low quality hits, to obtain a
    # smaller file:
    uc.params['csv_filter_rules'] = [
        ['estimated_FDR', 'lte', 0.06],
        ['Is decoy', 'equals', 'false']
    ]
    cFDR_filtered_results = uc.execute_misc_engine(
        input_file=cFDR_FDR,
        engine='filter_csv_1_0_0',
    )
    filtered_final_results.append(cFDR_filtered_results)

    # Since we produced quite a lot of files, let's print the full
    # paths to our most important result files so we find them quickly:
    print(
        '''
These files can now be easily parsed and plotted with your
plotting tool of choice! We used the Python plotting library
matplotlib. Each unique combination of Sequence, modification
and charge was counted as a unique peptide.
        '''
    )
    print("\n########### Result files: ##############")
    for result_file in filtered_final_results:
        print(
            '\t*{0}'.format(
                result_file
            )
        )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)
    main(sys.argv[1])
