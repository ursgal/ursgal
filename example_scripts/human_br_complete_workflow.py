#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import os
import sys
import pprint


def main(folder):
    '''

    usage:

        ./human_br_complete_workflow.py <folder_with_human_br_files>

    This scripts produces the data for figure 3.

    '''

    # Initialize the UController:
    uc = ursgal.UController(
        params={
            'enzyme': 'trypsin',
            'decoy_generation_mode': 'reverse_protein',
        }
    )

    # MS Spectra, downloaded from http://proteomecentral.proteomexchange.org
    # via the dataset accession PXD000263 and converted to mzML

    mass_spec_files = [
        '120813OTc1_NQL-AU-0314-LFQ-LCM-SG-01_013.mzML',
        '120813OTc1_NQL-AU-0314-LFQ-LCM-SG-02_025.mzML',
        '120813OTc1_NQL-AU-0314-LFQ-LCM-SG-03_033.mzML',
        '120813OTc1_NQL-AU-0314-LFQ-LCM-SG-04_048.mzML',
    ]

    for mass_spec_file in mass_spec_files:
        if os.path.exists(os.path.join(folder, mass_spec_file)) is False:
            print(
                'Please download RAW files to folder {} and convert to mzML:'.format(folder))
            pprint.pprint(mass_spec_files)
            sys.exit(1)

    # mods from Wen et al. (2015):
    modifications = [
        # Carbamidomethyl  (C) was set as fixed modification
        'C,fix,any,Carbamidomethyl',
        'M,opt,any,Oxidation',        # Oxidation (M) as well as
        # Deamidated (NQ) were set as optional modification
        'N,opt,any,Deamidated',
        # Deamidated (NQ) were set as optional modification
        'Q,opt,any,Deamidated',
    ]

    # The target peptide database which will be searched (UniProt Human
    # reference proteome from July 2013)
    target_database = 'uniprot_human_UP000005640_created_until_20130707.fasta'
    # Let's turn it into a target decoy database by reversing peptides:
    target_decoy_database = uc.execute_misc_engine(
        input_file=target_database,
        engine='generate_target_decoy_1_0_0'
    )

    # OMSSA parameters from Wen et al. (2015):
    omssa_params = {
        # (used by default) # -w
        'he': '1000', # -he 1000
        'zcc': '1', # -zcc 1
        'frag_mass_tolerance': '0.6', # -to 0.6
        'frag_mass_tolerance_unit': 'da', # -to 0.6
        'precursor_mass_tolerance_minus': '10', # -te 10
        'precursor_mass_tolerance_plus': '10', # -te 10
        'precursor_mass_tolerance_unit': 'ppm', # -teppm
        'score_a_ions': False, # -i 1,4
        'score_b_ions': True, # -i 1,4
        'score_c_ions': False, # -i 1,4
        'score_x_ions': False, # -i 1,4
        'score_y_ions': True, # -i 1,4
        'score_z_ions': False, # -i 1,4
        'enzyme': 'trypsin_p', # -e 10
        'maximum_missed_cleavages': '1', # -v 1
        'precursor_max_charge': '8', # -zh 8
        'precursor_min_charge': '1', # -zl 1
        'tez': '1', # -tez 1
        'precursor_isotope_range': '0,1', # -ti 1
        'num_match_spec': '1', # -hc 1

        'database': target_decoy_database,
        'modifications': modifications,
    }

    # MS-GF+ parameters from Wen et al. (2015):
    msgf_params = {
        # precursor ion mass tolerance was set to 10 ppm
        'precursor_mass_tolerance_unit': 'ppm',
        # precursor ion mass tolerance was set to 10 ppm
        'precursor_mass_tolerance_minus': '10',
        # precursor ion mass tolerance was set to 10 ppm
        'precursor_mass_tolerance_plus': '10',
        # the max number of optional modifications per peptide were set as 3
        # (used by default) # number of allowed isotope errors was set as 1
        'enzyme': 'trypsin', # the enzyme was set as trypsin
        # (used by default) # fully enzymatic peptides were specified, i.e. no non-enzymatic termini
        'frag_method': '1',  # the fragmentation method selected in the search was CID
        'max_pep_length': '45',  # the maximum peptide length to consider was set as 45
        # the minimum precursor charge to consider if charges are not specified
        # in the spectrum file was set as 1
        'precursor_min_charge': '1',
        # the maximum precursor charge to consider was set as 8
        'precursor_max_charge': '8',
        # (used by default) # the parameter 'addFeatures' was set as 1 (required for Percolator)
        # all of the other parameters were set as default
        # the instrument selected
        # was High-res

        'database': target_decoy_database,
        'modifications': modifications,
    }

    # X!Tandem parameters from Wen et al. (2015):
    xtandem_params = {
        # precursor ion mass tolerance was set to 10 ppm
        'precursor_mass_tolerance_unit': 'ppm',
        # precursor ion mass tolerance was set to 10 ppm
        'precursor_mass_tolerance_minus': '10',
        # precursor ion mass tolerance was set to 10 ppm
        'precursor_mass_tolerance_plus': '10',
        # the fragment ion mass tolerance was set to 0.6 Da
        'frag_mass_tolerance': '0.6',
        # the fragment ion mass tolerance was set to 0.6 Da
        'frag_mass_tolerance_unit': 'da',
        # parent monoisotopic mass isotope error was set as 'yes'
        'precursor_isotope_range': '0,1',
        'precursor_max_charge': '8', # maximum parent charge of spectrum was set as 8
        'enzyme': 'trypsin',  # the enzyme was set as trypsin ([RK]|[X])
        # the maximum missed cleavage sites were set as 1
        'maximum_missed_cleavages': '1',
        # (used by default) # no model refinement was employed.

        'database': target_decoy_database,
        'modifications': modifications,
    }

    search_engine_settings = [
        # not used in Wen et al., so we use the same settings as xtandem
        ('msamanda_1_0_0_5243', xtandem_params, 'LTQ XL high res'),
        # not used in Wen et al., so we use the same settings as xtandem
        ('myrimatch_2_1_138', xtandem_params, 'LTQ XL high res'),
        # the instrument selected was High-res
        ('msgfplus_v9979', msgf_params, 'LTQ XL high res'),
        ('xtandem_jackhammer', xtandem_params, None),
        ('omssa_2_1_9', omssa_params, None),
    ]

    merged_validated_files_3_engines = []
    merged_validated_files_5_engines = []

    for engine, wen_params, instrument in search_engine_settings:

        # Initializing the uPLANIT UController class with
        # our specified modifications and mass spectrometer
        uc = ursgal.UController(
            params=wen_params
        )

        if instrument is not None:
            uc.set_profile(instrument)

        unified_results = []
        percolator_validated_results = []

        for mzML_file in mass_spec_files:
            unified_search_results = uc.search(
                input_file=mzML_file,
                engine=engine,
            )
            unified_results.append(
                unified_search_results
            )
            validated_csv = uc.validate(
                input_file=unified_search_results,
                engine='percolator_2_08',
            )
            percolator_validated_results.append(validated_csv)

        merged_validated_csv = uc.execute_misc_engine(
            input_file=percolator_validated_results,
            engine='merge_csvs_1_0_0'
        )
        merged_unvalidated_csv = uc.execute_misc_engine(
            input_file=unified_results,
            engine='merge_csvs_1_0_0',
        )

        if engine in ["omssa_2_1_9", "xtandem_jackhammer", "msgfplus_v9979"]:
            merged_validated_files_3_engines.append(merged_validated_csv)
        merged_validated_files_5_engines.append(merged_validated_csv)

    uc.params['prefix'] = '5-engines-summary'
    uc.combine_search_results(
        input_files=merged_validated_files_5_engines,
        engine='combine_FDR_0_1',
    )

    uc.params['prefix'] = '3-engines-summary'
    uc.combine_search_results(
        input_files=merged_validated_files_3_engines,
        engine='combine_FDR_0_1',
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)
    main(sys.argv[1])
