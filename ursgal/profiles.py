# Default params are listed in uparams.py and include e.g.:
#     'score_ion_list'                    : [b', 'y'],
#     'precursor_mass_tolerance_unit'     : 'ppm',
#     'precursor_mass_tolerance_minus'    : 5,
#     'precursor_mass_tolerance_plus'     : 5,
#     'frag_mass_tolerance_unit'          : 'ppm',
#     'frag_mass_tolerance'               : 20,


PROFILES = {
    'LTQ XL low res' : {
        # MS 1 orbitrap & MSn iontrap
        'frag_mass_tolerance'       : 0.5,
        'frag_mass_tolerance_unit'  : 'da',
        'instrument'                : 'low_res_ltq',
        'frag_method'               : 'cid'
    },

    'LTQ XL high res' : {
        # MS 1 & MSn orbitrap
        'score_ion_list'            : ['a', 'b', 'y'],
        'instrument'                : 'high_res_ltq',
    },

    'QExactive+' : {
        'score_ion_list'            : ['a', 'b', 'y', 'imm', 'int'],
        'instrument'                : 'q_exactive',
    },
}

# score ions for HCD spectra, according to 
# Michalski et al (2012): A systematic investigation into the nature of tryptic HCD spectra. J Proteome Res (11)
