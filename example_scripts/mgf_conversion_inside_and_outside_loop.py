#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import shutil


def main():
    '''
    '''
    R = ursgal.UController(
        profile='LTQ XL low res',
        params={
            'database': os.path.join(os.pardir, 'example_data', 'BSA.fasta'),
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl'    # N-Acteylation[]
            ]
        },
    )

    engine = 'omssa'
    output_files = []

    mzML_file = os.path.join(
        os.pardir,
        'example_data',
        'mgf_conversion_example',
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

    # First method: Convert to MGF outside of the loop:
    # (saves some time cause the MGF conversion is not always re-run)
    mgf_file = R.convert(
        input_file=mzML_file,  # from OpenMS example files
        engine='mzml2mgf_1_0_0'
    )
    for prefix in ['10ppm', '20ppm']:
        R.params['prefix'] = prefix

        output_file = R.search(
            input_file=mgf_file,
            engine=engine,
            # output_file_name = 'some_userdefined_name'
        )

    # Second method: Automatically convert to MGF inside the loop:
    # (MGF conversion is re-run every time because the prexix changed!)
    for prefix in ['5ppm', '15ppm']:
        R.params['prefix'] = prefix

        output_file = R.search(
            input_file=mzML_file,  # from OpenMS example files
            engine=engine,
            # output_file_name = 'another_fname',
        )
        output_files.append(output_file)

    print('\tOutput files:')
    for f in output_files:
        print(f)

if __name__ == '__main__':
    print(__doc__)
    main()
