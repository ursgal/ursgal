#!/usr/bin/env python3
import ursgal
import os


def main():
    """."""
    params = {
        'csv_filter_rules': [
            ['q-value', 'lte', 0.01],
            ['Is decoy', 'equals', 'false']
        ],
        'modifications': [
            "M,opt,any,Oxidation",
            "*,opt,Prot-N-term,Acetyl",
            "C,fix,any,Carbamidomethyl",
        ],
        'database': '/media/external/Projects/proteomics_blog_hackathon/data/Uniprot_swissprot_TREMBL_cRAP_target_decoy.fasta',
        "isotopic_distribution_tolerance": 5,
        "normalize_intensities": False,
        "integrate_peak_areas": False,
        "only_precursor_charge": False,
        "match_between_runs": True,
        "match_between_runs_RT_window": 0.5,
        "require_msms_id": False,
        "bayesian_fold_change": False,
        "bayesian_fold_change_control_condition": "WT",
        "fold_change_cutoff": 0.1,
        "markov_chain_iterations": 3000,
        "markov_chain_burn_in_iterations": 1000,
        "use_shared_peptides": False,
        "random_seed": 200,
    }

    uc = ursgal.UController(
        profile='QExactive+',
        params=params
    )
    uc.params['experiment_setup'] = {
        # "1": {"FileName": "TN_CSF_062617_03", "Condition": "WT", "Biorep": 1, "Fraction": 1, "Techrep":1},
        # "2": {"FileName": "TN_CSF_062617_04", "Condition": "KO", "Biorep": 1, "Fraction": 1, "Techrep":1},
    }

    mzml_files = [
        '/media/external/Projects/proteomics_blog_hackathon/data/flash_lfq_test/TN_CSF_062617_03.mzML',
        # '/media/external/Projects/proteomics_blog_hackathon/data/flash_lfq_test/TN_CSF_062617_04.mzML',
    ]
    all_res = []
    for file in mzml_files:

        res = uc.search(
            input_file=file,
            # force=True,
            engine='xtandem_alanine',
        )
        val = uc.validate(
            input_file=res,
            engine='percolator_2_08'
        )
        fil = uc.filter_csv(
            input_file=val
        )
        all_res.append(fil)

    merged_res = uc.merge_csvs(input_files=all_res)
    merged_res = '/media/external/Projects/proteomics_blog_hackathon/data/flash_lfq_test/All_merged_results_accepted.csv'
    uc.params['quantification_evidences'] = merged_res
    print(mzml_files)
    print()
    mzml_files = '/media/external/Projects/proteomics_blog_hackathon/data/flash_lfq_test/TN_CSF_062617_03.mzML'
    uc.quantify(
        input_file=mzml_files,
        engine='flash_lfq_1_1_1',
        force=True,
        multi=False,
    )


if __name__ == '__main__':
    main()
