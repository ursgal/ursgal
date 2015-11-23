META_INFO = {
    'engine_type' : {
        'fetcher' : True,
    },
    # 'engine_exe' : {
    #     'arc_independent' : 'get_http_files_1_0_0.py',
    # },
    # 'engine_url' : {
    #     'internal' : True,
    # },
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'get_http_files_1_0_0.py',
            },
        },
    },

    'input_types': '',

    'output_suffix':None,


    'include_in_git' : True,

    # 'in_development' : True
    # is available but not displayed :)
}


DEFAULT_PARAMS = {
    # 'http_url', # it will fail if this is not set by the user :)
    'http_output_folder' : None,
}
