META_INFO = {
    'engine_type' : {
        'search_engine' : False,
        'converter'     : True
    },
    'output_extension'  : '.csv',
    'output_suffix'     : None,
    'input_types'       : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'],
    # 'can_gz': True,
    'citation'       : 'Reisinger F, Krishna R, Ghali F, Ríos D, '\
        'Hermjakob H, Vizcaíno JA, Jones AR. (2012) jmzIdentML API: '\
        'A Java interface to the mzIdentML standard for peptide and '\
        'protein identification data.',
'in_development'            : True,
    'include_in_git'            : False,

    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'            : 'mzidentml-lib-1.6.10.jar',
                'url'            : '',
                'zip_md5'        : '61451563e924b13eebca24e903340da9',
                'additional_exe' : [],
            },
        },
    },

    # 'engine_exe':{
    #     'arc_independent':'mzidentml-lib-1.6.10.jar',
    # },
    # 'zip_md5'                   : {
    #         'arc_independent' : {
    #             'arc_independent' : '61451563e924b13eebca24e903340da9'
    #     }
    # },
}

DEFAULT_PARAMS = {
'mzidentml_outputFragmentation' : False,
'mzidentml_compress'            : False,
'mzidentml_exportType'          :'exportPSMs',
'mzidentml_verboseOutput'       : False,
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    False : 'false',
    True  : 'true',
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}

USED_USEARCH_PARAMS = set([
    'java_-Xmx',
    'decoy_tag',
    'mzidentml_outputFragmentation',
    'mzidentml_compress',
    'mzidentml_exportType',
    'mzidentml_verboseOutput',
    ])
