# META_INFO = {
#     'in_development'    : False,
#     'engine_type' : {
#         'search_engine' : False,
#         'converter'     : True
#     },
#     'output_extension'  : '.csv',
#     'output_suffix'     : None,
#     'input_types'       : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'],
#     # 'can_gz': True,
#     'citation'       : 'Reisinger F, Krishna R, Ghali F, Ríos D, '\
#         'Hermjakob H, Vizcaíno JA, Jones AR. (2012) jmzIdentML API: '\
#         'A Java interface to the mzIdentML standard for peptide and '\
#         'protein identification data.',
# 'in_development'            : True,
#     'include_in_git'            : False,

#     'engine': {
#         'platform_independent' : {
#             'arc_independent' : {
#                 'exe'            : 'mzidentml-lib-1.6.11.jar',
#                 'url'            : '',
#                 'zip_md5'        : '77757dc40d2eca87c49899a27c3f14a0',
#                 'additional_exe' : [],
#             },
#         },
#     },
# }

DEFAULT_PARAMS = {
    'mzidentml_outputFragmentation' : False,
    # 'mzidentml_compress'            : False,
    # this is determined autmoatically now
    'mzidentml_exportType'          : 'exportPSMs',
    'mzidentml-verboseOutput'       : False,
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    False : 'false',
    True  : 'true',
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
}

USED_USEARCH_PARAMS = set([
    'java_-Xmx',
    'decoy_tag',
    'mzidentml_outputFragmentation',
    'mzidentml_compress',
    'mzidentml_exportType',
    'mzidentml_verboseOutput',
    ])
