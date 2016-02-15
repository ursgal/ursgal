META_INFO = {
    'name': 'X!Tandem',
    'version' : 'Vengeance',
    'engine_type' : {
        'search_engine' : True,
    },
    'output_extension'          : '.xml',
    'input_types'               : ['.mgf'],
    'create_own_folder'         : True,
    'citation'                  : 'Craig R, Beavis RC. (2004) TANDEM: '\
        'matching proteins with tandem mass spectra.',
    'include_in_git'            : False,

    'engine': {
        'darwin' : {
            '64bit' : {
                'exe'            : 'tandem',
                'url'            : '',
                # 'zip_md5'        : '261dce3746481d1cc4223bccb6bf265e',
                'additional_exe' : [],
            },
        },
        'linux' : {
            '64bit' : {
                'exe'            : 'tandem.exe',
                'url'            : '',
                # 'zip_md5'        : 'af307fea9f2b954f1a9a3652c14a5742',
                'additional_exe' : [],
            },
        },
        'win32' : {
            '64bit' : {
                'exe'            : 'tandem.exe',
                'url'            : '',
                # 'zip_md5'        : '16c3b766e02690386f280515175cdc90',
                'additional_exe' : [],
            },
        },
    },
}

DEFAULT_PARAMS = {
    'validation_score_field'    : 'X\!Tandem:hyperscore',
    'evalue_field'              : 'X\!Tandem:expect',
    'validation_minimum_score'  : 0,
    'bigger_scores_better'      : True,
    'max_mod_alternatives'      : 6.0,
    'search_for_saps'           : False, # if set to 'True', this will (most likely) cause problems for unify_csv
    'forbidden_cterm_mods'      : [],
    'max_num_per_mod'           : {}
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    True: 'yes',
    False: 'no',
    'da': 'Daltons',
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
    'precursor_isotope_range'   : {
        '0'     : 'no',
        '0,1'   : 'yes',
        '0,1,2' : 'yes'
    },
    'enzyme' : {
        # NOTE: '{' & '}' are used by pythons format function, thus
        # they have to be escaped, i.e. {P} -> {{P}}!
        'argc' : '[R]|{P}',
        'aspn' : '[X]|[D]',
        'chymotrypsin' : '[FMWY]|{P}',
        'chymotrypsin_p' : '[FMWY]|[X]',
        'clostripain' : '[R]|[X]',
        'cnbr' : '[M]|{P}',
        'elastase' : '[AGILV]|{P}',
        'formic_acid' : '[D]|{P}',
        'gluc' : '[DE]|{P}',
        'gluc_bicarb' : '[E]|{P}',
        'iodosobenzoate' : '[W]|[X]',
        'lysc' : '[K]|{P}',
        'lysc_p' : '[K]|[X]',
        'lysn' : '[X]|[K]',
        'lysn_promisc' : '[X]|[AKRS]',
        'nonspecific' : '[X]|[X]',
        'pepsina' : '[FL]|[X]',
        'protein_endopeptidase' : '[P]|[X]',
        'staph_protease' : '[E]|[X]',
        'tca' : '[FMWY]|{P},[KR]|{P},[X]|[D]',
        'trypsin' : '[KR]|{P}',
        'trypsin_p' : '[RK]|[X]',
        'trypsin_cnbr' : '[KR]|{P},[M]|{P}',
        'trypsin_gluc' : '[DEKR]|{P}',
    }
}
USED_USEARCH_PARAMS = set([
    # 'minimal_required_assigned_peaks',
    # 'saps',
    # 'search_c_terminal_ions',
    # 'search_first_b1_ion',
    'modifications',
    'batch_size',
    'cleavage_cterm_mass_change',
    'cleavage_nterm_mass_change',
    'compensate_small_fasta',
    'cpus',
    'enzyme',
    'forbidden_cterm_mods',
    'frag_mass_tolerance',
    'frag_mass_tolerance_unit',
    'frag_mass_type',
    'frag_method',
    'frag_min_mz',
    # 'input_file',
    'input_file_type',
    #'instrument',
    'label',
    'max_num_per_mod',
    'maximal_accounted_observed_peaks',
    'maximum_missed_cleavages',
    'mininimal_required_matched_peaks',
    'mininimal_required_observed_peaks',
    'neutral_loss_enabled',
    'neutral_loss_mass',
    'neutral_loss_window',
    'num_match_spec',
    'precursor_isotope_range',
    'precursor_mass_tolerance_minus',
    'precursor_mass_tolerance_plus',
    'precursor_mass_tolerance_unit',
    'precursor_mass_type',
    'precursor_max_charge',
    'precursor_min_charge',
    'precursor_min_mass',
    'score_a_ions',
    'score_b_ions',
    'score_c_ions',
    'score_x_ions',
    'score_y_ions',
    'score_z_ions',
    'search_for_saps',
    'semi_enzyme',
    'spec_dynamic_range',
    'stp_bias',
    'use_refine'
])
