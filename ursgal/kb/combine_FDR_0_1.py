META_INFO = {
    'engine_type'    : {
        'controller'        : False,
        'converter'         : False,
        'validation_engine' : False,
        'search_engine'     : False,
        'meta_engine'       : True,
    },
    'input_types'               : ['.csv'],
    'output_extension'          : '.csv',
    'create_own_folder'         : False,
    'citation' : 'An implementation of the "combined FDR Score" algorithm, '\
        'as described in: Jones AR, Siepen JA, Hubbard SJ, Paton NW (2009) '\
        'Improving sensitivity in proteome studies by analysis of false '\
        'discovery rates for multiple search engines.',
    'include_in_git'            : True,
    
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'combine_FDR_0_1.py',
            },
        },
    },    
    # 'engine_exe'                : {
    #     'arc_independent':'combine_FDR_0_1.py',
    # },
    # 'engine_url' : {
    #     'internal' : True,
    # },
}

REQUIREMENTS = {
    "percolator",
}

DEFAULT_PARAMS = {
    'apply_combined_FDR_cutoff' : False,
    'filter_decoys'             : False,
    'combined_FDR_cutoff'       : 0.01,
}
