#!/usr/bin/env python3.4
# encoding: utf-8
"""
peptide_fragmentor.py

usage:
peptide_fragmentor.py <PEPITDE>

Originally PeptideFragmentor involved these options:
 [light|heavy] <light N15 labled ?> [mod={'K':12}]

Created by le.fu on 2010-07-14.
Copyright under MIT license
"""
from __future__ import absolute_import
from __future__ import print_function
import sys
from collections import defaultdict as ddict
import pyqms
import pprint


rules = {
    'C-Term' : [
        {
            'name' : 'water loss form c-terminal',
            'aa'  : ['any']
        },
        {
            'name' : 'pyroglutamic acid formation on n-term',
            'aa' : ['E', 'D']
        }
    ],
    'N-Term' : [
    ],
    'Anywhere' : [
        # those create just additional peptide versions
        {
            'name' : 'loss of water from S',
            'aa' : ['S', 'T'],
        },
        {
            'name' : 'loss of ammonia via cyclization of side chain',
            'aa' : ['K', 'R'],
        },
        {
            'name' : 'loss of ammonia form side chain',
            'aa' : ['Q', 'N']
        },
        {
            'name' : 'internal fragment',
            'aa' : ['any'],
            'note' : '-CO'
        }
    ]
}


def update_ions( ions=None, root_ion_info=None, charges=None, cc_factory=None):
    # import pyqms
    # import pyqms.knowledge_base

    ION_NAME = '{type}{pos} {neutral_loss} (+{charge}) {modifications}'
    NO_LOSS  = {'neutral_loss': '', 'cc': {}}  # pure vanilla fragment
    basic_neutral_loss_list = [ NO_LOSS ]
    if 'neutral losses' in root_ion_info.keys():
        root_ion_info['neutral losses'] += basic_neutral_loss_list
    else:
        root_ion_info['neutral losses'] = basic_neutral_loss_list
    if 'mods' not in root_ion_info.keys():
        root_ion_info['mods'] = []
    if ions is None:
        ions = {}
    if charges is None:
        charges = [1, ]
    ion_info_template = {
        'type' : root_ion_info['type'],
        'pos': root_ion_info['pos'] ,
        'modifications' : '',
        'neutral_loss' : '',
        'charge' : -1,
    }
    if root_ion_info['type'] not in ions.keys():
        ions[ root_ion_info['type'] ] = {}
    # ion_info_template.update( ion_info )
    if len( root_ion_info['modifications'] ) > 0:
        ion_info_template['modifications'] = '#' + ';'.join(
            root_ion_info['modifications']
        )
    else:
        ion_info_template['modifications'] = ''
    for charge in charges:
        ion_info_template['charge'] = charge

        for neulo in root_ion_info['neutral losses']:
            ion_info_template['neutral_loss'] = neulo['neutral_loss']
            tmp_cc = root_ion_info['cc basis'].copy()
            for element, count in neulo['cc'].items():
                tmp_cc[ element ] += count
            mass = cc_factory._mass( cc=tmp_cc )
            mz = mass / charge + pyqms.knowledge_base.PROTON
            final_ion_name = ION_NAME.format( **ion_info_template ).strip()
            ions[ root_ion_info['type'] ][ final_ion_name ] = {
                'name'  : final_ion_name,
                'mz'    : mz,
                'cc'    : cc_factory.hill_notation( cc=tmp_cc ),
                'pyqms' : cc_factory.hill_notation_unimod( cc=tmp_cc ),
                'type'  : root_ion_info['type'],
                'pos'   : int(root_ion_info['pos']),
                'nl'    : neulo['neutral_loss'],
                'charge': charge
            }
    return ions


def induce_fragmentation( peptide, charges=None ):
    '''
    Creates fragmentation dictionary
    '''
    cc_factory = pyqms.ChemicalComposition()
    cc_factory.use( peptide )
    # defaults
    ADD_WATER    = {'neutral_loss' : '+H2O', 'cc' : {'H':  2, 'O':  1}}
    SUB_WATER    = {'neutral_loss' : '-H2O', 'cc' : {'H': -2, 'O': -1}}
    SUB_AMMONIAK = {'neutral_loss' : '-NH3', 'cc' : {'H': -3, 'N': -1}}
    ions         = {}
    # b ion (and like storage)
    b_mods       = []  # accumulated mods
    b_ccs        = ddict(int)  # accumulated ccs
    b_mass       = cc_factory._mass( cc = b_ccs )
    b_neulo      = []
    # y ion (and like storage)
    y_mods       = []  # accumulated mods
    y_ccs        = ddict(int)
    y_ccs['O']   = 1
    y_ccs['H']   = 2
    y_mass       = cc_factory._mass( cc = y_ccs )
    y_neulo      = []

    # pairs = {}
    for pos, aa in enumerate( cc_factory.peptide ):
        # aa_cc = cc_factory.composition_of_aa_at_pos.get( pos + 1, None)
        # mod_cc = cc_factory.composition_of_mod_at_pos.get( pos + 1, None)
        # cc = cc_factory.composition_at_pos.get( pos + 1 , None)
        # unimod = cc_factory.unimod_at_pos.get( pos + 1 , None)
        # print( pos+1, aa, aa_cc, cc, unimod )
        b_pos = pos + 1
        b_aa = aa
        tmp_pairs_b = {}
        tmp_pairs_y = {}
        if b_aa in 'KHR':
            b_neulo.append( ADD_WATER )
        if b_aa in 'NQKR':
            b_neulo.append( SUB_AMMONIAK )
        if b_aa in 'STDE':
            b_neulo.append( SUB_WATER )
        if b_pos != len(cc_factory.peptide):
            # print( '''>>>>''', b_pos)
            b_cc = cc_factory.composition_at_pos[ b_pos ]
            for element, count in b_cc.items():
                b_ccs[ element ] += count
            b_mass += cc_factory._mass( cc=b_cc )
            b_unimod = cc_factory.unimod_at_pos.get( b_pos, None )
            if b_unimod is not None:
                b_mods.append( b_unimod )
            root_ion_info = {
                'type': 'b',
                'pos': b_pos,
                'mass' : b_mass,
                'modifications' : b_mods[:],
                'cc basis' : b_ccs.copy(),
                'neutral losses': b_neulo[:],
                'aa': b_aa,
            }
            if b_pos != 1:
                ions = update_ions(
                    ions = ions,
                    root_ion_info = root_ion_info,
                    charges = charges,
                    cc_factory = cc_factory
                )
                tmp_pairs_b = update_ions(
                    ions = tmp_pairs_b,
                    root_ion_info = root_ion_info,
                    charges = charges,
                    cc_factory = cc_factory
                )
            # a -ions
            root_ion_info['type'] = 'a'
            root_ion_info['cc basis']['O'] -= 1
            root_ion_info['cc basis']['C'] -= 1
            ions = update_ions(
                ions = ions,
                root_ion_info = root_ion_info,
                charges = charges,
                cc_factory = cc_factory
            )

        y_pos = len( cc_factory.peptide ) - pos
        y_aa = cc_factory.peptide[ y_pos - 1 ]
        if y_aa in 'NQKR':
            y_neulo.append( SUB_AMMONIAK )
        if y_aa in 'STDE':
            y_neulo.append( SUB_WATER )

        y_cc = cc_factory.composition_at_pos[ y_pos  ]
        # position in cc is starting at 1
        for element, count in y_cc.items():
            y_ccs[ element ] += count
        y_mass += cc_factory._mass( cc=y_cc )
        y_unimod = cc_factory.unimod_at_pos.get( y_pos , None )
        if y_unimod is not None:
            y_mods.append( y_unimod )
        root_ion_info = {
            'type': 'y',
            'pos': b_pos,  # the naming is backwards
            'mass' : y_mass,
            'modifications' : y_mods[:],
            'cc basis' : y_ccs.copy(),
            'neutral losses': y_neulo[:],
            'aa': y_aa
        }
        if y_pos == 1:
            root_ion_info['type'] = 'MH'
            root_ion_info['pos'] = 0
            root_ion_info['aa'] = peptide
        else:
            tmp_pairs_y = update_ions(
                ions = tmp_pairs_y,
                root_ion_info = root_ion_info,
                charges = charges,
                cc_factory = cc_factory
            )
        ions = update_ions(
            ions = ions,
            root_ion_info = root_ion_info,
            charges = charges,
            cc_factory = cc_factory
        )
        if 'pairs' not in ions.keys():
            ions['pairs'] = {}
        if b_pos not in ions['pairs'].keys():
            ions['pairs'][ b_pos ] = {}
        if y_pos - 1 not in ions['pairs'].keys():
            ions['pairs'][ y_pos - 1 ] = {}

        ions['pairs'][ b_pos ]['b'] = tmp_pairs_b.copy()
        ions['pairs'][ y_pos - 1  ]['y'] = tmp_pairs_y.copy()
    return ions


if __name__ == '__main__':
    # the_all_new_pf('AMQAK#Oxidation:2')
    if len(sys.argv) == 1:
        peptide = 'LVQFHFHWGSSDDQGSEHTVDR'
        print(__doc__)
    else:
        peptide = sys.argv[1]
    ions = induce_fragmentation(
        peptide,
        charges=[1, 2, 3]
    )
    pprint.pprint( ions )

