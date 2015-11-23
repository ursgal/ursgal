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
    downloaded_zips = uc.download_resources(
        http_url_root = 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/'
    )
    print()
    if len(downloaded_zips) == 0:
        print('[ INFO ] No engines were downloaded, all should be available')
    else:
        print(
            '[ INFO ] Downloaded and installed {0} engine(s)'.format(
                len( downloaded_zips )
            )
        )
        for engine, zip_file in downloaded_zips:
            print(
                '[ INFO ] Engine: {0} has been installed from {1}'.format(
                    engine,
                    zip_file
                )
            )
    return


if __name__ == '__main__':
    main()
