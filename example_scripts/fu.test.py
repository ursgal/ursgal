#!/usr/bin/env python3.4
# encoding: utf-8
import ursgal
import pprint


def main():
    uc = ursgal.UController()
    for unode_key in uc.unodes.keys():
        if uc.unodes[ unode_key ].get('available', False):
            print( unode_key)
            pprint.pprint( uc.unodes[unode_key]['class'].UNODE_UPARAMS_GROUPED_BY_TAG)


if __name__ == '__main__':
    main(    )
