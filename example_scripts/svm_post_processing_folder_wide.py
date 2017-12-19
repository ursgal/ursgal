#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import glob
import sys


def main(folder=None, profile=None, target_decoy_database=None):
    '''
    An example test script to search all mzML files which are present in the
    specified folder and post-process them with a support vector machine.
    This method is similar to Percolator. Furthermore, SVM scores are used
    to estimate the false discovery rate (FDR) of PSMs. This allows the user
    to choose an error rate.

    Note:
        SVM post-processing requires the free Python module scikit-learn.
        For installation instructions, see http://scikit-learn.org/stable/install.html

    The machine profile has to be specified as well as the target-decoy
    database.

    usage:

        ./simple_svm_post_processing_folder_wide.py <mzML_folder> <profile> <target_decoy_database>


    Current profiles:

        * 'QExactive+'
        * 'LTQ XL low res'
        * 'LTQ XL high res'

    '''
    input_params = {
        'database': target_decoy_database,
        'modifications': [
            'M,opt,any,Oxidation',
            '*,opt,Prot-N-term,Acetyl',  # N-Acetylation
        ],

        # You can customize the SVM kernel and parameters like this:

        'fdr_cutoff': 0.01,  # target PSMs with a lower FDR than this
        # threshold will be used as a positive training set in the SVM
        'kernel': 'rbf',  # the kernel function of the SVM ("rbf",
        # "linear", "poly" or "sigmoid")
        'svm_c_param': 1.0,  # penalty parameter C of the error
        # term of the SVM
    }

    uc = ursgal.UController(
        profile=profile,
        params=input_params,
    )

    engine_list = [
        'omssa',
        'xtandem_vengeance',
        'msgfplus_v2016_09_16',
        'myrimatch_2_1_138',
    ]

    # find all .mzML files in the folder that was
    # specified as first command line argument
    mzML_files = glob.glob(os.path.join(folder, '*.mzML'))

    svm_validated_files = []

    for search_engine in engine_list:
        unified_csvs = []
        for mzML_file in mzML_files:
            unified_search_result_file = uc.search(
                input_file=mzML_file,
                engine=search_engine,
            )
            unified_csvs.append(unified_search_result_file)

        merged_unified_csv = uc.execute_misc_engine(
            input_file=unified_csvs,
            engine='merge_csvs'
        )

        # Statistical post-processing of PSMs with a support vector machine
        svm_validated_csv = uc.validate(
            input_file=merged_unified_csv,
            engine='svm_1_0_0',
        )

        # Estimate the false discovery rate (FDR) for each PSM,
        # based on the support vector machine's score
        uc.params['validation_score_field'] = 'SVMscore'
        # Larger SVM scores indicate higher confidence
        uc.params['bigger_scores_better'] = True
        svm_results_with_fdr = uc.add_estimated_fdr(
            input_file=svm_validated_csv,
        )
        # Reset validation parameters to default (for subsequent SVM
        # validation)
        uc.params['validation_score_field'] = None
        uc.params['bigger_scores_better'] = None
        svm_validated_files.append(svm_results_with_fdr)

    print('\nYour SVM-validated search results:')
    for svm_validated_file in svm_validated_files:
        print(svm_validated_file)
    return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(main.__doc__)
        sys.exit('You did not specify three command line arguments, exiting.')
    main(
        folder=sys.argv[1],
        profile=sys.argv[2],
        target_decoy_database=sys.argv[3]
    )
