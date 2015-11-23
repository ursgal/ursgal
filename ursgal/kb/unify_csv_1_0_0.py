META_INFO = {
    'engine_type' : {
        'search_engine' : False,
        'converter'     : True
    },
    'output_extension'  : '.csv',
    'output_suffix'     : 'unified',
    'input_types'       : ['.csv'],
    'include_in_git' : True,

    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe' : 'unify_csv_1_0_0.py',
            },
        },
    },

}

DEFAULT_PARAMS = {
    'aa_exception_dict': {
        'U' : {
            'unimod_name' : 'Delta:S(-1)Se(1)',
            'original_aa' : 'C',
            'unimod_name_with_cam': 'SecCarbamidomethyl',
        },
        'J' : {
            # 'unimod_name' : 'Delta:S(-1)Se(1)',
            'original_aa' : 'L', #is always leucin
            # 'unimod_name_with_cam': 'SecCarbamidomethyl',
        }
    },
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
}


USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}
USED_USEARCH_PARAMS = set()
