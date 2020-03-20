ursgal_params = {
    'infer_proteins' : {
        'edit_version': 1.00,
        'available_in_unode' : [
            'percolator_2_08',
            'percolator_3_2_1',
            'percolator_3_4_0',
        ],
        'default_value' : False,
        'description' :  ''' Use the picked-protein algorithm to infer protein PEP and FDR in Percolator''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'percolator_style_1' : 'infer_proteins',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_option' : {
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "bool",
    },
    'percolator_post_processing': {
        'edit_version': 1.00,
        'available_in_unode' : [
            'percolator_3_2_1',
            'percolator_3_4_0',
        ],
        'default_value' : 'tdc',
        'description' :  ''' Method to assign FDR and PEP to PSMs''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'percolator_style_1' : ('-y','-Y'),
        },
        'utag' : [
            'validation',
        ],
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type'    : 'radio_button',
            'available_values'  : ['mix-max', 'tdc'],
            'custom_val_max' : 0,
        },
    },
    'pyqms_verbosity': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
        },
        'default_value': True,
        'description': '''verbosity for pyqms''',
        'triggers_rerun': False,
        'ukey_translation': {
            'pyqms_style_1': 'pyqms_verbosity',
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "bool",
    },
    'label_percentile_format_string': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': '{0}',
            'multiple_line': False,
            'unit': 'psms',
        },
        'default_value': '{0:.3f}',
        'description': """Defines the standard format string when
            formatting labeling percentile float""",
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1' : 'PERCENTILE_FORMAT_STRING',
            'sugarpy_run_style_1' : 'PERCENTILE_FORMAT_STRING',
            'sugarpy_plot_style_1' : 'PERCENTILE_FORMAT_STRING',
        },
        'utag': [
            'quantification',
            'label',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "str",
    },
    'min_element_abundance': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 0.001,
            'unit': 'abundance',
            'f-point': 1e-02
        },
        'default_value': 1e-3,
        'description': """ Set minmal abundance for elements used when building isotopologue library """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1' : 'ELEMENT_MIN_ABUNDANCE',
            'sugarpy_run_style_1' : 'ELEMENT_MIN_ABUNDANCE',
            'sugarpy_plot_style_1' : 'ELEMENT_MIN_ABUNDANCE',
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'min_rel_peak_intensity_for_matching': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 0.01,
            'unit': 'a.u.',
            'f-point': 1e-02
        },
        'default_value': 0.01,
        'description': """ Minimum required intensity for pyqms peak matching """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1' : 'MIN_REL_PEAK_INTENSITY_FOR_MATCHING',
            'sugarpy_run_style_1' : 'MIN_REL_PEAK_INTENSITY_FOR_MATCHING',
            'sugarpy_plot_style_1': 'MIN_REL_PEAK_INTENSITY_FOR_MATCHING',
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'required_percentile_peak_overlap': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1,
            'min': 0,
            'updownval': 0.1,
            'unit': 'a.u.',
            'f-point': 1e-02
        },
        'default_value': 0.5,
        'description': """ Minimum percentile overlap for matching labeled peaks """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1' : 'REQUIRED_PERCENTILE_PEAK_OVERLAP',
            'sugarpy_run_style_1' : 'REQUIRED_PERCENTILE_PEAK_OVERLAP',
            'sugarpy_plot_style_1' : 'REQUIRED_PERCENTILE_PEAK_OVERLAP',
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'min_number_of_matched_isotopologues': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1000,
            'min': 0,
            'updownval': 1,
            'unit': '',
        },
        'default_value': 2,
        'description': """ Min number of matched isotopologues for pyqms to consider for quantification """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES',
            'sugarpy_run_style_1': 'MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES',
            'sugarpy_plot_style_1': 'MINIMUM_NUMBER_OF_MATCHED_ISOTOPOLOGUES',
        },
        'utag': [
            'quantification',
            'accuracy'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "int",
    },
    'intensity_transformation_factor': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1e20,
            'min': 0,
            'updownval': 1e4,
            'unit': 'a.u.',
            'f-point': 0.1
        },
        'default_value': 1e5,
        'description': """ Tranform intensity by this factor for quantification """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'INTENSITY_TRANSFORMATION_FACTOR',
            'sugarpy_run_style_1': 'INTENSITY_TRANSFORMATION_FACTOR',
            'sugarpy_plot_style_1': 'INTENSITY_TRANSFORMATION_FACTOR',
        },
        'utag': [
            'quantification',
            'conversion'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'upper_mz_limit': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 20000,
            'min': 0,
            'updownval': 100,
            'unit': 'a.u.',
            'f-point': 1e-01,
        },
        'default_value': 2000,
        'description': """ Highest considered mz for quantification """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'UPPER_MZ_LIMIT',
            'sugarpy_run_style_1': 'UPPER_MZ_LIMIT',
            'sugarpy_plot_style_1': 'UPPER_MZ_LIMIT',
        },
        'utag': [
            'quantification',
            'spectrum',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'lower_mz_limit': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0'
        ],
        'uvalue_option': {
            'none_val': 0,
            'multiple_line': False,
            'max': 20000,
            'min': 0,
            'updownval': 100,
            'unit': 'a.u.',
            'f-point': 1e-01,
        },
        'default_value': 150,
        'description': """ lowest considered mz for quantification """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'LOWER_MZ_LIMIT',
            'sugarpy_run_style_1': 'LOWER_MZ_LIMIT',
            'sugarpy_plot_style_1': 'LOWER_MZ_LIMIT',
        },
        'utag': [
            'quantification',
            'spectrum',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'mz_transformation_factor': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1e10,
            'min': 0,
            'updownval': 100,
            'unit': 'a.u.',
            'f-point': 1e-01
        },
        'default_value': 1000,
        'description': """ Factor which will be multiplied with mz before conversion to integer """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'MZ_TRANSFORMATION_FACTOR',
            'sugarpy_run_style_1': 'MZ_TRANSFORMATION_FACTOR',
            'sugarpy_plot_style_1': 'MZ_TRANSFORMATION_FACTOR',
        },
        'utag': [
            'quantification',
            'conversion',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'rel_intensity_range': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1,
            'min': 0,
            'updownval': 0.01,
            'unit': 'a.u.',
            'f-point': 1e-02
        },
        'default_value': 0.2,
        'description': """ rel Intensity Error """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'REL_I_RANGE',
            'sugarpy_run_style_1': 'REL_I_RANGE',
            'sugarpy_plot_style_1': 'REL_I_RANGE'
        },
        'utag': [
            'quantification',
            'accuracy'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'internal_precision': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1e10,
            'min': 0,
            'updownval': 100,
            'unit': 'a.u.',
            'f-point': 1e-01
        },
        'default_value': 1000.0,
        'description': """ Float to int conversion precision """,
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'INTERNAL_PRECISION',
            'sugarpy_run_style_1': 'INTERNAL_PRECISION',
            'sugarpy_plot_style_1': 'INTERNAL_PRECISION',
        },
        'utag': [
            'quantification',
            'conversion'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'max_molecules_per_match_bin': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 1,
            'unit': 'a.u',
        },
        'default_value': 5000,
        'description': ''' Max number of molecules in one matching bin. ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'MAX_MOLECULES_PER_MATCH_BIN',
            'sugarpy_run_style_1': 'MAX_MOLECULES_PER_MATCH_BIN',
            'sugarpy_plot_style_1': 'MAX_MOLECULES_PER_MATCH_BIN',
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "int",
    },
    'silac_aas_locked_in_experiment': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': [None],
            'multiple_line': False,
            'item_type': 'str',
            'item_title': 'aminoacid',
            'custom_val_max': 20,
            'custom_type' : {
            }
        },
        'default_value': None,
        'description': ''' AA which are always SILAC labeled and not considered for calculating partially labeling percentile ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'SILAC_AAS_LOCKED_IN_EXPERIMENT',
            'sugarpy_run_style_1': 'SILAC_AAS_LOCKED_IN_EXPERIMENT',
            'sugarpy_plot_style_1': 'SILAC_AAS_LOCKED_IN_EXPERIMENT',
        },
        'utag': [
            'quantification',
            'label',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "list",
    },
    'build_pyqms_result_index': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 1,
            'unit': 'psms',
        },
        'default_value': True,
        'description': ''' Build index for faster access ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'BUILD_RESULT_INDEX',
            'sugarpy_run_style_1': 'BUILD_RESULT_INDEX',
            'sugarpy_plot_style_1': 'BUILD_RESULT_INDEX',
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "bool",
    },
    # 'pyQms_colors': {
    #     'edit_version' : 1.00,
    #     'available_in_unode': [
    #         'pyqms_1_0_0',
    #     ],
    #     'uvalue_option': {
    #         'none_val': None,
    #         'multiple_line': False,
    #         # 'max': 10000,
    #         # 'min': 0,
    #         # 'updownval': 1,
    #         'custom_val_max': 11,
    #         'dict_type': {
    #             '0.0': 'tuple',
    #             '0.1': 'tuple',
    #             '0.2': 'tuple',
    #             '0.3': 'tuple',
    #             '0.4': 'tuple',
    #             '0.5': 'tuple',
    #             '0.6': 'tuple',
    #             '0.7': 'tuple',
    #             '0.8': 'tuple',
    #             '0.9': 'tuple',
    #             '1.0': 'tuple'
    #         },
    #         'dict_title': {
    #             'Enrichment' : 'Color'
    #         },
    #         'title_list' : {
    #             '0.0' : [],
    #             '0.1' : [],
    #             '0.2' : [],
    #             '0.3' : [],
    #             '0.4' : [],
    #             '0.5' : [],
    #             '0.6' : [],
    #             '0.7' : [],
    #             '0.8' : [],
    #             '0.9' : [],
    #             '1.0' : []
    #         },
    #         'type_dict'  : {
    #             '0.0': {},
    #             '0.1': {},
    #             '0.2': {},
    #             '0.3': {},
    #             '0.4': {},
    #             '0.5': {},
    #             '0.6': {},
    #             '0.7': {},
    #             '0.8': {},
    #             '0.9': {},
    #             '1.0': {},
    #         }
    #     },
    #     'default_value': {
    #         '0.0' : (37  , 37  , 37)  ,
    #         '0.1' : (99  , 99  , 99)  ,
    #         '0.2' : (150 , 150 , 150) ,
    #         '0.3' : (204 , 204 , 204) ,
    #         '0.4' : (247 , 247 , 247) ,
    #         '0.5' : (203 , 27  , 29)  ,
    #         '0.6' : (248 , 120 , 72)  ,
    #         '0.7' : (253 , 219 , 121) ,
    #         '0.8' : (209 , 239 , 121) ,
    #         '0.9' : (129 , 202 , 78)  ,
    #         '1.0' : (27  , 137 , 62)
    #     },
    #     'description': ''' Minimum number of peptide spectrum matches required \
    #         for considering a peptide for quantification ''',
    #     'triggers_rerun': True,
    #     'ukey_translation': {
    #         'pyqms_style_1': 'COLORS'
    #     },
    #     'utag': [
    #         'quantification',
    #     ],
    #     'uvalue_translation': {
    #     },
    #     'uvalue_type': "dict",
    # },
    'evidence_score_field': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
        ],
        'default_value': "PEP",
        'description':  ''' Field which is used for scoring in pyqms_1_0_0 ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1' : 'evidence_score_field'
        },
        'utag': [
            'quantification',
            'scoring',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
        },
        'uvalue_translation': {
        },
        'uvalue_type': 'str',
    },
    'quantification_evidences': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
        ],
        'default_value': None,
        'description':  ''' Molecules to quantify. Can be either a list of strings or a csv file ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'evidences'
        },
        'uvalue_option': {
            'none_val': [None],
            'item_title': 'path',
            'custom_val_max': 100000,
            'item_type': 'str',
            'multiple_line' : False,
            'custom_type': {}
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': 'list',
    },
    'm_score_cutoff': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1,
            'min': 0,
            'updownval': 0.1,
            'unit': 'a.u.',
            'f-point': 1e-02
        },
        'default_value': 0.7,
        'description':  ''' minimum required pyQms m_score for a quant event to be evaluated ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'M_SCORE_THRESHOLD',
            'sugarpy_run_style_1': 'M_SCORE_THRESHOLD',
            'sugarpy_plot_style_1': 'M_SCORE_THRESHOLD'
        },
        'utag': [
            'quantification',
            'scoring',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'molecules_to_quantify': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
        ],
        'uvalue_option': {
            'none_val': [],
            'item_type': 'str',
            'item_title': 'molecule',
            'custom_val_max': 100000,
            'multiple_line' : False,
            'custom_type': {
                'str': {
                    'multiple_line': False,
                },
            },
        },
        'default_value': None,
        'description':  ''' Molecules to quantify. Can be either a list of strings or a csv file ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'molecules',
        },
        'utag': [
            'quantification',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': 'list',
    },
    'mz_score_percentile': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'default_value': 0.4,
        'description':  ''' weighting factor for pyQms mz score ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'MZ_SCORE_PERCENTILE',
            'sugarpy_run_style_1': 'MZ_SCORE_PERCENTILE',
            'sugarpy_plot_style_1': 'MZ_SCORE_PERCENTILE',
        },
        'utag': [
            'quantification',
            'scoring',
        ],
        'uvalue_option': {
            'max': 1.0,
            'min': 0,
            'updownval': 0.01,
            'none_val': None,
            'f-point': 1e-02,
            'unit': 'percent'
        },
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'ms_level': {
        'edit_version' : 1.01,
        'available_in_unode': [
            'pyqms_1_0_0',
            'mzml2mgf_1_0_0',
            'mzml2mgf_2_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 5,
            'min': 1,
            'updownval': 1,
            'unit': 'ms_level'
        },
        'default_value': 2,
        'description': 'MS level on which that is taken into account, e.g. for spectrum extraction, matching of evidences, etc.',
        'triggers_rerun': True,
        'ukey_translation': {
            'pyqms_style_1': 'ms_level',
            'mzml2mgf_style_1' : 'ms_level',
            'sugarpy_run_style_1' : 'ms_level',
            'sugarpy_plot_style_1' : 'ms_level',
            'pipi_style_1' : 'ms_level',
        },
        'utag': [
            'spectrum'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': 'int',
    },
    'label_percentile' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pyqms_1_0_0',
        ],
        'default_value' : [0.0],
        'description' :  ''' Enrichment level of the label ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pyqms_style_1' : 'label_percentile',
        },
        'utag' : [
            'label',
            'quantification'
        ],
        'uvalue_option' : {
            'none_val' : [],
            'item_title' : 'label_percentile',
            'item_type' : 'float',
            'custom_val_max' : 0,
            # 'f-point' : {
            #     'enrichment percentage': 0.001
            # },
            # 'max' : {
            #     'enrichment percentage':1
            # },
            # 'min' : {
            #     'enrichment percentage':0
            # },
            # 'none_val' : None,
            # 'custom_val_max': 1000,
            # 'type_dict': {
            #     'enrichment percentage' : 'float'
            # },
            # 'title_list': ['enrichment percentage'],
            # 'unit' : {
            #     'enrichment percentage' : '%'
            # },
            # 'updownval' : {
            #     'enrichment percentage': 0.001
            # },
            # 'custom_type': {}
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "list",
    },
    'fixed_label_isotope_enrichment_levels' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : {
            '13C' : 0.996,
            '15N' : 0.994,
            '2H' : 0.994,
        },
        'description' :  ''' Enrichment of labeled elements in labeled chemical used ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pyqms_style_1' : 'FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS',
            'sugarpy_run_style_1' : 'FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS',
            'sugarpy_plot_style_1' : 'FIXED_LABEL_ISOTOPE_ENRICHMENT_LEVELS',
        },
        'utag' : [
            'quantification',
            'label',
        ],
        'uvalue_option' : {
            'item_titles':  {
                'Isotope' : 'Enrichment',
            },
            'value_types': {
                'Isotope' : 'float',
            },
            'multiple_line' : {
                'Isotope' : False,
            },
            'none_val' : None,
            'max' : {
                'Isotope' : 1.0,
            },
            'min' : {
                'Isotope' : 0.0,
            },
            'unit' : {
                'Isotope' : 'psms',
            },
            'f-point' : {
                'Isotope' : 0.1,
            },
            'updownval' : {
                'Isotope' : 0.1,
            },
            'custom_val_max' : 3,
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            # 'dict_type': {
            #     '13C' : {'str' : 'float'},
            #     '15N' : {'str' : 'float'},
            #     '2H' : {'str' : 'float'},
            # },
            # 'dict_title' : {
            #     'Isotope' : 'Enrichment'
            # },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'pyqms_trivial_names' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pyqms_1_0_0',
        ],
        'default_value' : None,
        'description' :  ''' Trivial name lookup mapping molecules to a trivial name ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pyqms_style_1' : 'trivial_names'
        },
        'utag' : [
            'quantification',
            'output',
        ],
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'formula' : 'trivial',
            },
            'value_types' : {
                'str' : 'str',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'rt_border_tolerance' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : 1,
        'description' :  ''' Retention time border tolerance (in min) for curating RT windows ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pyqms_style_1' : 'rt_border_tolerance',
            'sugarpy_run_style_1' : 'rt_border_tolerance',
            'sugarpy_plot_style_1' : 'rt_border_tolerance',
        },
        'utag' : [
            'quantification',
            'chromatography'
        ],
        'uvalue_option' : {
            'f-point' : 0.01,
            'max' : 200,
            'min' : 0,
            'none_val' : None,
            'unit' : 'minute',
            'updownval' : 1,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "float",
    },
    '-xmx' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msgfplus2csv_v2016_09_16',
            'msgfplus2csv_v2017_01_27',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'msgfplus_style_1'  : '-Xmx',
            'mzidentml_style_1' : '-Xmx',
            'msfragger_style_1' : '-Xmx',
            'pipi_style_1'      : '-Xmx',
        },
        'utag' : [
            'hardware_resources',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value'  : '13312m',
        'description' : \
            'Set maximum Java heap size (used RAM)',
    },
    'aa_exception_dict' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'unify_csv_1_0_0',
            'upeptide_mapper_1_0_0',
            'compomics_utilities_4_11_5'
        ],
        'default_value' : {
            'J' : {
                'original_aa' : ['L','I'],
            },
            'O' : {
                'original_aa' : ['K'],
                'unimod_name' : 'Methylpyrroline',
            },
            # 'U' : {
            #     'original_aa' : 'C',
            #     'unimod_name' : 'Delta:S(-1)Se(1)',
            #     'unimod_name_with_cam' : 'SecCarbamidomethyl',
            # },
        },
        'description' : \
            'Unusual aminoacids that are not accepted (e.g. by unify_csv_1_0_0), '
            'but reported by some engines. Given as a dictionary mapping on he '
            'original_aa as well as the unimod modification name. '
            'U is now accepted as regular amino acid (2017/03/30)'
        ,
        'triggers_rerun' : True,
        'ukey_translation' : {
            'unify_csv_style_1' : 'aa_exception_dict',
            'upeptide_mapper_style_1' : 'aa_exception_dict',
            'compomics_utilities_style_1' : 'aa_exception_dict'
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'dict',
        'uvalue_option' : {
            'none_val' : {},
            'item_titles' : {
                'amino_acid' : {
                    'original_aa' : 'aa_list',
                    'unimod_name' : 'name',
                    # 'unimod_name_with_cam' : 'name',
                }
            },
            'value_types' : {
                'amino_acid'           : 'dict',
                'original_aa'          : 'list',
                'unimod_name'          : 'str',
                # 'unimod_name_with_cam' : 'str',
            },
            'multiple_line' : {
                # 'original_aa'          : False,
                'unimod_name'          : False,
            #     # 'unimod_name_with_cam' : False,
            },
            # 'custom_type' : {
            #     'str' : {
            #         'multiple_line' : False,
            #     },
            # },
            'custom_val_max' : 0,
        },
    },
    'accept_conflicting_psms' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'sanitize_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sanitize_csv_style_1' : 'accept_conflicting_psms',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'bool',
        'uvalue_option' : {
        },
        'default_value'  : False,
        'description' : \
            'If True, multiple PSMs for one spectrum can be reported if their '\
            'score difference is below the threshold. If False, all PSMs for '\
            'one spectrum are removed if the score difference between the '\
            'best and secondbest PSM is not above the threshold, i.e. if '\
            'there are conflicting PSMs with similar scores.',
    },
    'allow_multiple_variable_mods_on_residue' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : True,
        'description' :  ''' Static mods are not considered ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'allow_multiple_variable_mods_on_residue',
        },
        'utag' : [
            'modifications'
        ],
        'uvalue_option' : {
        },
        'uvalue_translation' : {
            'msfragger_style_1' : {
                False : 0,
                True : 1,
            }
        },
        'uvalue_type' : "bool",
    },
    'base_mz' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'    : 'base_mz',
            'omssa_style_1'   : 'base_mz',
            'pepnovo_style_1' : 'base_mz',
            'pipi_style_1'    : 'base_mz',
            'novor_style_1'   : 'base_mz',
            'pyqms_style_1'      : 'REL_MZ_RANGE',
            'sugarpy_run_style_1': 'REL_MZ_RANGE',
            'sugarpy_plot_style_1': 'REL_MZ_RANGE',
            'deepnovo_style_1': 'base_mz',
        },
        'utag' : [
            'conversion'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value'  : 1000,
        'description' : \
            'm/z value that is used as basis for the conversion from ppm to Da',
    },
    'batch_size' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'myrimatch_style_1' : 'NumBatches',
            'xtandem_style_1'   : 'spectrum, sequence batch size',
            'msamanda_style_1'  : 'LoadedProteinsAtOnce',
        },
        'utag' : [
            'hardware_resources',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 10000,
            'unit'      : ''
        },
        'default_value'  : 100000,
        'description' : \
            'Sets the number of sequences loaded in as a batch from the '\
            'database file',
    },
    'batch_size_spectra' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'msamanda_style_1'  : 'LoadedSpectraAtOnce',
            'deepnovo_style_1'  : 'buffer_size'
        },
        'utag' : [
            'hardware_resources',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 10000,
            'unit'      : ''
        },
        'default_value'  : 2000,
        'description' : \
            'sets the number of spectra loaded into memory as a batch',
    },
    'bigger_scores_better' : {
        'edit_version'   : 1.01,
        'available_in_unode' : [
            'add_estimated_fdr_1_0_0',
            'percolator_2_08',
            'percolator_3_2_1',
            'percolator_3_4_0',
            'qvality_2_02',
            'sanitize_csv_1_0_0',
            'svm_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'add_estimated_fdr_style_1' : 'bigger_scores_better',
            'percolator_style_1'        : 'bigger_scores_better',
            'qvality_style_1'           : '-r',
            'sanitize_csv_style_1'      : 'bigger_scores_better',
            'svm_style_1'               : 'bigger_scores_better',
        },
        'utag' : [
            'scoring',
            'validation',
        ],
        'uvalue_translation' : {
            'add_estimated_fdr_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msamanda_2_0_0_9706'  : True,
                'msamanda_2_0_0_9695'  : True,
                'msamanda_2_0_0_10695' : True,
                'msamanda_2_0_0_11219' : True,
                'msamanda_2_0_0_13723' : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v2018_01_30' : False,
                'msgfplus_v2018_06_28' : False,
                'msgfplus_v2018_09_12' : False,
                'msgfplus_v2019_01_22' : False,
                'msgfplus_v2019_04_18' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance' : True,
                'xtandem_alanine' : True,
                'msfragger_20170103' : True,
                'msfragger_20171106' : True,
                'msfragger_20190222'   : True,
                'mascot_x_x_x'  : True,
                'pipi_1_4_5' : True,
                'pipi_1_4_6' : True,
                'moda_v1_51' : True,
                'moda_v1_61' : True,
                'moda_v1_62' : True,
                'pglyco_db_2_2_0' : True,
                'deepnovo_0_0_1' : True,
            },
            'percolator_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msamanda_2_0_0_9706'  : True,
                'msamanda_2_0_0_9695'  : True,
                'msamanda_2_0_0_10695' : True,
                'msamanda_2_0_0_11219' : True,
                'msamanda_2_0_0_13723' : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v2018_01_30' : False,
                'msgfplus_v2018_06_28' : False,
                'msgfplus_v2018_09_12' : False,
                'msgfplus_v2019_01_22' : False,
                'msgfplus_v2019_04_18' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'xtandem_alanine'    : True,
                'msfragger_20170103'   : True,
                'msfragger_20171106'   : True,
                'msfragger_20190222'   : True,
                'mascot_x_x_x'  : True,
                'pipi_1_4_5' : True,
                'pipi_1_4_6' : True,
                'moda_v1_51' : True,
                'moda_v1_61' : True,
                'moda_v1_62' : True,
                'pglyco_db_2_2_0' : True,
                'deepnovo_0_0_1' : True,
            },
            'qvality_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msamanda_2_0_0_9706'  : True,
                'msamanda_2_0_0_9695'  : True,
                'msamanda_2_0_0_10695' : True,
                'msamanda_2_0_0_11219' : True,
                'msamanda_2_0_0_13723' : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v2018_01_30' : False,
                'msgfplus_v2018_06_28' : False,
                'msgfplus_v2018_09_12' : False,
                'msgfplus_v2019_01_22' : False,
                'msgfplus_v2019_04_18' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'xtandem_alanine'    : True,
                'msfragger_20170103'   : True,
                'msfragger_20171106'   : True,
                'msfragger_20190222'   : True,
                'mascot_x_x_x'  : True,
                'pipi_1_4_5' : True,
                'pipi_1_4_6' : True,
                'moda_v1_51' : True,
                'moda_v1_61' : True,
                'moda_v1_62' : True,
                'pglyco_db_2_2_0' : True,
                'deepnovo_0_0_1' : True,
            },
            'sanitize_csv_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msamanda_2_0_0_9706'  : True,
                'msamanda_2_0_0_9695'  : True,
                'msamanda_2_0_0_10695' : True,
                'msamanda_2_0_0_11219' : True,
                'msamanda_2_0_0_13723' : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v2018_01_30' : False,
                'msgfplus_v2018_06_28' : False,
                'msgfplus_v2018_09_12' : False,
                'msgfplus_v2019_01_22' : False,
                'msgfplus_v2019_04_18' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'xtandem_alanine'    : True,
                'msfragger_20170103'   : True,
                'msfragger_20171106'   : True,
                'msfragger_20190222'   : True,
                'mascot_x_x_x'  : True,
                'pipi_1_4_5' : True,
                'pipi_1_4_6' : True,
                'moda_v1_51' : True,
                'moda_v1_61' : True,
                'moda_v1_62' : True,
                'pglyco_db_2_2_0' : True,
                'deepnovo_0_0_1' : True,
            },
            'svm_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msamanda_2_0_0_9706'  : True,
                'msamanda_2_0_0_9695'  : True,
                'msamanda_2_0_0_10695' : True,
                'msamanda_2_0_0_11219' : True,
                'msamanda_2_0_0_13723' : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v2018_01_30' : False,
                'msgfplus_v2018_06_28' : False,
                'msgfplus_v2018_09_12' : False,
                'msgfplus_v2019_01_22' : False,
                'msgfplus_v2019_04_18' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'xtandem_alanine'    : True,
                'msfragger_20170103'   : True,
                'msfragger_20171106'   : True,
                'msfragger_20190222'   : True,
                'mascot_x_x_x'  : True,
                'pipi_1_4_5' : True,
                'pipi_1_4_6' : True,
                'moda_v1_51' : True,
                'moda_v1_61' : True,
                'moda_v1_62' : True,
                'pglyco_db_2_2_0' : True,
                'deepnovo_0_0_1' : True,
            },
        },
        'uvalue_type'    : 'select',
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'None',
                'msamanda_1_0_0_5242',
                'msamanda_1_0_0_5243',
                'msamanda_1_0_0_6299',
                'msamanda_1_0_0_6300',
                'msamanda_1_0_0_7503',
                'msamanda_1_0_0_7504',
                'msamanda_2_0_0_9706',
                'msamanda_2_0_0_9695',
                'msamanda_2_0_0_10695',
                'msamanda_2_0_0_11219',
                'msamanda_2_0_0_13723',
                'msfragger_20170103',
                'msfragger_20171106',
                'msfragger_20190222',
                'msgfplus_v2016_09_16',
                'msgfplus_v2017_01_27',
                'msgfplus_v2018_01_30',
                'msgfplus_v2018_06_28',
                'msgfplus_v2018_09_12',
                'msgfplus_v2019_01_22',
                'msgfplus_v2019_04_18',
                'msgfplus_v9979',
                'myrimatch_2_1_138',
                'myrimatch_2_2_140',
                'omssa_2_1_9',
                'xtandem_cyclone_2010',
                'xtandem_jackhammer',
                'xtandem_piledriver',
                'xtandem_sledgehammer',
                'xtandem_vengeance',
                'xtandem_alanine',
                'mascot_x_x_x',
                'pglyco_db_2_2_0',
            ],
            'custom_val_max' : 0,
        },
        'default_value'  : 'None',
        'description' : \
            'Defines if bigger scores are better (or the other way round), '\
            'for scores that should be validated (see validation_score_field) '\
            'e.g. by percolator, qvality',
    },
    'cleavage_cterm_mass_change' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, cleavage C-terminal mass change',
        },
        'utag' : [
            'protein',
            'cleavage',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value'  : 17.00305,
        'description' : \
            'The mass added to the peptide C-terminus by protein cleavage',
    },
    'cleavage_nterm_mass_change' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, cleavage N-terminal mass change',
        },
        'utag' : [
            'protein',
            'cleavage'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value'  : 1.00794,
        'description' : \
            'The mass added to the peptide N-terminus by protein cleavage',
    },
    'clip_nterm_m' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : False,
        'description' :  ''' Specifies the trimming of a protein N-terminal methionine as a variable modification ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'clip_nTerm_M',
        },
        'utag' : [
        ],
        'uvalue_option' : {
        },
        'uvalue_translation' : {
            'msfragger_style_1' : {
                False : 0,
                True : 1,
            }
        },
        'uvalue_type' : "bool",
    },
    'compensate_small_fasta' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'scoring, cyclic permutation',
        },
        'utag' : [
            'database',
        ],
        'uvalue_translation' : {
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type'    : 'bool',
        'uvalue_option' : {
        },
        'default_value'  : False,
        'description' : \
            'Compensate for very small database files.',
    },
    'compomics_utility_name' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'compomics_utilities_4_11_5',
        ],
        'default_value' : 'com.compomics.util.experiment.identification.protein_inference.executable.PeptideMapping',
        'description' :  \
            'Default value accesses the PeptideMapper tool, other tools are not '
            'implemented/covered yet',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'compomics_utilities_style_1' : 'compomics_utility_name',
        },
        'utag' : [
            'database',
        ],
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
    },
    'compomics_version' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'default_value' : "compomics_utilities_4_11_5",
        'description' :  \
            'Defines the compomics version to use',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'compomics_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "str",
    },
    'compress_raw_search_results_if_possible' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'compress_raw_search_results_if_possible',
        },
        'utag' : [
            'file_handling',
            'conversion'
        ],
        'uvalue_translation' : {
            'ucontroller_style_1':{
                'crux_2_1' : False,
                'kojak_1_5_3' : False,
                'mascot_x_x_x' : True,
                'moda_v1_51' : False,
                'moda_v1_61' : False,
                'moda_v1_62' : False,
                'msamanda_1_0_0_5242'  : False,
                'msamanda_1_0_0_5243'  : False,
                'msamanda_1_0_0_6299'  : False,
                'msamanda_1_0_0_6300'  : False,
                'msamanda_1_0_0_7503'  : False,
                'msamanda_1_0_0_7504'  : False,
                'msamanda_2_0_0_9706'  : False,
                'msamanda_2_0_0_9695'  : False,
                'msamanda_2_0_0_10695' : False,
                'msamanda_2_0_0_11219' : False,
                'msamanda_2_0_0_13723' : False,
                'msfragger_20170103'   : False,
                'msfragger_20171106'   : False,
                'msfragger_20190222'   : False,
                'msgfplus_v2016_09_16' : True,
                'msgfplus_v2017_01_27' : True,
                'msgfplus_v2018_01_30' : True,
                'msgfplus_v2018_06_28' : True,
                'msgfplus_v2018_09_12' : True,
                'msgfplus_v2019_01_22' : True,
                'msgfplus_v2019_04_18' : True,
                'msgfplus_v9979' : True,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'novor_1_1beta' : False,
                'novor_1_05' : False,
                'omssa_2_1_9' : False,
                'pepnovo_3_1' : False,
                'pipi_1_4_5' : False,
                'pipi_1_4_6' : False,
                'xtandem_alanine' : True,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer' : True,
                'xtandem_piledriver' : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance' : True,
                'pglyco_db_2_2_0' : False,
                'deepnovo_0_0_1' : False,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Compress raw search result to .gz: True or False',
    },
    'compute_xcorr' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'ComputeXCorr',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'myrimatch_style_1' : {
                False : 0,
                True  : 1,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Compute xcorr',
    },
    'consecutive_ion_prob' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-scorp',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.5,
        'description' : \
            'Probability of consecutive ion (used in correlation correction)',
    },
    'count_column_names' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'csv2counted_results_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'csv2counted_results_style_1' : 'count_column_names',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'column name',
            'item_type' : 'str',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
            'Sequence',
            'Modifications'
        ],
        'description' : \
            'List of column headers which are used for counting. '
            'The combination of these headers creates the unique countable element.',
    },
    'count_by_file' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'csv2counted_results_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'csv2counted_results_style_1' : 'count_by_file',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'the number of unique hits for each identifier '
            'is given in separate columns for each raw file '
            '(file name as defiened in Spectrum Title)',
    },
    'convert_to_sfinx' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'csv2counted_results_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'csv2counted_results_style_1' : 'convert2sfinx',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'If True, the header of the identifier column is "rownames". '
            'If False, the joined identifier header name will be used',
    },
    'cpus' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'ucontroller',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'moda_v1_62',
            'moda_v1_61',
            'pglyco_db_2_2_0',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'kojak_style_1'       : 'cpus',
            'msgfplus_style_1'    : '-thread',
            'myrimatch_style_1'   : '-cpus',
            'omssa_style_1'       : '-nt',
            'ucontroller_style_1' : 'cpus',
            'xtandem_style_1'     : 'spectrum, threads',
            'msfragger_style_1'   : 'num_threads',
            'pipi_style_1'        : 'thread_num',
            'moda_style_1'        : '-@',
            'pglyco_db_style_1'      : 'process',
        },
        'utag' : [
            'hardware_resources',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                -1 : 'max - 1',
            },
            'msgfplus_style_1' : {
                -1 : 'max - 1',
            },
            'myrimatch_style_1' : {
                -1 : 'max - 1',
            },
            'omssa_style_1' : {
                -1 : 'max - 1',
            },
            'ucontroller_style_1' : {
                -1 : 'max - 1',
            },
            'xtandem_style_1' : {
                -1 : 'max - 1',
            },
            'moda_style_1' : {
                -1 : 'max - 1',
            },
            'pglyco_db_style_1' : {
                -1 : 'max - 1',
            },
            'pipi_style_1' : {
                -1 : 'max - 1',
            },
            'msfragger_style_1' : {
                -1 : 'max - 1',
            },
        },
        'uvalue_type' : 'int _uevaluation_req',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : '_uevaluation_req',
            'min'       : -1,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : -1,
        'description' : \
            'Number of used cpus/threads\n\n'
            '    -1 : \'max - 1\'\n'
            '    >0 : cpu num',
    },
    'cross_link_definition' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'cross_link_definition',
        },
        'utag' : [
            'cross_linking',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'nK  nK  138.0680742 BS3',
        'description' : \
            'Cross-link and mono-link masses allowed.\n'\
            'May have more than one of each parameter.\n'\
            'Format for cross_link is: \n\n'\
            '**[amino acids] [amino acids] [mass mod] [identifier]**\n\n'\
            'One or more amino acids (uppercase only!!) can be specified for '\
            'each linkage moiety. Use lowercase \'n\' or \'c\' to indicate '\
            'protein N-terminus or C-terminus',
    },
    'csv_filter_rules' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'filter_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'filter_csv_style_1' : 'filter_rules',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
            'filter_csv_style_1' : {
            }
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : [],
            'item_title' : 'filter rule',
            'item_type' : 'list',
            'custom_val_max' : 0,
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Rules are defined as list of lists with three elements:\n\n'\
            '1. the column name/csv fieldname,\n\n'\
            '2. the rule,\n\n'\
            '3. the value which should be compared\n\n'\
            'e.g.: [\'Is decoy\', \'equals\', \'false\']'
    },
    'database' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'upeptide_mapper_1_0_0',
            'compomics_utilities_4_11_5',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pglyco_db_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'               : 'database',
            'moda_style_1'                : 'Fasta',
            'msamanda_style_1'            : 'database',
            'msgfplus_style_1'            : '-d',
            'myrimatch_style_1'           : 'ProteinDatabase',
            'omssa_style_1'               : '-d',
            'unify_csv_style_1'           : 'database',
            'xtandem_style_1'             : 'file URL',
            'upeptide_mapper_style_1'     : 'database',
            'compomics_utilities_style_1' : 'database',
            'msfragger_style_1'           : 'database_name',
            'pipi_style_1'                : 'db',
            'pglyco_db_style_1'           : 'fasta',
            'deepnovo_style_1'            : 'db_fasta_file',

        },
        'utag' : [
            'database',
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'         : '',
            'multiple_line'    : False,
            'input_extensions' : ['.fasta', '.fa']
        },
        'default_value' : None,
        'description' : \
            'Path to database file containing protein sequences in fasta format.'
    },
    'database_taxonomy' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'taxon label',
        },
        'utag' : [
            'database',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                'all' : 0,
            },
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'all',
        'description' : \
            'If a taxonomy ID is specified, only the corresponding protein '\
            'sequences from the fasta database are included in the search.',
    },
    'decoy_generation_mode' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'generate_target_decoy_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'generate_target_decoy_style_1' : 'mode',
        },
        'utag' : [
            'database',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type'    : 'radio_button',
            'available_values'  : ['reverse_protein', 'shuffle_peptide'],
            'custom_val_max' : 0,
        },
        'default_value' : 'shuffle_peptide',
        'description' : \
            'Decoy database: creates a target decoy database based on '\
            'shuffling of peptides (shuffle_peptide) or complete reversing '\
            'the protein sequence (reverse_protein).',
    },
    'decoy_tag' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'generate_target_decoy_1_0_0',
            'kojak_1_5_3',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
            'unify_csv_1_0_0',
            'xtandem2csv_1_0_0',
            'upeptide_mapper_1_0_0',
            'percolator_3_2_1',
            'percolator_3_4_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'generate_target_decoy_style_1' : 'decoy_tag',
            'kojak_style_1'                 : 'decoy_tag',
            'myrimatch_style_1'             : 'DecoyPrefix',
            'mzidentml_style_1'             : '-decoyRegex',
            'unify_csv_style_1'             : 'decoy_tag',
            'xtandem2csv_style_1'           : 'decoy_tag',
            'upeptide_mapper_style_1'       : 'decoy_tag',

        },
        'utag' : [
            'database',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'decoy_',
        'description' : \
            'decoy-specific tag to differentiate between targets and decoys',
    },
    'deisotope_spec' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'PerformDeisotoping',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
            'msamanda_style_1' : {
                False : 'false',
                True  : 'true',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : 'Perform Deisotoping for MS2 spectra',
    },
    'del_from_params_before_json_dump' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'del_from_params_before_json_dump',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title'   : 'del param',
            'item_type' : 'str',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
            'grouped_psms',
        ],
        'description' : \
            'List of parameters that are deleted before .json is dumped '\
            '(to not overload the .json with unimportant informations)',
    },
    'denovo_model' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-model',
        },
        'utag' : [
            'model',
            'denovo'
        ],
        'uvalue_translation' : {
            'pepnovo_style_1' : {
                'cid_trypsin' : 'CID_IT_TRYP',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['cid_trypsin'],
            'custom_val_max' : 1,
        },
        'default_value' : 'cid_trypsin',
        'description' : \
            'PepNovo model used for de novo sequencing. Based on the enzyme '\
            'and fragmentation type. Currently only CID_IT_TRYP available.',
    },
    'denovo_model_dir' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-model_dir',
            'deepnovo_style_1': 'train_dir',
        },
        'utag' : [
            'model',
            'file_handling',
        ],
        'uvalue_translation' : {
            'pepnovo_style_1' : {
                'default' : None
            },
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : 'default',
        'description' : \
            'Directory containing the model files de novo sequencing. Use "default" for the default folder of the engine (DeepNovo: <deepnovo_resources>/train.example; PepNovo: resources/<platform>/<architecture>/pepnovo_3_1)'
    },
    'engine_internal_decoy_generation' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'generate_decoy',
            'msgfplus_style_1' : '-tda',
            'xtandem_style_1'  : 'scoring, include reverse',
            'pipi_style_1'     : 'add_decoy'
        },
        'utag' : [
            'database',
        ],
        'uvalue_translation' : {
            'msamanda_style_1' : {
                False : 'false',
                True  : 'true',
            },
            'msgfplus_style_1' : {
                False : '0',
                True  : '1',
            },
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
            'pipi_style_1' : {
                False : '0',
                True  : '1',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Engine creates an own decoy database. Not recommended, because a '\
            'target decoy database should be generated independently from the '\
            'search engine, e.g. by using the uNode generate_target_decoy_1_0_0',
    },
    'engines_create_folders' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'engines_create_folders',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Create folders for the output of engines that allow this option '\
            'in their META_INFO (\'create_own_folder\' : True). True or False',
    },
    'enzyme' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'generate_target_decoy_1_0_0',
            'kojak_1_5_3',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'percolator_2_08',
            'percolator_3_2_1',
            'percolator_3_4_0',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pglyco_db_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'generate_target_decoy_style_1' : 'enzyme',
            'kojak_style_1'                 : 'enzyme',
            'moda_style_1'                  : 'Enzyme',
            'msamanda_style_1'              : 'enzyme specificity',
            'msgfplus_style_1'              : '-e',
            'myrimatch_style_1'             : 'CleavageRules',
            'novor_style_1'                 : 'enzyme',
            'omssa_style_1'                 : '-e',
            'pepnovo_style_1'               : '-digest',
            'percolator_style_1'            : 'enzyme',
            'unify_csv_style_1'             : 'enzyme',
            'xtandem_style_1'               : 'protein, cleavage site',
            'msfragger_style_1'             : 'enzyme',
            'percolator_style_1'            : 'enz',
            'pipi_style_1'                  : 'enzyme',
            'pglyco_db_style_1'             : 'enzyme',
            'deepnovo_style_1'              : 'cleavage_rule',
        },
        'utag' : [
            'database',
            'protein',
            'cleavage',
        ],
        'uvalue_translation' : {
            'generate_target_decoy_style_1' : {
                'argc'                  : 'R;C;P',
                'aspn'                  : 'D;N;',
                'chymotrypsin'          : 'FMWY;C;P',
                'chymotrypsin_p'        : 'FMWY;C;',
                'clostripain'           : 'R;C;',
                'cnbr'                  : 'M;C;P',
                'elastase'              : 'AGILV;C;P',
                'formic_acid'           : 'D;C;P',
                'gluc'                  : 'DE;C;P',
                'gluc_bicarb'           : 'E;C;P',
                'iodosobenzoate'        : 'W;C;',
                'lysc'                  : 'K;C;P',
                'lysc_gluc'             : 'DEK;C;P',
                'lysc_p'                : 'K;C;',
                'lysn'                  : 'K;N;',
                'lysn_promisc'          : 'AKRS;N;',
                'pepsina'               : 'FL;C;',
                'protein_endopeptidase' : 'P;C;',
                'staph_protease'        : 'E;C;',
                'trypsin'               : 'KR;C;P',
                'trypsin_cnbr'          : 'KRM;C;P',
                'trypsin_gluc'          : 'DEKR;C;P',
                'trypsin_p'             : 'KR;C;',
            },
            'kojak_style_1' : {
                'gluc'                  : '[DE]|{P}',
                'lysc_gluc'             : '[DEK]|{P}',
                'lysn'                  : '|[K]',
                'trypsin'               : '[KR]|{P}',
                'trypsin_p'             : '[RK]|',
            },
            'moda_style_1' : {
                'argc'                  : 'argc, R/C',
                'aspn'                  : 'aspn, D/N;',
                'chymotrypsin'          : 'chymotrypsin, FMWY/C',
                'chymotrypsin_p'        : 'chymotrypsin, FMWY/C',
                'clostripain'           : 'clostripain, R/C',
                'cnbr'                  : 'cnbr, M/C',
                'elastase'              : 'elastase, AGILV/C',
                'formic_acid'           : 'formic_acid, D/C',
                'gluc'                  : 'gluc, DE/C',
                'gluc_bicarb'           : 'gluc_bicarb, E/C',
                'iodosobenzoate'        : 'iodosobenzoate, W/C',
                'lysc'                  : 'lysc, K/C',
                'lysc_p'                : 'lysc_p, K/C',
                'lysn'                  : 'lysn, K/N',
                'lysn_promisc'          : 'lysn_promisc, AKRS/N',
                'no_cleavage'           : 'NONE',
                'pepsina'               : 'pepsina, FL/C',
                'protein_endopeptidase' : 'protein_endopeptidase, P/C',
                'staph_protease'        : 'staph_protease, E/C',
                'trypsin'               : 'trypsin, KR/C',
                'trypsin_cnbr'          : 'trypsin_cnbr, KRM/C',
                'trypsin_gluc'          : 'trypsin_gluc, DEKR/C',
                'trypsin_p'             : 'trypsin_p, KR/C',
            },
            'msamanda_style_1' : {
                'argc'                  : 'R;after;P',
                'aspn'                  : 'D;before;',
                'chymotrypsin'          : 'FMWY;after;P',
                'chymotrypsin_p'        : 'FMWY;after;',
                'clostripain'           : 'R;after;',
                'cnbr'                  : 'M;after;P',
                'elastase'              : 'AGILV;after;P',
                'formic_acid'           : 'D;after;P',
                'gluc'                  : 'DE;after;P',
                'gluc_bicarb'           : 'E;after;P',
                'iodosobenzoate'        : 'W;after;',
                'lysc'                  : 'K;after;P',
                'lysc_gluc'             : 'DEK;after;P',
                'lysc_p'                : 'K;after;',
                'lysn'                  : 'K;before;',
                'lysn_promisc'          : 'AKRS;before;',
                'nonspecific'           : ';;',
                'pepsina'               : 'FL;after;',
                'protein_endopeptidase' : 'P;after;',
                'staph_protease'        : 'E;after;',
                'trypsin'               : 'KR;after;P',
                'trypsin_cnbr'          : 'KRM;after;P',
                'trypsin_gluc'          : 'DEKR;after;P',
                'trypsin_p'             : 'KR;after;',
            },
            'msgfplus_style_1' : {
                'alpha_lp'              : '8',
                'argc'                  : '6',
                'aspn'                  : '7',
                'chymotrypsin'          : '2',
                'gluc'                  : '5',
                'lysc'                  : '3',
                'lysn'                  : '4',
                'no_cleavage'           : '9',
                'nonspecific'           : '0',
                'trypsin'               : '1',
                'trypsin_p'             : '1',
            },
            'myrimatch_style_1' : {
                'aspn'                  : 'Asp-N',
                'chymotrypsin'          : 'Chymotrypsin',
                'cnbr'                  : 'CNBr',
                'formic_acid'           : 'Formic_acid',
                'lysc'                  : 'Lys-C',
                'lysc_p'                : 'Lys-C/P',
                'pepsina'               : 'PepsinA',
                'trypsin'               : 'Trypsin',
                'trypsin_chymotrypsin'  : 'TrypChymo',
                'trypsin_p'             : 'Trypsin/P',
            },
            'novor_style_1' : {
                'trypsin'               : 'Trypsin',
            },
            'omssa_style_1' : {
                'argc'                  : '1',
                'aspn'                  : '12',
                'aspn_gluc'             : '14',
                'chymotrypsin'          : '3',
                'chymotrypsin_p'        : '18',
                'cnbr'                  : '2',
                'formic_acid'           : '4',
                'gluc'                  : '13',
                'lysc'                  : '5',
                'lysc_p'                : '6',
                'lysn'                  : '21',
                'no_cleavage'           : '11',
                'nonspecific'           : '17',
                'pepsina'               : '7',
                'thermolysin_p'         : '22',
                'top_down'              : '15',
                'trypsin'               : '0',
                'trypsin_chymotrypsin'  : '9',
                'trypsin_cnbr'          : '8',
                'trypsin_p'             : '10',
            },
            'pepnovo_style_1' : {
                'nonspecific'           : 'NON_SPECIFIC',
                'trypsin'               : 'TRYPSIN',
            },
            'percolator_style_1' : {
                'argc'                  : 'R;C;P',
                'aspn'                  : 'D;N;',
                'chymotrypsin'          : 'FMWY;C;P',
                'chymotrypsin_p'        : 'FMWY;C;',
                'clostripain'           : 'R;C;',
                'cnbr'                  : 'M;C;P',
                'elastase'              : 'AGILV;C;P',
                'formic_acid'           : 'D;C;P',
                'gluc'                  : 'DE;C;P',
                'gluc_bicarb'           : 'E;C;P',
                'iodosobenzoate'        : 'W;C;',
                'lysc'                  : 'K;C;P',
                'lysc_gluc'             : 'DEK;C;P',
                'lysc_p'                : 'K;C;',
                'lysn'                  : 'K;N;',
                'lysn_promisc'          : 'AKRS;N;',
                'pepsina'               : 'FL;C;',
                'protein_endopeptidase' : 'P;C;',
                'staph_protease'        : 'E;C;',
                'trypsin'               : 'KR;C;P',
                'trypsin_cnbr'          : 'KRM;C;P',
                'trypsin_gluc'          : 'DEKR;C;P',
                'trypsin_p'             : 'KR;C;',
                'nonspecific'           : 'ACDEFGHIKLMNPQRSTVWY;C;'
            },
            'unify_csv_style_1' : {
                'argc'                  : 'R;C;P',
                'aspn'                  : 'D;N;',
                'chymotrypsin'          : 'FMWY;C;P',
                'chymotrypsin_p'        : 'FMWY;C;',
                'clostripain'           : 'R;C;',
                'cnbr'                  : 'M;C;P',
                'elastase'              : 'AGILV;C;P',
                'formic_acid'           : 'D;C;P',
                'gluc'                  : 'DE;C;P',
                'gluc_bicarb'           : 'E;C;P',
                'iodosobenzoate'        : 'W;C;',
                'lysc'                  : 'K;C;P',
                'lysc_gluc'             : 'DEK;C;P',
                'lysc_p'                : 'K;C;',
                'lysn'                  : 'K;N;',
                'lysn_promisc'          : 'AKRS;N;',
                'pepsina'               : 'FL;C;',
                'protein_endopeptidase' : 'P;C;',
                'staph_protease'        : 'E;C;',
                'trypsin'               : 'KR;C;P',
                'trypsin_cnbr'          : 'KRM;C;P',
                'trypsin_gluc'          : 'DEKR;C;P',
                'trypsin_p'             : 'KR;C;',
                'nonspecific'           : 'ACDEFGHIKLMNPQRSTVWY;C;'
            },
            'xtandem_style_1' : {
                'argc'                  : '[R]|{P}',
                'aspn'                  : '[X]|[D]',
                'chymotrypsin'          : '[FMWY]|{P}',
                'chymotrypsin_p'        : '[FMWY]|[X]',
                'clostripain'           : '[R]|[X]',
                'cnbr'                  : '[M]|{P}',
                'elastase'              : '[AGILV]|{P}',
                'formic_acid'           : '[D]|{P}',
                'gluc'                  : '[DE]|{P}',
                'gluc_bicarb'           : '[E]|{P}',
                'iodosobenzoate'        : '[W]|[X]',
                'lysc'                  : '[K]|{P}',
                'lysc_gluc'             : '[DEK]|[X]|{P}',
                'lysc_p'                : '[K]|[X]',
                'lysn'                  : '[X]|[K]',
                'lysn_promisc'          : '[X]|[AKRS]',
                'nonspecific'           : '[X]|[X]',
                'pepsina'               : '[FL]|[X]',
                'protein_endopeptidase' : '[P]|[X]',
                'staph_protease'        : '[E]|[X]',
                'tca'                   : '[FMWY]|{P},[KR]|{P},[X]|[D]',
                'trypsin'               : '[KR]|{P}',
                'trypsin_cnbr'          : '[KR]|{P},[M]|{P}',
                'trypsin_gluc'          : '[DEKR]|{P}',
                'trypsin_p'             : '[RK]|[X]',
            },
            'msfragger_style_1' : {
                'argc' : 'R;C;P',
                'aspn' : 'D;N;',
                'chymotrypsin' : 'FMWY;C;P',
                'chymotrypsin_p' : 'FMWY;C;',
                'clostripain' : 'R;C;',
                'cnbr' : 'M;C;P',
                'elastase' : 'AGILV;C;P',
                'formic_acid' : 'D;C;P',
                'gluc' : 'DE;C;P',
                'gluc_bicarb' : 'E;C;P',
                'iodosobenzoate' : 'W;C;',
                'lysc' : 'K;C;P',
                'lysc_gluc' : 'DEK;C;P',
                'lysc_p' : 'K;C;',
                'lysn' : 'K;N;',
                'lysn_promisc' : 'AKRS;N;',
                'pepsina' : 'FL;C;',
                'protein_endopeptidase' : 'P;C;',
                'staph_protease' : 'E;C;',
                'trypsin' : 'KR;C;P',
                'trypsin_cnbr' : 'KRM;C;P',
                'trypsin_gluc' : 'DEKR;C;P',
                'trypsin_p' : 'KR;C;',
                'nonspecific' : 'ACDEFGHIKLMNPQRSTVWY;C;',
            },
            'pipi_style_1' : {
                'aspn' : 'AspN;0;D;-',
                'chymotrypsin' : 'Chymotrypsin;1;FMWY;P',
                'gluc' : 'GluC;1;DE;P',
                'lysc_p' : 'LysC;1;K;-',
                'lysn' : 'LysN;0;K;-',
                'trypsin' : 'Trypsin;1;KR;P',
            },
            'pglyco_db_style_1' : {
                'trypsin_p' : 'Trypsin_KR-C',
                'chymotrypsin' : 'Chymotrypsin_FYWL-P-C',
                'formic_acid_p' : 'FormicAcid_D-C',
                'lysc' : 'Lys_K-P-C',
                'lysc_p': 'Lys_K-C',
                'pepsina' : 'PepsinA_FL-C',
                'trypsin' : 'Trypsin_KR-P-C',
                'gluc' : 'GluC_DE-P-C'
            },
            'deepnovo_style_1' : {
                'argc': 'arg-c',
                'aspn': 'asp-n',
                'clostripain': 'clostripain',
                'cnbr': 'cnbr',
                'formic_acid': 'formic acid',
                'lysc': 'lysc',
                'trypsin': 'trypsin',
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'argc',
                'aspn',
                'aspn_gluc',
                'chymotrypsin',
                'chymotrypsin_p',
                'clostripain',
                'cnbr',
                'elastase',
                'formic_acid',
                'gluc',
                'gluc_bicarb',
                'iodosobenzoate',
                'lysc',
                'lysc_p',
                'lysn',
                'lysn_promisc',
                'no_cleavage',
                'nonspecific',
                'pepsina',
                'protein_endopeptidase',
                'staph_protease',
                'tca',
                'thermolysin_p',
                'top_down',
                'trypsin',
                'trypsin_chymotrypsin',
                'trypsin_cnbr',
                'trypsin_gluc',
                'trypsin_p'
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'trypsin',
        'description' :  \
            'Enzyme: Rule of protein cleavage'\
            'Possible cleavages are :\n'\
            '    argc           -> [R]|{P}\n'\
            '    aspn           -> [X]|[D]\n'\
            '    aspn_gluc\n'\
            '    chymotrypsin   -> [FMWY]|{P}\n'\
            '    chymotrypsin_p -> [FMWY]|[X]\n'\
            '    cnbr           -> [M]|{P}\n'\
            '    elastase       -> [AGILV]|{P}\n'\
            '    formic_acid    -> [D]|{P}\n'\
            '    gluc\n'\
            '    lysc\n'\
            '    lysc_p\n'\
            '    lysn\n'\
            '    no_cleavage\n'\
            '    nonspecific\n'\
            '    pepsina\n'\
            '    semi_chymotrypsin\n'\
            '    semi_gluc\n'\
            '    semi_tryptic\n'\
            '    thermolysin_p\n'\
            '    top_down\n'\
            '    trypsin\n'\
            '    trypsin_chymotrypsin\n'\
            '    trypsin_cnbr\n'\
            '    trypsin_p\n'\
            '    lysc_gluc',
    },
    'fdr_cutoff' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'svm_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'svm_style_1' : 'fdr_cutoff',
        },
        'utag' : [
            'scoring',
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1,
            'min'       : 0,
            'f-point'   : 1e-03,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.01,
        'description' : \
            'Target PSMs with a lower FDR than this threshold will be used as '\
            'a positive training set for SVM post-processing',
    },
    'forbidden_cterm_mods' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'residue, potential modification mass',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'unimod name',
            'item_type' : 'str',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
        ],
        'description' : \
            'List of modifications (unimod name) that are not allowed to '\
            'occur at the C-terminus of a peptide, e.g. [\'GG\']',
    },
    'forbidden_residues' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'novor_1_1beta',
            'novor_1_05',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'novor_style_1' : 'forbiddenResidues',
        },
        'utag' : [
            'denovo',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'I,U',
        'description' : \
            'Aminoacids that are not allowed during/taken into account during '\
            'denovo searches. Given as a string of comma seperated aminoacids '\
            '(single letter code)',
    },
    'force' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'force',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'If set \'True\', engines are forced to re-run although no '\
            'node-related parameters have changed',
    },
    'frag_clear_mz_range' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'default_value' : [0.0, 0.0],
        'description' :  ''' Removes peaks in this m/z range prior to matching. Given as list [min_clear_mz, max_clear_mz]. Useful for iTRAQ/TMT experiments, i.e. [0.0, 150.0]. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'clear_mz_range',
            'pipi_style_1' : 'frag_clear_mz_range',
        },
        'utag' : [
            'fragment',
            'spectrum'
        ],
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'mz value',
            'item_type' : 'float',
            'custom_val_max' : 2,
            'max': 100000,
            'min': 0,
            'unit': 'm/z',
            'updownval': 1,
            'custom_type' : {
                'int' : {
                    'max'       : 10000,
                    'min'       : 0,
                    'updownval' : 1,
                    'unit'      : '',
                },
            },
            'custom_val_max' : 100000,
            'f-point': 1e-01,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "list",
    },
    'frag_mass_tolerance' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'pglyco_db_2_2_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'      : 'FragTolerance',
            'msamanda_style_1'  : 'ms2_tol',
            'myrimatch_style_1' : 'FragmentMzTolerance',
            'novor_style_1'     : 'fragmentIonErrorTol',
            'omssa_style_1'     : '-to',
            'pepnovo_style_1'   : '-fragment_tolerance',
            'xtandem_style_1'   : 'spectrum, fragment monoisotopic mass error',
            'msfragger_style_1' : 'fragment_mass_tolerance',
            'pipi_style_1'      : 'ms2_tolerance',
            'pyqms_style_1'      : 'REL_MZ_RANGE',
            'sugarpy_run_style_1': 'REL_MZ_RANGE',
            'sugarpy_plot_style_1': 'REL_MZ_RANGE',
            'pglyco_db_style_1'    : 'search_fragment_tolerance',
        },
        'utag' : [
            'fragment',
            'accuracy'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 20,
        'description' : \
            'Mass tolerance of measured and calculated fragment ions',
    },
    'frag_mass_tolerance_unit' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'pglyco_db_2_2_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'      : 'FragTolerance',
            'msamanda_style_1'  : 'ms2_tol unit',
            'myrimatch_style_1' : 'FragmentMzTolerance',
            'novor_style_1'     : 'fragmentIonErrorTol',
            'omssa_style_1'     : 'frag_mass_tolerance_unit',
            'pepnovo_style_1'   : 'frag_mass_tolerance_unit',
            'xtandem_style_1'   : 'spectrum, fragment monoisotopic mass error units',
            'msfragger_style_1' : 'fragment_mass_units',
            'pipi_style_1'      : 'frag_mass_tolerance_unit',
            'pyqms_style_1'      : 'REL_MZ_RANGE',
            'sugarpy_run_style_1': 'REL_MZ_RANGE',
            'sugarpy_plot_style_1': 'REL_MZ_RANGE',
            'pglyco_db_style_1'    : 'search_fragment_tolerance_type',
        },
        'utag' : [
            'fragment',
            'accuracy',
        ],
        'uvalue_translation' : {
            'msamanda_style_1' : {
                'da' : 'Da',
            },
            'myrimatch_style_1' : {
                'da' : 'Da',
            },
            'novor_style_1' : {
                'da' : 'Da',
            },
            'omssa_style_1' : {
                'da' : 'Da',
            },
            'xtandem_style_1' : {
                'da' : 'Daltons',
            },
            'msfragger_style_1' : {
                'ppm' : 1,
                'da'  : 0
            },
            'pglyco_db_style_1' : {
                'da'  : 'Da',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['da', 'mmu', 'ppm'],
            'custom_val_max' : 0,
        },
        'default_value' : 'ppm',
        'description' : \
            'Fragment mass tolerance unit: available in ppm '\
            '(parts-per-millon), da (Dalton) or mmu (Milli mass unit)',
    },
    'frag_mass_type' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-tom',
            'xtandem_style_1' : 'spectrum, fragment mass type',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                'average'      : '1',
                'monoisotopic' : '0',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['average', 'monoisotopic'],
            'custom_val_max' : 0,
        },
        'default_value' : 'monoisotopic',
        'description' : \
            'Fragment mass type: monoisotopic or average',
    },
    'frag_max_charge' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-zoh',
            'msfragger_style_1': 'max_fragment_charge',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 4,
        'description' : \
            'Maximum fragment ion charge to search.',
    },
    'frag_method' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'novor_1_1beta',
            'novor_1_05',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1' : '-m',
            'novor_style_1'    : 'fragmentation',
        },
        'utag' : [
            'instrument',
            'fragment',
            'model',
        ],
        'uvalue_translation' : {
            'msgfplus_style_1' : {
                'cid' : '1',
                'etd' : '2',
                'hcd' : '3',
            },
            'novor_style_1' : {
                'cid' : 'CID',
                'hcd' : 'HCD',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['cid', 'ecd', 'etd', 'hcd'],
            'custom_val_max' : 0,
        },
        'default_value' : 'hcd',
        'description' : \
            'Used fragmentation method, e.g. collision-induced dissociation '\
            '(cid), electron-capture dissociation (ecd), electron-transfer '\
            'dissociation (etd), Higher-energy C-trap dissociation (hcd)',
    },
    'frag_min_mz' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'spectrum, minimum fragment mz',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 150,
        'description' : \
            'Minimal considered fragment ion m/z',
    },
    'ftp_blocksize' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_blocksize',
        },
        'utag' : [
            'download',
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1000000000,
            'min'       : 1,
            'updownval' : 1,
            'unit'      : 'bytes'
        },
        'default_value' : 1024,
        'description' : \
            'Blocksize for ftp download',
    },
    'ftp_folder' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_folder',
        },
        'utag' : [
            'download',
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            '''ftp folder that should be downloaded'''
    },
    'ftp_include_ext' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_include_ext',
        },
        'utag' : [
            'download',
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : '''Only files with the defined file extension are downloaded with ftp download'''
    },
    'ftp_login' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_login',
        },
        'utag' : [
            'download',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Login name/user for the ftp server e.g. "PASS00269" in peptideatlas.org'\
            'ftp download\n'\
            '    \'\' : None',
    },
    'ftp_max_number_of_files' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_max_number_of_files',
        },
        'utag' : [
            'download',
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : 0,
            'max'       : 1000000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : 'files'
        },
        'default_value' : None,
        'description' : \
            'Maximum number of files that will be downloaded\n'\
            '     0 : No Limitation',
    },
    'ftp_output_folder' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_output_folder',
        },
        'utag' : [
            'download',
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Default ftp download path\n'\
            '    \'\' : None',
    },
    'ftp_password' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_password',
        },
        'utag' : [
            'download',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str_password',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'ftp download password\n'\
            '    \'\' : None',
    },
    'ftp_url' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_ftp_style_1' : 'ftp_url',
        },
        'utag' : [
            'download',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'ftp download URL, will fail if it is not set by the user\n'\
            '    \'\' : None',
    },
    'header_translations' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'kojak_percolator_2_08',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus2csv_v2016_09_16',
            'msgfplus2csv_v2017_01_27',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'msgfplus2csv_v2017_07_04',
            'msgfplus2csv_v1_2_0',
            'msgfplus2csv_v1_2_1',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pglyco_db_2_2_0',
            'pglyco_fdr_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_percolator_style_1' : 'header_translations',
            'msamanda_style_1'         : 'header_translations',
            'msgfplus_style_1'         : 'header_translations',
            'novor_style_1'            : 'header_translations',
            'omssa_style_1'            : 'header_translations',
            'pepnovo_style_1'          : 'header_translations',
            'msfragger_style_1'        : 'header_translations',
            'pipi_style_1'             : 'header_translations',
            'pglyco_db_style_1'        : 'header_translations',
            'pglyco_fdr_style_1'       : 'header_translations',
            'deepnovo_style_1'         : 'header_translations',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
            'kojak_percolator_style_1' : {
                'PSMId'                : 'PSMId',
                'peptide'              : 'Sequence',
                'posterior_error_prob' : 'PEP',
                'proteinIds'           : 'Protein ID',
                'q-value'              : 'q-value',
                'score'                : 'Kojak:score',
            },
            'msamanda_style_1' : {
                'Amanda Score'         : 'Amanda:Score',
                'Charge'               : 'Charge',
                'Filename'             : 'Filename',
                'Modifications'        : 'Modifications',
                'Protein Accessions'   : 'proteinacc_start_stop_pre_post_;',
                'RT'                   : 'Retention Time (s)',
                'Rank'                 : 'Rank',
                'Scan Number'          : 'Spectrum ID',
                'Sequence'             : 'Sequence',
                'Title'                : 'Spectrum Title',
                'Weighted Probability' : 'Amanda:Weighted Probability',
                'm/z'                  : 'Exp m/z',
            },
            'msgfplus_style_1' : {
                'Charge'               : 'Charge',
                'DeNovoScore'          : 'MS-GF:DeNovoScore',
                'EValue'               : 'MS-GF:EValue',
                'MSGFScore'            : 'MS-GF:RawScore',
                'Peptide'              : 'Sequence',
                'Precursor'            : 'Exp m/z',
                'Protein'              : 'proteinacc_start_stop_pre_post_;',
                'ScanNum'              : 'Spectrum ID',
                'SpecEValue'           : 'MS-GF:SpecEValue',
                'SpecFile'             : 'Raw data location',
                '#SpecFile'            : 'Raw data location',
                'Title'                : 'Spectrum Title',
            },
            'novor_style_1' : {
                ' RT'                  : 'Retention Time (s)',
                ' aaScore'             : 'Novor:aaScore',
                ' err(data-denovo)'    : 'Error (exp-calc)',
                ' mz(data)'            : 'Exp m/z',
                ' pepMass(denovo)'     : 'Calc mass',
                ' peptide'             : 'Sequence',
                ' ppm(1e6*err/(mz*z))' : 'Error (ppm)',
                ' scanNum'             : 'Spectrum ID',
                ' score'               : 'Novor:score',
                ' z'                   : 'Charge',
                '# id'                 : 'Novor:id',
            },
            'omssa_style_1' : {
                ' Accession'           : 'Accession',
                ' Charge'              : 'Charge',
                ' Defline'             : 'proteinacc_start_stop_pre_post_;',
                ' E-value'             : 'OMSSA:evalue',
                ' Filename/id'         : 'Spectrum Title',
                ' Mass'                : 'Exp m/z',
                ' Mods'                : 'Modifications',
                ' NIST score'          : 'NIST score',
                ' P-value'             : 'OMSSA:pvalue',
                ' Peptide'             : 'Sequence',
                ' Start'               : 'Start',
                ' Stop'                : 'Stop',
                ' Theo Mass'           : 'Calc m/z',
                ' gi'                  : 'gi',
                'Spectrum number'      : 'Spectrum ID',
            },
            'pepnovo_style_1' : {
                '#Index'               : 'Pepnovo:id',
                'C-Gap'                : 'Pepnovo:C-Gap',
                'CumProb'              : 'Pepnovo:CumProb',
                'N-Gap'                : 'Pepnovo:N-Gap',
                'PnvScr'               : 'Pepnovo:PnvScr',
                'RnkScr'               : 'Pepnovo:RnkScr',
                '[M+H]'                : 'Calc mass(Da)',
                'output_aa_probs'      : 'Pepnovo:aaScore',
            },
            'pipi_style_1' : {
                'scan_num' : 'Spectrum ID',
                'peptide' : 'Sequence',
                'charge' : 'Charge',
                'theo_mass' : 'Calc m/z',
                'exp_mass' : 'Exp m/z',
                'abs_ppm' : 'PIPI:abs_ppm',
                'delta_C_n' : 'PIPI:delta_C_n',
                'protein_ID' : 'Protein ID',
                'score' : 'PIPI:score',
                'A_score' : 'A-Score',
                'labelling' : 'Label',
                'isotope_correction' : 'PIPI:isotope_correction',
                'MS1_pearson_correlation_coefficient' : 'PIPI:MS1_pearson_correlation_coefficient',
                'other_PTM_patterns' : 'PIPI:other_PTM_patterns',
                'MGF_title' : 'Spectrum Title',
            },
            'msfragger_style_1' : {
                'ScanID' : 'Spectrum ID',
                'Peptide Sequence' : 'Sequence',
                'Precursor charge': 'Charge',
                'Upstream Amino Acid': 'Sequence Pre AA',
                'Downstream Amino Acid' : 'Sequence Post AA',
                'Protein' : 'Protein ID',
                'Variable modifications detected':'Modifications', #'(starts with M, separated by |, formated as position,mass)
                'Retention time (minutes)': 'Retention Time (s)',
                'Precursor neutral mass (Da)' : 'MSFragger:Precursor neutral mass (Da)',
                'Neutral mass of peptide' : 'MSFragger:Neutral mass of peptide',# (including any variable modifications) (Da)
                'Hit rank':'Rank',
                'Mass difference':'Mass Difference',
                'Matched fragment ions':'MSFragger:Matched fragment ions',
                'Total possible number of matched theoretical fragment ions':'MSFragger:Total possible number of matched theoretical fragment ions',
                'Hyperscore':'MSFragger:Hyperscore',
                'Next score':'MSFragger:Next score',
                'Number of tryptic termini':'MSFragger:Number of tryptic termini',
                'Number of missed cleavages':'MSFragger:Number of missed cleavages',
                'Intercept of expectation model (expectation in log space)':'MSFragger:Intercept of expectation model (expectation in log space)',
                'Slope of expectation model (expectation in log space)':'MSFragger:Slope of expectation model (expectation in log space)',
            },
            'pglyco_db_style_1' : {
                'GlySpec': 'Spectrum Title',
                'PepSpec': 'Spectrum Title',
                'RawName': 'Spectrum Title',
                'Scan': 'Spectrum ID',
                'RT': 'Retention Time (s)',
                'PrecursorMH': 'Exp Mass',
                'PrecursorMZ': 'Exp m/z',
                'Charge': 'Charge',
                'Rank': 'Rank',
                'Peptide': 'Sequence',
                'Mod': 'Modifications',
                'PeptideMH': 'Calc Mass',
                'Glycan(H,N,A,G,F)': 'Glycan',
                'PlausibleStruct': 'Plausible Glycan Structure',
                'GlyID': 'Glycan ID',
                'GlyFrag': 'Glycan Fragments',
                'GlyMass': 'Glycan Mass',
                'GlySite': 'Glycosite',
                'TotalScore': 'pGlyco:TotalScore',
                'PepScore': 'pGlyco:PepScore',
                'GlyScore': 'pGlyco:GlyScore',
                'CoreMatched': 'CoreMatched',
                'CoreFuc': 'CoreFuc',
                'MassDeviation': 'Mass Difference',
                'PPM': 'Accuracy (ppm)',
                'GlyIonRatio': 'GlyIonRatio',
                'PepIonRatio': 'PepIonRatio',
                'GlyDecoy': 'GlyDecoy',
                'PepDecoy': 'PepDecoy',
            },
            'pglyco_fdr_style_1' : {
                'GlySpec': 'Spectrum Title',
                'PepSpec': 'Spectrum Title',
                'RawName': 'Spectrum Title',
                'Scan': 'Spectrum ID',
                'RT': 'Retention Time (s)',
                'PrecursorMH': 'Exp Mass',
                'PrecursorMZ': 'Exp m/z',
                'Charge': 'Charge',
                'Rank': 'Rank',
                'Peptide': 'Sequence',
                'Mod': 'Modifications',
                'PeptideMH': 'Calc Mass',
                'Glycan(H,N,A,G,F)': 'Glycan',
                'PlausibleStruct': 'Plausible Glycan Structure',
                'GlyID': 'Glycan ID',
                'GlyFrag': 'Glycan Fragments',
                'GlyMass': 'Glycan Mass',
                'GlySite': 'Glycosite',
                'TotalScore': 'pGlyco:TotalScore',
                'PepScore': 'pGlyco:PepScore',
                'GlyScore': 'pGlyco:GlyScore',
                'CoreMatched': 'CoreMatched',
                'CoreFuc': 'CoreFuc',
                'MassDeviation': 'Mass Difference',
                'PPM': 'Accuracy (ppm)',
                'GlyIonRatio': 'GlyIonRatio',
                'PepIonRatio': 'PepIonRatio',
                'GlyDecoy': 'GlyDecoy',
                'PepDecoy': 'PepDecoy',
                'GlycanFDR': 'Glycan FDR',
                'PeptideFDR': 'Peptide FDR',
                'TotalFDR': 'q-value',
            },
            'deepnovo_style_1' : {
                'predicted_position_score': 'DeepNovo:aaScore',
                'predicted_sequence': 'Sequence',
                'scan': 'Spectrum ID',
                'predicted_score': 'DeepNovo:score',
            },
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : 'None',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Translate output headers into Ursgal unify_csv style headers\n'\
            '    \'None\' : None',
    },
    'heatmap_annotation_field_name' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_annotation_field_name',
        },
        'utag' : [
            'visualization',
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'Protein',
        'description' : \
            'The name of the annotation to plot in the heatmap',
    },
    'heatmap_box_style' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_box_style',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'classic',
        'description' : \
            'Box style for the heatmap',
    },
    'heatmap_color_gradient' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_color_gradient',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'Spectral',
        'description' : \
            'Color gradient for the heatmap',
    },
    'heatmap_column_positions' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_column_positions',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : None,
            'item_titles' : {'position':'column name'},
            'value_types' : {'position':'str'},
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : {},
        'description' : \
            'The position of each column in the heatmap is given as a dict '\
            'with keys corresponding to the position and values corresponding'\
            'to the column name, e.g: {"0" : "Ratio1_2", "1" : "Ratio2_3"}',
    },
    'heatmap_error_suffix' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_error_suffix',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '_std',
        'description' : \
            'The suffix to identify the value error holding columns',
    },
    'heatmap_identifier_field_name' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_identifier_field_name',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'Protein',
        'description' : \
            'The name of the identifier to plot in the heatmap',
    },
    'heatmap_max_value' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_max_value',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 3,
        'description' : \
            'Maximum value for the color gradient',
    },
    'heatmap_min_value' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_min_value',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : -10000,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : -3,
        'description' : \
            'Minimum vaue for the color gradient',
    },
    'heatmap_value_suffix' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_value_suffix',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '_mean',
        'description' : \
            'The suffix to identify the value columns, which should be plotted',
    },
    'helper_extension' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'helper_extension',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '.u.json',
        'description' : \
            'Exension for helper files',
    },
    'http_output_folder' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_http_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_http_style_1' : 'http_output_folder',
        },
        'utag' : [
            'download',
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Default http download path\n'\
            '    \'\' : None',
    },
    'http_url' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_http_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_http_style_1' : 'http_url',
        },
        'utag' : [
            'download',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'http download URL, will fail if it is not set by the user\n'\
            '    \'\' : None',
    },
    'instrument' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'novor_1_1beta',
            'novor_1_05',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'    : 'instrument',
            'moda_style_1'     : 'Instrument',
            'msgfplus_style_1' : '-inst',
            'novor_style_1'    : 'massAnalyzer',
        },
        'utag' : [
            'instrument',
            'model',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                'FTICR'        : '1',
                'high_res_ltq' : '0',
                'low_res_ltq'  : '0',
                'q_exactive'   : '0',
            },
            'moda_style_1' : {
                'high_res_ltq' : 'ESI-TRAP',
                'low_res_ltq'  : 'ESI-TRAP',
                'q_exactive'   : 'ESI-TRAP',
                'tof'          : 'ESI-QTOF',
            },
            'msgfplus_style_1' : {
                'high_res_ltq' : '1',
                'low_res_ltq'  : '0',
                'q_exactive'   : '3',
                'tof'          : '2',
            },
            'novor_style_1' : {
                'high_res_ltq' : 'Trap',
                'low_res_ltq'  : 'Trap',
                'q_exactive'   : 'FT',
                'tof'          : 'TOF',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : [
                'high_res_ltq',
                'low_res_ltq',
                'q_exactive',
                'tof',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'q_exactive',
        'description' : \
            'Type of mass spectrometer (used to determine the scoring model)',
    },
    'identifier_column_names' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'csv2counted_results_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'csv2counted_results_style_1' : 'identifier_column_names',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'column_name',
            'item_type' : 'str',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
            'Protein ID',
        ],
        'description' : \
            'The (combination of) specified csv column name(s) are used as identifiers. '\
            'E.g. to count the number of peptides for these identifiers. '\
            'The parameter "count_column_names" defines the countable elements.',
    },
    'ion_mode' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_2_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'ion_mode',
        },
        'utag' : [
            'ionization',
        ],
        'uvalue_translation' : {
            'mzml2mgf_style_1': {
                'positive' : '+',
                'negative' : '-',
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['positive', 'negative'],
            'custom_val_max' : 1,
        },
        'default_value' : 'positive',
        'description' : \
            'The ion mode that has been used for acquiring mass spectra (positive or negative)'
    },
    'intensity_cutoff' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-cl',
            'msfragger_style_1': 'minimum_ratio'
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.0,
        'description' : \
            'Low intensity cutoff as a fraction of max peak',
    },
    'json_extension' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'json_extension',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '.u.json',
        'description' : \
            'Exension for .json files',
    },
    'keep_asp_pro_broken_peps' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'unify_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'unify_csv_style_1' : 'keep_asp_pro_broken_peps',
        },
        'utag' : [
            'protein',
            'cleavage',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'X!tandem searches for peptides broken between Asp (D) and '\
            'Pro (P) for every enzyme. Therefore, it reports peptides that '\
            'are not enzymatically cleaved. Specify, if those should be kept '\
            'during unify_csv or removed.',
    },
    'kernel' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'svm_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'svm_style_1' : 'kernel',
        },
        'utag' : [
            'scoring',
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['rbf', 'linear', 'poly', 'sigmoid'],
            'custom_val_max' : 1,
        },
        'default_value' : 'rbf',
        'description' : \
            'The kernel function of the support vector machine used for PSM '\
            'post-processing (\'rbf\', \'linear\', \'poly\' or \'sigmoid\')',
    },
    'ms1_is_centroided' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS1_centroid',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                True : 1,
                False  : 0,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'MS1 are centroided data: True or False',
    },
    'ms1_resolution' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS1_resolution',
        },
        'utag' : [
            'spectrum',
            'accuracy'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000000,
            'min'       : 0,
            'updownval' : 1000,
            'unit'      : ''
        },
        'default_value' : 30000,
        'description' : \
            'MS1 resolution',
    },
    'ms2_is_centroided' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS2_centroid',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                True : 1,
                False : 0,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'MS2 are centroided data: True or False',
    },
    'ms2_resolution' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS2_resolution',
        },
        'utag' : [
            'spectrum',
            'accuracy'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000000,
            'min'       : 0,
            'updownval' : 1000,
            'unit'      : ''
        },
        'default_value' : 25000,
        'description' : \
            'MS2 resolution',
    },
    'keep_column_names' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'csv2counted_results_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'csv2counted_results_style_1' : 'keep_column_names',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'column name',
            'item_type' : 'str',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
            'Protein ID',
        ],
        'description' : \
            'List of column headers which are are not used as identifiers but kept in the output, '\
            'e.g. when counting ["Sequence", "Modifications"] the column '\
            '["Protein ID"] could be specified here. Multiple entries '\
            'for one identifier (e.g. when identifier_column_names = ["Potein ID"] '\
            'and keep_column_names = ["Sequence"]) are seperated by "<#>".',
    },
    'kojak_diff_mods_on_xl' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_diff_mods_on_xl',
        },
        'utag' : [
            'cross_linking',
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'To search differential modifications on cross-linked peptides: '\
            'diff_mods_on_xl = 1',
    },
    'kojak_enrichment' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_enrichment',
        },
        'utag' : [
            'cross_linking',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1,
            'min'       : 0,
            'f-point'   : 1e-03,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'Values between 0 and 1 to describe 18O APE \n'\
            'For example, 0.25 equals 25 APE',
    },
    'kojak_export_pepxml' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_export_pepXML',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                True   : 1,
                False : 0,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Activate (True) or deactivate (False) output as pepXML',
    },
    'kojak_export_percolator' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_export_percolator',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                True   : 1,
                False  : 0,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Activate (True) or deactivate (False) output for percolator',
    },
    'kojak_fragment_bin_offset' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_fragment_bin_offset',
        },
        'utag' : [
            'accuracy',
            'hardware_resources'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1,
            'min'       : 0,
            'f-point'   : 1e-01,
            'updownval' : 0.1,
            'unit'      : ''
        },
        'default_value' : 0.0,
        'description' : \
            'fragment_bin_offset and fragment_bin_size\n'\
            'influence algorithm precision and memory usage.\n'\
            'They should be set appropriately for the data analyzed.\n'\
            'For ion trap ms/ms:  1.0005 size, 0.4 offset\n'\
            'For high res ms/ms:    0.03 size, 0.0 offset',
    },
    'kojak_fragment_bin_size' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_fragment_bin_size',
        },
        'utag' : [
            'accuracy',
            'hardware_resources'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 2,
            'min'       : 0,
            'f-point'   : 1e-04,
            'updownval' : 0.1,
            'unit'      : ''
        },
        'default_value' : 0.03,
        'description' : \
            'fragment_bin_offset and fragment_bin_size\n'\
            'influence algorithm precision and memory usage.\n'\
            'They should be set appropriately for the data analyzed.\n'\
            'For ion trap ms/ms:  1.0005 size, 0.4 offset\n'\
            'For high res ms/ms:    0.03 size, 0.0 offset',
    },
    'kojak_mono_links_on_xl' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_mono_links_on_xl',
        },
        'utag' : [
            'cross_linking',
            'modifications'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'To search for mono-linked cross-linker on cross-linked peptides: '\
            'mono_links_on_xl = 1',
    },
    'kojak_percolator_version' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_percolator_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '2.08',
        'description' : \
            'Defines the output format of Kojak for Percolator',
    },
    'kojak_prefer_precursor_pred' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_prefer_precursor_pred',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                'ignore_previous' : 0,
                'only_previous'   : 1,
                'supplement'      : 2,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : [
                'ignore_previous',
                'only_previous',
                'supplement',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'supplement',
        'description' : \
            'prefer precursor mono mass predicted by instrument software.\n'\
            'Available values:\n\n'\
            '    ignore_previous: previous predictions are ignored\n\n'\
            '    only_previous: only previous predictions are used\n\n'\
            '    supplement: predictions are supplemented with additional analysis',
    },
    'kojak_spectrum_processing' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_spectrum_processing',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : 0,
                True  : 1,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'True, if spectrum should be processed by kojak',
    },
    'kojak_top_count' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_top_count',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 300,
        'description' : \
            'number of top scoring single peptides to combine in relaxed '\
            'analysis',
    },
    'kojak_truncate_prot_names' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_truncate_prot_names',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'Max protein name character to export, 0=off',
    },
    'kojak_turbo_button' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_turbo_button',
        },
        'utag' : [
            'hardware_resources',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : 0,
                True  : 1,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Generally speeds up analysis. Special cases cause reverse '\
            'effect, thus this is allowed to be disabled. True if it should '\
            'be used.',
    },
    'label' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'      : 'label',
            'msamanda_style_1'  : 'label',
            'msgfplus_style_1'  : 'label',
            'myrimatch_style_1' : 'label',
            'omssa_style_1'     : ('-tem', '-tom'),
            'xtandem_style_1'   : 'protein, modified residue mass file',
            'msfragger_style_1' : 'label',
            'pipi_style_1'      : '15N',
            'pyqms_style_1'     : 'label'
        },
        'utag' : [
            'label',
            'modifications',
        ],
        'uvalue_translation' : {
            'pipi_style_1': {
                '14N' : 0,
                '15N' : 1,
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['14N', '15N'],
            'custom_val_max' : 0,
        },
        'default_value' : '14N',
        'description' : \
            '15N if the corresponding amino acid labeling was applied',
    },
    'machine_offset_in_ppm' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
            'mzml2mgf_2_0_0',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'machine_offset_in_ppm',
            'pyqms_style_1'    : 'MACHINE_OFFSET_IN_PPM',
            'sugarpy_run_style_1'  : 'MACHINE_OFFSET_IN_PPM',
            'sugarpy_plot_style_1'  : 'MACHINE_OFFSET_IN_PPM',
        },
        'utag' : [
            'conversion',
            'instrument',
            'accuracy',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.0,
        'description' : \
            'Machine offset, m/z values will be corected/shifted by the given '\
            'value.',
    },
    'max_accounted_observed_peaks' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'max_accounted_observed_peaks',
            'myrimatch_style_1' : 'MaxPeakCount',
            'xtandem_style_1'   : 'spectrum, total peaks',
            'msfragger_style_1' : 'use_topN_peaks'
        },
        'utag' : [
            'spectrum',
            'fragment',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 100,
        'description' : \
            'Maximum number of peaks from a spectrum used.',
    },
    'max_missed_cleavages' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'unify_csv_1_0_0',
            'upeptide_mapper_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'pglyco_db_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'           : 'max_missed_cleavages',
            'moda_style_1'            : 'MissedCleavage',
            'msamanda_style_1'        : 'missed_cleavages',
            'myrimatch_style_1'       : 'MaxMissedCleavages',
            'omssa_style_1'           : '-v',
            'xtandem_style_1'         : 'scoring, maximum missed cleavage sites',
            'unify_csv_style_1'       : 'max_missed_cleavages',
            'upeptide_mapper_style_1' : 'max_missed_cleavages',
            'msfragger_style_1'       : 'allowed_missed_cleavage',
            'pipi_style_1'            : 'missed_cleavage',
            'msgfplus_style_1'        : '-maxMissedCleavages',
            'pglyco_db_style_1'       : 'max_miss_cleave',
            'deepnovo_style_1'        : 'num_missed_cleavage',
        },
        'utag' : [
            'protein',
            'cleavage'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 2,
        'description' : \
            'Maximum number of missed cleavages per peptide',
    },
    'max_mod_alternatives' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, ptm complexity',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 6,
        'description' : \
            'Maximal number of variable modification alternatives, given as C '\
            'in 2^C',
    },
    'max_mod_size' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'MaxModSize',
            'pipi_style_1' : 'max_ptm_mass',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : -10000,
            'updownval' : 10,
            'unit'      : ''
        },
        'default_value' : 200,
        'description' : \
            'Maximum modification size to consider (in Da)',
    },
    'max_num_mods' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'pglyco_db_2_2_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'max_num_mods',
            'msgfplus_style_1'  : 'NumMods',
            'myrimatch_style_1' : 'MaxDynamicMods',
            'msamanda_style_1'  : 'MaxNoDynModifs',
            'pglyco_db_style_1'    : 'max_var_modify_num',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : 'mods'
        },
        'default_value' : 3,
        'description' : \
            'Maximal number of modifications per peptide',
    },
    'max_num_mod_sites' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
        ],
        'default_value' : 6,
        'description' :  ''' Maximum number of potential modification sites for a specific modification per peptide. Peptides with a higher number are discarded, due to a too high complexity. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1'  : 'MaxNumberModSites',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 20,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'max_num_neutral_loss' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
        ],
        'default_value' : 1,
        'description' :  ''' Maximum number of same neutral losses per peptide regarding water and ammonia losses. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1'  : 'MaxNumberNeutralLoss',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'max_num_neutral_loss_mod' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
        ],
        'default_value' : 2,
        'description' :  ''' Maximum number of same neutral losses per peptide regarding modification specific losses.  ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1'  : 'MaxNumberNeutralLossModificati',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 5,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'max_num_of_ions_per_series_to_search' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-sp',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                'all' : 0,
            },
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'Max number of ions in each series being searched\n'
            '     0 : all',
    },
    'max_num_per_mod' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
        ],
        'default_value' : 3,
        'description' :  ''' Maximum number of residues that can be occupied by each variable modification (maximum of 5) ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'max_variable_mods_per_mod',
            'msamanda_style_1'  : 'MaxNoModifs',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'max_num_per_mod_name_specific' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'residue, potential modification mass',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : {},
            'item_titles' : {
                'unimod_name' : 'number'
            },
            'value_types' : {
                'unimod_name' : 'int'
            },
            'custom_type' : {
                'int' : {
                    'max'       : 10000,
                    'min'       : 0,
                    'updownval' : 1,
                    'unit'      : '',
                },
            },
            'custom_val_max' : 0,
        },
        'default_value' : {
        },
        'description' : \
            'Maximal number of modification sites per peptide for a specific '\
            'modification, given as a dictionary: \n'\
            '    {unimod_name : number}',
    },
    'max_output_e_value' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1'   : '-he',
            'xtandem_style_1' : 'output, maximum valid expectation value',
        },
        'utag' : [
            'output',
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 1.0,
        'description' : \
            'Highest e-value for reported peptides',
    },
    'max_pep_length' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pglyco_db_2_2_0'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1'  : '-maxLength',
            'myrimatch_style_1' : 'MaxPeptideLength',
            'omssa_style_1'     : '-nox',
            'msfragger_style_1' : 'digest_max_length',
            'pipi_style_1' : 'max_peptide_length',
            'pglyco_db_style_1' : 'max_peptide_len',
        },
        'utag' : [
            'peptide',
            'cleavage',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 10,
            'unit'      : ''
        },
        'default_value' : 40,
        'description' : \
            'Maximal length of a peptide',
    },
    'max_pep_var' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1'  : '-maxLength',
            'myrimatch_style_1' : 'MaxPeptideVariants',
            'omssa_style_1'     : '-nox',
            'msfragger_style_1' : 'max_variable_mods_combinations'
        },
        'utag' : [
            'peptide',
            'modifications'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1000000000,
            'min'       : 0,
            'updownval' : 100000,
            'unit'      : ''
        },
        'default_value' : 1000,
        'description' : \
            'Maximal peptide variants, new default defined by msfragger',
    },
    'mgf_input_file' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'deepnovo_0_0_1',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'pglyco_db_2_2_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'     : 'Spectra',
            'msamanda_style_1' : 'mgf_input_file',
            'msgfplus_style_1' : '-s',
            'novor_style_1'    : '-f',
            'omssa_style_1'    : '-fm',
            'pepnovo_style_1'  : '-file',
            'xtandem_style_1'  : 'spectrum, path',
            'pglyco_db_style_1': 'file1',
            'deepnovo_style_1' : ('denovo_input_file', 'hybrid_input_file', 'db_input_file'),
        },
        'utag' : [
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'         : '',
            'multiple_line'    : False,
            'input_extensions' : ['.mgf']
        },
        'default_value' : None,
        'description' : \
            'Path to input .mgf file\n'\
            '    \'\' : None',
    },
    'min_mod_size' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'MinModSize',
            'pipi_style_1' : 'min_ptm_mass',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : -100000,
            'updownval' : 10,
            'unit'      : 'Da'
        },
        'default_value' : -200,
        'description' : \
            'Minimum modification size to consider (in Da)',
    },
    'min_output_score' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'MinResultScore',
            'pepnovo_style_1'   : '-min_filter_prob',
        },
        'utag' : [
            'output',
            'scoring',
        ],
        'uvalue_translation' : {
            'myrimatch_style_1' : {
                -1e-10    : 1e-07,
            },
            'pepnovo_style_1' : {
                -1e-10    : 0.9,
            },
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10,
            'min'       : -1e-10,
            'f-point'   : 1e-10,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : -1e-10,
        'description' : \
            'Lowest score for reported peptides. If set to \'-1e-10\', '\
            'default values fo each engine will be used.\n'\
            '    -1e-10 = \'default\'',
    },
    'min_pep_length' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pglyco_db_2_2_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1'  : '-minLength',
            'myrimatch_style_1' : 'MinPeptideLength',
            'omssa_style_1'     : '-no',
            'msfragger_style_1' : 'digest_min_length',
            'msamanda_style_1'  : 'MinimumPepLength',
            'pipi_style_1'      : 'min_peptide_length',
            'pglyco_db_style_1'    : 'min_peptide_len',
        },
        'utag' : [
            'peptide',
            'cleavage'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 6,
        'description' : \
            'Minimal length of a peptide',
    },
    'min_precursor_matches' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-pc',
        },
        'utag' : [
            'precursor',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 1,
        'description' : \
            'Minimum number of precursors that match a spectrum.',
    },
    'min_required_matched_peaks' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'MinMatchedFragments',
            'omssa_style_1'     : '-hm',
            'xtandem_style_1'   : 'scoring, minimum ion count',
            'msfragger_style_1' : 'min_matched_fragments'
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 4,
        'description' : \
            'Mimimum number of matched ions required for a peptide to be scored, MSFragger default: 4',
    },
    'min_required_observed_peaks' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-hs',
            'xtandem_style_1' : 'spectrum, minimum peaks',
            'msfragger_style_1': 'minimum_peaks',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 5,
        'description' : \
            'Mimimum number of peaks in the spectrum to be considered. MSFragger default: 15',
    },
    'moda_blind_mode' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'BlindMode',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
            'moda_style_1' : {
                'no_modification'   : 0,
                'one_modification'  : 1,
                'no_limit'          : 2,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : [
                'no_modification',
                'one_modification',
                'no_limit',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'no_limit',
        'description' : \
            'Allowed number of modifications per peptide in ModA BlindMode. \n'\
            'Available values:'
            '    no_modification\n'\
            '    one_modification\n'\
            '    no_limit',
    },
    'moda_high_res' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'HighResolution',
        },
        'utag' : [
            'fragment',
            'accuracy',
        ],
        'uvalue_translation' : {
            'moda_style_1' : {
                False : 'OFF',
                True  : 'ON',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'If True, fragment tolerance is set as the same as precursor '\
            'tolerance, when the peptide mass is significantly small, such '\
            'that fragment tolerance is larger than precursor tolerance',
    },
    'moda_protocol_id' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'Protocol',
        },
        'utag' : [
            'scoring',
            'label'
        ],
        'uvalue_translation' : {
            'moda_style_1' : {
                'None' : 'NONE',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : [
                'None',
                'iTRAQ4plex',
                'iTRAQ8plex',
                'TMT2plex',
                'TMT6plex'
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'None',
        'description' : \
            'MODa specific protocol to enable scoring parameters for labeled '\
            'samples.',
    },
    'modifications' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'unify_csv_1_0_0',
            'upeptide_mapper_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
            'pglyco_db_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'           : 'modifications',
            'moda_style_1'            : 'ADD',
            'msamanda_style_1'        : 'modifications',
            'msgfplus_style_1'        : '-mod',
            'myrimatch_style_1'       : ('DynamicMods', 'StaticMods'),
            'novor_style_1'           : ('variableModifications', 'fixedModifications'),
            'omssa_style_1'           : ('-mv', 'mf'),
            'pepnovo_style_1'         : '-PTMs',
            'unify_csv_style_1'       : 'modifications',
            'upeptide_mapper_style_1' : 'modifications',
            'msfragger_style_1'       : 'modifications',
            'pipi_style_1'            : 'modifications',
            'xtandem_style_1'         : (
                'residue, modification mass',
                'residue, potential modification mass',
                'protein, N-terminal residue modification mass',
                'protein, C-terminal residue modification mass',
                'protein, C-terminal residue modification mass',
                'protein, quick acetyl',
                'protein, quick pyrolidone'
            ),
            'pyqms_style_1' : 'modifications',
            'pglyco_db_style_1' : 'modifications',
            'deepnovo_style_1' : 'modifications',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'modification',
            'item_type' : 'str',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
            '*,opt,Prot-N-term,Acetyl',
            'M,opt,any,Oxidation',
        ],
        'description' : \
            'Modifications are given as a list of strings, each representing '\
            'the modification of one amino acid. The string consists of four '\
            'informations seperated by comma: \n\n'\
            '    \'amino acid, type, position, unimod name or id\'\n\n'\
            '    amino acid  : specify the modified amino acid as a single '\
            'letter, use \'*\' if the amino acid is variable\n'\
            '    type        : specify if it is a fixed (fix) or potential '\
            '(opt) modification\n'\
            '    position    : specify the position within the '\
            'protein/peptide (Prot-N-term, Prot-C-term), use \'any\' if the '\
            'positon is variable\n'\
            '    unimod name or id: specify the unimod PSI-MS Name '\
            'or unimod Accession # (see unimod.org)\n'\
            '\n'\
            'Examples:\n\n'\
            '    [ \'M,opt,any,Oxidation\' ] - potential oxidation of Met at '\
            'any position within a peptide\n'\
            '    [ \'*,opt,Prot-N-term,Acetyl\' ] - potential acetylation of '\
            'any amino acid at the N-terminus of a protein\n'\
            '    [ \'S,opt,any,Phospho\' ] - potential phosphorylation of '\
            'Serine at any position within a peptide\n'\
            '    [ \'C,fix,any,Carbamidomethyl\', \'N,opt,any,Deamidated\', '\
            '\'Q,opt,any,Deamidated\' ] - fixed carbamidomethylation of Cys '\
            'and potential deamidation of Asn and/or Gln at any position '\
            'within a peptide\n\n'\
            'Additionally, userdefined modifications can be given and are '\
            'written to a userdefined_unimod.xml in ursgal/kb/ext. '\
            'Userdefined modifications need to have a unique name instead of '\
            'the unimod name the chemical composition needs to be given as a '\
            'Hill notation on the fifth position in the string\n'\
            '\n'\
            'Example:\n\n'\
            '[ \'S,opt,any,New_mod,C2H5N1O3\' ]',
    },
    'mono_link_definition' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'mono_link_definition',
        },
        'utag' : [
            'cross_linking',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'nK  156.0786',
        'description' : \
            'Cross-link and mono-link masses allowed. \n'\
            'May have more than one of each parameter. \n'\
            'Format for mono_link is: \n'\
            '    [amino acids] [mass mod]\n'\
            'One or more amino acids (uppercase only!!) can be specified for '\
            'each linkage moiety. Use lowercase \'n\' or \'c\' to indicate '\
            'protein N-terminus or C-terminus',
    },
    'msgfplus_protocol_id' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1' : '-protocol',
        },
        'utag' : [
            'scoring',
            'label'
        ],
        'uvalue_translation' : {
            'msgfplus_style_1' : {
                '0' : 0,
                '1' : 1,
                '2' : 2,
                '3' : 3,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['0', '1', '2', '3'],
            'custom_val_max' : 0,
        },
        'default_value' : '0',
        'description' : \
            'MS-GF+ specific protocol identifier. Protocols are used to '\
            'enable scoring parameters for enriched and/or labeled samples.',
    },
    'msfragger_output_max_expect' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : 50,
        'description' :  ''' Suppresses reporting of PSM if top hit has expectation greater than this threshold ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'output_max_expect',
        },
        'utag' : [
            'output',
            'scoring'
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'msfragger_track_zero_topN' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : 0,
        'description' :  ''' Track top N unmodified peptide results separately from main results internally for boosting features. Should be set to a number greater than output_report_topN if zero bin boosting is desired. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'track_zero_topN',
        },
        'utag' : [
            'output',
            'scoring'
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'msfragger_zero_bin_accept_expect' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : 0.0,
        'description' :  ''' Ranks a zero-bin hit above all non-zero-bin hit if it has expectation less than this value. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'zero_bin_accept_expect',
        },
        'utag' : [
            'scoring'
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'f-point'   : 1e-02,
            'updownval' : 0.1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "float",
    },
    'msfragger_zero_bin_mult_expect' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : 1.0,
        'description' :  ''' Multiplies expect value of PSMs in the zero-bin during results ordering (set to less than 1 for boosting) ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'zero_bin_mult_expect',
        },
        'utag' : [
            'scoring'
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'f-point'   : 1e-02,
            'updownval' : 0.1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "float",
    },
    'msfragger_add_topN_complementary' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : False,
        'description' :  ''' Inserts complementary ions corresponding to the top N most intense fragments in each experimental spectrum. Useful for recovery of modified peptides near C-terminal in open search. Should be set to 0 (disabled) otherwise. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'add_topN_complementary',
        },
        'utag' : [
            'scoring',
            'spectrum'
        ],
        'uvalue_option' : {
        },
        'uvalue_translation' : {
            'msfragger_style_1' : {
                False : 0,
                True : 1,
            }
        },
        'uvalue_type' : "bool",
    },
    'msfragger_min_fragments_modelling' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : 3,
        'description' :  ''' Minimum number of matched peaks in PSM for inclusion in statistical modeling ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'min_fragments_modelling',
        },
        'utag' : [
            'spectrum',
            'scoring'
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 1000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'msgfplus_mzid_converter_version' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'default_value' : None,
        'description' :  ''' Determines which msgfplus mzid conversion node should be used e.g. "msgfplus2csv_v2017_07_04"''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'msgfplus_mzid_converter_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_option' : {
            'none_val'     : '',
            'multiple_line' : False,
        },
        'uvalue_translation' : {
            'ucontroller_style_1': {
                'msgfplus_v9979' : 'msgfplus2csv_py_v1_0_0',
                'msgfplus_v2016_09_16' : 'msgfplus2csv_py_v1_0_0',
                'msgfplus_v2017_01_27' : 'msgfplus2csv_py_v1_0_0',
                'msgfplus_v2018_01_30' : 'msgfplus2csv_py_v1_0_0',
                'msgfplus_v2018_06_28' : 'msgfplus2csv_py_v1_0_0',
                'msgfplus_v2018_09_12' : 'msgfplus2csv_py_v1_0_0',
                'msgfplus_v2019_01_22' : 'msgfplus2csv_py_v1_0_0',
                'msgfplus_v2019_04_18' : 'msgfplus2csv_py_v1_0_0',
            },
        },
        'uvalue_type' : "str",
    },
    'myrimatch_class_size_multiplier' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'ClassSizeMultiplier',
        },
        'utag' : [
            'scoring'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 2,
        'description' : \
            'Myrimatch ClassSizeMultiplier',
    },
    'myrimatch_num_int_classes' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'NumIntensityClasses',
        },
        'utag' : [
            'scoring'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 3,
        'description' : \
            'Myrimatch NumIntensityClasses',
    },
    'myrimatch_num_mz_fidelity_classes' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'NumMzFidelityClasses',
        },
        'utag' : [
            'spectrum',
            'scoring'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 3,
        'description' : \
            'Myrimatch NumMzFidelityClasses',
    },
    'myrimatch_prot_sampl_time' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'ProteinSamplingTime',
        },
        'utag' : [
            'chromatography'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 15,
        'description' : \
            'Myrimatch ProteinSamplingTime',
    },
    'myrimatch_smart_plus_three' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'UseSmartPlusThreeModel',
        },
        'utag' : [
            'model',
            'scoring'
        ],
        'uvalue_translation' : {
            'myrimatch_style_1' : {
                False : 0,
                True  : 1,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Use Myrimatch UseSmartPlusThreeModel',
    },
    'myrimatch_tic_cutoff' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'myrimatch_style_1' : 'TicCutoffPercentage',
        },
        'utag' : [
            'spectrum'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10,
            'min'       : 0,
            'f-point'   : 1e-02,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.98,
        'description' : \
            'Myrimatch TicCutoffPercentage',
    },
    'mzidentml_compress' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzidentml_style_1' : '-compress',
        },
        'utag' : [
            'output',
            'file_handling'
        ],
        'uvalue_translation' : {
            'mzidentml_style_1' : {
                False : 'false',
                True  : 'true',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Compress mzidentml_lib output files',
    },
    'mzidentml_converter_version' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'mzidentml_converter_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'mzidentml_lib_1_6_10',
        'description' : \
            'mzidentml converter version: version name',
    },
    'mzidentml_export_type' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzidentml_style_1' : '-exportType',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : [
                'exportPSMs',
                'exportProteinGroups',
                'exportProteinsOnly',
                'exportProteoAnnotator',
                'exportRepProteinPerPAGOnly',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'exportPSMs',
        'description' : \
            'Defines which paramters shoul be exporte by mzidentml_lib',
    },
    'mzidentml_function' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzidentml_style_1' : 'mzidentml_function',
        },
        'utag' : [
            'output'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : [
                'AddEmpaiToMzid',
                'CreateRestrictedFASTADatabase',
                'Csv2mzid',
                'FalseDiscoveryRate',
                'InsertMetaDataFromFasta',
                'Mzid2Csv',
                'Omssa2mzid',
                'ProteoGrouper',
                'Tandem2mzid',
                'Threshold',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'Mzid2Csv',
        'description' : \
            'Defines the mzidentml_lib function to be used. Note: only '\
            '\'Mzid2Csv\' is supported so far',
    },
    'mzidentml_output_fragmentation' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzidentml_style_1' : '-outputFragmentation',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'mzidentml_style_1' : {
                False : 'false',
                True  : 'true',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Include fragmentation in mzidentml_lib output',
    },
    'mzidentml_verbose_output' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzidentml_style_1' : '-verboseOutput',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'mzidentml_style_1' : {
                False : 'false',
                True  : 'true',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Verbose mzidentml_lib output',
    },
    'mzml2mgf_converter_version' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'mzml2mgf_converter_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'mzml2mgf_2_0_0',
        'description' : \
            'mzml to mgf converter version: version name',
    },
    'neutral_loss_enabled' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'spectrum, use neutral loss window',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Neutral losses enabled for spectrum algorithm: set  True or False',
    },
    'neutral_loss_mass' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'spectrum, neutral loss mass',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'Sets the centre of the window for ignoring neutral molecule '\
            'losses.',
    },
    'neutral_loss_window' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'spectrum, neutral loss window',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'Neutral loss window: sets the width of the window for ignoring '\
            'neutral molecule losses.',
    },
    'noise_suppression_enabled' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'spectrum, use noise suppression',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Used noise suppresssion',
    },
    'num_compared_psms' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sanitize_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sanitize_csv_style_1' : 'num_compared_psms',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 1,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 2,
        'description' : \
            'Maximum number of PSMs (sorted by score, starting with the best '\
            'scoring PSM) that are compared',
    },
    'num_hits_retain_spec' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-hl',
        },
        'utag' : [
            'output',
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 30,
        'description' : \
            'Maximum number of hits retained per precursor charge state per '\
            'spectrum during the search',
    },
    'num_i_decimals' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
            'mzml2mgf_2_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'number_of_i_decimals',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 7,
        'description' : \
            'Number of decimals for intensity (peak)',
    },
    'num_match_spec' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1'  : 'max_rank',
            'msgfplus_style_1'  : '-n',
            'myrimatch_style_1' : 'MaxResultRank',
            'omssa_style_1'     : '-hc',
            'pepnovo_style_1'   : '-num_solutions',
            'msfragger_style_1' : 'output_report_topN'
        },
        'utag' : [
            'output',
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 10,
        'description' : \
            'Maximum number of peptide spectrum matches to report for each spectrum',
    },
    'num_mz_decimals' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
            'mzml2mgf_2_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'number_of_mz_decimals',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 7,
        'description' : \
            'Number of decimals for m/z mass',
    },
    'omssa_cp' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-cp',
        },
        'utag' : [
            'precursor',
            'spectrum',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                False : 0,
                True  : 1,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Omssa: eliminate charge reduced precursors in spectra',
    },
    'omssa_h1' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-h1',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 2,
        'description' : \
            'Omssa: number of peaks allowed in single charge window',
    },
    'omssa_h2' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-h2',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 2,
        'description' : \
            'Omssa: number of peaks allowed in double charge window',
    },
    'omssa_ht' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-ht',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 6,
        'description' : \
            'Omssa: number of m/z values corresponding to the most intense '\
            'peaks that must include one match to the theoretical peptide',
    },
    'omssa_mm' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-mm',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 10,
            'unit'      : ''
        },
        'default_value' : 128,
        'description' : \
            'Omssa: the maximum number of mass ladders to generate per '\
            'database peptide',
    },
    'omssa_ta' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-ta',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 1.0,
        'description' : \
            'Omssa: automatic mass tolerance adjustment fraction',
    },
    'omssa_tex' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-tex',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'f-point'   : 1e-02,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 1446.94,
        'description' : \
            'Omssa: threshold in Da above which the mass of neutron should be '\
            'added in exact mass search',
    },
    'omssa_verbose' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-ni',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                False : '',
                True  : '-ni',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Omssa: verbose info print',
    },
    'omssa_w1' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-w1',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 27,
        'description' : \
            'Omssa: single charge window in Da',
    },
    'omssa_w2' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-w2',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 14,
        'description' : \
            'Omssa: double charge window in Da',
    },
    'omssa_z1' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-z1',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'f-point'   : 1e-02,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.95,
        'description' : \
            'Omssa: fraction of peaks below precursor used to determine if '\
            'spectrum is charge 1',
    },
    'omssa_zc' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-zc',
        },
        'utag' : [
            'precursor',
            'spectrum',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                False : 0,
                True  : 1,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Should charge plus one be determined algorithmically?',
    },
    'omssa_zcc' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-zcc',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 2,
        'description' : \
            'Omssa: how should precursor charges be determined?, use a range',
    },
    'omssa_zt' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-zt',
        },
        'utag' : [
            'precursor',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 3,
        'description' : \
            'Minimum precursor charge to start considering multiply charged '\
            'products',
    },
    'output_aa_probs' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-output_aa_probs',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Output probabilities for each amino acid.',
    },
    'output_add_features' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1' : '-addFeatures',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'msgfplus_style_1' : {
                False : '0',
                True  : '1',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Number of decimals for intensity (peak)',
    },
    'output_cum_probs' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-output_cum_probs',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Output cumulative probabilities.',
    },
    'output_file_incl_path' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'generate_target_decoy_1_0_0',
            'merge_csvs_1_0_0',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'percolator_2_08',
            'percolator_3_2_1',
            'percolator_3_4_0',
            'qvality_2_02',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'generate_target_decoy_style_1' : 'output_file',
            'merge_csvs_style_1'            : 'output',
            'moda_style_1'                  : '-o',
            'msamanda_style_1'              : 'output_file_incl_path',
            'msgfplus_style_1'              : '-o',
            'myrimatch_style_1'             : 'output_file_incl_path',
            'mzidentml_style_1'             : 'output_file_incl_path',
            'novor_style_1'                 : 'output_file_incl_path',
            'omssa_style_1'                 : 'output_file_incl_path',
            'pepnovo_style_1'               : 'output_file_incl_path',
            'percolator_style_1'            : 'output_file_incl_path',
            'qvality_style_1'               : '-o',
            'sugarpy_run_style_1'           : 'output_file',
            'sugarpy_plot_style_1'          : 'output_file',
            'venndiagram_style_1'           : 'output_file',
            'xtandem_style_1'               : 'output, path',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : 'None',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Path to output file\n'\
            '    \'None\' : None',
    },
    'output_file_type' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'thermo_raw_file_parser_1_1_2',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1'   : ('-oc', '-ox'),
            'xtandem_style_1' : 'output, mzid',
            'thermo_raw_file_parser_style_1' : '-f',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                '.csv'    : '-oc',
                '.omx'    : '-ox',
                'default' : '-oc',
            },
            'xtandem_style_1' : {
                '.mzid' : 'yes',
                'default' : 'no',
            },
            'thermo_raw_file_parser_style_1': {
                '.mgf' : 0,
                '.mzml' : 1,
                'indexed_mzml' : 2,
                'parquet' : 3,
                'default' : 1,
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['.csv', '.mzid', '.omx', 'default', '.mgf', '.mzml', 'parquet', 'indexed_mzml'],
            'custom_val_max' : 0,
        },
        'default_value' : 'default',
        'description' : \
            'Output file type. If set to \'default\', default output file '\
            'tzpes for each engine are used. Note: not every file type is '\
            'supported by every engine and usin non-default types might cause '\
            'problems during conversion to .csv.',
    },
    'output_prm' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-prm',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Only print spectrum graph nodes with scores.',
    },
    'output_prm_norm' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-prm_norm',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Prints spectrum graph scores after normalization and removal of '\
            'negative scores.',
    },
    'output_q_values' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msgfplus2csv_v2016_09_16',
            'msgfplus2csv_v2017_01_27',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1' : '-showQValue',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'msgfplus_style_1' : {
                False : '0',
                True  : '1',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Output Q-values',
    },
    'pepnovo_tag_length' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-tag_length',
        },
        'utag' : [
            'peptide',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : 0,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : None,
        'description' : \
            'Returns peptide sequences of the specified length (only lengths '\
            '3-6 are allowed)\n'\
            '    0 : None',
    },
    'peptide_mapper_class_version' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'upeptide_mapper_1_0_0',
        ],
        'default_value' : 'UPeptideMapper_v3',
        'description' :  '''version 3 and 4 are the fastest and most memory efficient class versions, version 2 is the classic approach ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'upeptide_mapper_style_1' : 'peptide_mapper_class_version',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_option' : {
            'none_val' : None,
            'multiple_line' : False
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "str",
    },
    'peptide_mapper_converter_version' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'default_value' : 'upeptide_mapper_1_0_0',
        'description' :  ''' determines which upeptide mapper node should be used''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'peptide_mapper_converter_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_option' : {
            'none_val'     : None,
            'multiple_line' : False,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "str",
    },
    'pipi_mz_bin_offset' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pipi_style_1' : 'mz_bin_offset',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100,
            'min'       : 0,
            'updownval' : 0.1,
            'f-point'   : 1e-02,
            'unit'      : ''
        },
        'default_value' : 0.0,
        'description' : \
            'PIPI mz_bin_offset'
    },
    'precursor_charge_dependency' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-tez',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                'linear' : 1,
                'none'   : 0,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['linear', 'none'],
            'custom_val_max' : 0,
        },
        'default_value' : 'linear',
        'description' : \
            'charge dependency of precursor mass tolerance (none or linear)',
    },
    'precursor_isotope_range' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'precursor_isotope_range',
            'msgfplus_style_1' : '-ti',
            'myrimatch_style_1' : 'MonoisotopeAdjustmentSet',
            'omssa_style_1' : '-ti',
            'pepnovo_style_1' : '-correct_pm',
            'unify_csv_style_1' : 'precursor_isotope_range',
            'xtandem_style_1' : 'spectrum, parent monoisotopic mass isotope error',
            'msfragger_style_1' : 'isotope_error',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                '0'     : '0',
                '0,1'   : '1',
                '0,2'   : '2',
            },
            'myrimatch_style_1' : {
                '0'     : '[0,]',
                '0,1'   : '[0,1]',
                '0,1,2' : '[0,1,2]',
            },
            'omssa_style_1' : {
                '0'     : '0',
                '0,1'   : '1',
                '0,2'   : '2',
            },
            'xtandem_style_1' : {
                '0'     : 'no',
                '0,1'   : 'yes',
                '0,2'   : 'yes',
            },
            'msfragger_style_1' : {
                '0' : '0',
                '0,1' : '0/1',
                '0,2' : '0/1/2',
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['0', '0,1', '0,2'],
            'custom_val_max' : 0,
        },
        'default_value' : '0,1',
        'description' : \
            'Error range for incorrect carbon isotope parent ion assignment',
    },
    'precursor_mass_tolerance_minus' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'pglyco_db_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'      : 'ppm_tolerance_pre',
            'moda_style_1'       : 'PPMTolerance',
            'msamanda_style_1'   : 'ms1_tol',
            'msgfplus_style_1'   : '-t',
            'myrimatch_style_1'  : 'MonoPrecursorMzTolerance',
            'novor_style_1'      : 'precursorErrorTol',
            'omssa_style_1'      : '-te',
            'pepnovo_style_1'    : '-pm_tolerance',
            'unify_csv_style_1'  : 'precursor_mass_tolerance_minus',
            'xtandem_style_1'    : 'spectrum, parent monoisotopic mass error minus',
            'msfragger_style_1'  : 'precursor_mass_lower',
            'pipi_style_1'       : 'ms1_tolerance',
            'pyqms_style_1'      : 'REL_MZ_RANGE',
            'sugarpy_run_style_1': 'REL_MZ_RANGE',
            'sugarpy_plot_style_1': 'REL_MZ_RANGE',
            'pglyco_db_style_1'  : 'search_precursor_tolerance',
            'deepnovo_style_1'   : ('precursor_mass_tolerance', 'precursor_mass_ppm')
        },
        'utag' : [
            'precursor',
            'accuracy'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 5,
        'description' : \
            'Lower precursor mass tolerance; maximum negative deviation of measured from calculated parent ion mass.',
    },
    'precursor_mass_tolerance_plus' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'pglyco_db_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'ppm_tolerance_pre',
            'moda_style_1'      : 'PPMTolerance',
            'msamanda_style_1'  : 'ms1_tol',
            'msgfplus_style_1'  : '-t',
            'myrimatch_style_1' : 'MonoPrecursorMzTolerance',
            'novor_style_1'     : 'precursorErrorTol',
            'omssa_style_1'     : '-te',
            'pepnovo_style_1'   : '-pm_tolerance',
            'unify_csv_style_1' : ' precursor_mass_tolerance_minus',
            'xtandem_style_1'   : 'spectrum, parent monoisotopic mass error plus',
            'msfragger_style_1' : 'precursor_mass_upper',
            'pipi_style_1'      : 'ms1_tolerance',
            'pyqms_style_1'      : 'REL_MZ_RANGE',
            'sugarpy_run_style_1': 'REL_MZ_RANGE',
            'sugarpy_plot_style_1': 'REL_MZ_RANGE',
            'pglyco_db_style_1'  : 'search_precursor_tolerance',
            'deepnovo_style_1'   : ('precursor_mass_tolerance', 'precursor_mass_ppm')
        },
        'utag' : [
            'precursor',
            'accuracy'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 5,
        'description' : \
            'Upper precursor mass tolerance; maximum positive deviation of measured from calculated parent ion mass.',
    },
    'precursor_mass_tolerance_unit' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'novor_1_05',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pipi_1_4_5',
            'pipi_1_4_6',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'pglyco_db_2_2_0',
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'      : 'PPMTolerance',
            'msamanda_style_1'  : 'ms1_tol unit',
            'msgfplus_style_1'  : '-t',
            'myrimatch_style_1' : 'MonoPrecursorMzTolerance',
            'novor_style_1'     : 'precursorErrorTol',
            'omssa_style_1'     : '-teppm',
            'pepnovo_style_1'   : 'precursor_mass_tolerance_unit',
            'xtandem_style_1'   : 'spectrum, parent monoisotopic mass error units',
            'msfragger_style_1' : 'precursor_mass_units',
            'pipi_style_1'      : 'ms1_tolerance_unit',
            'pyqms_style_1'      : 'REL_MZ_RANGE',
            'sugarpy_run_style_1': 'REL_MZ_RANGE',
            'sugarpy_plot_style_1': 'REL_MZ_RANGE',
            'pglyco_db_style_1'  : 'search_precursor_tolerance_type',
            'deepnovo_style_1'   : ('precursor_mass_tolerance', 'precursor_mass_ppm')
        },
        'utag' : [
            'precursor',
            'accuracy'
        ],
        'uvalue_translation' : {
            'msamanda_style_1' : {
                'da'  : 'Da',
            },
            'msgfplus_style_1' : {
                'da'  : 'Da',
            },
            'myrimatch_style_1' : {
                'da'  : 'Da',
            },
            'novor_style_1' : {
                'da'  : 'Da',
            },
            'omssa_style_1' : {
                'da'  : '',
                'ppm' : '-teppm',
            },
            'xtandem_style_1' : {
                'da'  : 'Daltons',
            },
            'msfragger_style_1' : {
                'ppm' : 1,
                'da'  : 0
            },
            'pipi_style_1' : {
                'ppm' : 1,
                'da'  : 0
            },
            'pglyco_db_style_1': {
                'da' : 'Da'
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['da', 'mmu', 'ppm'],
            'custom_val_max' : 0,
        },
        'default_value' : 'ppm',
        'description' : \
            'Precursor mass tolerance unit: available in ppm '\
            '(parts-per-millon), da (Dalton) or mmu (Milli mass unit)',
    },
    'precursor_mass_type' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'monoisotopic',
            'myrimatch_style_1' : 'PrecursorMzToleranceRule',
            'omssa_style_1' : '-tem',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
            'msamanda_style_1' : {
                'average' : 'false',
                'monoisotopic' : 'true',
            },
            'myrimatch_style_1' : {
                'average' : 'average',
                'monoisotopic' : 'mono',
            },
            'omssa_style_1' : {
                'average' : '1',
                'monoisotopic' : '0',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['average', 'monoisotopic'],
            'custom_val_max' : 0,
        },
        'default_value' : 'monoisotopic',
        'description' : \
            'Precursor mass type: monoisotopic or average',
    },
    'precursor_max_charge' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'mzml2mgf_2_0_0',
            'omssa_2_1_9',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1': 'considered_charges',
            'msgfplus_style_1': '-maxCharge',
            'myrimatch_style_1': 'NumChargeStates',
            'omssa_style_1': '-zh',
            'msfragger_style_1': 'precursor_max_charge',
            'pyqms_style_1': 'precursor_max_charge',
            'sugarpy_run_style_1': 'max_charge',
            'sugarpy_plot_style_1': 'max_charge',
            'mzml2mgf_style_1': 'precursor_max_charge',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 5,
        'description' : \
            'Maximal accepted parent ion charge',
    },
    'precursor_max_mass' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'kojak_1_5_3',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pglyco_db_2_2_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'precursor_max_mass',
            'myrimatch_style_1' : 'MaxPeptideMass',
            'xtandem_style_1'   : 'spectrum, minimum parent m+h',
            'msfragger_style_1' : 'precursor_max_mass',
            'pglyco_db_style_1'    : 'max_peptide_weight',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 100,
            'unit'      : ''
        },
        'default_value' : 7000,
        'description' : \
            'Maximal parent ion mass in Da. Adjusted to default used by MSFragger',
    },
    'precursor_min_charge' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'mzml2mgf_2_0_0',
            'omssa_2_1_9',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pyqms_1_0_0',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation': {
            'msamanda_style_1': 'considered_charges',
            'msgfplus_style_1': '-minCharge',
            'omssa_style_1': '-zl',
            'msfragger_style_1': 'precursor_min_charge',
            'pyqms_style_1': 'precursor_min_charge',
            'sugarpy_run_style_1': 'min_charge',
            'sugarpy_plot_style_1': 'min_charge',
            'mzml2mgf_style_1': 'precursor_min_charge',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 1,
        'description' : \
            'Minimal accepted parent ion charge',
    },
    'precursor_min_mass' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
            'pglyco_db_2_2_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'precursor_min_mass',
            'myrimatch_style_1' : 'MinPeptideMass',
            'xtandem_style_1'   : 'spectrum, minimum parent m+h',
            'msfragger_style_1' : 'precursor_min_mass',
            'pglyco_db_style_1'    : 'min_peptide_weight',
        },
        'utag' : [
            'precursor',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 400,
        'description' : \
            'Minimal parent ion mass',
    },
    'precursor_true_tolerance' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : 5,
        'description' :  'True precursor mass tolerance '\
        '(window is +/- this value). Used for tie breaker '\
        'of results (in spectrally ambiguous cases) '\
        'and zero bin boosting in open searches '\
        '(0 disables these features). This option is '\
        'STRONGLY recommended for open searches.',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'precursor_true_tolerance',
        },
        'utag' : [
            'precursor',
            'accuracy'
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "int",
    },
    'precursor_true_units' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'default_value' : 'ppm',
        'description' :  '''Mass tolerance units fo precursor_true_tolerance''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'precursor_true_units',
        },
        'utag' : [
            'precursor',
            'accuracy'
        ],
        'uvalue_option' : {
            'multiple_line' : False,
            'none_val'     : None
        },
        'uvalue_translation' : {
            'msfragger_style_1' : {
                'ppm' : 1,
                'da'  : 0
            }
        },
        'uvalue_type' : "str",
    },
    'prefix' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'prefix',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'None',
        'uvalue_option' : {
            'none_val' : 'None',
            'system_param' : True,
        },
        'default_value' : None,
        'description' : \
            '    \'None\' : None',
    },
    'protein_delimiter' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'percolator_2_08',
            'percolator_3_2_1',
            'percolator_3_4_0',
            'unify_csv_1_0_0',
            'upeptide_mapper_1_0_0'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'percolator_style_1'      : 'protein_delimiter',
            'unify_csv_style_1'       : 'protein_delimiter',
            'upeptide_mapper_style_1' : 'protein_delimiter',
        },
        'utag' : [
            'output',
            'protein',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '<|>',
        'description' : \
            'This delimiter seperates protein IDs/names in the unified csv',
    },
    'psm_defining_colnames' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'psm_defining_colnames',
        },
        'utag' : [
            'conversion',
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'column_name',
            'item_type' : 'str',
            'multiple_line' : False,
            'custom_val_max': 10000,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
            'Spectrum Title',
            'Sequence',
            'Modifications',
            'Mass Difference',
            'Charge',
            'Is decoy',
        ],
        'description' : \
            'List of column names that are used to define unique PSMs and to merge multiple lines of the same PSM (if specified). The validation_score_field is automatically added to this list. ',
    },
    'psm_colnames_to_merge_multiple_values' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'colnames_to_merge_multiple_values',
        },
        'utag' : [
            'conversion',
            'output',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'column_name_with_type_of_merge',
            'item_titles' : {
                'font_type' : 'type',
                'font_size_header' : 'size',
                'font_size_major' : 'size',
                'font_size_minor' : 'size',
                'font_size_venn' : 'size',
            },
            'value_types' : {
                'font_type' : 'str',
                'font_size_header' : 'int',
                'font_size_major' : 'int',
                'font_size_minor' : 'int',
                'font_size_venn' : 'int',
            },
            'multiple_line' : {
                'font_type' : False,
            },
            'max' : {
                'font_size_header' : 1000,
                'font_size_major' : 1000,
                'font_size_minor' : 1000,
                'font_size_venn' : 1000,
            },
            'min' : {
                'font_size_header' : 0,
                'font_size_major' : 0,
                'font_size_minor' : 0,
                'font_size_venn' : 0,
            },
            'updownval' : {
                'font_size_header' : 1,
                'font_size_major' : 1,
                'font_size_minor' : 1,
                'font_size_venn' : 1,
            },
            'unit' : {
                'font_size_header' : 'pt',
                'font_size_major' : 'pt',
                'font_size_minor' : 'pt',
                'font_size_venn' : 'pt',
            },
            'custom_val_max' : 0,
            'item_type' : 'str',
            'multiple_line' : False,
            'custom_val_max': 10000,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : {},
        'description' : \
            'Defines the column names which should have their different values merged '\
            'into a single value when merging rows corresponding the same PSM '\
            'Formatted as a dictionary with keys as the column names and values as '\
            'a parameter to specify which one of the different values to take '\
            'Available values:'
            '    max_value\n'\
            '    min_value\n'\
            '    most_frequent\n'\
            '    avg_value',
    },
    'psm_merge_delimiter' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'unify_csv_1_0_0',
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'unify_csv_style_1' : 'psm_merge_delimiter',
            'ucontroller_style_1' : 'psm_merge_delimiter',
        },
        'utag' : [
            'output',
            'protein',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : ';',
        'description' : \
            'This delimiter seperates differing values for merged rows in the '\
            'unified csv',
    },
    'qvality_cross_validation' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'qvality_2_02',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'qvality_style_1' : '-c',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'The relative crossvalidation step size used as treshhold before '\
            'ending the iterations, qvality determines step size '\
            'automatically when set to 0',
    },
    'qvality_epsilon_step' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'qvality_2_02',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'qvality_style_1' : '-s',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 0,
        'description' : \
            'The relative step size used as treshhold before cross validation '\
            'error is calculated, qvality determines step size automatically '\
            'when set to 0',
    },
    'qvality_number_of_bins' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'qvality_2_02',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'qvality_style_1' : '-n',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 10,
            'unit'      : ''
        },
        'default_value' : 500,
        'description' : \
            'Number of bins used in qvality',
    },
    'qvality_verbose' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'qvality_2_02',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'qvality_style_1' : '-v',
        },
        'utag' : [
            'output',
        ],
        'uvalue_translation' : {
            'qvality_style_1' : {
                '1' : 1,
                '2' : 2,
                '3' : 3,
                '4' : 4,
                '5' : 5,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['1', '2', '3', '4', '5'],
            'custom_val_max' : 0,
        },
        'default_value' : '2',
        'description' : \
            'Verbose qvality output (range from 0 = no processing info to 5 = '
            'all)',
    },
    'raw_ident_csv_suffix' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'raw_ident_csv_suffix',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '.csv',
        'description' : \
            'CSV suffix of raw indentification: this is the conversion result '\
            'after CSV conversion but before adding retention time',
    },
    'remove_redundant_psms' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sanitize_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sanitize_csv_style_1' : 'remove_redundant_psms',
        },
        'utag' : [
            'output'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'If True, redundant PSMs (e.g. the same identification reported '\
            'by multiple engines) for the same spectrum are removed. An '\
            'identification is defined by the combination of \'Sequence\', '\
            '\'Modifications\' and \'Charge\'.',
    },
    'remove_temporary_files' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'remove_temporary_files',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Remove temporary files: True or False',
    },
    'rounded_mass_decimals' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'unify_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'unify_csv_style_1' : 'rounded_mass_decimals',
        },
        'utag' : [
            'modifications',
            'conversion'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 3,
        'description' : \
            'Masses of modifications are rounded in order to match them to '\
            'their corresponding unimod name. Use this parameter to set the '\
            'number of decimal places after rounding.',
    },
    'rt_pickle_name' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
            'mgf_to_rt_lookup_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'rt_pickle_name',
            'sugarpy_run_style_1' : 'scan_rt_lookup',
            'sugarpy_plot_style_1' : 'scan_rt_lookup',
            'mgf_to_rt_lookup_style_1': 'rt_pickle_name',
        },
        'utag' : [
            'file_handling',
            'chromatography'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '_ursgal_lookup.pkl',
        'description' : \
            'name of the pickle that is used to map the retention time',
    },
    'scan_exclusion_list' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
            'mzml2mgf_2_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'scan_exclusion_list',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'spectrum number',
            'item_type' : 'int',
            'min' : 0,
            'max' : 100000000,
            'updownval' : 1,
            'unit' : '',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
        ],
        'description' : \
            'Spectra rejected during mzml2mgf conversion',
    },
    'scan_inclusion_list' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
            'mzml2mgf_2_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'scan_inclusion_list',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : [
            ],
            'item_title' : 'spectrum number',
            'item_type' : 'int',
            'max' : 10000000,
            'min' : 0,
            'unit' : '',
            'updownval' : 1,
            'custom_val_max' : 10000,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : None,
        'description' : \
            'Exclusively spectra included during mzml2mgf conversion',
    },
    'scan_skip_modulo_step' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
            'mzml2mgf_2_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'scan_skip_modulo_step',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
            'mzml2mgf_style_1' : {
            },
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : 1,
            'max'       : 10000000,
            'min'       : 1,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : None,
        'description' : \
            'Include only the n-th spectrum during mzml2mgf conversion\n'\
            '    1 : None',
    },
    'score_correlation_corr' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-scorr',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                False : 1,
                True : 0,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Use correlation correction to score?',
    },
    'score_diff_threshold' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sanitize_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sanitize_csv_style_1' : 'score_diff_threshold',
        },
        'utag' : [
            'scoring',
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100,
            'min'       : 0,
            'f-point'   : 1e-03,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.01,
        'description' : \
            'Minimum score difference between the best PSM and the first '\
            'rejected PSM of one spectrum, default: 0.01',
    },
    'score_ion_list' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : (
                'ion_series_X',
                'ion_series_Y',
                'ion_series_Z',
                'ion_series_A',
                'ion_series_B',
                'ion_series_C',
            ),
            'msamanda_style_1'  : 'series',
            'myrimatch_style_1' : 'FragmentationRule',
            'omssa_style_1'     : (
                '-i',
                '-sct',
                '-sb1',
            ),
            'xtandem_style_1'   : (
                'scoring, x ions',
                'scoring, y ions',
                'scoring, z ions',
                'scoring, a ions',
                'scoring, b ions',
                'scoring, c ions',
            ),
        },
        'utag' : [
            'scoring',
            'fragment'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : [],
            'item_type' : 'str',
            'item_title': 'ion type',
            'multiple_line' : False,
            'custom_val_max' : 100,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : ['b', 'y', ],
        'description' : \
            'List of ion types that are taken into account by the respective search engine.'\
            'Availabel ion types: a, b, c, x, y, z, -h2o, -nh3, b1, c_terminal, imm (immonium), int (internal), z+1, z+2',
    },
    #     'score_-h2o_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'msamanda_style_1' : 'series',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, ions loss of H2O are respected in algorithm',
    # },
    # 'score_-nh3_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'msamanda_style_1' : 'series',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, ions loss of NH3 are respected in algorithm',
    # },
    # 'score_a_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'kojak_1_5_3',
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #         'myrimatch_2_1_138',
    #         'myrimatch_2_2_140',
    #         'omssa_2_1_9',
    #         'xtandem_cyclone_2010',
    #         'xtandem_jackhammer',
    #         'xtandem_piledriver',
    #         'xtandem_sledgehammer',
    #         'xtandem_vengeance',
    #         'xtandem_alanine',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'kojak_style_1'     : 'ion_series_A',
    #         'msamanda_style_1'  : 'series',
    #         'myrimatch_style_1' : 'FragmentationRule',
    #         'omssa_style_1'     : '-i',
    #         'xtandem_style_1'   : 'scoring, a ions',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'kojak_style_1' : {
    #             False : '0',
    #             True  : '1',
    #         },
    #         'omssa_style_1' : {
    #             False : '',
    #             True  : '0',
    #         },
    #         'xtandem_style_1' : {
    #             False : 'no',
    #             True  : 'yes',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, a ions are used in algorithm',
    # },
    # 'score_b1_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'omssa_2_1_9',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'omssa_style_1' : '-sb1',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'omssa_style_1' : {
    #             False : '1',
    #             True  : '0',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'first forward (b1) product ions inclued in search',
    # },
    # 'score_b_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'kojak_1_5_3',
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #         'myrimatch_2_1_138',
    #         'myrimatch_2_2_140',
    #         'omssa_2_1_9',
    #         'xtandem_cyclone_2010',
    #         'xtandem_jackhammer',
    #         'xtandem_piledriver',
    #         'xtandem_sledgehammer',
    #         'xtandem_vengeance',
    #         'xtandem_alanine',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'kojak_style_1'     : 'ion_series_B',
    #         'msamanda_style_1'  : 'series',
    #         'myrimatch_style_1' : 'FragmentationRule',
    #         'omssa_style_1'     : '-i',
    #         'xtandem_style_1'   : 'scoring, b ions',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'kojak_style_1' : {
    #             False : '0',
    #             True  : '1',
    #         },
    #         'omssa_style_1' : {
    #             False : '',
    #             True  : '1',
    #         },
    #         'xtandem_style_1' : {
    #             False : 'no',
    #             True  : 'yes',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : True,
    #     'description' : \
    #         'Spectrum: if true, b ions are used in algorithm',
    # },
    # 'score_c_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'kojak_1_5_3',
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #         'myrimatch_2_1_138',
    #         'myrimatch_2_2_140',
    #         'omssa_2_1_9',
    #         'xtandem_cyclone_2010',
    #         'xtandem_jackhammer',
    #         'xtandem_piledriver',
    #         'xtandem_sledgehammer',
    #         'xtandem_vengeance',
    #         'xtandem_alanine',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'kojak_style_1'     : 'ion_series_C',
    #         'msamanda_style_1'  : 'series',
    #         'myrimatch_style_1' : 'FragmentationRule',
    #         'omssa_style_1'     : '-i',
    #         'xtandem_style_1'   : 'scoring, c ions',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'kojak_style_1' : {
    #             False : '0',
    #             True  : '1',
    #         },
    #         'omssa_style_1' : {
    #             False : '',
    #             True  : '2',
    #         },
    #         'xtandem_style_1' : {
    #             False : 'no',
    #             True  : 'yes',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, c ions are used in algorithm',
    # },
    # 'score_c_terminal_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'omssa_2_1_9',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'omssa_style_1' : '-sct',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'omssa_style_1' : {
    #             False : '1',
    #             True  : '0',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : True,
    #     'description' : \
    #         'Score c terminal ions',
    # },
    # 'score_imm_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'msamanda_style_1' : 'series',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, immonium ions are respected in algorithm',
    # },
    # 'score_int_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'msamanda_style_1' : 'series',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, internal fragment ions are respect in algorithm',
    # },
    # 'score_x_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'kojak_1_5_3',
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #         'myrimatch_2_1_138',
    #         'myrimatch_2_2_140',
    #         'omssa_2_1_9',
    #         'xtandem_cyclone_2010',
    #         'xtandem_jackhammer',
    #         'xtandem_piledriver',
    #         'xtandem_sledgehammer',
    #         'xtandem_vengeance',
    #         'xtandem_alanine',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'kojak_style_1'     : 'ion_series_X',
    #         'msamanda_style_1'  : 'series',
    #         'myrimatch_style_1' : 'FragmentationRule',
    #         'omssa_style_1'     : '-i',
    #         'xtandem_style_1'   : 'scoring, x ions',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'kojak_style_1' : {
    #             False : '0',
    #             True  : '1',
    #         },
    #         'omssa_style_1' : {
    #             False : '',
    #             True  : '3',
    #         },
    #         'xtandem_style_1' : {
    #             False : 'no',
    #             True  : 'yes',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, x ions are used in algorithm',
    # },
    # 'score_y_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'kojak_1_5_3',
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #         'myrimatch_2_1_138',
    #         'myrimatch_2_2_140',
    #         'omssa_2_1_9',
    #         'xtandem_cyclone_2010',
    #         'xtandem_jackhammer',
    #         'xtandem_piledriver',
    #         'xtandem_sledgehammer',
    #         'xtandem_vengeance',
    #         'xtandem_alanine',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'kojak_style_1'     : 'ion_series_Y',
    #         'msamanda_style_1'  : 'series',
    #         'myrimatch_style_1' : 'FragmentationRule',
    #         'omssa_style_1'     : '-i',
    #         'xtandem_style_1'   : 'scoring, y ions',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'kojak_style_1' : {
    #             False : '0',
    #             True  : '1',
    #         },
    #         'omssa_style_1' : {
    #             False : '',
    #             True  : '4',
    #         },
    #         'xtandem_style_1' : {
    #             False : 'no',
    #             True  : 'yes',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : True,
    #     'description' : \
    #         'Spectrum: if true, y ions are used in algorithm',
    # },
    # 'score_z+1_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'msamanda_style_1' : 'series',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, z ion plus 1 Da mass are used in algorithm',
    # },
    # 'score_z+2_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'msamanda_style_1' : 'series',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true z ion plus 2 Da mass are used in algorithm',
    # },
    # 'score_z_ions' : {
    #     'edit_version' : 1.00,
    #     'available_in_unode' : [
    #         'kojak_1_5_3',
    #         'msamanda_1_0_0_5242',
    #         'msamanda_1_0_0_5243',
    #         'msamanda_1_0_0_6299',
    #         'msamanda_1_0_0_6300',
    #         'msamanda_1_0_0_7503',
    #         'msamanda_1_0_0_7504',
    #         'myrimatch_2_1_138',
    #         'myrimatch_2_2_140',
    #         'omssa_2_1_9',
    #         'xtandem_cyclone_2010',
    #         'xtandem_jackhammer',
    #         'xtandem_piledriver',
    #         'xtandem_sledgehammer',
    #         'xtandem_vengeance',
    #         'xtandem_alanine',
    #     ],
    #     'triggers_rerun' : True,
    #     'ukey_translation' : {
    #         'kojak_style_1'     : 'ion_series_Z',
    #         'msamanda_style_1'  : 'series',
    #         'myrimatch_style_1' : 'FragmentationRule',
    #         'omssa_style_1'     : '-i',
    #         'xtandem_style_1'   : 'scoring, z ions',
    #     },
    #     'utag' : [
    #         'scoring',
    #     ],
    #     'uvalue_translation' : {
    #         'kojak_style_1' : {
    #             False : '0',
    #             True  : '1',
    #         },
    #         'omssa_style_1' : {
    #             False : '',
    #             True  : '5',
    #         },
    #         'xtandem_style_1' : {
    #             False : 'no',
    #             True  : 'yes',
    #         },
    #     },
    #     'uvalue_type' : 'bool',
    #     'uvalue_option' : {
    #     },
    #     'default_value' : False,
    #     'description' : \
    #         'Spectrum: if true, z ions are used in algorithm',
    # },
    'search_for_saps' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, saps',
        },
        'utag' : [
            'protein',
            'modifications'
        ],
        'uvalue_translation' : {
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Search for potential single amino acid polymorphisms. \'True\' '\
            'might cause problems in the downstream processing of th result '\
            'files (unify_csv, ...)',
    },
    'semi_enzyme' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msamanda_2_0_0_9706',
            'msamanda_2_0_0_9695',
            'msamanda_2_0_0_10695',
            'msamanda_2_0_0_11219',
            'msamanda_2_0_0_13723',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v2018_01_30',
            'msgfplus_v2018_06_28',
            'msgfplus_v2018_09_12',
            'msgfplus_v2019_01_22',
            'msgfplus_v2019_04_18',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'      : 'enzyme_constraint_min_number_termini',
            'msamanda_style_1'  : 'enzyme specificity',
            'msgfplus_style_1'  : '-ntt',
            'myrimatch_style_1' : 'MinTerminiCleavages',
            'omssa_style_1'     : 'semi_enzyme',
            'unify_csv_style_1' : 'semi_enzyme',
            'xtandem_style_1'   : 'protein, cleavage semi',
            'msfragger_style_1' : 'num_enzyme_termini'
        },
        'utag' : [
            'protein',
            'cleavage'
        ],
        'uvalue_translation' : {
            'moda_style_1' : {
                False : 2,
                True  : 1,
            },
            'msamanda_style_1' : {
                False : 'Full',
                True  : 'Semi',
            },
            'msgfplus_style_1' : {
                False : 2,
                True  : 1,
            },
            'myrimatch_style_1' : {
                False : 2,
                True  : 1,
            },
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
            'msfragger_style_1': {
                True : 1,
                False : 2
            }
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Allows semi-enzymatic peptide ends',
    },
    'show_unodes_in_development' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'show_unodes_in_development',
        },
        'utag' : [
            'internal'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Show ursgal nodes that are in development: False or True',
    },
    'spec_dynamic_range' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'spectrum, dynamic range',
        },
        'utag' : [
            'fragment',
            'spectrum',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 100,
        'description' : \
            'Internal normalization for MS/MS spectrum: The highest peak '\
            '(intensity) within a spectrum is set to given value and all '\
            'other peaks are normalized to this peak. If the normalized value '\
            'is less than 1 the peak is rejected.',
    },
    'ssl_score_column_name' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'csv2ssl_1_0_0',
        ],
        'default_value' : "q-value",
        'description' :  ''' Name of the column that includes the scores that should be used for the .ssl file ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'csv2ssl_style_1' : 'score_column_name',
        },
        'utag' : [
            'scoring',
            'conversion'
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'multiple_line' : False,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "str",
    },
    'ssl_score_type' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'csv2ssl_1_0_0',
        ],
        'default_value' : "PERCOLATOR QVALUE",
        'description' :  ''' Type of scores used for the .ssl file ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'csv2ssl_style_1' : 'score_type',
        },
        'utag' : [
            'scoring',
            'conversion'
        ],
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values' : ['UNKNOWN', 'PERCOLATOR QVALUE', 'TANDEM EXPECTATION VALUE', 'OMSSA EXPECTATION SCORE'],
            'radio_button' : False,
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "select",
    },
    'svm_c_param' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'svm_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'svm_style_1' : 'c',
        },
        'utag' : [
            'scoring',
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'f-point'   : 1e-01,
            'updownval' : 0.1,
            'unit'      : ''
        },
        'default_value' : 1.0,
        'description' : \
            'Penalty parameter C of the error term of the post-processing SVM',
    },
    'test_param1' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            '_test_node',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            '_test_node_style_1' : 'test_param1',
        },
        'utag' : [
            'internal',
            'testing',
        ],
        'uvalue_translation' : {
            '_test_node_style_1' : {
                'a' : 'A',
                'b' : 'B',
                'c' : 'C',
                'd' : 'D',
                'e' : 'E',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['a', 'b', 'c', 'd', 'e'],
            'custom_val_max' : 0,
        },
        'default_value' : 'b',
        'description' : \
            'TEST/DEBUG: Internal Ursgal parameter 1 for debugging and testing.',
    },
    'test_param2' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            '_test_node',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            '_test_node_style_1' : 'test_param2',
        },
        'utag' : [
            'internal',
            'testing',
        ],
        'uvalue_translation' : {
            '_test_node_style_1' : {
                'one'   : 1,
                'two'   : 2,
                'three' : 3,
                'four'  : 4,
                'five'  : 5,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'select_type' : 'radio_button',
            'available_values'  : ['one', 'two', 'three', 'four', 'five'],
            'custom_val_max' : 0,
        },
        'default_value' : 'three',
        'description' : \
            'TEST/DEBUG: Internal Ursgal parameter 2 for debugging and testing.',
    },
    'threshold_is_log10' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sanitize_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sanitize_csv_style_1' : 'threshold_is_log10',
        },
        'utag' : [
            'validation',
            'scoring'
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'True, if log10 scale has been used for score_diff_threshold.',
    },
    'unify_csv_converter_version' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'unify_csv_converter_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'unify_csv_1_0_0',
        'description' : \
            'unify csv converter version: version name',
    },
    'use_pyqms_for_mz_calculation' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'unify_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'unify_csv_style_1' : 'use_pyqms_for_mz_calculation',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Use pyQms for accurate calculation of isotopologue m/z. This will affect the accuracy (ppm) calculation as well. If True, unify_csv will be significantly slower. Please note that this does not work for any type of labeling yet.'
    },
    'ursgal_resource_url' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'ucontroller_style_1' : 'ursgal_resource_url',
        },
        'utag' : [
            'download',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'https://www.sas.upenn.edu/~sschulze/ursgal_resources/',
        'description' : \
            'URL that is used to prepare and install resources via corresponding scripts (prepare_resources.py and install_resources.py)',
    },
    'use_quality_filter' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-no_quality_filter',
        },
        'utag' : [
            'spectrum',
        ],
        'uvalue_translation' : {
            'pepnovo_style_1' : {
                False : True,
                True  : False,
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Use filter for low quality spectra.',
    },
    'use_refinement' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'refine',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'X! TANDEM can use \'refinement\' to improve the speed and '\
            'accuracy of peptide modelling. This is not included in Ursgal, '\
            'yet. See further: http://www.thegpm.org/TANDEM/api/refine.html',
    },
    'use_spectrum_charge' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
            'msfragger_20170103',
            'msfragger_20171106',
            'msfragger_20190222',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-use_spectrum_charge',
            'msfragger_style_1': 'override_charge'
        },
        'utag' : [
            'precursor',
            'spectrum'
        ],
        'uvalue_translation' : {
            'msfragger_style_1' : {
                True : 0,
                False : 1,
            }
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Does not correct precursor charge.',
    },
    'use_spectrum_mz' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'moda_v1_61',
            'moda_v1_62',
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'    : 'AutoPMCorrection',
            'pepnovo_style_1' : '-use_spectrum_mz',
        },
        'utag' : [
            'precursor',
            'spectrum'
        ],
        'uvalue_translation' : {
            'moda_style_1' : {
                False : '1',
                True  : '0',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Does not correct precusor m/z.',
    },
    'validated_ident_csv_suffix' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'validated_ident_csv_suffix',
        },
        'utag' : [
            'file_handling',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'validated.csv',
        'description' : \
            'CSV suffix of validated identification files: string, CSV-file '\
            'which contains PSMs validated with validation tools',
    },
    'validation_generalized' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'qvality_2_02',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'qvality_style_1' : '-g',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_translation' : {
            'qvality_style_1' : {
                False : None,
                True  : '',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Generalized target decoy competition, situations where PSMs '\
            'known to more frequently be incorrect are mixed in with the '\
            'correct PSMs',
    },
    'validation_minimum_score' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'qvality_2_02',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'qvality_style_1' : 'validation_minimum_score',
        },
        'utag' : [
            'scoring',
            'validation',
        ],
        'uvalue_translation' : {
            'qvality_style_1' : {
                'msamanda_1_0_0_5242'  : 0,
                'msamanda_1_0_0_5243'  : 0,
                'msamanda_1_0_0_6299'  : 0,
                'msamanda_1_0_0_6300'  : 0,
                'msamanda_1_0_0_7503'  : 0,
                'msamanda_1_0_0_7504'  : 0,
                'msamanda_2_0_0_9706'  : 0,
                'msamanda_2_0_0_9695'  : 0,
                'msamanda_2_0_0_10695' : 0,
                'msamanda_2_0_0_11219' : 0,
                'msamanda_2_0_0_13723' : 0,
                'msgfplus_v2018_01_30' : 1e-100,
                'msgfplus_v2016_09_16' : 1e-100,
                'msgfplus_v2017_01_27' : 1e-100,
                'msgfplus_v2018_09_12' : 1e-100,
                'msgfplus_v2019_01_22' : 1e-100,
                'msgfplus_v2019_04_18' : 1e-100,
                'msgfplus_v2018_06_28' : 1e-100,
                'msgfplus_v9979'       : 1e-100,
                'myrimatch_2_1_138'    : 0,
                'myrimatch_2_2_140'    : 0,
                'omssa_2_1_9'          : 1e-30,
                'xtandem_cyclone_2010' : 0,
                'xtandem_jackhammer'   : 0,
                'xtandem_piledriver'   : 0,
                'xtandem_sledgehammer' : 0,
                'xtandem_vengeance'    : 0,
                'xtandem_alanine'      : 0,
                'msfragger_20170103'   : 0,
                'msfragger_20171106'   : 0,
                'msfragger_20190222'   : 0,
                'pipi_1_4_5'           : 0,
                'pipi_1_4_6'           : 0,
                'moda_v1_51'           : 0,
                'moda_v1_61'           : 0,
                'moda_v1_62'           : 0,
            },
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : 'None',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Defines the minimum score used for validation. If scores lower '\
            'than this are produced, they are set to the minimum score. This '\
            'is used to avoid huge gaps/jumps in the score distribution\n'\
            '    \'None\' : None',
    },
    'validation_score_field' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'add_estimated_fdr_1_0_0',
            'percolator_2_08',
            'percolator_3_2_1',
            'percolator_3_4_0',
            'qvality_2_02',
            'sanitize_csv_1_0_0',
            'svm_1_0_0',
            'ucontroller',
            'unify_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'add_estimated_fdr_style_1' : 'validation_score_field',
            'percolator_style_1'        : 'validation_score_field',
            'qvality_style_1'           : 'validation_score_field',
            'sanitize_csv_style_1'      : 'validation_score_field',
            'svm_style_1'               : 'validation_score_field',
            'ucontroller_style_1'       : 'validation_score_field',
            'unify_csv_style_1'         : 'validation_score_field',
        },
        'utag' : [
            'validation',
            'scoring'
        ],
        'uvalue_translation' : {
            'add_estimated_fdr_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msamanda_2_0_0_9706'  : 'Amanda:Score',
                'msamanda_2_0_0_9695'  : 'Amanda:Score',
                'msamanda_2_0_0_10695' : 'Amanda:Score',
                'msamanda_2_0_0_11219' : 'Amanda:Score',
                'msamanda_2_0_0_13723' : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_01_30' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_06_28' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_09_12' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_01_22' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_04_18' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'novor_1_05'           : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'xtandem_alanine'      : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
                'msfragger_20171106'   : 'MSFragger:Hyperscore',
                'msfragger_20190222'   : 'MSFragger:Hyperscore',
                'mascot_x_x_x'         : 'Mascot:Score',
                'pipi_1_4_5'           : 'PIPI:score',
                'pipi_1_4_6'           : 'PIPI:score',
                'moda_v1_51'           : 'ModA:probability',
                'moda_v1_61'           : 'ModA:probability',
                'moda_v1_62'           : 'ModA:probability',
                'pglyco_db_2_2_0'      : 'pGlyco:TotalScore',
                'deepnovo_0_0_1'       : 'DeepNovo:score',
            },
            'percolator_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msamanda_2_0_0_9706'  : 'Amanda:Score',
                'msamanda_2_0_0_9695'  : 'Amanda:Score',
                'msamanda_2_0_0_10695' : 'Amanda:Score',
                'msamanda_2_0_0_11219' : 'Amanda:Score',
                'msamanda_2_0_0_13723' : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_01_30' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_06_28' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_09_12' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_01_22' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_04_18' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'novor_1_05'           : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'xtandem_alanine'      : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
                'msfragger_20171106'   : 'MSFragger:Hyperscore',
                'msfragger_20190222'   : 'MSFragger:Hyperscore',
                'mascot_x_x_x'         : 'Mascot:Score',
                'pipi_1_4_5'           : 'PIPI:score',
                'pipi_1_4_6'           : 'PIPI:score',
                'moda_v1_51'           : 'ModA:probability',
                'moda_v1_61'           : 'ModA:probability',
                'moda_v1_62'           : 'ModA:probability',
                'pglyco_db_2_2_0'      : 'pGlyco:TotalScore',
                'deepnovo_0_0_1'       : 'DeepNovo:score',
            },
            'qvality_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msamanda_2_0_0_9706'  : 'Amanda:Score',
                'msamanda_2_0_0_9695'  : 'Amanda:Score',
                'msamanda_2_0_0_10695' : 'Amanda:Score',
                'msamanda_2_0_0_11219' : 'Amanda:Score',
                'msamanda_2_0_0_13723' : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_01_30' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_06_28' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_09_12' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_01_22' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_04_18' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'novor_1_05'           : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'xtandem_alanine'      : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
                'msfragger_20171106'   : 'MSFragger:Hyperscore',
                'msfragger_20190222'   : 'MSFragger:Hyperscore',
                'mascot_x_x_x'         : 'Mascot:Score',
                'pipi_1_4_5'           : 'PIPI:score',
                'pipi_1_4_6'           : 'PIPI:score',
                'moda_v1_51'           : 'ModA:probability',
                'moda_v1_61'           : 'ModA:probability',
                'moda_v1_62'           : 'ModA:probability',
                'pglyco_db_2_2_0'      : 'pGlyco:TotalScore',
                'deepnovo_0_0_1'       : 'DeepNovo:score',
            },
            'sanitize_csv_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msamanda_2_0_0_9706'  : 'Amanda:Score',
                'msamanda_2_0_0_9695'  : 'Amanda:Score',
                'msamanda_2_0_0_10695' : 'Amanda:Score',
                'msamanda_2_0_0_11219' : 'Amanda:Score',
                'msamanda_2_0_0_13723' : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_01_30' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_06_28' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_09_12' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_01_22' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_04_18' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'novor_1_05'           : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'xtandem_alanine'      : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
                'msfragger_20171106'   : 'MSFragger:Hyperscore',
                'msfragger_20190222'   : 'MSFragger:Hyperscore',
                'mascot_x_x_x'         : 'Mascot:Score',
                'pipi_1_4_5'           : 'PIPI:score',
                'pipi_1_4_6'           : 'PIPI:score',
                'moda_v1_51'           : 'ModA:probability',
                'moda_v1_61'           : 'ModA:probability',
                'moda_v1_62'           : 'ModA:probability',
                'pglyco_db_2_2_0'      : 'pGlyco:TotalScore',
                'deepnovo_0_0_1'       : 'DeepNovo:score',
            },
            'svm_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msamanda_2_0_0_9706'  : 'Amanda:Score',
                'msamanda_2_0_0_9695'  : 'Amanda:Score',
                'msamanda_2_0_0_10695' : 'Amanda:Score',
                'msamanda_2_0_0_11219' : 'Amanda:Score',
                'msamanda_2_0_0_13723' : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_01_30' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_06_28' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_09_12' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_01_22' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_04_18' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'novor_1_05'           : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'xtandem_alanine'      : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
                'msfragger_20171106'   : 'MSFragger:Hyperscore',
                'msfragger_20190222'   : 'MSFragger:Hyperscore',
                'mascot_x_x_x'         : 'Mascot:Score',
                'pipi_1_4_5'           : 'PIPI:score',
                'pipi_1_4_6'           : 'PIPI:score',
                'moda_v1_51'           : 'ModA:probability',
                'moda_v1_61'           : 'ModA:probability',
                'moda_v1_62'           : 'ModA:probability',
                'pglyco_db_2_2_0'      : 'pGlyco:TotalScore',
                'deepnovo_0_0_1'       : 'DeepNovo:score',
            },
            'ucontroller_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msamanda_2_0_0_9706'  : 'Amanda:Score',
                'msamanda_2_0_0_9695'  : 'Amanda:Score',
                'msamanda_2_0_0_10695' : 'Amanda:Score',
                'msamanda_2_0_0_11219' : 'Amanda:Score',
                'msamanda_2_0_0_13723' : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_01_30' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_06_28' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_09_12' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_01_22' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_04_18' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'novor_1_05'           : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'xtandem_alanine'      : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
                'msfragger_20171106'   : 'MSFragger:Hyperscore',
                'msfragger_20190222'   : 'MSFragger:Hyperscore',
                'mascot_x_x_x'         : 'Mascot:Score',
                'pipi_1_4_5'           : 'PIPI:score',
                'pipi_1_4_6'           : 'PIPI:score',
                'moda_v1_51'           : 'ModA:probability',
                'moda_v1_61'           : 'ModA:probability',
                'moda_v1_62'           : 'ModA:probability',
                'pglyco_db_2_2_0'      : 'pGlyco:TotalScore',
                'deepnovo_0_0_1'       : 'DeepNovo:score',
            },
            'unify_csv_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msamanda_2_0_0_9706'  : 'Amanda:Score',
                'msamanda_2_0_0_9695'  : 'Amanda:Score',
                'msamanda_2_0_0_10695' : 'Amanda:Score',
                'msamanda_2_0_0_11219' : 'Amanda:Score',
                'msamanda_2_0_0_13723' : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_01_30' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_06_28' : 'MS-GF:SpecEValue',
                'msgfplus_v2018_09_12' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_01_22' : 'MS-GF:SpecEValue',
                'msgfplus_v2019_04_18' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'novor_1_05'           : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'xtandem_alanine'      : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
                'msfragger_20171106'   : 'MSFragger:Hyperscore',
                'msfragger_20190222'   : 'MSFragger:Hyperscore',
                'mascot_x_x_x'         : 'Mascot:Score',
                'pipi_1_4_5'           : 'PIPI:score',
                'pipi_1_4_6'           : 'PIPI:score',
                'moda_v1_51'           : 'ModA:probability',
                'moda_v1_61'           : 'ModA:probability',
                'moda_v1_62'           : 'ModA:probability',
                'pglyco_db_2_2_0'      : 'pGlyco:TotalScore',
                'deepnovo_0_0_1'       : 'DeepNovo:score',
            },
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : 'None',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Name of the column that is used for validation, e.g. by qvality '\
            'and percolator. If None is defined, default values are used\n'\
            '    \'None\' : None',
    },
    'visualization_column_names' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'visualization_column_names',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'item_title' : 'column name',
            'item_type' : 'str',
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
            'Modifications',
            'Sequence',
        ],
        'description' : \
            'The specified csv column names are used for the visualization. '\
            'E.g. for a Venn diagram the entries of these columns are used '\
            '(merged) to determine overlapping results.',
    },
    'visualization_font' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'visualization_font',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : {},
            'item_titles' : {
                'font_type' : 'type',
                'font_size_header' : 'size',
                'font_size_major' : 'size',
                'font_size_minor' : 'size',
                'font_size_venn' : 'size',
            },
            'value_types' : {
                'font_type' : 'str',
                'font_size_header' : 'int',
                'font_size_major' : 'int',
                'font_size_minor' : 'int',
                'font_size_venn' : 'int',
            },
            'multiple_line' : {
                'font_type' : False,
            },
            'max' : {
                'font_size_header' : 1000,
                'font_size_major' : 1000,
                'font_size_minor' : 1000,
                'font_size_venn' : 1000,
            },
            'min' : {
                'font_size_header' : 0,
                'font_size_major' : 0,
                'font_size_minor' : 0,
                'font_size_venn' : 0,
            },
            'updownval' : {
                'font_size_header' : 1,
                'font_size_major' : 1,
                'font_size_minor' : 1,
                'font_size_venn' : 1,
            },
            'unit' : {
                'font_size_header' : 'pt',
                'font_size_major' : 'pt',
                'font_size_minor' : 'pt',
                'font_size_venn' : 'pt',
            },
            'custom_val_max' : 0,
        },
        'default_value' : {
            'font_type' : 'Helvetica',
            'font_size_header' : 31,
            'font_size_major' : 25,
            'font_size_minor' : 20,
            'font_size_venn' : 20
        },
        'description' : \
            'Font used for visualization plots (e.g. Venn diagram), given as '\
            'dict with keys: font_type, font_size_header, font_size_major, font_size_minor,'\
            ' font_size_venn',
    },
    'visualization_header' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'header',
            'sugarpy_plot_style_1' : 'title',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : '',
        'description' : \
            'Header of visualization output (e.g. Venn diagram)',
    },
    'visualization_color_positions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'visualization_color_position',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : None,
            'item_titles' : {'position':'color'},
            'value_types' : {'position':'str'},
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : {},
        'description' : \
            'Specifies colors for the datasets that should be visualized. '\
            'Given as a dict in which the key represents the position '\
            'of the corresponding dataset in the list, e.g.: '\
            '{"0" : "#e41a1c", "1" : "#377eb8"}',
    },
    'visualization_label_positions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'visualization_label_position',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : None,
            'item_titles' : {'position':'label'},
            'value_types' : {'position':'str'},
            'custom_val_max' : 10000,
            'multiple_line' : False,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : {},
        'description' : \
            'Specifies labels for the datasets that should be visualized. '\
            'Given as a dict in which the key represents the position '\
            'of the corresponding dataset in the list, e.g.: '\
            '{"0" : "LabelA", "1" : "LabelB"}',
    },
    'visualization_opacity' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'opacity',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000,
            'min'       : 0,
            'f-point'   : 1e-03,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 0.35,
        'description' : \
            'Opacity used in visualization plots (e.g. Venn diagram)',
    },
    'visualization_scaling_factors' : {
        'edit_version' : 1.01,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'visualization_scaling_factors',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : {},
            'item_titles' : {
                'x_axis' : 'factor',
                'y_axis' : 'factor',
            },
            'value_types' : {
                'x_axis' : 'int',
                'y_axis' : 'int',
            },
            'max': {
                'x_axis' : 100000,
                'y_axis' : 100000,
            },
            'min': {
                'x_axis' : 1,
                'y_axis' : 1,
            },
            'updownval': {
                'x_axis' : 1,
                'y_axis' : 1,
            },
            'unit': {
                'x_axis' : '',
                'y_axis' : '',
            },
            'custom_val_max' : 0,
        },
        # 'uvalue_option' : {
            # 'none_val'       : None,
            # 'title_list' : [
            #     'x-axis-scaling-factor',
            #     'y-axis-scaling-factor',
            # ],
            # 'type_dict' : {
            #     'x-axis-scaling-factor' : 'int',
            #     'y-axis-scaling-factor' : 'int',
            # },
        # },
        'default_value' : {
            'x_axis' : 600,
            'y_axis' : 400,
        },
        'description' : \
            'Scaling factor for visualization plots (e.g. Venn diagram), '\
            'given as dict with keys: x_axis, y_axis',
    },
    'visualization_size' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'visualization_size',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'none_val' : {},
            'item_titles' : {
                'width' : 'size',
                'height' : 'size',
            },
            'value_types' : {
                'width' : 'int',
                'height' : 'int',
            },
            'max': {
                'width'  : 100000,
                'height' : 100000,
            },
            'min': {
                'width'  : 1,
                'height' : 1,
            },
            'updownval': {
                'width'  : 1,
                'height' : 1,
            },
            'unit': {
                'width'  : 'px',
                'height' : 'px',
            },
            'custom_val_max' : 0,
        },
        # 'uvalue_option' : {
            # 'none_val'       : None,
            # 'title_list' : [
            #     'width',
            #     'height',
            # ],
            # 'type_dict' : {
            #     'width'  : 'int',
            #     'height' : 'int',
            # },
        # },
        'default_value' : {
            'width' : 1200,
            'height' : 900
        },
        'description' : \
            'Size of visualization plots (e.g. Venn diagram), given as dict '\
            'with keys: width, height',
    },
    'visualization_stroke_width' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'stroke-width',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'f-point'   : 1e-05,
            'updownval' : 0.01,
            'unit'      : ''
        },
        'default_value' : 2.0,
        'description' : \
            'Stroke width used in visualization plots (e.g. Venn diagram)',
    },
    'window_size' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'combine_pep_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'combine_pep_style_1' : 'window_size',
        },
        'utag' : [
            'validation',
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 249,
        'description' : \
            'Combined PEPs are computed by iterating a sliding window over '\
            'the sorted PSMs. Each PSM receives a PEP based on the '\
            'target/decoy ratio of the surrounding PEPs. This parameter '\
            'defines the window size.',
    },
    'word_len' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'unify_csv_1_0_0',
            'upeptide_mapper_1_0_0',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'unify_csv_style_1' : 'word_len',
            'upeptide_mapper_style_1' : 'word_len',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 6,
        'description' : \
            'word length used to index '\
            'peptide mapper, smaller word len requires more memory',
    },
    'write_unfiltered_results' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'filter_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'filter_csv_style_1' : 'write_unfiltered_results',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Writes rejected results if True',
    },
    'xtandem_converter_version' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'default_value' : 'xtandem2csv_1_0_0',
        'description' :  ''' Determines which X!tandem conversion node should be used e.g. "xtandem2csv_1_0_0"''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'xtandem_converter_version',
        },
        'utag' : [
            'node_versions',
        ],
        'uvalue_option' : {
            'none_val'     : '',
            'multiple_line' : False,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "str",
    },
    'xtandem_stp_bias' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'xtandem_alanine',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, stP bias',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Interpretation of peptide phosphorylation models.',
    },
    'glycans_incl_as_mods' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : [
            'HexNAc',
            'HexNAc(2)',
        ],
        'description' :  ''' List of Unimod PSI-MS names corresponding to glycans that were included in the database search as modification (will be removed from the peptidoform by SugarPy). ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_run_style_1' : 'unimod_glycans_incl_in_search',
            'sugarpy_plot_style_1' : 'unimod_glycans_incl_in_search',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_option' : {
            'none_val' : [],
            'item_title' : 'PSI-MS',
            'item_type' : 'str',
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "list",
    },
    'use_median_accuracy' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_run_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_run_style_1' : 'use_median_accuracy',
        },
        'utag' : [
            'accuracy',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'select',
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'None',
                'all',
                'peptide',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'None',
        'description' : \
            'Accuracy of identifications (ident_file) are used to calculate the machine_offset_in_ppm. If "all" is selected, the median of all identifications will be used, for "peptide" the median of each peptide will be used.',
    },
    'min_glycan_length' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_run_1_0_0',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'sugarpy_run_style_1' : 'min_tree_length',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 3,
        'description' : \
            'Minimum number of monosaccharides per glycan'\
    },
    'max_glycan_length' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'sugarpy_run_style_1' : 'max_tree_length',
            'sugarpy_plot_style_1' : 'max_tree_length',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 15,
        'description' : \
            'Maximum number of monosaccharides per glycan'\
    },
    'monosaccharide_compositions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : {
            "dHex": 'C6H10O4',
            # "dHexNAc": 'C8H13NO4',
            "Hex": 'C6H10O5',
            # "HexA": 'C6H8O6',
            "HexNAc": 'C8H13NO5',
            # "Me2Hex": 'C8H14O5',
            # "MeHex": 'C7H12O5',
            "NeuAc": 'C11H17NO8',
            "Pent": 'C5H8O4',
            # 'dHexN': 'C6H11O3N',
            # 'HexN': 'C6H11O4N',
            # 'MeHexA': 'C7H10O6',
        },
        'description' :  ''' Dictionary defining the chemical formula (hill notation) for each monosaccharide that is used. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_run_style_1' : 'monosaccharides',
            'sugarpy_plot_style_1' : 'monosaccharides',
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'name' : 'formula',
            },
            'value_types' : {
                'str' : 'str',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'mzml_input_file' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_run_style_1': 'mzml_file',
            'sugarpy_plot_style_1': 'mzml_file',
        },
        'utag' : [
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
            'input_extensions' : ['.mzML']
        },
        'default_value' : None,
        'description' : \
            'Path to the mzML input file'
    },
    'sugarpy_results_pkl' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1': 'validated_results_pkl',
        },
        'utag' : [
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
            'input_extensions' : ['.pkl']
        },
        'default_value' : None,
        'description' : \
            'Path to the SugarPy results .pkl'
    },
    'sugarpy_results_csv' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1': 'result_file',
        },
        'utag' : [
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
            'input_extensions' : ['.csv']
        },
        'default_value' : None,
        'description' : \
            'Path to the SugarPy results .csv'
    },
    'min_number_of_spectra': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1000,
            'min': 0,
            'updownval': 1,
            'unit': '',
        },
        'default_value': 2,
        'description': """ Min number of spectra in which a molecule needs to be matched in order to consider it for further processing """,
        'triggers_rerun': True,
        'ukey_translation': {
            'sugarpy_run_style_1': 'min_spec_number',
            'sugarpy_plot_style_1': 'min_spec_number',
        },
        'utag': [
            'accuracy'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "int",
    },
    'max_trees_per_spec': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1000,
            'min': 0,
            'updownval': 1,
            'unit': '',
        },
        'default_value': 5,
        'description': """ Max number of glycoforms reported per spectrum for each peptide """,
        'triggers_rerun': True,
        'ukey_translation': {
            'sugarpy_run_style_1': 'max_trees_per_spec',
            'sugarpy_plot_style_1': 'max_trees_per_spec',
        },
        'utag': [
            'output'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "int",
    },
    'min_sugarpy_score': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 0.1,
            'unit': 'abundance',
            'f-point': 1e-02
        },
        'default_value': 1.0,
        'description': """ Min SugarPy score to be considered for output """,
        'triggers_rerun': True,
        'ukey_translation': {
            'sugarpy_run_style_1': 'min_sugarpy_score',
            'sugarpy_plot_style_1': 'min_sugarpy_score',
        },
        'utag': [
            'accuracy',
            'scoring',
            'output'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'min_subtree_coverage': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'sugarpy_run_1_0_0',
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 0.1,
            'unit': 'abundance',
            'f-point': 1e-02
        },
        'default_value': 0.6,
        'description': """ Min subtree coverage to be considered for output """,
        'triggers_rerun': True,
        'ukey_translation': {
            'sugarpy_run_style_1': 'min_sub_cov',
            'sugarpy_plot_style_1': 'min_sub_cov',
        },
        'utag': [
            'accuracy',
            'scoring',
            'output'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "float",
    },
    'sugarpy_plot_types' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : [
            'plot_glycan_elution_profile',
        ],
        'description' :  ''' List of plot types that should be created by the SugarPy plotting function. Available are: "plot_molecule_elution_profile", "plot_glycan_elution_profile", "plot_annotated_spectra", "check_peak_presence", "check_frag_specs" ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'plot_types',
        },
        'utag' : [
            'output',
            'visualization'
        ],
        'uvalue_option' : {
            'none_val' : [],
            'item_title' : 'Plot type',
            'item_type' : 'str',
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "list",
    },
    'sugarpy_plot_peak_types' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : [
            'matched',
            'unmatched',
            'labels',
        ],
        'description' :  ''' List of peak types that should be plotted by the SugarPy plot spectrum function. Available are: "matched" (peaks matched by pyQms), "unmatched" (unmatched peaks from matched formulas), "labels@ (for monoisotopic peaks) ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'plot_peak_types',
        },
        'utag' : [
            'output',
            'visualization'
        ],
        'uvalue_option' : {
            'none_val' : [],
            'item_title' : 'Plot peak type',
            'item_type' : 'str',
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "list",
    },
    'sugarpy_remove_subtrees' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : [
        ],
        'description' :  ''' List of subtree formulas (hill notation) that should not be plotted. Formulas include the complete molecule, i.e. peptide and glycan ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'remove_subtrees',
        },
        'utag' : [
            'output',
            'visualization',
        ],
        'uvalue_option' : {
            'none_val' : [],
            'item_title' : 'Formula',
            'item_type' : 'str',
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "list",
    },
    'sugarpy_include_subtrees' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : 'no_subtrees',
        'description' :  ''' Defines if/how subtrees should be taken into account for plotting molecule elution profiles in SugarPy. Available are: "no_subtrees", "sum_subtrees", "individual_subtrees" ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'include_subtrees',
        },
        'utag' : [
            'output',
            'visualization',
        ],
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'no_subtrees',
                'sum_subtrees',
                'individual_subtrees',
            ],
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "select",
    },
    'sugarpy_plot_molecule_dict' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : {
        },
        'description' :  ''' The dict contains all peptidoforms (Peptide#Unimod:Pos) as keys and a dict with the glycans (keys) and {'charges':set(), 'file_names':set()} (value) as values. It can be auto generated from a SugarPy results .csv (use uparam sugarpy_results_file to specify). Don't use sugarpy_results_file and sugarpy_plot_molecule_dict at the same time! ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'plot_molecule_dict'
        },
        'utag' : [
            'output',
            'visualization'
        ],
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'Peptidoform' : 'Glycans',
            },
            'value_types' : {
                'str' : 'dict',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'peak_colors' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : {
            'matched': 'rgb(0, 200, 0)',
            'unmatched': 'rgb(200, 0, 0)',
            'labels': 'rgb(0, 0, 200)',
            'raw': 'rgb(100, 100, 100)',
        },
        'description' :  ''' The dict defines the colors of "matched", "unmatched", "raw" peaks and "labels" ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'peak_colors'
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'Peak type' : 'Color',
            },
            'value_types' : {
                'str' : 'dict',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'x_axis_type' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : 'retention_time',
        'description' :  ''' Defines the values used for the x-axis. Available are: "retention_time", "spectrum_id" ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'x_axis_type',
        },
        'utag' : [
            'output',
            'visualization',
        ],
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'retention_time',
                'spectrum_id',
            ],
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "select",
    },
    'sugarpy_score_type' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : 'top_scores',
        'description' :  ''' Defines the score type used for the y-axis. Available are: "top_scores", "sum_scores" ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'score_type',
        },
        'utag' : [
            'output',
            'visualization',
        ],
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'top_scores',
                'sum_scores',
            ],
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "select",
    },
    'plotly_layout' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'default_value' : {
        },
        'description' :  ''' The dict defines plotly layout options. Checkout https://plot.ly/python/reference/#layout for all available options ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1' : 'plotly_layout'
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'Plotly option' : 'Value',
            },
            'value_types' : {
                'str' : 'dict',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'sugarpy_decoy_glycan' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1': 'decoy_glycan',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : 'End(HexNAc)Hex(5)HexNAc(3)NeuAc(1)dHex(1)',
        'description' : '''Glycan (given in the SugarPy Hill noation format) that will be used for matching glycopeptide fragment ions in MS2 spectra from non-glycosylated peptides '''
    },
    'min_oxonium_ions': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1000,
            'min': 0,
            'updownval': 1,
            'unit': '',
        },
        'default_value': 3,
        'description': """ Min number of oxonium ions that need to be matched in an MS/MS spectrum, to be accepted as containing oxonium ions (i.e. considered as glycopeptide) """,
        'triggers_rerun': True,
        'ukey_translation': {
            'sugarpy_plot_style_1': 'min_oxonium_ions'
        },
        'utag': [
            'scoring'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "int",
    },
    'min_y_ions': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'sugarpy_plot_1_0_0',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1000,
            'min': 0,
            'updownval': 1,
            'unit': '',
        },
        'default_value': 1,
        'description': """ Min number of Y-ions that need to be matched in an MS/MS spectrum, to be accepted as containing Y-ions (i.e. considered as glycopeptide) """,
        'triggers_rerun': True,
        'ukey_translation': {
            'sugarpy_plot_style_1': 'min_Y_ions'
        },
        'utag': [
            'scoring'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "int",
    },
    'ursgal_results_csv' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'sugarpy_plot_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'sugarpy_plot_style_1': 'ursgal_ident_file',
        },
        'utag' : [
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
            'input_extensions' : ['.csv']
        },
        'default_value' : None,
        'description' : \
            'Path to the Ursgal results .csv containing all PSMs in the unified format'
    },
    'add_contaminants' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pipi_1_4_5',
            'pipi_1_4_6',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pipi_style_1'     : 'add_contaminant'
        },
        'utag' : [
            'database',
        ],
        'uvalue_translation' : {
            'pipi_style_1' : {
                False : '0',
                True  : '1',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Contaminants are added automatically to the database by the search engine. PIPI uses the same contaminants database as MaxQuant',
    },
    'extract_venndiagram_file' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
            'venndiagram_1_1_0'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'extract_venndiagram_file'
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_option' : {
        },
        'uvalue_type' : 'bool',
        'default_value' : False,
        'description' : \
            'The user can retrieve a csv file containing results from the venn diagram',
    },
    'pymzml_spec_id_attribute' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_2_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'spec_id_attribute',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'dict',
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'id attribute' : 'Value',
            },
            'value_types' : {
                'str' : 'dict',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'default_value' : {
            'ID': None
        },
        'description' : \
            'Specify the spectrum ID attribute to be used to access the spectrum ID (ID, id_dict or index). Given as a dict (key = attribute, value = key in id_dict). For .wiff files, during conversion to mzML, spectrum IDs are formatted differently; pymzml can deal with this by returning an id_dict or accessing the index.'
    },
    'convert_aa_in_motif' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'generate_target_decoy_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'generate_target_decoy_style_1': 'convert_aa_in_motif',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : None,
        'description' : \
            'Convert a single aminoacid in a sequence motif into another characeter using a string "new_aa,motif,position_to_be_replaced" where new_aa is the new character, motif is the regular expression that identifies the sequenc motif and position_to_be_replaced is the position in the motif that should be replaced (e.g. use "J,N[^P][ST],0" to convert N-X-S/T into J-X-S/T'
    },
    'pparse_options' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pparse_2_0',
        ],
        'default_value' : {
            '-F': 'raw',
            '-m': '1',
            '-p': '0',
        },
        'description' :  ''' Dictionary to specify options and their value for pParse. For available options see http://pfind.ict.ac.cn/software/pParse/# ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pparse_style_1' : 'pparse_options',
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'pparse option' : 'value',
            },
            'value_types' : {
                'str' : 'str',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'thermo_raw_file_parser_options' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'thermo_raw_file_parser_1_1_2',
        ],
        'default_value' : {
            '-e': None,
            '-m': 0,
        },
        'description' :  ''' Dictionary to specify options and their value for ThermoRawFileParser. If options are given as a flag only, specify 'None' as their value. For available options see https://github.com/compomics/ThermoRawFileParser ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'thermo_raw_file_parser_style_1' : ('-h', '-m', '-g', '-u', '-k', '-t', '-n', '-v', '-e'),
        },
        'utag' : [
            'conversion',
        ],
        'uvalue_option' : {
            'custom_type' : {
                'str' : {'multiple_line': False},
            },
            'custom_val_max' : 100000,
            'item_titles' : {
                'converter option' : 'value',
            },
            'value_types' : {
                'str' : 'str',
            },
            'multiple_line' : False,
            'none_val' : {
            },
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "dict",
    },
    'deepnovo_direction' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'deepnovo_0_0_1',
        ],
        'default_value' : 'bi_directional',
        'description' :  ''' Defines the direction for DeepNovo ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'deepnovo_style_1' : 'direction',
        },
        'utag' : [
            'de novo',
        ],
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'bi_directional',
                'forward',
                'reverse',
            ],
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
            'deepnovo_style_1': {
                'bi_directional': 2,
                'forward' : 0,
                'reverse' : 1,
            },
        },
        'uvalue_type' : "select",
    },
    'deepnovo_use_intensity': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'deepnovo_0_0_1',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 1,
            'unit': 'psms',
        },
        'default_value': True,
        'description': ''' DeepNovo uses intensity ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'deepnovo_style_1': 'use_intensity',
        },
        'utag': [
            'de novo',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "bool",
    },
    'deepnovo_shared_weights': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'deepnovo_0_0_1',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 1,
            'unit': 'psms',
        },
        'default_value': True,
        'description': ''' DeepNovo uses shared weights ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'deepnovo_style_1': 'shared',
        },
        'utag': [
            'de novo',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "bool",
    },
    'deepnovo_use_lstm': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'deepnovo_0_0_1',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 1,
            'unit': 'psms',
        },
        'default_value': True,
        'description': ''' DeepNovo uses lstm ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'deepnovo_style_1': 'use_lstm',
        },
        'utag': [
            'de novo',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "bool",
    },
    'deepnovo_build_knapsack': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'deepnovo_0_0_1',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 1,
            'unit': 'psms',
        },
        'default_value': False,
        'description': ''' DeepNovo builds the knapsack matrix ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'deepnovo_style_1': 'knapsack_build',
        },
        'utag': [
            'de novo',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "bool",
    },
    'deepnovo_beam_search': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'deepnovo_0_0_1',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 10000,
            'min': 0,
            'updownval': 1,
            'unit': 'psms',
        },
        'default_value': True,
        'description': ''' DeepNovo builds beam search ''',
        'triggers_rerun': True,
        'ukey_translation': {
            'deepnovo_style_1': 'beam_search',
        },
        'utag': [
            'de novo',
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "bool",
    },
    'deepnovo_beam_size': {
        'edit_version' : 1.00,
        'available_in_unode': [
            'deepnovo_0_0_1',
        ],
        'uvalue_option': {
            'none_val': None,
            'multiple_line': False,
            'max': 1000,
            'min': 0,
            'updownval': 1,
            'unit': '',
        },
        'default_value': 5,
        'description': """ Number of optimal paths to search during decoding """,
        'triggers_rerun': True,
        'ukey_translation': {
            'deepnovo_style_1': 'beam_size'
        },
        'utag': [
            'de novo'
        ],
        'uvalue_translation': {
        },
        'uvalue_type': "int",
    },
    'deepnovo_mode' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'deepnovo_0_0_1',
        ],
        'default_value' : 'search_denovo',
        'description' :  ''' Defines the search mode for DeepNovo ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'deepnovo_style_1': ('search_denovo', 'search_hybrid', 'search_db', 'decode'),
        },
        'utag' : [
            'de novo',
        ],
        'uvalue_option' : {
            'select_type'   : 'radio_button',
            'available_values'  : [
                'search_denovo',
                'search_hybrid',
                'search_db',
                'decode',
            ],
            'custom_val_max' : 0,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "select",
    },
    'deepnovo_knapsack_file' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'deepnovo_0_0_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'deepnovo_style_1': 'knapsack_file',
        },
        'utag' : [
            'de novo',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : '',
            'multiple_line' : False,
        },
        'default_value' : 'default',
        'description' : \
            'Path to the knapsack matrix for DeepNovo. Use "default" for the default file location in the resources'
    },
}
