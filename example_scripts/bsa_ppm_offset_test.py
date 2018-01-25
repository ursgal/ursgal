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
    Example script to do a simple machine ppm offset parameter sweep.
    The m/z values in the example mgf file are stepwise changed and the in the
    final output the total peptides are counted.

    usage:
        ./bsa_ppm_offset_test.py

    Note:
        As expected, if the offset becomes to big no peptides can be found anymore.

    '''
    ppm_offsets = [
        (-10, '-10_ppm_offset'),
        (-9, '-9_ppm_offset'),
        (-8, '-8_ppm_offset'),
        (-7, '-7_ppm_offset'),
        (-6, '-6_ppm_offset'),
        (-5, '-5_ppm_offset'),
        (-4, '-4_ppm_offset'),
        (-3, '-3_ppm_offset'),
        (-2, '-2_ppm_offset'),
        (-1, '-1_ppm_offset'),
        (None, '0_ppm_offset'),
        (1, '1_ppm_offset'),
        (2, '2_ppm_offset'),
        (3, '3_ppm_offset'),
        (4, '4_ppm_offset'),
        (5, '5_ppm_offset'),
        (6, '6_ppm_offset'),
        (7, '7_ppm_offset'),
        (8, '8_ppm_offset'),
        (9, '9_ppm_offset'),
        (10, '10_ppm_offset'),
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
        'BSA_machine_ppm_offset_example',
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

    for engine in engine_list:
        for (ppm_offset, prefix) in ppm_offsets:

            R.params['machine_offset_in_ppm'] = ppm_offset
            R.params['prefix'] = prefix

            unified_search_result_file = R.search(
                input_file=mzML_file,
                engine=engine,
                force=False,
            )

    collector = ddict(set)
    for csv_path in glob.glob('{0}/*/*unified.csv'.format(os.path.dirname(mzML_file))):
        for line_dict in csv.DictReader(open(csv_path, 'r')):
            collector[csv_path].add(line_dict['Sequence'])
    for csv_path, peptide_set in sorted(collector.items()):
        file_name = os.path.basename(csv_path)
        offset = file_name.split('_')[0]
        print(
            'Search with {0: >3} ppm offset found {1: >2} peptides'.format(
                offset,
                len(peptide_set)
            )
        )

    return

if __name__ == '__main__':
    main()
