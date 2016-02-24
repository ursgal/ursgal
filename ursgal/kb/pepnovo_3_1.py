META_INFO = {
    # see http://proteomics.ucsd.edu/Software/UniNovo/#Downloads
    'engine_type' : {
        'denovo_engine' : True,
    },
    'engine' : {
        'linux' : {
            '64bit' : {
                'exe'            :'PepNovo_bin',
            }
        },
        'darwin' : {
           '64bit' : {
               'exe'             :'PepNovo_bin',
           }
        },
        'win32' : {
            '64bit' : {
                'exe'            : 'PepNovo.exe',
            }
        },
    },
    'input_types'               : ['.mgf'],
    'output_extension'          : '.csv',
    'create_own_folder'         : True,
    'citation'   : 'Ari M. Frank, Mikhail M. Savitski, Michael L. Nielsen, Roman A. Zubarev, and Pavel A. Pevzner (2007) De Novo Peptide Sequencing and Identification with Precision Mass Spectrometry, J. Proteome Res. 6:114-123.',
    'in_development' : False,
    'include_in_git'            : False,
}
DEFAULT_PARAMS = {
    'validation_score_field'  : 'Pepnovo:PnvScr',
    'pepnovo_model'           : 'CID_IT_TRYP',
    'pepnovo_model_dir'       : None,
    'pepnovo_tag_length'      : None,
    'output_cum_probs'        : True, 
    'output_aa_probs'         : True,  
    'prm'                     : False,
    'prm_norm'                : False,
    'correct_pm'              : False,
    'use_spectrum_charge'     : True,
    'use_spectrum_mz'         : True,
    'no_quality_filter'       : False,
    'min_filter_prob'         : 0.5,
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    'nonspecific'            : 'NON_SPECIFIC',
    'trypsin'                : 'TRYPSIN',
    '#Index'                 : 'Pepnovo:id',
    'RnkScr'                 : 'Pepnovo:RnkScr',
    'CumProb'                : 'Pepnovo:CumProb',
    'PnvScr'                 : 'Pepnovo:PnvScr',
    'N-Gap'                  : 'Pepnovo:N-Gap',
    'C-Gap'                  : 'Pepnovo:C-Gap',
    '[M+H]'                  : 'Calc mass(Da)', 
    'output_aa_probs'        : 'Pepnovo:aaScore'
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
    'num_match_spec',
    'modifications',
    'pepnovo_model',
    'pepnovo_model_dir',
    'base_mz',
    'pepnovo_tag_length',
    'output_cum_probs', 
    'output_aa_probs',  
    'prm',
    'prm_norm',
    'correct_pm',
    'use_spectrum_charge',
    'use_spectrum_mz',
    'no_quality_filter',
    'min_filter_prob',
    ]
     )

