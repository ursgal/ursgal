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
    #'citation' : 'Combines PEP scores from different search engines.',
    'include_in_git'            : True,
    
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'combine_pep_1_0_0.py',
            },
        },
    },    
}

DEFAULT_PARAMS = {
    'cPEP:pep_colname': 'PEP',
    'cPEP:window_size': 249,
}

# Changing these params will trigger re-run:
USED_USEARCH_PARAMS = set([
    'cPEP:pep_colname',
    'cPEP:window_size',
])