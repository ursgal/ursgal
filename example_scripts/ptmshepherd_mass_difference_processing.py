#!/usr/bin/env python3
import os
import ursgal
import sys
import glob
from collections import defaultdict as ddict
import csv


def main(folder=None, sanitized_search_results=None):
    '''
    Downstream processing of mass differences from open modification search results
    using PTM-Shepherd.
    A folder containing all relevant mzML files and a sanitized (one PSM per spectrum)
    Ursgal result file (containing open modification search results) are required.

    usage:
        ./ptmshepherd_mass_difference_processing.py <folder_with_mzML> <sanitized_result_file>

    '''
    mzml_files = []
    for mzml in glob.glob(os.path.join(folder, "*.mzML")):
        mzml_files.append(mzml)

    params = {
        "use_pyqms_for_mz_calculation": True,
        "cpus": 8,
        "precursor_mass_tolerance_unit": "ppm",
        "precursor_mass_tolerance_plus": 5,
        "precursor_mass_tolerance_minus": 5,
        "frag_mass_tolerance_unit": "ppm",
        "frag_mass_tolerance": 20,
        "modifications": [
            "C,opt,any,Carbamidomethyl",
        ],
        "-xmx": '12G',
        'psm_defining_colnames': [
            'Spectrum Title',
            'Sequence',
            # 'Modifications',
            # 'Mass Difference',
            # 'Charge',
            # 'Is decoy',
        ],
        'mzml_input_files' : mzml_files,
        'validation_score_field': 'combined PEP',
        'bigger_scores_better': False,
    }

    uc = ursgal.UController(params=params, profile="QExactive+", verbose=False)

    ptmshepherd_results = uc.validate(
        input_file=sanitized_search_results,
        engine='ptmshepherd_0_3_5',
        # force=True,
    )

if __name__ == '__main__':
    main(
        folder=sys.argv[1],
        sanitized_search_results=sys.argv[2],
    )