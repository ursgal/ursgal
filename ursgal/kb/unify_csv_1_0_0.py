META_INFO = {
    'engine_type' : {
        'search_engine' : False,
        'converter'     : True
    },
    'output_extension'  : '.csv',
    'output_suffix'     : 'unified',
    'input_types'       : ['.csv'],
    'include_in_git' : True,
'in_development'            : True,
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
    'argc' :            ('R', 'C'),
    'aspn' :            ('D', 'N'),
    'chymotrypsin' :    ('FMWY', 'C'),
    'chymotrypsin_p' :  ('FMWY', 'C'),
    'clostripain' :     ('R', 'C'),
    'cnbr' :            ('M', 'C'),
    'elastase' :        ('AGILV', 'C'),
    'formic_acid' :     ('D', 'C'),
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
    'trypsin_cnbr' :    ('KRM', 'C'),
    'trypsin_gluc' :    ('DEKR', 'C'),
    'nonspecific' :     ('ACDEFGHIKLMNPQRSTVWY', 'C'),
}


USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}
USED_USEARCH_PARAMS = set([
    'enzyme',
    ])
