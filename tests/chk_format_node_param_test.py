#!/usr/bin/env python3.4
# encoding: utf-8
'''

check the format of node and param.

'''
from datetime import datetime
from ursgal import uparams
from ursgal import UController


uc = UController()
all_node  = uc.unodes
all_node_name = list(all_node)
all_node_name.sort()
remove_list = []
for node_name in all_node_name:
    if node_name[0] == '_':
        if len(node_name) < 5 or node_name[0:5] != '_test':
            remove_list.append(node_name)
for remove_name in remove_list:
    all_node_name.remove(remove_name)

node_meta_info = {
    'cannot_distribute' : {
        'essential' : False,
        'type'      : bool,
    },
    'citation' : {
        'essential' : True,
        'type'      : str,
    },
    'compress_raw_search_results' : {
        'essential' : False,
        'type'      : bool,
    },
    'cpu_usage' : {
        'essential' : False,
        'type'      : int,
    },
    'create_own_folder' : {
        'essential' : False,
        'type'      : bool,
    },
    'edit_version' : {
        'essential' : True,
        'type'      : float,
    },
    'engine' : {
        'essential' : False,
        'type'      : dict,
    },
    'engine_exe' : {
        'essential' : False,
        'type'      : dict,
    },
    'engine_type' : {
        'essential' : True,
        'type'      : dict,
    },
    'engine_url' : {
        'essential' : False,
        'type'      : dict,
    },
    'group_psms' : {
        'essential' : False,
        'type'      : bool,
    },
    'in_development' : {
        'essential' : True,
        'type'      : bool,
    },
    'include_in_git' : {
        'essential' : True,
        'type'      : [bool, type(None)],
    },
    'input_extensions' : {
        'essential' : True,
        'type'      : list,
    },
    'input_multi_file' : {
        'essential' : True,
        'type'      : bool,
    },
    'mods_to_unimod_correction' : {
        'essential' : False,
        'type'      : dict,
    },
    'name' : {
        'essential' : True,
        'type'      : str,
    },
    'output_extensions' : {
        'essential' : True,
        'type'      : list,
    },
    'output_suffix' : {
        'essential' : False,
        'type'      : [str, type(None)],
    },
    'rejected_output_suffix' : {
        'essential' : False,
        'type'      : str,
    },
    'release_date' : {
        'essential' : True,
        'type'      : ['datetime', type(None)],
    },
    'utranslation_style' : {
        'essential' : True,
        'type'      : str,
    },
    'version' : {
        'essential' : True,
        'type'      : str,
    },
}

style_list = [
    'ucontroller_style_1',
]

all_param = uparams.ursgal_params
all_param_name = list(all_param)
all_param_name.sort()
remove_list = []
for param_name in all_param_name:
    if param_name[0] == '_':
        if len(param_name) < 5 or param_name[0:5] != '_test':
            remove_list.append(param_name)
for remove_name in remove_list:
    all_param_name.remove(remove_name)

param_info = {
    'available_in_unode' : {
        'essential'   : True,
        'type'        : list,
        'ignore_key'  : ['ucontroller']
    },
    'default_value'   : {
        'essential'   : True,
        'type'        : [type(None), str, int, float, bool, list, tuple, dict],
    },
    'description' : {
        'essential'   : True,
        'type'        : str,
    },
    'edit_version' : {
        'essential'   : True,
        'type'        : float,
    },
    'triggers_rerun' : {
        'essential'   : True,
        'type'        : bool,
    },
    'ukey_translation' : {
        'essential'   : True,
        'type'        : dict,
    },
    'utag' : {
        'essential'   : True,
        'type'        : list,
    },
    'uvalue_option'   : {
        'essential'   : True,
        'type'        : dict,
    },
    'uvalue_translation' : {
        'essential'   : True,
        'type'        : dict,
    },
    'uvalue_type' : {
        'essential'   : True,
        'type'        : str,
    },
}


def chk_format_node_test():
    for node_name in all_node_name:
        node_dict = all_node[node_name]
        yield chk_format_node, node_name, node_dict


def chk_format_node( node_name, node_dict ):
    for k in node_dict['META_INFO'].keys():
        node_meta_info[k]

    for k, v in node_meta_info.items():
        if v['essential'] is True or node_dict['META_INFO'].get(k) is not None:
            if type(v['type']) is list:
                answer = False
                metainfo_value = node_dict['META_INFO'][k]
                for type_item in v['type']:
                    if type_item == type(metainfo_value):
                        answer = True
                        break
                    elif type_item == 'datetime' and type(metainfo_value) is str:
                        num = len(metainfo_value) - len(metainfo_value.\
                                              replace('-', '').replace(':', ''))
                        if num == 2:
                            datetime.strptime(metainfo_value, '%Y-%m-%d')
                            answer = True
                            break
                        elif num == 4:
                            datetime.strptime(metainfo_value, '%Y-%m-%d %H:%M:%S')
                            answer = True
                            break
                if answer is not True:
                    error_msg = 'The type of \'' + str(k) + '\'' + ' is not exactly.'
                    raise ValueError(error_msg)
            else:
                if v['type'] != type(node_dict['META_INFO'][k]):
                    error_msg = 'The type of \'' + str(k) + '\'' + ' is not exactly.'
                    raise ValueError(error_msg)

    all_extensions    = list(all_param['_extentions']['default_value'])
    output_extensions = node_dict['META_INFO']['output_extensions']
    input_extensions  = node_dict['META_INFO']['input_extensions']
    for ext in (output_extensions + input_extensions):
        if (ext in all_extensions) is False:
            error_msg = '\'' + str(ext) + '\'' + ' could not be found in '\
                'uparams.ursgal_params[\'_extentions\'][\'default_value\'].keys()'
            raise ValueError(error_msg)

    if type(node_dict['META_INFO']['utranslation_style']) is not str:
        error_msg = 'The type of \'utranslation_style\' is str.'
        raise ValueError(error_msg)
    else:
        global style_list
        style_list.append(node_dict['META_INFO']['utranslation_style'])


def chk_format_param_test():
    for param_name in all_param_name:
        param_dict = all_param[param_name]
        yield chk_format_param, param_name, param_dict


def chk_format_param( param_name, param_dict ):
    for k in param_dict.keys():
        param_info[k]

    for k, v in param_info.items():
        if v['essential'] is True or param_dict.get(k) is not None:
            if type(v['type']) is list:
                answer = False
                param_value = param_dict[k]
                for type_item in v['type']:
                    if type_item == type(param_value):
                        answer = True
                        break
                if answer is not True:
                    error_msg = 'The type of \'' + str(k) + '\'' + ' is not exactly.'
                    raise ValueError(error_msg)
            else:
                if v['type'] != type(param_dict[k]):
                    error_msg = 'The type of \'' + str(k) + '\'' + ' is not exactly.'
                    raise ValueError(error_msg)

    for ava_node in param_dict['available_in_unode']:
        if (ava_node in param_info['available_in_unode']['ignore_key']) is False:
            all_node[ava_node]

    uvalue_type   = param_dict['uvalue_type']
    default_value = param_dict['default_value']
    uvalue_option = param_dict['uvalue_option']
    if param_dict.get('input_files') is not None:
        if uvalue_option.get('input_extensions') is None:
            error_msg = 'input_extensions is required in uvalue_option, '\
                'because this is input file params.'
            raise ValueError(error_msg)
        elif type(uvalue_option['input_extensions']) is not list:
            error_msg = 'The type of \'input_extensions\' is list.'
            raise ValueError(error_msg)

    global style_list
    style_list = list(set(style_list))
    ukey_translation_keys   = list(param_dict['ukey_translation'])
    uvalue_translation_keys = list(param_dict['uvalue_translation'])
    search_style_list = list(set(ukey_translation_keys+uvalue_translation_keys))

    for search_style in search_style_list:
        if (search_style in style_list) is False:
            error_msg = str(search_style) + ' is unknown style.'
            raise ValueError(error_msg)

    if uvalue_type is str:
        if type(default_value) is not type(None) and \
                                                 type(default_value) is not str:
            error_msg = 'The type of \'default_value\' is str or None.'
            raise ValueError(error_msg)
        if uvalue_option.get('multipleLine') is None:
            error_msg = 'multipleLine is required in uvalue_option.'
            raise ValueError(error_msg)
        elif type(uvalue_option['multipleLine']) is not bool:
            error_msg = 'The type of \'multipleLine\' is bool.'
            raise ValueError(error_msg)




if __name__ == '__main__':
    print(__doc__)
    for node_name in all_node_name:
        node_dict = all_node[node_name]
        chk_format_node( node_name, node_dict )

    for param_name in all_param_name:
        param_dict = all_param[param_name]
        chk_format_param( param_name, param_dict )



