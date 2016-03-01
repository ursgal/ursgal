META_INFO = {
    'engine_type' : {
        'denovo_engine' : True,
    },
    'engine' : {
        'linux' : {
            '64bit' : {
                'exe'            :'novor.sh',
            }
        },
        'darwin' : {
            '64bit' : {
                'exe'            :'novor.sh',
            }
        },
        'win32' : {
            '64bit' : {
                'exe'            : 'novor.bat',
            }
        },
    },
    'in_development'            : True,
    'output_extension'          : '.csv',
    'input_types'               : ['.mgf'],
    'create_own_folder'         : True,
    'citation'                  : \
        'Bin Ma (2015) Novor: Real-Time Peptide de Novo Sequencing Software.',
    'include_in_git'            : False,
}

DEFAULT_PARAMS = {
    'novor_forbidden_residues'    : 'I,U',
    'validation_score_field'      : 'Novor:score',

}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    'trypsin'                : 'Trypsin',
    'cid'                    : 'CID',
    'hcd'                    : 'HCD',
    'da'                     : 'Da',
    'low_res_LTQ'            : 'Trap',
    'high_res_LTQ'           : 'Trap',
    'tof'                    : 'TOF',
    'q_exactive'             : 'FT',

    ' scanNum'               : 'Spectrum ID',
    ' peptide'               : 'Sequence',
    ' score'                 : 'Novor:score',
    ' mz(data)'              : 'Exp m/z',
    ' RT'                    : 'Retention Time (s)',
    ' z'                     : 'Charge',
    '# id'                   : 'Novor:id',
    ' pepMass(denovo)'       : 'Calc mass',
    ' err(data-denovo)'      : 'Error (exp-calc)',
    ' ppm(1e6*err/(mz*z))'   : 'Error (ppm)',
    ' aaScore'               : 'Novor:aaScore',

}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}

USED_USEARCH_PARAMS = set( [
    'modifications',
    'enzyme',
    'precursor_mass_tolerance_unit',
    'precursor_mass_tolerance_minus',
    'precursor_mass_tolerance_plus',
    'frag_mass_tolerance',
    'frag_mass_tolerance_unit',
    'frag_method',
    'instrument'
    ]
     )

