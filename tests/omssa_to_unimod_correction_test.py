#!/usr/bin/env python3
# encoding: utf-8
'''

Test the OMSSA mop remap of e.g. TMT labeling

TMT labeling has the wrong unimod name in the OMSSA mods xml file

Probably more mods need remap

'K,fix,any,TMT6plex',
'*,opt,N-term,TMT6plex',
'K,fix,any,TMT2plex',
'*,opt,N-term,TMT2plex',

'''
import ursgal
import csv
import os
import pprint


TESTS = [
    {
        'modifications' : [ 'K,fix,any,TMT6plex' ],
        'result_dict': {
            '737' : {
                '198' : {
                    'aa_targets'  : ['K'],
                }
            }
        },
    },
    {
        'modifications' : [ '*,opt,N-term,TMT6plex' ],
        'result_dict': {
            '737' : {
                '199' : {
                    'aa_targets'  : ['N-term'],
                }
            }
        },
    },
    {
        'modifications' : [ 'K,fix,any,TMT2plex' ],
        'result_dict': {
            '738' : {
                '198' : {
                    'aa_targets'  : ['K'],
                }
            }
        },
    },
    {
        'modifications' : [ '*,opt,N-term,TMT2plex' ],
        'result_dict': {
            '738' : {
                '199' : {
                    'aa_targets'  : ['N-term'],
                }
            }
        },
    },

]

uc = ursgal.UController()
IS_AVAILABLE = uc.unodes['omssa_2_1_9']['available']

def map_mods_test():
    for test_id, test_dict in enumerate(TESTS):
        yield map_mods, test_dict


def map_mods( test_dict ):
    if IS_AVAILABLE:
        uc.params['modifications'] = test_dict['modifications']
        omssa_class = cl=uc.unodes['omssa_2_1_9']['_wrapper_class']()
        cl.exe = os.path.join(uc.unodes['omssa_2_1_9']['resource_folder'],'omssacl')
        cl._load_omssa_xml()
        for unimod_id in test_dict['result_dict'].keys():
            assert unimod_id in cl.omssa_mod_Mapper.keys()
            for omssa_id in test_dict['result_dict'][unimod_id].keys():
                assert omssa_id in cl.omssa_mod_Mapper[unimod_id].keys()
                for k,v in test_dict['result_dict'][unimod_id][omssa_id].items():
                    assert cl.omssa_mod_Mapper[unimod_id][omssa_id][k] == v


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        map_mods(test_dict)
