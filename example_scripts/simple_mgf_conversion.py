#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import shutil


def main():
    '''
    Simple example script to demonstrate conversion for mzML to mgf file
    conversion

    '''
    uc = ursgal.UController(
        profile = 'LTQ XL low res',
        params  = {},
    )

    mzML_file = os.path.join(
        os.pardir,
        'example_data',
        'simple_mzml_to_mgf_conversion',
        'BSA1.mzML'
    )
    if os.path.exists(mzML_file) is False:
        uc.params['http_url'] = 'http://sourceforge.net/p/open-ms/code/HEAD/tree/OpenMS/share/OpenMS/examples/BSA/BSA1.mzML?format=raw'
        uc.params['http_output_folder'] = os.path.dirname(mzML_file)
        uc.fetch_file(
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

    mgf_file = uc.convert(
        input_file = mzML_file,  # from OpenMS example files
        engine     = 'mzml2mgf_1_0_0'
    )

if __name__ == '__main__':
    print(__doc__)
    main()
