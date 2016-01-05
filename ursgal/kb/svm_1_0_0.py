META_INFO = {
    'in_development' : True,  # do not show in UNode overview
    'engine_type'            : {
        'controller'        : False,
        'converter'         : False,
        'validation_engine' : True,
        'search_engine'     : False,
        'meta_engine'       : False
    },
    'input_types'      : ['.csv'],
    'output_extension' : '.csv',
    'output_suffix'    : 'svm_validated',
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe' : 'svm.py',
            },
        },
    },
    'create_own_folder'         : False,
    'include_in_git'            : False,
}


DEFAULT_PARAMS = {
    'validation_score_field' : None,
    'validation_reverse_scores' : None,
    'kernel' : 'rbf',  # linear kernel yields good
        # results at all possible FDR cutoffs. rbf kernel seems to be better
        # at low FDR cutoffs (around 0.01), but linear is better when using
        # high cutoffs (i.e. 0.3)
    'c' : 1,  # penalty parameter C of the error term, one seems to be good
    'fdr_cutoff' : 0.01,  # 0.01 works well (for humanBR omssa/xtandem/msgfplus results at least...)
    'columns_as_features' : ','.join([
        'MS-GF:RawScore',
        'MS-GF:DeNovoScore',
        'MS-GF:SpecEValue',
        'MS-GF:EValue',
        'OMSSA:evalue',
        'OMSSA:pvalue',
        'X\!Tandem:expect',
        'X\!Tandem:hyperscore',
    ]),
    'available_RAM_in_MB' : 3000,
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {}
USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {}
USED_USEARCH_PARAMS = set([
    'validation_score_field',
    'validation_reverse_scores',
    'kernel',
    'c',
    'fdr_cutoff',
    'columns_as_features',
])