META_INFO = {
    'in_development'    : False,
    'engine_type' : {
        'search_engine' : False,
        'converter'     : True
    },
    'output_extension'  : '.csv',
    'output_suffix'     : None,
    'input_types'       : ['.xml', '.csv', '.mzid'],
    # 'can_gz': True,
    'citation'       : 'Reisinger F, Krishna R, Ghali F, Ríos D, '\
        'Hermjakob H, Vizcaíno JA, Jones AR. (2012) jmzIdentML API: '\
        'A Java interface to the mzIdentML standard for peptide and '\
        'protein identification data.',

    'include_in_git'            : False,
    
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'            : 'mzidentml-lib-1.6.11.jar',
                'url'            : '',
                'zip_md5'        : '77757dc40d2eca87c49899a27c3f14a0',
                'additional_exe' : [],
            },
        },
    },
    

    # 'engine_exe':{
    #     'arc_independent':'mzidentml-lib-1.6.11.jar',
    # },
    # 'zip_md5' : {
    #     'arc_independent' : {
    #         'arc_independent' : '77757dc40d2eca87c49899a27c3f14a0'
    #     }
    # }

}

DEFAULT_PARAMS = {
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
}


USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}
USED_USEARCH_PARAMS = set()
