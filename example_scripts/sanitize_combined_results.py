#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import sys
import os

def main(infile=None):
    '''
    Sanitize an Ursgal result file after combining results
    from multiple search engines (or single search engine results,
    with modified parameters)

    usage:
        ./sanitize_combined_results.py <Ursgal_result_file>

    '''
    mass_spectrometer = 'QExactive+'
    params = {
        'precursor_mass_tolerance_minus' : 10,
        'precursor_mass_tolerance_plus': 10,
        'frag_mass_tolerance' : 10,
        'frag_mass_tolerance_unit': 'ppm',
        '-xmx'     : '32g',
    }

    uc = ursgal.UController(
        profile = mass_spectrometer,
        params = params
    )

    # Parameters need to be adjusted based on the input file
    # and the desired type of sanitizing.
    # E.g. 'combined PEP' or 'Bayed PEP' can be used for combined PEP results,
    # while 'PEP' should be used for results from single engines.
    # A minimum difference between the top scoring, conflicting PSMs can be defined
    # using the parameters 'score_diff_threshold' and 'threshold_is_log10'
    uc.params.update({
        'validation_score_field': 'Bayes PEP',
        # 'validation_score_field': 'PEP',
        'bigger_scores_better': False,
        'num_compared_psms': 25,
        'accept_conflicting_psms': False,
        'threshold_is_log10': True,
        'score_diff_threshold': 0.0,
        'psm_defining_colnames': [
            'Spectrum Title',
            'Sequence',
        #     'Modifications',
        #     'Charge',
        #     'Is decoy',
        ],
        'max_num_psms_per_spec': 1,
        # 'preferred_engines': [],
        'preferred_engines': [
            'msfragger_2_3',
            'pipi_1_4_6',
            'moda_v1_61',
        ],
        'remove_redundant_psms': False,
    })

    sanitized_combined_results = uc.execute_misc_engine(
        input_file = infile,
        engine='sanitize_csv',
    )

if __name__ == '__main__':
    main(
        infile = sys.argv[1],
    )
