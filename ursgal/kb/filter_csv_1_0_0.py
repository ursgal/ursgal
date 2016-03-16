META_INFO = {
    'engine_type' : {
        'converter'     : True
    },
    'output_extension' : '.csv',
    'output_suffix'    : 'accepted',
    'input_types'      : ['.csv'],

    'rejected_output_suffix': 'rejected',

    'include_in_git'            : True,
    
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'filter_csv_1_0_0.py',
            },
        },
    }, 
}

DEFAULT_PARAMS = {
    'write_unfiltered_results' : False,
    'csv_filter_rules'         : None,

}

USEARCH_PARAM_VALUE_TRANSLATIONS = {}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {}

USED_USEARCH_PARAMS = set([
    'write_unfiltered_results',
    'csv_filter_rules'
])
