#!/usr/bin/env python3.4
# encoding: utf-8

import ursgal
import os
import sys
import pprint

def main():
    '''
    Download all resources from our webpage

    '''
    uc = ursgal.UController()
    zip_files_list, update_kb_list =uc.prepare_resources(
        root_zip_target_folder='/tmp'
    )
    print()
    print('<<<Summary>>>')
    if len(zip_files_list) == 0:
        print('[ INFO ] All files are correct stored in online repository')
    else:
        for zip_file, md5 in zip_files_list:
            print(
                '[ INFO ] File: {0} was created with md5: {1}'.format(
                    zip_file,
                    md5
                )
            )
            print()
    print()
    if len(update_kb_list) == 0:
        print('[ INFO ] No kb information has to be updated')
    else:
        for engine, message in update_kb_list:
            print(
                '[ INFO ] Please update kb for {0}'.format(
                    engine,
                )
            )
            print(message)
            print()

    return


if __name__ == '__main__':
    main()
