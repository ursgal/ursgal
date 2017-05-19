ursgal_params = {
    '_extentions' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
        },
        'utag' : [
        ],
        'uvalue_translation' : {
        },
        'uvalue_type'    : 'dict',
        'uvalue_option' : {
            'dict_title' : {
                'extension' : {
                    'tag' : 'cont',
                },
            },
            'dict_type' : {
                'short_name'     : 'str',
                'long_name'      : 'str',
                'same_extension' : 'list',
                'description'    : 'str',
            },
            'multiple_line' : {
                'short_name'     : False,
                'long_name'      : False,
                'description'    : False,
            },
            'title_list' : {
                'same_extension' : [],
            },
            'type_dict' : {
            },
            'custom_val_max' : 0,
        },
        'default_value' : {
            '.csv' : {
                'short_name'     : 'CSV',
                'long_name'      : 'CSV (Comma Delimited)',
                'same_extension' : [],
                'description'    : \
                    'The comma-separated values (CSV) file format is a '\
                    'tabular data format that has fields separated by the '\
                    'comma character and quoted by the double quote '\
                    'character.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.den' : {
                'short_name'     : 'DEN',
                'long_name'      : 'DEN (XMVB Density Data)',
                'same_extension' : [],
                'description'    : \
                    'DEN file is a XMVB Density Data. Xiamen Valence Bond '\
                    '(XMVB) is a quantum chemistry program for performing '\
                    'electronic structure calculations based on the '\
                    'non-orthogonal Valence Bond methods.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.dta' : {
                'short_name'     : 'DTA',
                'long_name'      : 'DTA (Stata Data)',
                'same_extension' : [],
                'description'    : \
                    'DTA file is a Stata Data File. Stata is a '\
                    'general-purpose statistical software package created in '\
                    '1985 by StataCorp. It is used by many businesses and '\
                    'academic institutions around the world.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.dta.txt' : {
                'short_name'     : 'DTA_Text',
                'long_name'      : 'DTA_Text (Text Fromat of DTA)',
                'same_extension' : [],
                'description'    : \
                    'Text format of DTA format.',
            },
            '.fasta' : {
                'short_name'     : 'FASTA',
                'long_name'      : 'FASTA (Sequence Alignment)',
                'same_extension' : ['.fa', '.mpfa', '.fna', '.fsa', '.fas'],
                'description'    : \
                    'FASTA file is a FASTA Sequence. In bioinformatics, FASTA '\
                    'format is a text-based format for representing either '\
                    'nucleotide sequences or peptide sequences, in which '\
                    'nucleotides or amino acids are represented using '\
                    'single-letter codes.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.gaml' : {
                'short_name'     : 'GAML',
                'long_name'      : 'GAML (GAML spectra)',
                'same_extension' : [],
                'description'    : \
                    'GAML spectra',
            },
            '.kojak.txt' : {
                'short_name'     : 'Kojak',
                'long_name'      : 'Kojak (Kojak result)',
                'same_extension' : [],
                'description'    : \
                    'Kojak result',
            },
            '.mgf' : {
                'short_name'     : 'MGF',
                'long_name'      : 'MGF (Materials and Geometry)',
                'same_extension' : [],
                'description'    : \
                    'MGF file is a Materials and Geometry Format Data. The '\
                    'Materials and Geometry Format (MGF) is a description '\
                    'language for 3-dimensional environments expressly suited '\
                    'to visible light simulation and rendering.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.ms2' : {
                'short_name'     : 'MS2',
                'long_name'      : 'MS2 (MS data)',
                'same_extension' : [],
                'description'    : \
                    'Mass spectrometry data format',
            },
            '.mzData' : {
                'short_name'     : 'mzData',
                'long_name'      : 'mzData (MS data)',
                'same_extension' : [],
                'description'    : \
                    'This format was deprecated, and was replaced by mzML',
            },
            '.mzid' : {
                'short_name'     : 'mzid',
                'long_name'      : 'mzid (MS data)',
                'same_extension' : [],
                'description'    : \
                    'Mass spectrometry data format',
            },
            '.mzid.gz' : {
                'short_name'     : 'mzid.gz',
                'long_name'      : 'mzid.gz (Compressed mzid)',
                'same_extension' : [],
                'description'    : \
                    'Compressed mzid',
            },
            '.mzML' : {
                'short_name'     : 'mzML',
                'long_name'      : 'mzML (MS data)',
                'same_extension' : [],
                'description'    : \
                    'Mass spectrometry data format',
            },
            '.mzML.gz' : {
                'short_name'     : 'mzML',
                'long_name'      : 'mzML (MS data)',
                'same_extension' : [],
                'description'    : \
                    'Compressed mzML',
            },
            '.mzXML' : {
                'short_name'     : 'mzXML',
                'long_name'      : 'mzXML (MS data)',
                'same_extension' : [],
                'description'    : \
                    'This format was replaced by mzML',
            },
            '.pep.xml' : {
                'short_name'     : 'pep.xml',
                'long_name'      : 'pep.xml (Kojak result)',
                'same_extension' : [],
                'description'    : \
                    'Kojak result',
            },
            '.perc.inter.txt' : {
                'short_name'     : 'perc.inter.txt',
                'long_name'      : 'perc.inter.txt (Kojak result)',
                'same_extension' : [],
                'description'    : \
                    'Kojak result',
            },
            '.perc.intra.txt' : {
                'short_name'     : 'perc.intra.txt',
                'long_name'      : 'perc.intra.txt (Kojak result)',
                'same_extension' : [],
                'description'    : \
                    'Kojak result',
            },
            '.perc.loop.txt' : {
                'short_name'     : 'perc.loop.txt',
                'long_name'      : 'perc.loop.txt (Kojak result)',
                'same_extension' : [],
                'description'    : \
                    'Kojak result',
            },
            '.perc.single.txt' : {
                'short_name'     : 'perc.single.txt',
                'long_name'      : 'perc.single.txt (Kojak result)',
                'same_extension' : [],
                'description'    : \
                    'Kojak result',
            },
            '.pkl' : {
                'short_name'     : 'PKL',
                'long_name'      : 'PKL (pickle)',
                'same_extension' : [],
                'description'    : \
                    'PKL file is a file created by pickle module',
            },
            '.raw' : {
                'short_name'     : 'RAW',
                'long_name'      : 'RAW',
                'same_extension' : [],
                'description'    : \
                    'ThermoFisher RAW format',
            },
            '.svg' : {
                'short_name'     : 'SVG',
                'long_name'      : 'SVG (Scalable Vector Graphic)',
                'same_extension' : [],
                'description'    : \
                    'SVG file is a Scalable Vector Graphic. SVG is a language '\
                    'for describing two-dimensional graphics and graphical '\
                    'applications in XML.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.tsv' : {
                'short_name'     : 'TSV',
                'long_name'      : 'TSV (Tab-Separated Values document)',
                'same_extension' : [],
                'description'    : \
                    'TSV is a Tab-Separated Values document. It is very '\
                    'simple textual data format which allows tabular data to '\
                    'be exhanged between applications that use different '\
                    'internal data formats.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.txt' : {
                'short_name'     : 'Text',
                'long_name'      : 'Text (General text format)',
                'same_extension' : ['.text'],
                'description'    : \
                    'TXT file is a plain text. Plain text is textual '\
                    'material, usually in a disk file, that is (largely) '\
                    'unformatted.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.xml' : {
                'short_name'     : 'XML',
                'long_name'      : 'XML (Extensible Markup Language document)',
                'same_extension' : [],
                'description'    : \
                    'XML file is an Extensible Markup Language document. XML '\
                    'is a simple, very flexible text format derived from SGML '\
                    '(ISO 8879). Originally designed to meet the challenges '\
                    'of large-scale electronic publishing, XML is also '\
                    'playing an increasingly important role in the exchange '\
                    'of a wide variety of data on the Web and elsewhere.\n'\
                    '(DataTypes.net; https://datatypes.net)',
            },
            '.xml.gz' : {
                'short_name'     : 'XML.gz',
                'long_name'      : 'XML.gz (Compressed mzid)',
                'same_extension' : [],
                'description'    : \
                    'Compressed xml',
            },
        },
        'description' : \
            'information of extentions',
    },
    '-xmx' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'msgfplus2csv_v2016_09_16',
            'msgfplus2csv_v2017_01_27',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
            'msfragger_20170103'
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'msgfplus_style_1'  : '-Xmx',
            'mzidentml_style_1' : '-Xmx',
            'msfragger_style_1' : '-Xmx',
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
            'none_val' : None,
            'dict_title' : {
                'Data Set' : {
                    'Format' : 'Unusual AA'
                }
            },
            'dict_type' : {
                'original_aa'          : 'str',
                'unimod_name'          : 'str',
                'unimod_name_with_cam' : 'str',
            },
            'multiple_line' : {
                'original_aa'          : False,
                'unimod_name'          : False,
                'unimod_name_with_cam' : False,
            },
            'custom_val_max' : 10000,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
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
    'add_cterm_peptide' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 0.0,
        'description' :  ''' Statically add mass in Da to C-terminal of peptide ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'add_Cterm_peptide',
        },
        'utag' : [
            'validation',
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'f-point'   : 1e-02,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "float",
    },
    'add_nterm_peptide' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 0.0,
        'description' :  ''' Statically add mass in Da to N-terminal of peptide ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'add_Nterm_peptide',
        },
        'utag' : [
        ],
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 10000,
            'min'       : 0,
            'f-point'   : 1e-02,
            'updownval' : 1,
            'unit'      : ''
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : 'float',
    },
    'allow_multiple_variable_mods_on_residue' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 1,
        'description' :  ''' static mods are not considered ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'allow_multiple_variable_mods_on_residue',
        },
        'utag' : [
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
    'base_mz' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'omssa_2_1_9',
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'    : 'base_mz',
            'omssa_style_1'   : 'base_mz',
            'pepnovo_style_1' : 'base_mz',
        },
        'utag' : [
            'fragment',
            'precursor',
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
        ],
        'triggers_rerun' : False,
        'ukey_translation' : {
            'myrimatch_style_1' : 'NumBatches',
            'xtandem_style_1'   : 'spectrum, sequence batch size',
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
            'sets the number of sequences loaded in as a batch from the '\
            'database file',
    },
    'bigger_scores_better' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'add_estimated_fdr_1_0_0',
            'percolator_2_08',
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
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance' : True,
                'msfragger_20170103' : True,
            },
            'percolator_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'msfragger_20170103'   : True,

            },
            'qvality_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'msfragger_20170103'   : True,
            },
            'sanitize_csv_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'msfragger_20170103'   : True,
            },
            'svm_style_1' : {
                'None'                 : None,
                'msamanda_1_0_0_5242'  : True,
                'msamanda_1_0_0_5243'  : True,
                'msamanda_1_0_0_6299'  : True,
                'msamanda_1_0_0_6300'  : True,
                'msamanda_1_0_0_7503'  : True,
                'msamanda_1_0_0_7504'  : True,
                'msgfplus_v2016_09_16' : False,
                'msgfplus_v2017_01_27' : False,
                'msgfplus_v9979'       : False,
                'myrimatch_2_1_138'    : True,
                'myrimatch_2_2_140'    : True,
                'omssa_2_1_9'          : False,
                'xtandem_cyclone_2010' : True,
                'xtandem_jackhammer'   : True,
                'xtandem_piledriver'   : True,
                'xtandem_sledgehammer' : True,
                'xtandem_vengeance'    : True,
                'msfragger_20170103'   : True,
            },
        },
        'uvalue_type'    : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
                'None',
                'msamanda_1_0_0_5242',
                'msamanda_1_0_0_5243',
                'msamanda_1_0_0_6299',
                'msamanda_1_0_0_6300',
                'msamanda_1_0_0_7503',
                'msamanda_1_0_0_7504',
                'msgfplus_v2016_09_16',
                'msgfplus_v2017_01_27',
                'msgfplus_v9979',
                'myrimatch_2_1_138',
                'myrimatch_2_2_140',
                'omssa_2_1_9',
                'xtandem_cyclone_2010',
                'xtandem_jackhammer',
                'xtandem_piledriver',
                'xtandem_sledgehammer',
                'xtandem_vengeance',
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, cleavage C-terminal mass change',
        },
        'utag' : [
            'protein',
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, cleavage N-terminal mass change',
        },
        'utag' : [
            'protein',
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
            'The mass added to the peptide N-terminus bz protein cleavage',
    },
    'clip_nterm_m' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 0,
        'description' :  ''' Specifies the trimming of a protein N-terminal methionine as a variable modification (0 or 1) ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'clip_nTerm_M',
        },
        'utag' : [
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
    'compensate_small_fasta' : {
        'edit_version'   : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
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
            'converter_version',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'compress_raw_search_results_if_possible',
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
    'cpus' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
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
            'msfragger_20170103',
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
            'Number of used cpus/threads\n'
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
            'cross-linking',
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
            'Format for cross_link is: \n'\
            '    **[amino acids] [amino acids] [mass mod] [identifier]**\n'\
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
            'none_val' : [
                '',
                '',
                ''
            ],
            'title_list' : [
                'column name/csv fieldname',
                'rule',
                'compared value',
            ],
            'type_dict' : {
                'column name/csv fieldname' : 'str',
                'rule'                      : 'str',
                'compared value'            : 'str',
            },
            'multiple_line' : {
                'column name/csv fieldname' : False,
                'rule'                      : False,
                'compared value'            : False,
            },
            'custom_val_max' : 0,
        },
        'default_value' : None,
        'description' : \
            'Rules are defined as list of tuples with the first tuple element '\
            'as the column name/csv fieldname, the second tuple element the '\
            'rule and the third tuple element the value which should be '\
            'compared',
    },
    'database' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
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
            'upeptide_mapper_1_0_0',
            'compomics_utilities_4_11_5',
            'msfragger_20170103',
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
            'msfragger_style_1'           : 'database_name'

        },
        'utag' : [
            'database',
            'input',
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'         : '',
            'multiple_line'    : False,
            'input_extensions' : ['.fasta', '.fa'],
        },
        'default_value' : None,
        'description' : \
            'Path to database file containing protein sequences in fasta format\n'\
            '    \'\' : None',
    },
    'database_taxonomy' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
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
        'edit_version' : 1.00,
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['reverse_protein', 'shuffle_peptide'],
            'custom_val_max' : 0,
        },
        'default_value' : 'shuffle_peptide',
        'description' : \
            'Decoy database: Creates a target decoy database based on '\
            'shuffling of peptides or complete reversing the protein sequence '\
            '(reverse_protein).',
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
            'upeptide_mapper_1_0_0'
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
            'title_list'   : [
                'del param',
            ],
            'type_dict' : {
                'del param' : 'str',
            },
            'multiple_line' : {
                'del param' : False,
            },
            'custom_val_max' : 10000,
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-model',
        },
        'utag' : [
            'model',
        ],
        'uvalue_translation' : {
            'pepnovo_style_1' : {
                'cid_trypsin' : 'CID_IT_TRYP',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['cid_trypsin'],
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-model_dir',
        },
        'utag' : [
            'model',
            'input_dir',
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
            'Directory containing the model files for PepNovo. If \'None\', '\
            'it is supposed to be in :\n'\
            '    resources/<platform>/<architecture>/pepnovo_3_1\n'\
            '\n'\
            '    \'\' : None',
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
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'generate_decoy',
            'msgfplus_style_1' : '-tda',
            'xtandem_style_1'  : 'scoring, include reverse',
        },
        'utag' : [
            'database',
            'input',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'generate_target_decoy_1_0_0',
            'kojak_1_5_3',
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'percolator_2_08',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103',
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
            'msfragger_style_1'             : 'enzyme'
        },
        'utag' : [
            'database',
            'protein',
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
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
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
            'statistics',
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
    'filter_csv_converter_version' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'filter_csv_converter_version',
        },
        'utag' : [
            'converter_version',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'filter_csv_1_0_0',
        'description' : \
            'filter csv converter version: version name',
    },
    'forbidden_cterm_mods' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_vengeance',
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
            'title_list' : [
            ],
            'type_dict' : {
            },
            'custom_val_max' : 10000,
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'novor_style_1' : 'forbiddenResidues',
        },
        'utag' : [
            'de_novo',
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
    'frag_mass_tolerance' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103'
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
            'msfragger_style_1' : 'fragment_mass_tolerance'
        },
        'utag' : [
            'fragment',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103'
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
            'msfragger_style_1' : 'fragment_mass_units'
        },
        'utag' : [
            'fragment',
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
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['da', 'mmu', 'ppm'],
            'custom_val_max' : 0,
        },
        'default_value' : 'ppm',
        'description' : \
            'Fragment mass tolerance unit: available in ppm '\
            '(parts-per-millon), da (Dalton) or mmu (Milli mass unit)',
    },
    'frag_mass_type' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['average', 'monoisotopic'],
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'novor_1_1beta',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1' : '-m',
            'novor_style_1'    : 'fragmentation',
        },
        'utag' : [
            'instrument',
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['cid', 'ecd', 'etd', 'hcd'],
            'custom_val_max' : 0,
        },
        'default_value' : 'hcd',
        'description' : \
            'Used fragmentation method, e.g. collision-induced dissociation '\
            '(CID), electron-capture dissociation (ECD), electron-transfer '\
            'dissociation (ETD), Higher-energy C-trap dissociation (HCD)',
    },
    'frag_min_mz' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
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
            'get_http_style_1' : 'ftp_blocksize',
        },
        'utag' : [
            'download',
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
            'get_http_style_1' : 'ftp_folder',
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
            'ftp folder that should be downloaded\n'\
            '    \'\' : None',
    },
    'ftp_include_ext' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'get_ftp_files_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'get_http_style_1' : 'ftp_include_ext',
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
            'Only files with the defined file extension are downloaded with '\
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
            'get_http_style_1' : 'ftp_max_number_of_files',
        },
        'utag' : [
            'download',
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
            'get_http_style_1' : 'ftp_output_folder',
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
            'get_http_style_1' : 'ftp_password',
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
            'get_http_style_1' : 'ftp_url',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_percolator_2_08',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus2csv_v2016_09_16',
            'msgfplus2csv_v2017_01_27',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_percolator_style_1' : 'header_translations',
            'msamanda_style_1'         : 'header_translations',
            'msgfplus_style_1'         : 'header_translations',
            'novor_style_1'            : 'header_translations',
            'omssa_style_1'            : 'header_translations',
            'pepnovo_style_1'          : 'header_translations',
            'msfragger_style_1'        : 'header_translations'
        },
        'utag' : [
            'Conversion',
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
                'Hit rank':'MSFragger:Hit rank',
                'Mass difference':'MSFragger:Mass difference',
                'Matched fragment ions':'MSFragger:Matched fragment ions',
                'Total possible number of matched theoretical fragment ions':'MSFragger:Total possible number of matched theoretical fragment ions',
                'Hyperscore':'MSFragger:Hyperscore',
                'Next score':'MSFragger:Next score',
                'Number of tryptic termini':'MSFragger:Number of tryptic termini',
                'Number of missed cleavages':'MSFragger:Number of missed cleavages',
                'Intercept of expectation model (expectation in log space)':'MSFragger:Intercept of expectation model (expectation in log space)',
                'Slope of expectation model (expectation in log space)':'MSFragger:Slope of expectation model (expectation in log space)',
            }
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
            '',
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
            '',
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
            '',
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
    'heatmap_column_order' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'plot_pygcluster_heatmap_from_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'heatmap_style_1' : 'heatmap_column_order',
        },
        'utag' : [
            '',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'title_list' : [
            ],
            'type_dict' : {
            },
            'custom_val_max' : 10000,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
        ],
        'description' : \
            'The plot order of the columns',
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
            '',
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
            '',
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
            '',
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
            '',
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
            '',
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
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'novor_1_1beta',
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
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
    'intensity_cutoff' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
            'msfragger_20170103'
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
            'statistics',
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['rbf', 'linear', 'poly', 'sigmoid'],
            'custom_val_max' : 1,
        },
        'default_value' : 'rbf',
        'description' : \
            'The kernel function of the support vector machine used for PSM '\
            'post-processing (\'rbf\', \'linear\', \'poly\' or \'sigmoid\')',
    },
    'kojak_MS1_centroid' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS1_centroid',
        },
        'utag' : [
            'cross-linking',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                'Yes' : 1,
                'No'  : 0,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['Yes', 'No'],
            'custom_val_max' : 0,
        },
        'default_value' : 'No',
        'description' : \
            'MS1 centroided data yes (1) or no (0)',
    },
    'kojak_MS1_resolution' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS1_resolution',
        },
        'utag' : [
            'cross-linking',
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
    'kojak_MS2_centroid' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS2_centroid',
        },
        'utag' : [
            'cross-linking',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                'Yes' : 1,
                'No'  : 0,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['Yes', 'No'],
            'custom_val_max' : 0,
        },
        'default_value' : 'Yes',
        'description' : \
            'MS2 centroided data yes (1) or no (0)',
    },
    'kojak_MS2_resolution' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS2_resolution',
        },
        'utag' : [
            'cross-linking',
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
            'cross-linking',
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
            'cross-linking',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_export_pepXML',
        },
        'utag' : [
            'cross-linking',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                'Activate'   : 1,
                'Deactivate' : 0,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['Activate', 'Deactivate'],
            'custom_val_max' : 0,
        },
        'default_value' : 'Deactivate',
        'description' : \
            'Activate (1) or deactivate (0) output as pepXML',
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
            'cross-linking',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                'Activate'   : 1,
                'Deactivate' : 0,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['Activate', 'Deactivate'],
            'custom_val_max' : 0,
        },
        'default_value' : 'Activate',
        'description' : \
            'Activate (1) or deactivate (0) output for percolator',
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
            'cross-linking',
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
            'cross-linking',
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
            'cross-linking',
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
            'cross-linking',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_prefer_precursor_pred',
        },
        'utag' : [
            'cross-linking',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                '0: ignore previous' : 0,
                '1: only previous'   : 1,
                '2: supplement'      : 2,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
                '0: ignore previous',
                '1: only previous',
                '2: supplement',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'supplement',
        'description' : \
            'prefer precursor mono mass predicted by instrument software.\n'\
            '    0 = ignore previous predictions\n'\
            '    1 = use only previous predictions\n'\
            '    2 = supplement predictions with additional analysis',
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
            'cross-linking',
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
            'cross-linking',
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
            'cross-linking',
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
            'cross-linking',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103',
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
        },
        'utag' : [
            'label',
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['14N', '15N'],
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'machine_offset_in_ppm',
        },
        'utag' : [
            'converter',
            'instrument',
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
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'max_accounted_observed_peaks',
            'myrimatch_style_1' : 'MaxPeakCount',
            'xtandem_style_1'   : 'spectrum, total peaks',
            'msfragger_style_1' : 'use_topN_peaks'
        },
        'utag' : [
            'MS2',
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
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
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
            'msfragger_20170103',

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
            'msfragger_style_1'       : 'allowed_missed_cleavage'
        },
        'utag' : [
            'protein',
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'MaxModSize',
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
            'Minimum modification size to consider (in Da)',
    },
    'max_num_mods' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'max_num_mods',
            'msgfplus_style_1'  : 'NumMods',
            'myrimatch_style_1' : 'MaxDynamicMods',
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
            'msfragger_20170103'
        ],
        'default_value' : 2,
        'description' :  ''' Maximum number of residues that can be occupied by each variable modification (maximum of 5) ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'max_variable_mods_per_mod'
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
        'available_in_unode' : [
            'xtandem_vengeance',
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
            'none_val' : None,
            'dict_title' : {
                'unimod_name' : 'number'
            },
            'dict_type' : {
            },
            'custom_val_max' : 10000,
            'custom_type' : {
                'int' : {
                    'max'       : 10000,
                    'min'       : 0,
                    'updownval' : 1,
                    'unit'      : '',
                },
            },
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
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1'  : '-maxLength',
            'myrimatch_style_1' : 'MaxPeptideLength',
            'omssa_style_1'     : '-nox',
            'msfragger_style_1' : 'digest_max_length'
        },
        'utag' : [
            'peptide',
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
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
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
        },
        'utag' : [
            'input',
            'input_files',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'         : '',
            'multiple_line'    : False,
            'input_extensions' : ['.mgf'],
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'MinModSize',
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
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'msfragger_20170103',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1'  : '-minLength',
            'myrimatch_style_1' : 'MinPeptideLength',
            'omssa_style_1'     : '-no',
            'msfragger_style_1' : 'digest_min_length'
        },
        'utag' : [
            'peptide',
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
            'msfragger_20170103'
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
            'msfragger_20170103'
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
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
                'No Modification'   : 0,
                'One Modification'  : 1,
                'No Limit'          : 2,
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
                'No Modification',
                'One Modification',
                'No Limit',
            ],
            'custom_val_max' : 0,
        },
        'default_value' : 'No Limit',
        'description' : \
            'Allowed number of modifications per peptide. \n'\
            '    \'0\' = no modification, \n'\
            '    \'1\' = one modification, \n'\
            '    \'2\' = no limit',
    },
    'moda_high_res' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'HighResolution',
        },
        'utag' : [
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1' : 'Protocol',
        },
        'utag' : [
        ],
        'uvalue_translation' : {
            'moda_style_1' : {
                'None' : 'NONE',
            },
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
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
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'unify_csv_1_0_0',
            'upeptide_mapper_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103'
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
            'xtandem_style_1'         : (
                'residue, modification mass',
                'residue, potential modification mass',
                'protein, N-terminal residue modification mass',
                'protein, C-terminal residue modification mass',
                'protein, C-terminal residue modification mass',
                'protein, quick acetyl',
                'protein, quick pyrolidone'
            ),
        },
        'utag' : [
            'modifications',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'title_list' : [
                'mod_1',
                'mod_2',
            ],
            'type_dict' : {
                'mod_1' : 'str',
                'mod_2' : 'str',
            },
            'multiple_line' : {
                'mod_1' : False,
                'mod_2' : False,
            },
            'custom_val_max' : 10000,
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
            'informations seperated by comma: \n'\
            '    \'amino acid, type, position, unimod name or id\'\n'\
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
            'Examples:\n'\
            '    [ \'M,opt,any,Oxidation\' ] - potential oxidation of Met at '\
            'any position within a peptide\n'\
            '    [ \'*,opt,Prot-N-term,Acetyl\' ] - potential acetylation of '\
            'any amino acid at the N-terminus of a protein\n'\
            '    [ \'S,opt,any,Phospho\' ] - potential phosphorylation of '\
            'Serine at any position within a peptide\n'\
            '    [ \'C,fix,any,Carbamidomethyl\', \'N,opt,any,Deamidated\', '\
            '\'Q,opt,any,Deamidated\' ] - fixed carbamidomethylation of Cys '\
            'and potential deamidation of Asn and/or Gln at any position '\
            'within a peptide\n'\
            'Additionally, userdefined modifications can be given and are '\
            'written to a userdefined_unimod.xml in ursgal/kb/ext. '\
            'Userdefined modifications need to have a unique name instead of '\
            'the unimod name the chemical composition needs to be given as a '\
            'Hill notation on the fifth position in the string\n'\
            '\n'\
            'Example:\n'\
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
            'cross-linking',
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
    'ms1_centroided' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS1_centroid',
        },
        'utag' : [
            'cross-linking',
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
            'MS1 data are centroided: True or False',
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
            'cross-linking',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 30000,
        'description' : \
            'MS1 resolution',
    },
    'ms2_centroided' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1' : 'kojak_MS2_centroid',
        },
        'utag' : [
            'cross-linking',
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
        'default_value' : True,
        'description' : \
            'MS2 data are centroided: True or False',
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
            'cross-linking',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : None,
            'max'       : 100000000,
            'min'       : 0,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : 25000,
        'description' : \
            'MS2 resolution',
    },
    'msgfplus_protocol_id' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msgfplus_style_1' : '-protocol',
        },
        'utag' : [
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['0', '1', '2', '3'],
            'custom_val_max' : 0,
        },
        'default_value' : '0',
        'description' : \
            'MS-GF+ specific protocol identifier. Protocols are used to '\
            'enable scoring parameters for enriched and/or labeled samples.',
    },
    'msfragger_output_max_expect' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 50,
        'description' :  ''' Suppresses reporting of PSM if top hit has expectation greater than this threshold ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'output_max_expect',
        },
        'utag' : [
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
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 0,
        'description' :  ''' Track top N unmodified peptide results separately from main results internally for boosting features. Should be set to a number greater than output_report_topN if zero bin boosting is desired. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'track_zero_topN',
        },
        'utag' : [
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
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 0,
        'description' :  ''' Ranks a zero-bin hit above all non-zero-bin hit if it has expectation less than this value. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'zero_bin_accept_expect',
        },
        'utag' : [
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
    'msfragger_zero_bin_mult_expect' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 1,
        'description' :  ''' Multiplies expect value of PSMs in the zero-bin during results ordering (set to less than 1 for boosting) ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'zero_bin_mult_expect',
        },
        'utag' : [
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
    'msfragger_add_topN_complementary' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 0,
        'description' :  ''' Inserts complementary ions corresponding to the top N most intense fragments in each experimental spectra. Useful for recovery of modified peptides near C-terminal in open search. Should be set to 0 (disabled) otherwise. ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'add_topN_complementary',
        },
        'utag' : [
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
    'msfragger_min_fragments_modelling' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 3,
        'description' :  ''' Minimum number of matched peaks in PSM for inclusion in statistical modeling ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'min_fragments_modelling',
        },
        'utag' : [
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
    'msfragger_clear_mz_range' : {
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : '0.0 0.0',
        'description' :  ''' Removes peaks in this m/z range prior to matching. Useful for iTRAQ/TMT experiments (i.e. 0.0 150.0) ''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'clear_mz_range',
        },
        'utag' : [
        ],
        'uvalue_option' : {
            'none_val' : None,
            'multiple_line' : False
        },
        'uvalue_translation' : {
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
            'converter_version',
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
        'edit_version' : 1.00,
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
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
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : [
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
            '\'Mzid2Csv\' is suppoted so far',
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
            'converter_version',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'mzml2mgf_1_0_0',
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'number_of_i_decimals',
        },
        'utag' : [
            'converter',
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
        'default_value' : 5,
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
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'msfragger_20170103'
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
            'Maximum number of peptide spectrum matches to report for each '\
            'spectrum',
    },
    'num_mz_decimals' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'number_of_mz_decimals',
        },
        'utag' : [
            'converter',
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
        'default_value' : 5,
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
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'mzidentml_lib_1_6_10',
            'mzidentml_lib_1_6_11',
            'mzidentml_lib_1_7',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'percolator_2_08',
            'qvality_2_02',
            'venndiagram_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'generate_target_decoy_style_1' : 'output_file',
            'merge_csvs_style_1'             : 'output',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1'   : ('-oc', '-ox'),
            'xtandem_style_1' : 'output, mzid',
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
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['.csv', '.mzid', '.omx', 'default'],
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
            'converter_version',
        ],
        'uvalue_option' : {
            'none_val'     : None,
            'multiple_line' : False,
        },
        'uvalue_translation' : {
        },
        'uvalue_type' : "str",
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['linear', 'none'],
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
            'msfragger_20170103'
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['0', '0,1', '0,2'],
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
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103',
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
            'unify_csv_style_1' : 'precursor_mass_tolerance_minus',
            'xtandem_style_1' : 'spectrum, parent monoisotopic mass error minus',
            'msfragger_style_1' : 'precursor_mass_tolerance'
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
            'Precursor mass tolerance: lower mass tolerance of measured and '\
            'calculated parent ion M+H',
    },
    'precursor_mass_tolerance_plus' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'unify_csv_1_0_0',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103'
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
            'msfragger_style_1' : 'precursor_mass_tolerance'

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
            'Precursor mass tolerance: higher mass tolerance of measured and '\
            'calculated parent ion M+H',
    },
    'precursor_mass_tolerance_unit' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'moda_v1_51',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'novor_1_1beta',
            'omssa_2_1_9',
            'pepnovo_3_1',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
            'msfragger_20170103'
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
        },
        'utag' : [
            'precursor',
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
            }
        },
        'uvalue_type' : 'select',
        'uvalue_option' : {
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['da', 'mmu', 'ppm'],
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['average', 'monoisotopic'],
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
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1'  : 'considered_charges',
            'msgfplus_style_1'  : '-maxCharge',
            'myrimatch_style_1' : 'NumChargeStates',
            'omssa_style_1'     : '-zh',
            'msfragger_style_1' : 'precursor_max_charge'
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'precursor_max_mass',
            'myrimatch_style_1' : 'MaxPeptideMass',
            'xtandem_style_1'   : 'spectrum, minimum parent m+h',
            'msfragger_style_1' : 'precursor_max_mass'
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
            'Maximal parent ion mass. Adjusted to default used by MSFragger',
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
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
            'msgfplus_v9979',
            'omssa_2_1_9',
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'considered_charges',
            'msgfplus_style_1' : '-minCharge',
            'omssa_style_1' : '-zl',
            'msfragger_style_1' : 'precursor_min_charge'

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
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'precursor_min_mass',
            'myrimatch_style_1' : 'MinPeptideMass',
            'xtandem_style_1'   : 'spectrum, minimum parent m+h',
            'msfragger_style_1' : 'precursor_min_mass'
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
        'available_in_unode' : [
            'msfragger_20170103',
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
        'available_in_unode' : [
            'msfragger_20170103',
        ],
        'default_value' : 'ppm',
        'description' :  '''Mass tolerance units fo precursor_true_tolerance''',
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msfragger_style_1' : 'precursor_true_units',
        },
        'utag' : [
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
    'psm_merge_delimiter' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'unify_csv_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'unify_csv_style_1' : 'psm_merge_delimiter',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'qvality_2_02',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'qvality_style_1' : '-v',
        },
        'utag' : [
            'validation',
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['1', '2', '3', '4', '5'],
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
            'validation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'If True, redundant PSMs (e.g. the same identification reported '\
            'by multiple engined) for the same spectrum are removed. An '\
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'rt_pickle_name',
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
        'default_value' : '_ursgal_lookup.pkl',
        'description' : \
            'name of the pickle that is used to map the retention time',
    },
    'sanitize_csv_converter_version' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'ucontroller',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'ucontroller_style_1' : 'sanitize_csv_converter_version',
        },
        'utag' : [
            'converter_version',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'sanitize_csv_1_0_0',
        'description' : \
            'sanitize csv converter version: version name',
    },
    'scan_exclusion_list' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'scan_exclusion_list',
        },
        'utag' : [
            'converter',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'title_list' : [
            ],
            'type_dict' : {
            },
            'custom_val_max' : 10000,
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'scan_inclusion_list',
        },
        'utag' : [
            'converter',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : [
            ],
            'title_list' : [
            ],
            'type_dict' : {
            },
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'mzml2mgf_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'mzml2mgf_style_1' : 'scan_skip_modulo_step',
        },
        'utag' : [
            'converter',
        ],
        'uvalue_translation' : {
            'mzml2mgf_style_1' : {
            },
        },
        'uvalue_type' : 'int',
        'uvalue_option' : {
            'none_val'  : -1,
            'max'       : 10000000,
            'min'       : -1,
            'updownval' : 1,
            'unit'      : ''
        },
        'default_value' : None,
        'description' : \
            'Include only the n-th spectrum during mzml2mgf conversion\n'\
            '    -1 : None',
    },
    'score_-h2o_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'series',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Spectrum: if true, ions loss of H2O are respected in algorithm',
    },
    'score_-nh3_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'series',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Spectrum: if true, ions loss of NH3 are respected in algorithm',
    },
    'score_a_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'ion_series_A',
            'msamanda_style_1'  : 'series',
            'myrimatch_style_1' : 'FragmentationRule',
            'omssa_style_1'     : '-i',
            'xtandem_style_1'   : 'scoring, a ions',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : '0',
                True  : '1',
            },
            'omssa_style_1' : {
                False : '',
                True  : '0',
            },
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
            'Spectrum: if true, a ions are used in algorithm',
    },
    'score_b1_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-sb1',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                False : '1',
                True  : '0',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'first forward (b1) product ions inclued in search',
    },
    'score_b_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'ion_series_B',
            'msamanda_style_1'  : 'series',
            'myrimatch_style_1' : 'FragmentationRule',
            'omssa_style_1'     : '-i',
            'xtandem_style_1'   : 'scoring, b ions',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : '0',
                True  : '1',
            },
            'omssa_style_1' : {
                False : '',
                True  : '1',
            },
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Spectrum: if true, b ions are used in algorithm',
    },
    'score_c_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'ion_series_C',
            'msamanda_style_1'  : 'series',
            'myrimatch_style_1' : 'FragmentationRule',
            'omssa_style_1'     : '-i',
            'xtandem_style_1'   : 'scoring, c ions',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : '0',
                True  : '1',
            },
            'omssa_style_1' : {
                False : '',
                True  : '2',
            },
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
            'Spectrum: if true, c ions are used in algorithm',
    },
    'score_c_terminal_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'omssa_2_1_9',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'omssa_style_1' : '-sct',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'omssa_style_1' : {
                False : '1',
                True  : '0',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Score c terminal ions',
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
    'score_imm_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'series',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Spectrum: if true, immonium ions are respected in algorithm',
    },
    'score_int_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'series',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Spectrum: if true, internal fragment ions are respect in algorithm',
    },
    'score_x_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'ion_series_X',
            'msamanda_style_1'  : 'series',
            'myrimatch_style_1' : 'FragmentationRule',
            'omssa_style_1'     : '-i',
            'xtandem_style_1'   : 'scoring, x ions',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : '0',
                True  : '1',
            },
            'omssa_style_1' : {
                False : '',
                True  : '3',
            },
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
            'Spectrum: if true, x ions are used in algorithm',
    },
    'score_y_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'ion_series_Y',
            'msamanda_style_1'  : 'series',
            'myrimatch_style_1' : 'FragmentationRule',
            'omssa_style_1'     : '-i',
            'xtandem_style_1'   : 'scoring, y ions',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : '0',
                True  : '1',
            },
            'omssa_style_1' : {
                False : '',
                True  : '4',
            },
            'xtandem_style_1' : {
                False : 'no',
                True  : 'yes',
            },
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
        'description' : \
            'Spectrum: if true, y ions are used in algorithm',
    },
    'score_z+1_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'series',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Spectrum: if true, z ion plus 1 Da mass are used in algorithm',
    },
    'score_z+2_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'msamanda_style_1' : 'series',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : False,
        'description' : \
            'Spectrum: if true z ion plus 2 Da mass are used in algorithm',
    },
    'score_z_ions' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'kojak_1_5_3',
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'myrimatch_2_1_138',
            'myrimatch_2_2_140',
            'omssa_2_1_9',
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'kojak_style_1'     : 'ion_series_Z',
            'msamanda_style_1'  : 'series',
            'myrimatch_style_1' : 'FragmentationRule',
            'omssa_style_1'     : '-i',
            'xtandem_style_1'   : 'scoring, z ions',
        },
        'utag' : [
            'scoring',
        ],
        'uvalue_translation' : {
            'kojak_style_1' : {
                False : '0',
                True  : '1',
            },
            'omssa_style_1' : {
                False : '',
                True  : '5',
            },
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
            'Spectrum: if true, z ions are used in algorithm',
    },
    'search_for_saps' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'protein, saps',
        },
        'utag' : [
            'protein',
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
            'msamanda_1_0_0_5242',
            'msamanda_1_0_0_5243',
            'msamanda_1_0_0_6299',
            'msamanda_1_0_0_6300',
            'msamanda_1_0_0_7503',
            'msamanda_1_0_0_7504',
            'msgfplus_v2016_09_16',
            'msgfplus_v2017_01_27',
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
            'msfragger_20170103'
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
            'statistics',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            '_test_node',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            '_test_node_style_1' : 'test_param1',
        },
        'utag' : [
            'debugging',
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['a', 'b', 'c', 'd', 'e'],
            'custom_val_max' : 0,
        },
        'default_value' : 'b',
        'description' : \
            'TEST/DEBUG: Internal Ursgal parameter 1 for debugging and testing.',
    },
    'test_param2' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            '_test_node',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            '_test_node_style_1' : 'test_param2',
        },
        'utag' : [
            'debugging',
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
            'combo_box'      : True,
            'radio_button'   : False,
            'initial_value'  : ['one', 'two', 'three', 'four', 'five'],
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
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'bool',
        'uvalue_option' : {
        },
        'default_value' : True,
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
            'converter_version',
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
            'installation',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'str',
        'uvalue_option' : {
            'none_val'      : None,
            'multiple_line' : False,
        },
        'default_value' : 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/',
        'description' : \
            'URL that is used to install and prepare_resources.py',
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
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'xtandem_style_1' : 'refine',
        },
        'utag' : [
            'refinement',
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
            'msfragger_20170103'
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'pepnovo_style_1' : '-use_spectrum_charge',
            'msfragger_style_1': 'override_charge'
        },
        'utag' : [
            'precursor',
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
            'pepnovo_3_1',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'moda_style_1'    : 'AutoPMCorrection',
            'pepnovo_style_1' : '-use_spectrum_mz',
        },
        'utag' : [
            'precursor',
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
            'file_extension',
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
                'msgfplus_v2016_09_16' : 1e-100,
                'msgfplus_v2017_01_27' : 1e-100,
                'msgfplus_v9979'       : 1e-100,
                'myrimatch_2_1_138'    : 0,
                'myrimatch_2_2_140'    : 0,
                'omssa_2_1_9'          : 1e-30,
                'xtandem_cyclone_2010' : 0,
                'xtandem_jackhammer'   : 0,
                'xtandem_piledriver'   : 0,
                'xtandem_sledgehammer' : 0,
                'xtandem_vengeance'    : 0,
                'msfragger_20170103'   : 0,
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'add_estimated_fdr_1_0_0',
            'percolator_2_08',
            'qvality_2_02',
            'sanitize_csv_1_0_0',
            'svm_1_0_0',
            'ucontroller',
            'unify_csv_1_0_0',
            'msfragger_20170103'
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
            'msfragger_style_1'         : 'validation_score_field'

        },
        'utag' : [
            'validation',
        ],
        'uvalue_translation' : {
            'add_estimated_fdr_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore'
            },
            'percolator_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
            },
            'qvality_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore'
            },
            'sanitize_csv_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore'
            },
            'svm_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore'
            },
            'ucontroller_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
            },
            'unify_csv_style_1' : {
                'msamanda_1_0_0_5242'  : 'Amanda:Score',
                'msamanda_1_0_0_5243'  : 'Amanda:Score',
                'msamanda_1_0_0_6299'  : 'Amanda:Score',
                'msamanda_1_0_0_6300'  : 'Amanda:Score',
                'msamanda_1_0_0_7503'  : 'Amanda:Score',
                'msamanda_1_0_0_7504'  : 'Amanda:Score',
                'msgfplus_v2016_09_16' : 'MS-GF:SpecEValue',
                'msgfplus_v2017_01_27' : 'MS-GF:SpecEValue',
                'msgfplus_v9979'       : 'MS-GF:SpecEValue',
                'myrimatch_2_1_138'    : 'MyriMatch:MVH',
                'myrimatch_2_2_140'    : 'MyriMatch:MVH',
                'novor_1_1beta'        : 'Novor:score',
                'omssa_2_1_9'          : 'OMSSA:pvalue',
                'pepnovo_3_1'          : 'Pepnovo:PnvScr',
                'xtandem_cyclone_2010' : 'X\!Tandem:hyperscore',
                'xtandem_jackhammer'   : 'X\!Tandem:hyperscore',
                'xtandem_piledriver'   : 'X\!Tandem:hyperscore',
                'xtandem_sledgehammer' : 'X\!Tandem:hyperscore',
                'xtandem_vengeance'    : 'X\!Tandem:hyperscore',
                'msfragger_20170103'   : 'MSFragger:Hyperscore',
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
            'title_list' : [
                'column_name_1',
                'column_name_2',
            ],
            'type_dict' : {
                'column_name_1' : 'str',
                'column_name_2' : 'str',
            },
            'multiple_line' : {
                'column_name_1' : False,
                'column_name_2' : False,
            },
            'custom_val_max' : 10000,
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
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
        'uvalue_type' : 'tuple',
        'uvalue_option' : {
            'none_val' : None,
            'title_list' : [
                'font-type',
                'font-size header',
                'font-size major',
                'font-size minor',
                'font-size venn',
            ],
            'type_dict' : {
                'font-type'        : 'str',
                'font-size header' : 'int',
                'font-size major'  : 'int',
                'font-size minor'  : 'int',
                'font-size venn'   : 'int',
            },
            'multiple_line' : {
                'font-type'        : False,
            },
            'max': {
                'font-size header' : 1000,
                'font-size major'  : 1000,
                'font-size minor'  : 1000,
                'font-size venn'   : 1000,
            },
            'min': {
                'font-size header' : 0,
                'font-size major'  : 0,
                'font-size minor'  : 0,
                'font-size venn'   : 0,
            },
            'updownval': {
                'font-size header' : 1,
                'font-size major'  : 1,
                'font-size minor'  : 1,
                'font-size venn'   : 1,
            },
            'unit': {
                'font-size header' : 'pt',
                'font-size major'  : 'pt',
                'font-size minor'  : 'pt',
                'font-size venn'   : 'pt',
            },
            'custom_val_max' : 0,
        },
        'default_value' : (
            'Helvetica',
            31,
            25,
            20,
            20
        ),
        'description' : \
            'Font used for visualization plots (e.g. Venn diagram), given as '\
            'tuple (font-type, font-size header, font-size major, font-size '\
            'minor, font-size venn)',
    },
    'visualization_header' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'header',
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
        'default_value' : 'ursgal Venn Diagram',
        'description' : \
            'Header of visualization output (e.g. Venn diagram)',
    },
    'visualization_label_list' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
        ],
        'triggers_rerun' : True,
        'ukey_translation' : {
            'venndiagram_style_1' : 'visualization_label_list',
        },
        'utag' : [
            'visualization',
        ],
        'uvalue_translation' : {
        },
        'uvalue_type' : 'list',
        'uvalue_option' : {
            'none_val' : None,
            'initialValue' : [
            ],
            'title_list' : [
            ],
            'type_dict' : {
            },
            'custom_val_max' : 10000,
            'custom_type' : {
                'str' : {
                    'multiple_line' : False,
                },
            },
        },
        'default_value' : [
        ],
        'description' : \
            'Specifies labels for the datasets that should be visualized. '\
            'Needs to be given in the same order as the datasets.',
    },
    'visualization_opacity' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
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
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
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
        'uvalue_type' : 'tuple',
        'uvalue_option' : {
            'none_val'       : None,
            'title_list' : [
                'x-axis-scaling-factor',
                'y-axis-scaling-factor',
            ],
            'type_dict' : {
                'x-axis-scaling-factor' : 'int',
                'y-axis-scaling-factor' : 'int',
            },
            'max': {
                'x-axis-scaling-factor' : 100000,
                'y-axis-scaling-factor' : 100000,
            },
            'min': {
                'x-axis-scaling-factor' : 1,
                'y-axis-scaling-factor' : 1,
            },
            'updownval': {
                'x-axis-scaling-factor' : 1,
                'y-axis-scaling-factor' : 1,
            },
            'unit': {
                'x-axis-scaling-factor' : '',
                'y-axis-scaling-factor' : '',
            },
            'custom_val_max' : 0,
        },
        'default_value' : (600, 400),
        'description' : \
            'Scaling factor for visualization plots (e.g. Venn diagram), '\
            'given as tuple (x-axis-scaling-factor, y-axis-scaling-factor)',
    },
    'visualization_size' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
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
        'uvalue_type' : 'tuple',
        'uvalue_option' : {
            'none_val'       : None,
            'title_list' : [
                'width',
                'height',
            ],
            'type_dict' : {
                'width'  : 'int',
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
        'default_value' : (1200, 900),
        'description' : \
            'Size of visualization plots (e.g. Venn diagram), given as tuple '\
            '(width, height)',
    },
    'visualization_stroke_width' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'venndiagram_1_0_0',
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
            'combining_search_results',
            'statistics',
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
    'xtandem_stp_bias' : {
        'edit_version' : 1.00,
        'available_in_unode' : [
            'xtandem_cyclone_2010',
            'xtandem_jackhammer',
            'xtandem_piledriver',
            'xtandem_sledgehammer',
            'xtandem_vengeance',
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
}
