#!/usr/bin/env python3.4
META_INFO = {
    'engine_type'            : {
        'converter'         : True,
        'validation_engine' : False,
        'search_engine'     : False,
        'meta_engine'       : False
    },

    'output_extension'       : '.mgf',
    'output_suffix'          : None,
    'input_types'            : ['.mzml', '.mzml.gz'],

    'include_in_git'         : True,
    
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'mzml2mgf_1_0_0.py',
            },
        },
    },    


    # 'engine_exe':{
    #     'arc_independent':'mzml2mgf_1_0_0.py',
    # },
    # 'engine_url' : {
    #     'internal' : True,
    # },
}

DEFAULT_PARAMS = {
    'number_of_mz_decimals' : 5,
    'number_of_i_decimals'  : 5,
    # 'precursor_ppm_offset'  : None,
    # 'fragment_ppm_offset'   : None,
    'machine_offset_in_ppm'  : None,
    'scan_exclusion_list'   : None,
    'scan_skip_modulo_step' : None,
}

USED_USEARCH_PARAMS = [
    # used to be AVAILABLE PARAMS ..
    # Only these will be translated ...
    # Only those will trigger a re-run if changed!!
    'number_of_mz_decimals',
    'number_of_i_decimals',
    'machine_offset_in_ppm',
    'scan_exclusion_list',
    'scan_skip_modulo_step'
]

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
    # USED TO BE UBER_SPECIFIC_TRANSLATIONS
    # params['mega_flag'] of 5 is translated to 'monster peanut' for unode
    # because Gnome Chompski
    # Note: only USED_USEARCH_PARAMS are actually translated !!
    'mega_flag' : {
        1 : 'little peanut',
        2 : 'not bad',
        3 : 'big peanut',
        4 : 'mega peanut',
        5 : 'monster peanut',
    }
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    # USED TO BE UBER_UBER_VALUE_TRANSLATIONS
    # USearch value is not know to the node bu can be mapped 1 to 1
    'trypsin' : 'at least no human can read it in our code ...',
}
