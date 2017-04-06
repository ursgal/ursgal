#!/usr/bin/env python3.4
# encoding: utf-8
'''

check the format of node and param.

'''
import datetime
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
    'edit_version' : {
        'essential' : True,
        'type'      : [float],
    },
    'name' : {
        'essential' : True,
        'type'      : [str],
    },
    'version' : {
        'essential' : True,
        'type'      : [str],
    },
    'release_date' : {
        'essential' : True,
        'type'      : ['datetime', None],
    },
    'engine_type' : {
        'essential' : True,
        'type'      : dict,
    },
    'input_extensions' : {
        'essential' : True,
        'type'      : list,
    },
    'input_multi_file' : {
        'essential' : True,
        'type'      : bool,
    },
    'output_extensions' : {
        'essential' : True,
        'type'      : list,
    },
    'in_development' : {
        'essential' : True,
        'type'      : bool,
    },
    'include_in_git' : {
        'essential' : True,
        'type'      : bool,
    },
    'citation' : {
        'essential' : True,
        'type'      : str,
    },
}

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


##all_cont = []

def chk_format_node_test():
    for node_name in all_node_name:
        node_dict = all_node[node_name]
        yield chk_format_node, node_name, node_dict

def chk_format_node( node_name, node_dict ):
##    global all_cont
##    for key in list(node_dict['META_INFO']):
##        all_cont.append(key)
##    all_cont = list(set(all_cont))
##    return

    node_dict['META_INFO']
    node_dict['META_INFO']['edit_version']
    node_dict['META_INFO']['name']
    node_dict['META_INFO']['version']
    node_dict['META_INFO']['release_date']
    node_dict['META_INFO']['engine_type']
    node_dict['META_INFO']['input_extensions']
    node_dict['META_INFO']['input_multi_file']
    node_dict['META_INFO']['output_extensions']
    node_dict['META_INFO']['in_development']
    node_dict['META_INFO']['include_in_git']
    node_dict['META_INFO']['citation']

##    node_dict['META_INFO']['output_suffix']
##    node_dict['META_INFO']['utranslation_style']

##    node_dict['META_INFO']['engine']
##    node_dict['META_INFO']['engine_exe']
##    engine_url

##    node_dict['META_INFO']['group_psms']
##    node_dict['META_INFO']['compress_raw_search_results']
##    node_dict['META_INFO']['create_own_folder']
##    node_dict['META_INFO']['cpu_usage']
##    node_dict['META_INFO']['rejected_output_suffix']
##    node_dict['META_INFO']['cannot_distribute']
##    node_dict['META_INFO']['mods_to_unimod_correction']




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
    for node_name in all_node_name:
        node_dict = all_node[node_name]
        chk_format_node( node_name, node_dict )

##    global all_cont
##    print(all_cont)

