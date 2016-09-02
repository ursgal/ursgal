#!/usr/bin/env python3.4
'''
Converts mzML to mgf

Usage:
./_mzml_2_mgf.py <mzML File1> ... <mzML FileN>

Note:
1) A new mgf file will be created at the same location as the mzML file
2) only ms2 are converted to mgf
3) on /media/plan-f/mzML/ there is a local linked pymzML folder !
4) this
'''
# 18.11.2014
# By C. Fufezan

from __future__ import print_function
import sys
import os
import argparse
import pymzml



def _determine_mzml_name_base( file_name, prefix ):
    file_name = os.path.basename( file_name )
    if file_name.upper().endswith('.MZML.GZ'):
        mzml_name_base = file_name[:-8]
    elif file_name.upper().endswith('.MZML'):
        mzml_name_base = file_name[:-5]
    else:
        raise Exception("Can not determine mzml base name from {0}".format( file_name))
    if prefix is not None and prefix is not '':
        mzml_name_base = '_'.join( [prefix, mzml_name_base] )
    return mzml_name_base


def main(
        mzml                  = None,
        mgf                   = None,
        i_decimals            = 5,
        mz_decimals           = 5,
        machine_offset_in_ppm = None,
        scan_exclusion_list   = None,
        scan_inclusion_list   = None,
        prefix                = None,
        scan_skip_modulo_step = None
    ):

    print('Converting file:\n\tmzml : {0}\n\tto\n\tmgf : {1}'.format(
        mzml,
        mgf,
    ))
    mzml_name_base = _determine_mzml_name_base( mzml, prefix )
    # rt_lookup = mzml_name_base + '_rt_lookup.pkl'
    oof = open( mgf , 'w' )
    run = pymzml.run.Reader(
        mzml,
        extraAccessions=[ ('MS:1000016', ['value', 'unitName'] )],
        obo_version = '1.1.0'
    )
    tmp = {
        'rt_2_scan' : {},
        'scan_2_rt' : {},
    }
    mgf_entries = 0
    if scan_exclusion_list is None:
        scan_exclusion_list = []
    else:
        scan_exclusion_list = [ int(spec_id) for spec_id in scan_exclusion_list ]

    if machine_offset_in_ppm is not None:
        mz_correction_factor = machine_offset_in_ppm
    else:
        mz_correction_factor = 0

    for n, spec in enumerate(run):
        if n % 500 == 0:
            print(
                'File : {0:^40} : Processing spectrum {1}'.format(
                    os.path.basename( mzml ),
                    n,
                ),
                end = '\r'
            )

        # if n >= 1000:
        #     break
        if spec['ms level'] != 2:
            continue
        scan_time, unit = spec['scan time']
        spectrum_id = spec['id']
        if scan_inclusion_list != None:
            if int(spectrum_id) not in scan_inclusion_list:
                continue

        if int(spectrum_id) in scan_exclusion_list:
            continue
        mgf_entries += 1

        if scan_skip_modulo_step is not None:
            if mgf_entries % scan_skip_modulo_step != 0:
                continue


        tmp['rt_2_scan'][ scan_time ] = '{id}'.format(**spec)
        tmp['scan_2_rt'][ '{id}'.format(**spec) ] = scan_time
        tmp['unit'] = unit

        print('BEGIN IONS', file=oof)
        print(
            'TITLE={0}.{1}.{1}.{2}'.format(
                mzml_name_base,
                spec['id'],
                spec['precursors'][0]['charge'],
            ),
            file = oof
        )
        print('SCANS={id}'.format(**spec), file=oof)

        scan_time, unit = spec['scan time']
        if unit == 'second':
            scan_time = float(scan_time)
        else:
            scan_time = float(scan_time) * 60
        print(
            'RTINSECONDS={0}'.format(
                scan_time
            ),
            file = oof
        )
        precursor_mz = spec['precursors'][0]['mz']

        precursor_mz += precursor_mz * mz_correction_factor
        print(
            'PEPMASS={0}'.format(
                precursor_mz
            ),
            file = oof
        )
        if spec['precursors'][0]['charge'] is not None:
            print(
                'CHARGE={0}'.format(
                    spec['precursors'][0]['charge']
                ),
                file=oof
            )

        for mz, intensity in spec.centroidedPeaks:
            # if fragment_ppm_offset is not None:
            mz += mz * mz_correction_factor
            print(
                '{0:<10.{mzDecimals}f} {1:<10.{intensityDecimals}f}'.format(
                    mz,
                    intensity,
                    mzDecimals = mz_decimals,
                    intensityDecimals = i_decimals
                ),
                file = oof
            )

        print('END IONS\n', file = oof )
    print('')
    print('Wrote {0} mgf entries'.format( mgf_entries))
    oof.close()
    return tmp


if __name__ == '__main__':
    # parsing command line arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mzml',
        help='mzml input file')
    parser.add_argument(
        'mgf',
        help='mzml output file')
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
        # print(tmp.keys())
        # print(sorted( tmp['scan_2_rt'].keys() ))
