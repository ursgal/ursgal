META_INFO = {
    'in_development' : True,  # do not show in UNode overview
    'engine_type' : {
        'converter'  : True
    },
    'input_types'      : ['.txt', '.csv', '.fasta', '.mzml'],
    'output_extension' : '.csv',
    'output_suffix'    : 'test_node',
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe' : 'test_node_exe.py',
            },
        },
    },
    'citation' : 'TEST/DEBUG: Internal Ursgal UNode for debugging and testing.',
    'include_in_git' : True,
}

DEFAULT_PARAMS = {
    'test_param1' : 'b',
    'test_param2' : 'three',
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    'one'   : 1,
    'two'   : 2,
    'three' : 3,
    'four'  : 4,
    'five'  : 5,
    'a'     : 'A',
    'b'     : 'B',
    'c'     : 'C',
    'd'     : 'D',
    'e'     : 'E',
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {}

USED_USEARCH_PARAMS = set([
    'test_param1',
    'test_param2',
])
