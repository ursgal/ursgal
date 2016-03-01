META_INFO = {
    # see http://proteomics.ucsd.edu/Software/UniNovo/#Downloads
    'engine_type' : {
        'denovo_engine' : True,
    },
    'citation'                  : 'Jeong K, Kim S, Pevzner PA (2013): UniNovo: a universal tool for de novo peptide sequencing.',
    'in_development'            : True,

    'include_in_git'            : None,
'in_development'            : True,
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'            : 'UniNovo.jar',
                'url'            : 'http://proteomics.ucsd.edu/Software/UniNovo/UniNovo.20130520.zip',
                # 'zip_md5'        : '',
                # 'additional_exe' : [],
            },
        },
    },

    'output_extension'          : '.den',
    'input_types'               : ['.mgf'],
    'create_own_folder'         : True,
}
DEFAULT_PARAMS = {
    'uninovo_num_13C'      : 0,
    'uninovo_accuracy'     : 0.8,
    'uninovo_num_mass_gaps': 10,
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    'nonspecific'            : 0,
    'trypsin'                : 1,
    'lys_c'                  : 2,
    'etd'                    : 'ETD',
    'cid'                    : 'CID',
    'hcd'                    : 'HCD',
    'da'                     : 'Da',
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}

USED_USEARCH_PARAMS = set( [
    'enzyme',
    'precursor_mass_tolerance_unit',
    'precursor_mass_tolerance_minus',
    'precursor_mass_tolerance_plus',
    'frag_mass_tolerance',
    'frag_mass_tolerance_unit',
    'frag_method',
    'min_pep_length',
    'num_match_spec',
    ]
     )

