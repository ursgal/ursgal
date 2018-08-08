def fix_line_dict(line_dict, variables):

    return


# def replacement_for_postflight(line_dict, variables):
#     '''
#     *** MOVED FROM POSTFLIGHT TO HERE ***
#     We will save 


#     Will correct the OMSSA headers and add the column retention time to the
#     csv file

#     '''
#     # we translate it for every line, super overhead... do this already in the
#     # new unify csv core
#     headers = variables['fieldnames']
#     header_translations = self.UNODE_UPARAMS['header_translations']['uvalue_style_translation']
#     translated_headers = []
#     for header in headers:
#         if header in [' E-value',' P-value']:
#             continue
#         translated_headers.append(
#             header_translations.get(header, header)
#         )
#     translated_headers += [
#         'Is decoy',
#         'Retention Time (s)',
#         header_translations.get(' E-value', ' E-value'),
#         header_translations.get(' P-value', ' P-value'),
#         'Raw data location',
#     ]

#     updated_line_dict = {}
#     for header in headers:
#         translated_header = header_translations.get(
#             header,
#             header
#         )
#         updated_line_dict[ translated_header ] = line_dict[ header ]
#     updated_line_dict['Sequence'] = updated_line_dict['Sequence'].upper()

#     translated_mods = []
#     if updated_line_dict['Modifications'] != '':
#         splitted_Modifications = updated_line_dict['Modifications'].split(',')
#         for mod in splitted_Modifications:
#             omssa_name, position = mod.split(':')
#             omssa_name  = omssa_name.strip()
#             position    = position.strip()
#             unimod_name = self.lookups[ omssa_name ]['name']
#             if position.strip() == '1':
#                 # print( self.lookups[ omssa_name ] )
#                 for target in self.lookups[ omssa_name ]['aa_targets']:
#                     if 'N-TERM' in target.upper():
#                         position = '0'
#             translated_mods.append(
#                 '{0}:{1}'.format(
#                     unimod_name,
#                     position
#                 )
#             )

#     updated_line_dict['Modifications'] = ';'.join( translated_mods )
#     updated_line_dict['Raw data location'] = self.params['translations']['mgf_input_file']

#     return updated_line_dict, variables
