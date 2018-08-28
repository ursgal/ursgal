#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import glob
import csv
from collections import defaultdict as ddict
import os
import shutil


def main():
    '''
    Example script to do a precursor mass tolerance parameter sweep.

    usage:
        ./bsa_precursor_mass_tolerance_example.py


    '''
    precursor_mass_tolerance_list = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
    ]

    engine_list = [
        'xtandem_vengeance'
    ]

    R = ursgal.UController(
        profile='LTQ XL low res',
        params={
            'database': os.path.join(
                os.pardir,
                'example_data',
                'BSA.fasta'
            ),
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
            ],
        }
    )

    mzML_file = os.path.join(
        os.pardir,
        'example_data',
        'BSA_precursor_mass_tolerance_example',
        'BSA1.mzML'
    )
    if os.path.exists(mzML_file) is False:

        R.params['http_url'] = 'http://sourceforge.net/p/open-ms/code/HEAD/tree/OpenMS/share/OpenMS/examples/BSA/BSA1.mzML?format=raw'

        R.params['http_output_folder'] = os.path.dirname(mzML_file)
        R.fetch_file(
            engine='get_http_files_1_0_0'
        )
        try:
            shutil.move(
                '{0}?format=raw'.format(mzML_file),
                mzML_file
            )
        except:
            shutil.move(
                '{0}format=raw'.format(mzML_file),
                mzML_file
            )
    # Convert mzML to MGF outside the loop, so this step is not repeated in
    # the loop
    mgf_file = R.convert(
        input_file=mzML_file,
        engine='mzml2mgf_1_0_0'
    )

    for engine in engine_list:
        for precursor_mass_tolerance in precursor_mass_tolerance_list:

            R.params['precursor_mass_tolerance_minus'] = precursor_mass_tolerance
            R.params['precursor_mass_tolerance_plus'] = precursor_mass_tolerance

            R.params['prefix'] = '{0}_precursor_mass_tolerance_'.format(
                precursor_mass_tolerance
            )

            unified_search_result_file = R.search(
                input_file=mgf_file,
                engine=engine,
                force=False,
            )

    collector = ddict(set)
    for csv_path in glob.glob('{0}/*/*unified.csv'.format(os.path.dirname(mzML_file))):
        for line_dict in csv.DictReader(open(csv_path, 'r')):
            collector[csv_path].add(line_dict['Sequence'])
    for csv_path, peptide_set in sorted(collector.items()):
        file_name = os.path.basename(csv_path)
        tolerance = file_name.split('_')[0]
        print(
            'Search with {0: >2} ppm precursor mass tolerance found {1: >2} peptides'.format(
                tolerance,
                len(peptide_set)
            )
        )

    return

if __name__ == '__main__':
    main()
