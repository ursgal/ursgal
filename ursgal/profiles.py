PROFILES = {
    'LTQ XL low res' : {
        # MS 1 orbitrap & MSn iontrap
        'frag_mass_tolerance'       : 0.5,
        'frag_mass_tolerance_unit'  : 'da',
        'instrument'                : 'low_res_LTQ',
        'frag_method'               : 'cid'
    },

    'LTQ XL high res' : {
        # MS 1 & MSn orbitrap
        'score_a_ions'              : True,
        'instrument'                : 'high_res_LTQ',
    },

    'QExactive+' : {
        'score_a_ions'              : True,
        'score_ions'                : ['a', 'b', 'x', 'b-h2o'],
        'instrument'                : 'q_exactive',

    },
}
