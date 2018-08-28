#!/usr/bin/env python3.4
# encoding: utf-8

'''

Retrieve data via http protocol

usage:
    get_http_files_1_0_0.py <http_url>

'''

# import glob
from urllib import request as request
import os
import tempfile
import urllib
import string


def format_filename(s):
    """
    Take a string and return a valid filename constructed from the string.
    Any characters not present in valid_chars are removed.
    """
    valid_chars = "-_.()=# " + string.ascii_letters + string.digits
    filename = ''.join(char for char in s if char in valid_chars)
    return filename


def main( http_url = None, http_output_folder = None):
    # retrieve files via http
    assert http_url is not None, '[ -<HTPP>- ] Require http_url not None to run ;)'

    print(
        '[ -<HTPP>- ] Downloading files from {0} ...'.format(
            http_url
        )
    )

    basename = format_filename(os.path.basename(http_url))

    if http_output_folder is None:
        http_output_folder = tempfile.gettempdir()
    else:
        if os.path.exists( http_output_folder ) is False:
            os.makedirs( http_output_folder )

    output_path = os.path.join( http_output_folder, basename )

    try:
        with open( output_path, 'wb') as ooo:
            local_filename, headers = request.urlretrieve(
                http_url,
                filename = output_path
            )
        print('[ -<HTPP>- ] Saved file as {0}'.format(
            output_path,
        ))
    except urllib.error.URLError:
        print( 
            '[ -<HTPP>- ] \t WARNING! Could not download {0} Check your internet connection!'.format(
                http_url
            ),
            '[ -<HTPP>- ] For OSX, make sure that certificates are installed (Applications/Python 3.x/Install Certificates.command)'
        )
        os.remove( output_path )
    return output_path


if __name__ == '__main__':
    main(
        http_url = 'http://www.tagesschau.de/multimedia/bilder/beckenbauer-113~_v-modPremium.jpg',
        http_output_folder = '.'
    )
