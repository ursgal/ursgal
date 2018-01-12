#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os


def main():
    '''
    Downloads an example file from peptideatlas.org

    usage:
        ./get_file_from_ftp_server_example.py


    This is an simple example which shows how to load data from a ftp server.


    '''
    params = {
        'ftp_url': 'ftp.peptideatlas.org',
        'ftp_login': 'PASS00269',
        'ftp_password': 'FI4645a',
        'ftp_include_ext': [
            'JB_FASP_pH8_2-3_28122012.mzML',
        ],
        'ftp_output_folder': os.path.join(
            os.pardir,
            'example_data',
            'get_file_from_ftp_server_example'
        ),
    }
    if os.path.exists(params['ftp_output_folder']) is False:
        print(
            'Ceated folder: {0}'.format(
                params['ftp_output_folder']
            )
        )
        os.mkdir(params['ftp_output_folder'])
    R = ursgal.UController(
        params=params
    )
    R.fetch_file(
        engine='get_ftp_files_1_0_0'
    )
    return

if __name__ == '__main__':
    main()
