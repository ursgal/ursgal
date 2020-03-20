#!/usr/bin/env python
'''
Converts mzML to mgf

Usage:
./_mzml_2_mgf.py <mzML File1> ... <mzML FileN>

Note:
1) A new mgf file will be created at the same location as the mzML file
2) only ms2 are converted to mgf
'''
# 18.11.2014
# By C. Fufezan

from __future__ import print_function
import sys
import os
import argparse
import pymzml

try:
    version = pymzml.__version__
except AttributeError:
    version = '0.x.x'
if version.split('.')[0] != '2':
    raise RuntimeError(
        'Using mzml2mgf converter V2, however pymzML version {version} is installed\n'.format(version=version),
        'Please install pymzML version 0.x.x or set the mzml2mgf_converter_version param to mzml2mgf_1_0_0'
    )


def _determine_mzml_name_base(file_name, prefix):
    file_name = os.path.basename(file_name)
    if file_name.upper().endswith('.MZML.GZ'):
        mzml_name_base = file_name[:-8]
    elif file_name.upper().endswith('.MZML'):
        mzml_name_base = file_name[:-5]
    elif file_name.upper().endswith('.IDX.GZ'):
        mzml_name_base = file_name[:-7]
    else:
        raise Exception(
            "Can not determine mzml base name from {0}".format(
                file_name
            )
        )
    if prefix is not None and prefix is not '':
        mzml_name_base = '_'.join([prefix, mzml_name_base])
    return mzml_name_base


def main(
    mzml=None,
    mgf=None,
    i_decimals=5,
    mz_decimals=5,
    machine_offset_in_ppm=None,
    scan_exclusion_list=None,
    scan_inclusion_list=None,
    prefix=None,
    scan_skip_modulo_step=None,
    ms_level=2,
    precursor_min_charge=1,
    precursor_max_charge=5,
    ion_mode='+',
    spec_id_attribute=None,
):

    print(
        'Converting file:\n\tmzml : {0}\n\tto\n\tmgf : {1}'.format(
            mzml,
            mgf,
        )
    )
    mzml_name_base = _determine_mzml_name_base(mzml, prefix)
    # rt_lookup = mzml_name_base + '_rt_lookup.pkl'
    oof = open(mgf , 'w')
    run = pymzml.run.Reader(
        mzml
    )
    tmp = {
        'rt_2_scan' : {},
        'scan_2_rt' : {},
        'scan_2_mz': {}
    }
    mgf_entries = 0
    if scan_exclusion_list is None:
        scan_exclusion_list = []
    else:
        scan_exclusion_list = [int(spec_id) for spec_id in scan_exclusion_list]

    if machine_offset_in_ppm is not None:
        mz_correction_factor = machine_offset_in_ppm * 1e-6
    else:
        mz_correction_factor = 0
    precursor_charge_range = '{0}'.format(precursor_min_charge)
    for charge in range(precursor_min_charge + 1, precursor_max_charge + 1):
        precursor_charge_range += ' and {0}'.format(charge)
    mzml_basename = os.path.basename(mzml)
    for n, spec in enumerate(run):
        if n % 500 == 0:
            print(
                'File : {0:^40} : Processing spectrum {1}'.format(
                    mzml_basename,
                    n,
                ),
                end='\r'
            )

        spec_ms_level = spec.ms_level
        scan_time, scan_time_unit = spec.scan_time
        if scan_time_unit == 'seconds':
            scan_time /= 60
        elif scan_time_unit != 'minute':
            print('''
                [Warning] The retention time unit is not recognized or not specified.
                [Warning] It is assumed to be minutes and continues with that.
            ''')
        if spec_id_attribute is None:
            spectrum_id = spec.ID
        else:
            id_attribute, id_key = list(spec_id_attribute.items())[0]
            if id_attribute == 'ID':
                spectrum_id = spec.ID
            elif id_attribute == 'index':
                spectrum_id = spec.index+1
            elif id_attribute == 'id_dict':
                spectrum_id = spec.id_dict[id_key]
            else:
                print('''
                    [ERROR] Please specifiy an available spec_id_attribute for mzml2mgf.
                    [ERROR] Available: ID, id_dict, index
                ''')
        tmp['rt_2_scan'][scan_time] = spectrum_id
        tmp['scan_2_rt'][spectrum_id] = scan_time
        tmp['unit'] = 'minute'

        if spec_ms_level != ms_level:
            continue

        peaks_2_write = spec.peaks('centroided')

        precursor_mz = spec.selected_precursors[0]['mz']
        precursor_charge = spec.selected_precursors[0].get('charge', None)

        if scan_inclusion_list is not None:
            if int(spectrum_id) not in scan_inclusion_list:
                continue

        if int(spectrum_id) in scan_exclusion_list:
            continue
        mgf_entries += 1

        if scan_skip_modulo_step is not None:
            if mgf_entries % scan_skip_modulo_step != 0:
                continue

        print(
            'BEGIN IONS',
            file=oof
        )
        print(
            'TITLE={0}.{1}.{1}.{2}'.format(
                mzml_name_base,
                spectrum_id,
                precursor_charge,
            ),
            file=oof
        )
        print(
            'SCANS={0}'.format(
                spectrum_id
            ),
            file=oof
        )

        scan_time = float(scan_time) * 60
        print(
            'RTINSECONDS={0}'.format(
                round(
                    scan_time,
                    11
                )
            ),
            file=oof
        )

        precursor_mz += precursor_mz * mz_correction_factor
        tmp['scan_2_mz'][spectrum_id] = precursor_mz
        print(
            'PEPMASS={0}'.format(
                precursor_mz
            ),
            file=oof
        )
        if precursor_charge is not None:
            print(
                'CHARGE={0}{1}'.format(
                    precursor_charge,
                    ion_mode
                ),
                file=oof
            )
        else:
            print(
                'CHARGE={0}{1}'.format(
                    precursor_charge_range,
                    ion_mode
                ),
                file=oof
            )

        for mz, intensity in peaks_2_write:
            # if fragment_ppm_offset is not None:
            mz += mz * mz_correction_factor
            print(
                '{0:<10.{mzDecimals}f} {1:<10.{intensityDecimals}f}'.format(
                    mz,
                    intensity,
                    mzDecimals=mz_decimals,
                    intensityDecimals=i_decimals
                ),
                file=oof
            )

        print(
            'END IONS\n',
            file=oof
        )
    print('')
    print(
        'Wrote {0} mgf entries to file {1}'.format(
            mgf_entries,
            mgf
        )
    )

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

    if len(sys.argv) <= 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        tmp = main(**args.__dict__)
        # print(tmp.keys())
        # print(sorted( tmp['scan_2_rt'].keys() ))
