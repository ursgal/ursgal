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
        'score_imm_ions'            : True, # only MSAmanda
        'score_int_ions'            : True, # only MSAmanda
        'instrument'                : 'q_exactive',

    },
}

# score a ions for HCD spectra, according to 
# Michalski et al (2012): A systematic investigation into the nature of tryptic HCD spectra. J Proteome Res (11)
