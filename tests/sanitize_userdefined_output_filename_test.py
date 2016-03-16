#!/usr/bin/env python3
# encoding: utf-8
import ursgal
R = ursgal.UController()

TESTS = [
    {
        'input' : {
            'user_fname'   : 'my_file.svg',
            'engine'       : 'venndiagram_1_0_0',
        },
        'output' : 'my_file.svg'
    },

    {
        'input' : {
            'user_fname'   : 'my_file',
            'engine'       : 'venndiagram_1_0_0',
        },
        'output' : 'my_file.svg'
    },

    {
        'input' : {
            'user_fname'   : 'my_file.png',
            'engine'       : 'venndiagram_1_0_0',
        },
        'output' : 'my_file.png.svg'
    },

    {
        'input' : {
            'user_fname'   : 'my_file.png.gz',
            'engine'       : 'venndiagram_1_0_0',
        },
        'output' : 'my_file.png.gz.svg'
    },

    {
        'input' : {
            'user_fname'   : '/my_directory/my_file.png.gz',
            'engine'       : 'venndiagram_1_0_0',
        },
        'output' : 'my_file.png.gz.svg'
    },

    {
        'input' : {
            'user_fname'   : '/my_directory/my_file.png.gz',
            'engine'       : 'venndiagram_1_0_0',
        },
        'output' : 'my_file.png.gz.svg'
    },

    {
        'input' : {
            'user_fname'   : '/my_directory/my_file.svg',
            'engine'       : 'venndiagram_1_0_0',
        },
        'prefix' : 'xx',
        'output' : 'xx_my_file.svg'
    },

    {
        'input' : {
            'user_fname'   : '/my_directory/my_file.svg',
            'engine'       : 'venndiagram_1_0_0',
        },
        'prefix' : '',
        'output' : 'my_file.svg'
    },

    {
        'input' : {
            'user_fname'   : '/my_directory/my_file.svg',
            'engine'       : 'venndiagram_1_0_0',
        },
        'prefix' : None,
        'output' : 'my_file.svg'
    },
]


def sanitize_userdefined_output_filename_test():
    for test_id, test_dict in enumerate(TESTS):
        yield sanitize_userdefined_output_filename, test_dict


def sanitize_userdefined_output_filename( test_dict ):
    if 'prefix' in test_dict:
        R.params['prefix'] = test_dict['prefix']
    R.sanitize_userdefined_output_filename( **test_dict['input'] )
    out_put = R.sanitize_userdefined_output_filename(
        **test_dict['input']
    )
    print('Results', out_put , test_dict)
    assert out_put == test_dict['output'], '''
    sanitize_userdefined_output_filename {0} failed'''.format(
        test_dict
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        sanitize_userdefined_output_filename( test_dict )
