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
all_node_name  = list(all_node)
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
        'type'      : bool,
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
        'type'      : str,
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
        'essential' : False,
        'type'      : str,
    },
    'version' : {
        'essential' : True,
        'type'      : str,
    },
}


all_param = uparams.ursgal_params
all_param_name = list(all_param)
all_param_name.sort()
remove_list = []
for param_name in all_param_name:
##    if param_name[0] == '_' and param_name != '_extentions':
    if param_name[0] == '_':
        if len(param_name) < 5 or param_name[0:5] != '_test':
            remove_list.append(param_name)
for remove_name in remove_list:
    all_param_name.remove(remove_name)


print(all_param_name)



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
                meta_info_value = node_dict['META_INFO'][k]
                for type_item in v['type']:
                    if type_item == type(meta_info_value):
                        answer = True
                        break
                    elif type_item == 'datetime' and type(meta_info_value) is str:
                        num = len(meta_info_value) - len(meta_info_value.\
                                              replace('-', '').replace(':', ''))
                        if num == 2:
                            datetime.strptime(meta_info_value, '%Y-%m-%d')
                            answer = True
                            break
                        elif num == 4:
                            datetime.strptime(meta_info_value, '%Y-%m-%d %H:%M:%S')
                            answer = True
                            break
                if answer is not True:
                    raise ValueError(k)
            else:
                if v['type'] != type(node_dict['META_INFO'][k]):
                    raise ValueError(k)


def chk_format_node_test():
    for param_name in all_param_name:
        param_dict = all_param[param_name]
        yield chk_format_param, param_name, param_dict


def chk_format_param( param_name, param_dict ):
    pass


##def chk_format_param( test_dict, expected_dict ):
##    for key in [
##        'Raw data location',
##        'Spectrum ID',
##        'Spectrum Title',
##        'Retention Time (s)',
##        'rank',
##        'Calc m/z',
##        'Exp m/z',
##        'Charge',
##        'Sequence',
##        'Modifications',
##        'X\!Tandem:expect',
##        'X\!Tandem:hyperscore',
##        'proteinacc_start_stop_pre_post_;',
##        'Is decoy',
##        ]:
##        test_value = test_dict[key]
##        expected_value = expected_dict[key]
##        assert test_value == expected_value

if __name__ == '__main__':
    print(__doc__)
##    for node_name in all_node_name:
##        node_dict = all_node[node_name]
##        chk_format_node( node_name, node_dict )

    for param_name in all_param_name:
        param_dict = all_param[param_name]
        chk_format_param( param_name, param_dict )



