# META_INFO={
#     'engine_type': {
#         'search_engine': True,
#     },
#     'output_extension'          : '.csv',
#     'input_types'               : ['.mgf'],
#     'create_own_folder'         : True,
#     'citation'                  : 'Dorfer V, Pichler P, Stranzl T, '\
#         'Stadlmann J, Taus T, Winkler S, Mechtler K. (2014) MS Amanda, '\
#         'a universal identification algorithm optimized for high accuracy '\
#         'tandem mass spectra.',
#     'include_in_git'            : None,
#     'cannot_distribute'         : True,
#     'in_development'            : True,
#     'engine': {
#         'linux' : {
#             '64bit' : {
#                 'exe'            : 'MSAmanda.exe',
#                 'url'            : '',
#                 'zip_md5'        : None,
#                 'additional_exe' : [],
#             },
#         },
#         'darwin' : {
#             '64bit' : {
#                 'exe'            : 'MSAmanda.exe',
#                 'url'            : '',
#                 'zip_md5'        : None,
#                 'additional_exe' : [],
#             },
#         },
#     },

# }

# DEFAULT_PARAMS={
#     'validation_score_field'    : 'Amanda:Score',
#     'evalue_field'              : 'Amanda:Weighted Probability',
#     'validation_minimum_score'  : 0,
#     'bigger_scores_better'      : True,
#     'input_type'                : 'mgf',
# }

# USEARCH_PARAM_VALUE_TRANSLATIONS = {
#     'nonspecific'            : 'No-Enzyme',
#     'trypsin'                : 'Trypsin',
#     'lysc'                   : 'LysC',
#     'gluc'                   : 'GluC',
#     'no_cleavage'            : 'No-Cleavage',
#     'da'                     : 'Da',

#     'Scan Number'        : 'Spectrum ID',
#     'Title'              : 'Spectrum Title',
#     'Sequence'           : 'Sequence',
#     'Protein Accessions' : 'proteinacc_start_stop_pre_post_;',
#     'Modifications'      : 'Modifications',
#     'Charge'             : 'Charge',
#     'm/z'                : 'Exp m/z',
#     'Amanda Score'       : 'Amanda:Score',
#     'Weighted Probability' : 'Amanda:Weighted Probability',
#     'Filename'           : 'Filename',
#     'RT'                 : 'Retention Time (s)',
#     'Rank'               : 'Rank',

#     }

# USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
#     }

# USED_USEARCH_PARAMS = set( [
#     'modifications',
#     'enzyme',
#     'maximum_missed_cleavages',
#     'precursor_mass_tolerance_unit',
#     'precursor_mass_tolerance_minus',
#     'precursor_mass_tolerance_plus',
#     'precursor_mass_type',
#     'precursor_min_charge',
#     'precursor_max_charge',
#     'frag_mass_tolerance_unit',
#     'frag_mass_tolerance',
#     'score_a_ions',
#     'score_b_ions',
#     'score_c_ions',
#     'score_x_ions',
#     'score_y_ions',
#     'score_z_ions',
#     'score_-h2o_ions',
#     'score_-nh3_ions',
#     'score_imm_ions',
#     'score_int_ions',
#     'score_z+1_ions',
#     'score_z+2_ions',
#     'cpus',
#     'database',
#     'validation_score_field',
#     'evalue_field',
#     'validation_minimum_score',
#     'bigger_scores_better',
#     'input_type',
#     ]
#      )
