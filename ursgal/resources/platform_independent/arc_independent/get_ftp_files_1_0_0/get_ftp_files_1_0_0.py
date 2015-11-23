#!/usr/bin/env python3.4
# encoding: utf-8

'''

Retrieve data from ftp server

usage:
    get_ftp_files_1_0_0.py <ftp_address> <login> <password> <filter_entension>

'''

# import glob
import ftplib
from ftplib import FTP
import os
import tempfile


def main(
        ftp_url             = None,
        folder              = None,
        login               = None,
        password            = None,
        include_ext         = None,
        output_folder       = None,
        max_number_of_files = None,
        blocksize           = None
    ):
    # retrieve files via ftp
    assert ftp_url is not None, 'Require ftp_url not None to run ;)'

    print('Downloading files from {0}, this can take a while...'.format(
        ftp_url
    ))
    if include_ext is None:
        include_ext = set()
    # statinfo = os.stat( target_path )
    # 'size' : statinfo.st_size

    ftp = FTP(ftp_url.replace('ftp://', ''))
    ftp.login(
        user   = login,
        passwd = password,
    )
    if folder is not None:
        ftp.cwd( '/' + folder + '/' )
        # does not hurt, just to be sure ...

    if output_folder is None:
        output_folder = tempfile.gettempdir()

    def download_file(source, target, file_size ):
        print(
            'Downloading: {0} into {1} with file size of {2:1.1f} MB'.format(
                source,
                target,
                file_size / 1e6
            )
        )
        with open(target, 'wb') as io:
            ftp.retrbinary(
                'RETR ' + source,
                io.write,
                blocksize=1024
            )

        return

    def walk_deeper( folder = None, output_root = None):
        if folder is None:
            folder = ''

        for file_or_directory in ftp.nlst( folder ):
            # print( file_or_directory )
            try:
                ftp_size  = ftp.size(file_or_directory)
                is_file = True
                # this raises exeption ftplib.error_perm on peptideatlas.org
            except ftplib.error_perm:
                is_file = False
                walk_deeper(
                    file_or_directory,
                    output_root=output_root
                )
            if is_file:
                allowed_file = False
                for extension in include_ext:
                    if file_or_directory.upper().endswith(extension.upper()):
                        allowed_file = True
                        break

                # for extension in exclude_ext:
                #     if file_or_directory.upper().endswith(extension.upper()):
                #         allowed_file = False
                # this DOES not work ... :)

                if allowed_file:
                    dirname             = os.path.dirname(file_or_directory)
                    file_path_on_host   = os.path.join(
                        output_root,
                        file_or_directory
                    )
                    folder_path_on_host = os.path.join(output_root, dirname )
                    if os.path.exists(file_path_on_host):
                        if ftp_size != os.stat( file_path_on_host ).st_size:
                            print(
                                'Downloading again: {0} because download was incomplete!'.format(
                                    file_path_on_host
                                )
                            )
                            download_file(
                                file_or_directory,
                                file_path_on_host,
                                ftp_size
                            )
                        else:
                            print(
                                'File: {0} already downloaded!'.format(
                                    file_path_on_host
                                )
                            )
                    else:
                        if os.path.exists(folder_path_on_host) is False:
                            print(
                                'Created directory: {0}'.format(
                                    folder_path_on_host
                                )
                            )
                            os.makedirs( folder_path_on_host )

                        download_file(
                            file_or_directory,
                            file_path_on_host,
                            ftp_size
                        )

    walk_deeper( output_root = output_folder)

    # ftp shortcut for debugging if ftp.size() does not work!
    # for file_or_directory in ftp.nlst( folder ):
    #     allowed_file = False
    #     for extension in include_ext:
    #         if file_or_directory.upper().endswith(extension.upper()):
    #             allowed_file = True
    #             break
    #     dirname             = os.path.dirname(file_or_directory)
    #     file_path_on_host   = os.path.join(
    #         output_folder,
    #         os.path.basename(file_or_directory)
    #     )
    #     if allowed_file:
    #         download_file(
    #             file_or_directory,
    #             file_path_on_host,
    #             0
    #         )
    ftp.quit()
    # if total_download_volume > 0:
    #     print(
    #         'Downloaded {0} files with a total size of {1:1.2f} GB'.format(
    #             len(mzML_list),
    #             total_download_volume / 1e9
    #          )
    #     )

    return output_folder

if __name__ == '__main__':
    # main(
    #     ftp_url             = 'ftp.peptideatlas.org',
    #     login               = 'PASS00223',
    #     password            = 'KM7452j',
    #     include_ext         = ['.mzML', '.mzML.gz'],
    #     output_folder       = '/tmp',
    #     max_number_of_files = 1,
    #     blocksize           = None
    # )
    main(
        ftp_url               = 'ftp.pride.ebi.ac.uk',
        folder                = '/pride/data/archive/2013/08/PXD000278',
        include_ext           = ['.txt'],
        output_folder         = '/tmp',
        # max_number_of_files = 1,
        blocksize             = None
    )

