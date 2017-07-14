#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import pprint
import sys


def main(unode=None):
    '''
    Prints all available parameters for a given UNode, ordered by their tags.

    usage:
        ./show_unode_paramters.py <UNode>

    Example node names:
        * omssa_2_1_9
        * xtandem_vengeance

    '''
    uc = ursgal.UController()
    for unode_key in uc.unodes.keys():
        if unode_key == unode:
            if uc.unodes[ unode_key ].get('available', False):
                print( unode_key)
                pprint.pprint( uc.unodes[unode_key]['class'].UNODE_UPARAMS_GROUPED_BY_TAG)


if __name__ == '__main__':
    main( 
        unode = sys.argv[1]
    )
