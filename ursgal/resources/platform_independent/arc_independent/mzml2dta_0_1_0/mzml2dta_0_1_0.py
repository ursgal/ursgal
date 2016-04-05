#!/usr/bin/env python
'''
Converts mzML to dta

Usage:
./mzml2dta_0_1_0.py <mzML File1> ... <mzML FileN>

Note:
1) A new dta file will be created at the same location as the mzML file
2) only ms2 are converted to dta
'''
# 05.04.2016
# By C. Fufezan

from __future__ import print_function
import sys
import os
import argparse
import pymzml

PROTON   = 1.00727646677


def convert_mz_2_mass( mz, charge ):
    '''
    NOTE:
        equal to charge * mz - ( charge * PROTON)
    '''
    return charge * ( mz - PROTON )


def _determine_mzml_name_base( file_name ):
    file_name = os.path.basename( file_name )
    if file_name.upper().endswith('.MZML.GZ'):
        mzml_name_base = file_name[:-8]
    elif file_name.upper().endswith('.MZML'):
        mzml_name_base = file_name[:-5]
    else:
        raise Exception("Can not determine mzml base name from {0}".format(
            file_name
        ))
    return mzml_name_base


def main( mzml = None, i_decimals = 5, mz_decimals = 5 ):
    print('Converting file:\n\tmzml : {0}\n\tto\n\tdta-files'.format(
        mzml,
    ))
    mzml_name_base = _determine_mzml_name_base( mzml )
    run = pymzml.run.Reader(
        mzml,
        extraAccessions=[ ('MS:1000016', ['value', 'unitName'] )],
        obo_version = '1.1.0'
    )
    dta_entries = 0
    for n, spec in enumerate(run):
        if n % 500 == 0:
            print(
                'File : {0:^40} : Processing spectrum {1}'.format(
                    os.path.basename( mzml ),
                    n,
                ),
                end = '\r'
            )
        if spec['ms level'] != 2:
            continue
        scan_time, unit = spec['scan time']
        spectrum_id = spec['id']
        file_name = '{0}.{1}.{1}.dta'.format(
            mzml_name_base,
            spectrum_id,
        )
        with open(file_name, 'w') as oof:
            print(
                '{mh} {charge}'.format(
                    mh = convert_mz_2_mass(
                        spec['precursors'][0]['mz'],
                        spec['precursors'][0]['charge']
                    ) + PROTON,
                    charge = spec['precursors'][0]['charge']
                ),
                file=oof
            )
            for mz, intensity in spec.centroidedPeaks:
                print(
                    '{0:<10.{mzDecimals}f} {1:<10.{intensityDecimals}f}'.format(
                        mz,
                        intensity,
                        mzDecimals = mz_decimals,
                        intensityDecimals = i_decimals
                    ),
                    file = oof
                )
            print('\n', file = oof )
    print('')
    print('Wrote {0} dta entries'.format( dta_entries))
    return

if __name__ == '__main__':
    # parsing command line arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mzml',
        help='mzml input file')
    parser.add_argument(
        '-m', '--mz_decimals', default=5,
        help='Number of decimals for mz values', type=int)
    parser.add_argument(
        '-i', '--i_decimals', default=5,
        help='Number of decimals for intensity values', type=int)

    if len( sys.argv ) <= 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        tmp = main( **args.__dict__ )
