#!/usr/bin/env python3
# encoding: utf-8
'''

check the format of node and param.

'''
from datetime import datetime
from ursgal import uparams
from ursgal import UController
from ursgal import ukb

# node format
node_meta_info = {
    'distributable' : {
        'essential' : False,
        'types'     : [bool],
    },
    'citation' : {
        'essential' : True,
        'types'     : [str],
    },
    # 'compress_raw_search_results' : {
    #     'essential' : False,
    #     'types'     : [bool],
    # },
    # 'cpu_usage' : {
    #     'essential' : False,
    #     'types'     : [int],
    # },
    'create_own_folder' : {
        'essential' : False,
        'types'     : [bool],
    },
    'edit_version' : {
        'essential' : True,
        'types'     : [float],
    },
    'engine' : {
        'essential' : False,
        'types'     : [dict],
    },
    # 'engine_exe' : {
    #     'essential' : False,
    #     'types'     : [dict],
    # },
    'engine_type' : {
        'essential' : True,
        'types'     : [dict],
    },
    # 'engine_url' : {
    #     'essential' : False,
    #     'types'     : [dict],
    # },
    'group_psms' : {
        'essential' : False,
        'types'     : [bool],
    },
    'in_development' : {
        'essential' : True,
        'types'     : [bool],
    },
    'include_in_git' : {
        'essential' : True,
        'types'     : [bool, type(None)],
    },
    'input_extensions' : {
        'essential' : True,
        'types'     : [list],
    },
    # 'input_multi_file' : {
    #     'essential' : True,
    #     'types'     : [bool],
    # },
    'mods_to_unimod_correction' : {
        'essential' : False,
        'types'     : [dict],
    },
    'name' : {
        'essential' : True,
        'types'     : [str],
    },
    'output_extensions' : {
        'essential' : True,
        'types'     : [list],
    },
    'output_suffix' : {
        'essential' : False,
        'types'     : [str, type(None)],
    },
    'rejected_output_suffix' : {
        'essential' : False,
        'types'     : [str],
    },
    'release_date' : {
        'essential' : True,
        'types'     : ['datetime', type(None)],
    },
    'utranslation_style' : {
        'essential' : True,
        'types'     : [str],
    },
    'version' : {
        'essential' : True,
        'types'     : [str],
    },
    'uses_unode' : {
        'essential' : False,
        'types'     : [str],
    },
}

# param format
param_info = {
    'available_in_unode' : {
        'essential'   : True,
        'types'       : [list],
        'ignore_key'  : ['ucontroller']
    },
    'default_value'   : {
        'essential'   : True,
        'types'       : [type(None), str, int, float, bool, list, tuple, dict],
    },
    'description' : {
        'essential'   : True,
        'types'       : [str],
    },
    'edit_version' : {
        'essential'   : True,
        'types'       : [float],
    },
    'triggers_rerun' : {
        'essential'   : True,
        'types'       : [bool],
    },
    'ukey_translation' : {
        'essential'   : True,
        'types'       : [dict],
    },
    'utag' : {
        'essential'   : True,
        'types'       : [list],
    },
    'uvalue_option'   : {
        'essential'   : True,
        'types'       : [dict],
    },
    'uvalue_translation' : {
        'essential'   : True,
        'types'       : [dict],
    },
    'uvalue_type' : {
        'essential'   : True,
        'types'       : [str]
    },
}

# type format
type_info = {
    'str' : {
        'my_type' : str,
        'option'  : {
            'multiple_line'  : [bool],
        },
    },
    'str_password' : {
        'my_type' : str,
        'option'  : {
            'multiple_line'  : [bool],
        },
    },
    'int' : {
        'my_type' : int,
        'option'  : {
            'max'            : [int],
            'min'            : [int],
            'updownval'      : [int],
            'unit'           : [str],
        },
    },
    'int _uevaluation_req' : {
        'my_type' : int,
        'option'  : {
            'max'            : [int, str],
            'min'            : [int, str],
            'updownval'      : [int],
            'unit'           : [str],
        },
    },
    'float' : {
        'my_types' : [int, float],
        'option'  : {
            'max'            : [int, float],
            'min'            : [int, float],
            'f-point'        : [float],
            'updownval'      : [int, float],
            'unit'           : [str],
        },
    },
    'bool' : {
        'my_type' : bool,
        'option'  : {
        },
    },
    'select' : {
        'my_type' : str,
        'option'  : {
            'select_type'       : [str],
            'available_values'  : [list],
            'custom_val_max'    : [int],
        },
    },
    'list' : {
        'my_type' : list,
        'option'  : {
            'item_title'     : [str],
            'item_type'      : [str],
            'custom_val_max' : [int],
        },
    },
    # 'tuple' : {
    #     'my_type' : tuple,
    #     'option': {
    #         'titles'     : [list],
    #         'type_dict'      : [dict],
    #         'custom_val_max' : [int],
    #     },
    # },
    'dict' : {
        'my_type' : dict,
        'option'  : {
            'item_titles'     : [dict],
            'value_types'      : [dict],
        },
    },
    'None' : {
        'my_type' : type(None),
        'option'  : {
            'system_param'   : [bool]
        },
    },
}

# styles which is required by system
style_list = [
    'ucontroller_style_1',
]

# pre-treatment of Node format
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

# pre-treatment of Param format
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


def chk_dict_keys( parent_name='', key_list=[], dict_item={} ):
    for k in key_list:
        if dict_item.get(k) is None and \
                dict_item.get(k, 'None') == 'None':
            parent_info = ''
            if parent_name != '':
                parent_info = ' in ' + str(parent_name)
            error_msg = str(k) + ' is required' + parent_info + '.'
            raise ValueError(error_msg)


def chk_vals_types( parent_name='', key_name='', vals=[], type_list=[] ):
    if len(type_list) == 0:
        return

    for v in vals:
        v_type = type(v)
        if ('datetime' in type_list) is True and v_type is str:
            num = len(v) - len(v.replace('-', '').replace(':', ''))
            if num == 2:
                try:
                    datetime.strptime(v, '%Y-%m-%d')
                    datetime_chk = True
                except:
                    datetime_chk = False
            elif num == 4:
                try:
                    datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
                    datetime_chk = True
                except:
                    datetime_chk = False
        else:
            datetime_chk = False

        if (v_type in type_list) is not True and datetime_chk is not True:
            key_info = ''
            parent_info = ''
            if key_name != '':
                key_info = 'of \'' + str(key_name) + '\''
                if parent_name != '':
                    parent_info = ' in ' + str(parent_name) + ' '
            my_type = ''
            len_type_list = len(type_list)
            if len_type_list >= 1:
                num = 0
                for type_class in type_list:
                    if type_class == 'datetime':
                        type_name = 'datetime'
                    else:
                        type_name = type_class.__name__
                    if num == len_type_list-1:
                        if num == 0:
                            my_type = str(type_name)
                        else:
                            my_type = my_type + ' or ' + str(type_name)
                    elif num == 0:
                        my_type = str(type_name)
                    else:
                        my_type = my_type + ', ' + str(type_name)
                    num += 1
            error_msg = 'The type ' + key_info + parent_info + 'is not ' + \
                str(v_type.__name__) + '. ' + 'It has ' + my_type + '.'
            raise ValueError(error_msg)


def chk_json_item( parent_name='', essential=False, key_list=[], dict_item={}, \
        type_list=[] ):
    if essential is True:
        chk_dict_keys( parent_name, key_list, dict_item )

    for key_name in key_list:
        if dict_item.get(key_name) is not None or \
                dict_item.get(key_name) is None and \
                dict_item.get(key_name, 'None') != 'None':
            vals = [dict_item[key_name]]
            chk_vals_types( parent_name, key_name, vals, type_list )


def chk_format_node( node_name, node_dict ):
    print(node_name)
    chk_dict_keys(
        parent_name = node_name,
        key_list    = ['META_INFO'],
        dict_item   = node_dict,
    )
    chk_dict_keys(
        parent_name = 'node_meta_info',
        key_list    = list(node_dict['META_INFO']),
        dict_item   = node_meta_info,
    )

    for k, v in node_meta_info.items():
        chk_json_item(
            parent_name = 'META_INFO',
            essential   = v['essential'],
            key_list    = [k],
            dict_item   = node_dict['META_INFO'],
            type_list   = v['types'],
        )

    all_extensions    = list(ukb.FILE_EXTENSIONS)
    output_extensions = node_dict['META_INFO']['output_extensions']
    input_extensions  = node_dict['META_INFO']['input_extensions']
    for ext in (output_extensions + input_extensions):
        if (ext in all_extensions) is False:
            error_msg = '\'' + str(ext) + '\'' + ' could not be found in '\
                'uparams.ursgal_params[\'_extensions\'][\'default_value\'].keys()'
            raise ValueError(error_msg)

    global style_list
    style_list.append(node_dict['META_INFO']['utranslation_style'])


def search_dict_keys(dict_item, single_key=True, key_list=[], layer_num=0):
    layer_dict = {}
    for key in dict_item.keys():
        key_list.append(key)
        if isinstance(dict_item[key], dict):
            key_list2, layer_dict2 = search_dict_keys(
                dict_item[key],
                single_key,
                key_list,
                layer_num + 1,
            )
            for k, v in layer_dict2.items():
                if layer_dict.get(k) is None:
                    layer_dict[k] = []
                layer_dict[k].extend(v)

            if single_key is True:
                break
        else:
            if layer_dict.get(key) is None:
                layer_dict[key] = []
            layer_dict[key].append(layer_num+1)
    return key_list, layer_dict


def chk_format_param( param_name, param_dict ):
    chk_dict_keys(
        parent_name = 'param_info',
        key_list    = list(param_dict),
        dict_item   = param_info,
    )

    for k, v in param_info.items():
        chk_json_item(
            parent_name = param_name,
            essential   = v['essential'],
            key_list    = [k],
            dict_item   = param_dict,
            type_list   = v['types'],
        )

    for ava_node in param_dict['available_in_unode']:
        if (ava_node in param_info['available_in_unode']['ignore_key']) is False:
            chk_dict_keys(
                parent_name = 'wrappers',
                key_list    = [ava_node],
                dict_item   = all_node,
            )

    utag          = param_dict['utag']
    uvalue_option = param_dict['uvalue_option']
    uvalue_type   = param_dict['uvalue_type']
    default_value = param_dict['default_value']

    if ('input_files' in utag) is True:
        chk_json_item(
            parent_name = 'uvalue_option',
            essential   = True,
            key_list    = ['input_extensions'],
            dict_item   = uvalue_option,
            type_list   = [list],
        )

    global style_list
    style_list = list(set(style_list))
    ukey_translation_keys   = list(param_dict['ukey_translation'])
    uvalue_translation_keys = list(param_dict['uvalue_translation'])
    search_style_list = list(set(ukey_translation_keys+uvalue_translation_keys))

    for search_style in search_style_list:
        if (search_style in style_list) is False:
            error_msg = str(search_style) + ' is unknown style.'
            raise ValueError(error_msg)

    if (uvalue_type in list(type_info)) is False:
        error_msg = str(uvalue_type) + ' is unknown type.'
        raise ValueError(error_msg)

    if uvalue_type == 'str' or uvalue_type == 'str_password':
        my_type = type_info[uvalue_type]['my_type']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [my_type, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [my_type]
        elif type(default_value) is not type(None):
            type_list = [my_type, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'int':
        my_type = type_info[uvalue_type]['my_type']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [my_type, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [my_type]
        elif type(default_value) is not type(None):
            type_list = [my_type, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'int _uevaluation_req' and \
            type(default_value) is not type(None):
        my_type = type_info[uvalue_type]['my_type']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [my_type, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [my_type]
        elif type(default_value) is not type(None):
            type_list = [my_type, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'float':
        my_types = type_info[uvalue_type]['my_types']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = my_types + [type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = my_types
        elif type(default_value) is not type(None):
            type_list = my_types + [type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'bool':
        my_type = type_info[uvalue_type]['my_type']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [my_type],
        )

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'select':
        my_type = type_info[uvalue_type]['my_type']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [my_type],
        )

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

        chk_vals_types(
            parent_name = 'uvalue_option',
            key_name    = 'available_values',
            vals        = uvalue_option['available_values'],
            type_list   = [my_type],
        )

        chk_vals_types(
            parent_name = 'uvalue_option',
            key_name    = 'custom_val_max',
            vals        = [uvalue_option['custom_val_max']],
            type_list   = [int],
        )
        if uvalue_option['custom_val_max'] < 0:
            error_msg = 'custom_val_max is more than 0.'
            raise ValueError(error_msg)

    elif uvalue_type == 'list':
        my_type = type_info[uvalue_type]['my_type']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [my_type, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [my_type]
        elif type(default_value) is not type(None):
            type_list = [my_type, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        none_val   = uvalue_option['none_val']

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

        item_title = uvalue_option['item_title']
        item_type  = uvalue_option['item_type']

        # Why should checking for the same number of elements be necessary?
        # The number of elements in a list is variable
        # if default_value is not None:
        #     if len(title_list) != len(default_value):
        #         error_msg = 'default_value is not exactly number compared '\
        #             'with title_list.'
        #         raise ValueError(error_msg)
        # if none_val is not None:
        #     if len(title_list) != len(none_val):
        #         error_msg = 'none_val is not exactly number compared with '\
        #             'title_list.'
        #         raise ValueError(error_msg)

        # chk_json_item(
        #     parent_name = 'uvalue_option',
        #     essential   = True,
        #     key_list    = [item_title],
        #     dict_item   = item_type,
        #     type_list   = [str],
        # )

        # list_type_list = list(set(list(type_dict.values())))
        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )
        # for k, v in type_info.items():
        #     if k == item_type:
        #         chk_json_item(
        #             parent_name = 'uvalue_option',
        #             essential   = True,
        #             key_list    = list(v['option']),
        #             dict_item   = uvalue_option,
        #             type_list   = [eval(item_type)],
        #         )

        # Just one title for items in list now, so this should not be necessary anymore
        # for k, v in type_info.items():
        #     for title in title_list:
        #         if type_dict[title] == k:
        #             for k2, v2 in v['option'].items():
        #                 chk_json_item(
        #                     parent_name = k2,
        #                     essential   = True,
        #                     key_list    = [title],
        #                     dict_item   = uvalue_option[k2],
        #                     type_list   = v2,
        #                 )

        chk_vals_types(
            parent_name = 'uvalue_option',
            key_name    = 'custom_val_max',
            vals        = [uvalue_option['custom_val_max']],
            type_list   = [int],
        )
        if uvalue_option['custom_val_max'] < 0:
            error_msg = 'custom_val_max is more than 0.'
            raise ValueError(error_msg)
        elif uvalue_option['custom_val_max'] >= 1:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['custom_type'],
                dict_item   = uvalue_option,
                type_list   = [dict],
            )
            for type_name in list(uvalue_option['custom_type']):
                if (type_name in list(type_info)) is True:
                    chk_json_item(
                        parent_name = 'custom_type',
                        essential   = True,
                        key_list    = [type_name],
                        dict_item   = uvalue_option['custom_type'],
                        type_list   = [dict],
                    )
                    for k, v in type_info[type_name]['option'].items():
                        chk_json_item(
                            parent_name = type_name,
                            essential   = True,
                            key_list    = [k],
                            dict_item   = uvalue_option['custom_type'][type_name],
                            type_list   = v,
                        )
                else:
                    error_msg = str(uvalue_type) + ' is unknown type.'
                    raise ValueError(error_msg)

    elif uvalue_type == 'dict':
        my_type = type_info[uvalue_type]['my_type']

        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [my_type, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [my_type]
        elif type(default_value) is not type(None):
            type_list = [my_type, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        none_val = uvalue_option['none_val']

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

        dict_title = uvalue_option['item_titles']
        dict_type  = uvalue_option['value_types']

        title_key_list, title_layer_dict = search_dict_keys(
            dict_item  = dict_title,
            single_key = True,
            key_list   = [],
            layer_num  = 0,
        )
        title_layer_list = []
        [title_layer_list.extend(v) for v in title_layer_dict.values()]
        title_layer_list = list(set(title_layer_list))

        title_dict_len = len(title_key_list)
        key_list, layer_dict = search_dict_keys(
            dict_item  = dict_title,
            single_key = False,
            key_list   = [],
            layer_num  = 0,
        )

        if title_dict_len != len(key_list):
            error_msg = 'dict_title is single layer.'
            raise ValueError(error_msg)

        # for k in key_list:
        #     dict_title2chk = dict_title[k]
        #     chk_vals_types(
        #         parent_name = 'item_titles',
        #         key_name    = k,
        #         vals        = [dict_title2chk],
        #         type_list   = [eval(dict_type[k])],
        #     )

        dict_val_search = {
            'default_value' : default_value,
            'none_val'      : none_val,
        }
        for k, v in dict_val_search.items():
            if v is not None:
                key_list, layer_dict = search_dict_keys(
                    dict_item  = v,
                    single_key = False,
                    key_list   = [],
                    layer_num  = 0,
                )
                layer_list = []
                [layer_list.extend(v) for v in layer_dict.values()]
                layer_list = list(set(layer_list))
                if layer_list != [] and layer_list != title_layer_list:
                    error_msg = str(k) + ' has different layer number '\
                        'compared with dict_title. {0} vs {1}'.format(
                            layer_list,
                            title_layer_list
                        )
                    raise ValueError(error_msg)

                # title_list = list(layer_dict)
                # for k, v in type_info.items():
                #     for title in title_list:
                #         if dict_type[title] == k:
                #             for k2, v2 in v['option'].items():
                #                 chk_json_item(
                #                     parent_name = k2,
                #                     essential   = True,
                #                     key_list    = [title],
                #                     dict_item   = uvalue_option[k2],
                #                     type_list   = v2,
                                # )

        chk_vals_types(
            parent_name = 'uvalue_option',
            key_name    = 'custom_val_max',
            vals        = [uvalue_option['custom_val_max']],
            type_list   = [int],
        )
        if uvalue_option['custom_val_max'] < 0:
            error_msg = 'custom_val_max is more than 0.'
            raise ValueError(error_msg)
        elif uvalue_option['custom_val_max'] >= 1:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['custom_type'],
                dict_item   = uvalue_option,
                type_list   = [dict],
            )
            for type_name in list(uvalue_option['custom_type']):
                if (type_name in list(type_info)) is True:
                    chk_json_item(
                        parent_name = 'custom_type',
                        essential   = True,
                        key_list    = [type_name],
                        dict_item   = uvalue_option['custom_type'],
                        type_list   = [dict],
                    )
                    for k, v in type_info[type_name]['option'].items():
                        chk_json_item(
                            parent_name = type_name,
                            essential   = True,
                            key_list    = [k],
                            dict_item   = uvalue_option['custom_type'][type_name],
                            type_list   = v,
                        )
                else:
                    error_msg = str(uvalue_type) + ' is unknown type.'
                    raise ValueError(error_msg)

    elif uvalue_type == 'None':
        my_type = type_info[uvalue_type]['my_type']

        for k, v in type_info[uvalue_type]['option'].items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    else:
        error_msg = '\'' + str(uvalue_type) + '\' does not support.'
        raise ValueError(error_msg)


def chk_format_node_param_test():
    for node_name in all_node_name:
        node_dict = all_node[node_name]
        yield chk_format_node, node_name, node_dict

    for param_name in all_param_name:
        param_dict = all_param[param_name]
        yield chk_format_param, param_name, param_dict


if __name__ == '__main__':
    print(__doc__)
    for node_name in all_node_name:
        node_dict = all_node[node_name]
        chk_format_node( node_name, node_dict )

    for param_name in all_param_name:
        param_dict = all_param[param_name]
        chk_format_param( param_name, param_dict )

