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
        'types'     : [bool],
    },
    'citation' : {
        'essential' : True,
        'types'     : [str],
    },
    'compress_raw_search_results' : {
        'essential' : False,
        'types'     : [bool],
    },
    'cpu_usage' : {
        'essential' : False,
        'types'     : [int],
    },
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
    'engine_exe' : {
        'essential' : False,
        'types'     : [dict],
    },
    'engine_type' : {
        'essential' : True,
        'types'     : [dict],
    },
    'engine_url' : {
        'essential' : False,
        'types'     : [dict],
    },
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
    'input_multi_file' : {
        'essential' : True,
        'types'     : [bool],
    },
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
        'types'       : [str,]
    },
}


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
            type_info = ''
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
                            type_info = str(type_name)
                        else:
                            type_info = type_info + ' or ' + str(type_name)
                    elif num == 0:
                        type_info = str(type_name)
                    else:
                        type_info = type_info + ', ' + str(type_name)
                    num += 1
            error_msg = 'The type ' + key_info + parent_info + 'is not ' + \
                str(v_type.__name__) + '. ' + 'It has ' + type_info + '.'
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

    all_extensions    = list(all_param['_extentions']['default_value'])
    output_extensions = node_dict['META_INFO']['output_extensions']
    input_extensions  = node_dict['META_INFO']['input_extensions']
    for ext in (output_extensions + input_extensions):
        if (ext in all_extensions) is False:
            error_msg = '\'' + str(ext) + '\'' + ' could not be found in '\
                'uparams.ursgal_params[\'_extentions\'][\'default_value\'].keys()'
            raise ValueError(error_msg)

    global style_list
    style_list.append(node_dict['META_INFO']['utranslation_style'])


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

    if uvalue_type == 'str' or uvalue_type == 'str_password':
        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [str, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [str]
        elif type(default_value) is not type(None):
            type_list = [str, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        chk_json_item(
            parent_name = 'uvalue_option',
            essential   = True,
            key_list    = ['multiple_line'],
            dict_item   = uvalue_option,
            type_list   = [bool],
        )

    elif uvalue_type == 'int':
        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [int, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [int]
        elif type(default_value) is not type(None):
            type_list = [int, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        uvalue_type_dependence = {
            'max'       : [int],
            'min'       : [int],
            'updownval' : [int],
            'unit'      : [str],
        }
        for k, v in uvalue_type_dependence.items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'int _uevaluation_req' and \
            type(default_value) is not type(None):
        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [int, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [int]
        elif type(default_value) is not type(None):
            type_list = [int, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        uvalue_type_dependence = {
            'max'       : [int, str],
            'min'       : [int, str],
            'updownval' : [int],
            'unit'      : [str],
        }
        for k, v in uvalue_type_dependence.items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'float':
        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [int, float, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [int, float]
        elif type(default_value) is not type(None):
            type_list = [int, float, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        uvalue_type_dependence = {
            'max'       : [int, float],
            'min'       : [int, float],
            'f-point'   : [float],
            'updownval' : [int, float],
            'unit'      : [str],
        }
        for k, v in uvalue_type_dependence.items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

    elif uvalue_type == 'bool':
        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [bool],
        )

    elif uvalue_type == 'select':
        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [str],
        )

        uvalue_type_dependence = {
            'combo_box'      : [bool],
            'radio_button'   : [bool],
            'initial_value'  : [list],
            'custom_val_max' : [int],
        }
        for k, v in uvalue_type_dependence.items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

        chk_vals_types(
            parent_name = 'uvalue_option',
            key_name    = 'initial_value',
            vals        = uvalue_option['initial_value'],
            type_list   = [str],
        )

        if uvalue_option['custom_val_max'] < 0:
            error_msg = 'custom_val_max is more than 0.'
            raise ValueError(error_msg)

    elif uvalue_type == 'list':
        chk_vals_types(
            parent_name = param_name,
            key_name    = 'default_value',
            vals        = [default_value],
            type_list   = [list, type(None)],
        )

        type_list = None
        if type(default_value) is type(None):
            type_list = [list]
        elif type(default_value) is not type(None):
            type_list = [list, type(None)]
        if type_list is not None:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['none_val'],
                dict_item   = uvalue_option,
                type_list   = type_list,
            )

        none_val   = uvalue_option['none_val']

        uvalue_type_dependence = {
            'list_title'     : [list],
            'list_type'      : [dict],
            'custom_val_max' : [int],
        }
        for k, v in uvalue_type_dependence.items():
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = [k],
                dict_item   = uvalue_option,
                type_list   = v,
            )

        list_title = uvalue_option['list_title']
        list_type  = uvalue_option['list_type']

        if default_value is not None:
            if len(list_title) != len(default_value):
                error_msg = 'default_value is not exactly number compared '\
                    'with list_title.'
                raise ValueError(error_msg)
        if none_val is not None:
            if len(list_title) != len(none_val):
                error_msg = 'none_val is not exactly number compared with '\
                    'list_title.'
                raise ValueError(error_msg)

        chk_json_item(
            parent_name = 'uvalue_option',
            essential   = True,
            key_list    = list_title,
            dict_item   = list_type,
            type_list   = [str],
        )

        list_type_list = list(set(list(list_type.values())))
        if ('str' in list_type_list) is True:
            chk_json_item(
                parent_name = 'uvalue_option',
                essential   = True,
                key_list    = ['multiple_line'],
                dict_item   = uvalue_option,
                type_list   = [dict],
            )

        for k in list_title:
            if list_type[k] == 'str':
                chk_json_item(
                    parent_name = 'multiple_line',
                    essential   = True,
                    key_list    = [k],
                    dict_item   = uvalue_option['multiple_line'],
                    type_list   = [bool],
                )

    elif uvalue_type == 'tuple':
        pass

    elif uvalue_type == 'dict':
        pass

    elif uvalue_type == 'None':
        pass

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

