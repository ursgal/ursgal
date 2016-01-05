META_INFO = {
    'engine_type'            : {
        'controller'        : False,
        'converter'         : False,
        'validation_engine' : True,
        'search_engine'     : False,
        'meta_engine'       : False
    },
    'output_extension'          : '.csv',
    'output_suffix'             : 'qvality_validated',
    'input_types'               : ['.csv'],
    'create_own_folder'         : False,
    'citation'   : 'Käll L, Storey JD, Noble WS (2009) QVALITY: '\
        'non-parametric estimation of q-values and posterior error '\
        'probabilities.',
    'include_in_git'            : False,
    'group_psms'                : True,
    
    'engine': {
        'darwin' : {
            '64bit' : {
                'exe'            : 'qvality',
                'url'            : '',
                'zip_md5'        : '4f2c1a6eb697cb66d066047c98c1f114',
                'additional_exe' : [],
            },
        },
        'linux' : {
            '64bit' : {
                'exe'            : 'qvality',
                'url'            : '',
                'zip_md5'        : '2ddd863add4095b710e6883abbd5efbf',
                'additional_exe' : [],
            },
        },
        'win32' : {
            '64bit' : {
                'exe'            : 'qvality.exe',
                'url'            : '',
                'zip_md5'        : '45c98d18d99f46578d938362c3302804',
                'additional_exe' : [],
            },
            '32bit' : {
                'exe'            : 'qvality.exe',
                'url'            : '',
                'zip_md5'        : 'f10aee7feec1340364c64eccc6f75a3c',
                'additional_exe' : [],
            },
        },
    },

    # 'engine_exe' : {
    #     'linux'  : 'qvality',
    #     # 'darwin' : 'qvality',
    #     'win32'  : 'qvality.exe',
    # },
    # 'zip_md5' : {
    #     # 'darwin' : { 
    #     #     '64bit' : '4f2c1a6eb697cb66d066047c98c1f114'
    #     # },
    #     'linux' : { 
    #         '64bit' : '2ddd863add4095b710e6883abbd5efbf'
    #     },
    #     'win32' : { 
    #         '32bit' : 'f10aee7feec1340364c64eccc6f75a3c',
    #         '64bit' : '45c98d18d99f46578d938362c3302804'
    #     }
    # }
}


USEARCH_PARAM_VALUE_TRANSLATIONS = {
}

DEFAULT_PARAMS = {
    'validation_generalized'   : False,# '-g','False',#Generalized target decoy competition, situations where PSMs known to more frequently be incorrect are mixed in with the correct PSMs
    'qvality_number_of_bins'   : '500',
    'qvality_verbose'          : '2',#medium verbose
    'qvality_epsilon_step'     : '0',#epsilon step #The relative step size used as treshhold before cross validation error is calculated, qvality determines step size automatically when set to 0
    'qvality_cross_validation' : '0',#cross validation, The relative crossvalidation step size used as treshhold before ending the iterations, qvality determines step size automatically when set to 0commandLine : -c
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}
USED_USEARCH_PARAMS = set([
    'validation_generalized',
    'qvality_number_of_bins',
    'qvality_verbose',
    'qvality_epsilon_step',
    'qvality_cross_validation',
])

'''

parameters:
  - key: qvality __Fufezan__ number-of-bins
    group: General
    label: number-of-bins
    description: The number of spline knots used when interpolating spline function. Default is 500
    commandLine: -n
    type: int
    min: 0
    default: 500
  - key: qvality __Fufezan__ reverse
    group: General
    label: low scores are better (aka reverse)
    description: Indicating that the scoring mechanism is reversed, i.e., that low scores are better than higher scores
    commandLine: -r
    type: enum
    choices: [{'True': 'True'}, {'False': 'False'}]
    default: 'False'
  - key: qvality __Fufezan__ verbose
    group: General
    label: Verbosity
    description: Set verbosity of output. 0=no processing info, 5 all, default is 2
    commandLine: -v
    type: int
    min: 0
    max: 5
    default: 2
  - key: qvality __Fufezan__ epsilon-step
    group: General
    label: epsilon-step
    description: The relative step size used as treshhold before cross validation error is calculated, qvality determines step size automatically when set to 0
    commandLine: -s
    type: int
    min: 0
    default: 0
  - key: qvality __Fufezan__ epsilon-cross-validation
    group: General
    label: epsilon-cross-validation
    description: The relative crossvalidation step size used as treshhold before ending the iterations, qvality determines step size automatically when set to 0
    commandLine: -c
    type: int
    min: 0
    default: 0
  - key: qvality __Fufezan__ generalized
    group: General
    label: generalized
    description: Generalized target decoy competition, situations where PSMs known to more frequently be incorrect are mixed in with the correct PSMs
    commandLine: -g
    type: enum
    choices: [{'True': 'True'}, {'False': 'False'}]
    default: 'False'
  - key: debug
    group: General
    label: s
    description: Print additional debug output
    type: enum
    choices: [{'True': 'True'}, {'False': 'False'}]
    default: 'False'
'''

