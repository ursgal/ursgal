META_INFO = {
    'engine_type' : {
        'fetcher' : True,
    },
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'get_ftp_files_1_0_0.py',
            },
        },
    },

    'input_types': '',
    'output_suffix':None,
'in_development'            : True,
    'include_in_git' : True,

    # 'in_development' : True
    # is available but not displayed :)
    # 'engine_exe' : {
    #     'arc_independent' : 'get_ftp_files_1_0_0.py',
    # },
    # 'engine_url' : {
    #     'internal' : True,
    # },
}


DEFAULT_PARAMS = {
    # 'ftp_url', # it will fail if this is not set by the user :)
    'ftp_folder'              : None,
    'ftp_login'               : None,
    'ftp_password'            : None,
    'ftp_include_ext'         : None,
    'ftp_output_folder'       : None,
    'ftp_max_number_of_files' : None,
    'ftp_blocksize'           : 1024,
}

USED_USEARCH_PARAMS = set([
    'ftp_url',
    'ftp_folder',
    'ftp_login',
    'ftp_password',
    'ftp_include_ext',
    'ftp_output_folder',
    'ftp_max_number_of_files',
    'ftp_blocksize',
])
