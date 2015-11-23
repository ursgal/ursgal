from collections import OrderedDict

META_INFO={
     'engine_type'            : {
        'controller'        : False,
        'converter'         : False,
        'validation_engine' : True,
        'search_engine'     : False,
        'meta_engine'       : False
    },
    'output_extension'          : '.csv',
    'output_suffix'             : 'percolator_validated',
    'input_types'               : ['.csv'],
    'create_own_folder'         : False,
    'in_development'            : True,
    'citation'   : 'Käll L, Canterbury JD, Weston J, Noble WS, '\
        'MacCoss MJ. (2007) Semi-supervised learning for peptide '\
        'identification from shotgun proteomics datasets.',
    'include_in_git'            : False,
    # 'zip_md5'                   : None,
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
}

DEFAULT_PARAMS = {
    'validation_score_field' : None,
    'validation_minimum_score' : None,
    'validation_reverse_scores' : None
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {}

USED_USEARCH_PARAMS = set()

PERCOLATOR_FIELDS = OrderedDict([
    (
        'SpecId', {
            'csv_field': 'Spectrum Title',
            'DefaultDirection': 'DefaultDirection'
        }
    ),
    (
        'Label', {
            'csv_field': '',
            'DefaultDirection': '-'
        }
    ),
    (
        'ScanNr', {
            'csv_field': 'Spectrum ID',
            'DefaultDirection': '-'
        }
    ),
    (
        'lnrSp', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
        'The natural logarithm of the rank of the match based on the Sp score'
        }
    ),
    (
        'deltLCn', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
        "The difference between this PSM's XCorr and the XCorr of the last-ranked \
        PSM for this spectrum, divided by this PSM's XCorr or 1, whichever is larger."
        }
    ),
    (
        'deltCn', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
            "The difference between this PSM's XCorr and the XCorr of the next-ranked \
        PSM for this spectrum, divided by this PSM's XCorr or 1, whichever is larger. \
        Note that this definition differs from that of the standard delta Cn reported \
        by SEQUEST®"
                }
    ),
    (
        'Xcorr', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
                "The SEQUEST cross-correlation score"
                }
    ),
    (
        'Sp', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
        "The preliminary SEQUEST score."
                }
    ),
    (
        'IonFrac', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
        "The fraction of b and y ions theoretical ions matched to the spectrum"
                }
    ),
    (
        'Mass',    {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
        "The observed mass [M+H]+"
                }
    ),
    (
        'PepLen',  {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': \
        "The length of the matched peptide, in residues"
        }
    ),
    (
        'Charge1', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge2', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge3', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge4', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge5', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge6', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge7', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge8', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge9', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'Charge10', {
            'csv_field': '',
            'DefaultDirection': 0
        }
    ),
    (
        'enzN', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': "Is the peptide preceded by an enzymatic (tryptic) site?"
        }
    ),
    (
        'enzC', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': "Does the peptide have an enzymatic (tryptic) C-terminus?"
        }
    ),
    (
        'enzInt', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': "Number of missed internal enzymatic (tryptic) sites"
        }
    ),
    (
        'lnNumSP', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': "The natural logarithm of the number of database peptides within the \
            specified precursor range"
        }
    ),
    (
        'dM', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': "The difference between the calculated and observed mass"
        }
    ),
    (
        'absdM', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': "The absolute value of the difference between the calculated and \
            observed mass"
        }
    ),
    (
        'Peptide', {
            'csv_field': '',
            'DefaultDirection': 0,
            'description': ""
        }
    ),
    (
        'Proteins', {
            'csv_field': 'proteinacc_start_stop_pre_post_;',
            'DefaultDirection': 0,
            'description': ""
        }
    ),
])
