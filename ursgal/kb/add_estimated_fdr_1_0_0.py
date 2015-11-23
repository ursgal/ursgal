META_INFO = {
    'engine_type' : {
        'converter'  : True
    },
    'input_types'      : ['.csv'],
    'output_extension' : '.csv',
    'output_suffix'    : 'withFDR',
    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'add_estimated_fdr_1_0_0.py',
            },
        },
    },
    'citation' : 'An implementation of the target/decoy FDR estimation '\
        'method described in: Lukas Käll, John D. Storey, Michael J. '\
        'MacCoss and William Stafford Noble (2007) Assigning significance '\
        'to peptides identified by tandem mass spectrometry using decoy '\
        'databases.',

    'include_in_git'            : True,

}

DEFAULT_PARAMS = {}

USEARCH_PARAM_VALUE_TRANSLATIONS = {}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {}

USED_USEARCH_PARAMS = set()
