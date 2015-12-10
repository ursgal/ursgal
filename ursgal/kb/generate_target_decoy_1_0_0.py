META_INFO = {
    'engine_type' : {
        'search_engine' : False,
        'converter'     : True
    },
    'output_extension' : '.fasta',
    'output_suffix'    : 'target_decoy', 
    'input_types'      : [''],

    'include_in_git' : True,

    'engine': {
        'platform_independent' : {
            'arc_independent' : {
                'exe'     : 'generate_target_decoy_1_0_0.py',
            },
        },
    }, 

    # 'engine_exe'                : {
    #     'arc_independent' : 'generate_target_decoy_1_0_0.py',
    # },
    # 'engine_url' : {
    #     'internal' : True,
    # },

}

DEFAULT_PARAMS = {
    'decoy_generation_mode' : 'shuffle_peptide',
    'enzyme'                : 'trypsin'
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {}


USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
    'enzyme' : {
        'argc' :            ('R', 'C'),
        'aspn' :            ('D', 'N'),
        'chymotrypsin' :    ('FMWY', 'C'),
        'chymotrypsin_p' :  ('FMWY', 'C'),
        'clostripain' :     ('R', 'C'),
        'cnbr' :            ('M', 'C'),
        'elastase' :        ('AGILV', 'C'),
        'formicacid' :      ('D', 'C'),
        'gluc' :            ('DE', 'C'),
        'gluc_bicarb' :     ('E', 'C'),
        'iodosobenzoate' :  ('W', 'C'),
        'lysc' :            ('K', 'C'),
        'lysc_p' :          ('K', 'C'),
        'lysn' :            ('K', 'N'),
        'lysn_promisc' :    ('AKRS', 'N'),
        'pepsina' :         ('FL', 'C'),
        'protein_endopeptidase' : ('P', 'C'),
        'staph_protease' :  ('E', 'C'),
        'trypsin' :         ('KR', 'C'),
        'trypsin_p' :       ('KR', 'C'),
        'trypsin/cnbr' :    ('KRM', 'C'),
        'trypsin/gluc' :    ('DEKR', 'C'),
    }
}
USED_USEARCH_PARAMS = set([
    'enzyme',
    'decoy_generation_mode'
])
