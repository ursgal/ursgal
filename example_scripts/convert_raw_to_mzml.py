#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys
import glob


def main(input_path=None):
    '''
    Convert a .raw file to .mzML using the ThermoRawFileParser.
    The given argument can be either a single file or a folder 
    containing raw files.

    Usage:
        ./convert_raw_to_mzml.py <raw_file/raw_file_folder>
    '''
    R = ursgal.UController()

    # Check if single file or folder.
    # Collect raw files if folder is given
    input_file_list = []
    if input_path.lower().endswith('.raw'):
        input_file_list.append(input_path)
    else:
        for raw in glob.glob(os.path.join('{0}'.format(input_path), '*.raw')):
            input_file_list.append(raw)

    # Convert raw file(s)
    for raw_file in input_file_list:
        mzml_file = R.convert(
            input_file=raw_file,
            engine='thermo_raw_file_parser_1_1_2',
        )

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(main.__doc__)
    main(input_path=sys.argv[1])
