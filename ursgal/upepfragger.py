#!/usr/bin/env python3
from collections import defaultdict as ddict
import copy

import pandas as pd
import numpy as np

import ursgal
from pyqms.chemical_composition import ChemicalComposition


class UPeptideFragmentor:
    def __init__(self, upep, charges=None, neutral_losses=None, ions=None):
        """Fragment peptide and store data frame in self.df for a given peptide.

        Args:
            upep (str): Peptide with optional Unimod modification string in the
                format PEPTIDE#<UNIMOD_NAME>:<POS>;<UNIMOD_NAME>:<POS> ...
            charges (list, optional): Charges for frag ion creation, default
                is 1, 2, 3
            neutral_losses (list, optional): Additional neutral losses to be considered
                has to have the following  format::
                    {
                        'H' : [
                            {
                                'name': '+H2O',
                                'cc': {'H': +2, 'O': +1},
                                'available_in_series': ['b']
                            },
                            {}
                        ],  ...
                    }
                See ursagl.ukb for more examples ...
            ions (list of str): Which ions shall be calculated, available options are
                ['a', 'b', 'c', 'I', 'x', 'y', 'z']
        """
        if charges is None:
            self.charges = [1, 2, 3]
        else:
            self.charges = charges
        if neutral_losses is None:
            neutral_losses = ursgal.ukb.neutral_losses
        else:
            neutral_losses += ursgal.ukb.neutral_losses
        self.neutral_losses = neutral_losses

        if ions is None:
            ions = ['a', 'b', 'y']

        self.upep_cc = ChemicalComposition(upep)
        self.upep = upep
        split = self.upep.split('#')
        self.peptide = split[0]

        self.mods = []
        if len(split) == 2:
            self.mods = split[1].split(';')

        self.fragment_starts_forward = {
                'a': {
                    'cc': {'C': -1, 'O': -1},
                    'name_format_string' : 'a{pos}',
                    'html_format_string' : 'a<sub>{pos}</sub>{modstring}<sup>{charge}+</sup>'
                },
                'b': {
                    'cc': {},
                    'name_format_string' : 'b{pos}',
                    'html_format_string' : 'a<sub>{pos}</sub>{modstring}<sup>{charge}+</sup>'
                },
                'c': {
                    'cc': {'N': +1, 'H': +3},
                    'name_format_string' : 'c{pos}',
                    'html_format_string' : 'a<sub>{pos}</sub>{modstring}<sup>{charge}+</sup>'
                },
                # 'c(-1)': {
                #     'cc': {'N': +1, 'H': +2},
                #     'name_format_string' : 'c(-1){pos}'
                # },
                # 'c(+1)': {
                #     'cc': {'N': +1, 'H': +4},
                #     'name_format_string' : 'c(+1){pos}'
                # },
                # 'c(+2)': {
                #     'cc': {'N': +1, 'H': +5},
                #     'name_format_string' : 'c(+2){pos}'
                # },
        }
        self.fragment_starts_reverse = {
                'x': {
                    'cc': {'O': 2, 'C': 1},
                    'name_format_string' : 'x{pos}',
                    'html_format_string' : 'x<sub>{pos}</sub>{modstring}<sup>{charge}+</sup>'
                },
                'y': {
                    'cc': {'H': 2, 'O': 1},
                    'name_format_string' : 'y{pos}',
                    'html_format_string' : 'y<sub>{pos}</sub>{modstring}<sup>{charge}+</sup>'
                },
                'Y': {
                    'cc': {'H': 0, 'O': 1},
                    'name_format_string' : 'Y{pos}',
                    'html_format_string' : 'Y<sub>{pos}</sub>{modstring}<sup>{charge}+</sup>'
                },
                'z': {
                    'cc': {'O': 1, 'N': -1, 'H': 0},
                    'name_format_string' : 'z{pos}',
                    'html_format_string' : 'z<sub>{pos}</sub>{modstring}<sup>{charge}+</sup>'
                },
                # 'z(+1)': {
                #     'cc': {'O': 1, 'N': -1, 'H': 1},
                #     'name_format_string' : 'z(+1){pos}'
                # },
                # 'z(+2)': {
                #     'cc': {'O': 1, 'N': -1, 'H': 2},
                #     'name_format_string' : 'z(+2){pos}'
                # },
                # 'z(+3)': {
                #     'cc': {'O': 1, 'N': -1, 'H': 3},
                #     'name_format_string' : 'z(+3){pos}'
                # },
        }
        abc_ions = self._fragfest(
            forward=True,
            start_dict={
                k : v for k, v in self.fragment_starts_forward.items() if k in ions
            }
        )
        xyz_ions = self._fragfest(
            forward=False,
            start_dict={
                k : v for k, v in self.fragment_starts_reverse.items() if k in ions
            }
        )
        ions = [abc_ions, xyz_ions]

        if 'I' in ions:
            # Internal fragments
            # internal_frags = {}
            for i in range(1, len(self.peptide)):
                ions.append(
                    self._fragfest(
                        start_dict={
                            'I(b)' : {
                                'cc': {},
                                'name_format_string': 'Internal({seq})',
                                'html_format_string': 'Internal({seq})'

                            },
                            'I(a)' : {
                                'cc': {'C': -1, 'O': -1},
                                'name_format_string': 'I-28({seq})',
                                'html_format_string': 'I-28({seq})'
                            }

                        },
                        start_pos=i,
                    )
                )

        all_rows = []
        for pos_dict in ions:
            for pos in pos_dict.keys():
                for ion_type in pos_dict[pos].keys():
                    all_rows += pos_dict[pos][ion_type]

        # self.df = self._induce_fragmentation_of_ion_ladder()
        self.df = pd.DataFrame(all_rows).sort_values(by='mz').reset_index()
        self.df.drop(columns=['html_format_string', 'name_format_string'], inplace=True)

    def _init_pos0(self, start_dict):
        r = {'pos0' : {}}
        for ion_type in start_dict.keys():
            r['pos0'][ion_type] = \
                [{
                    'pos': 0,
                    'cc': ChemicalComposition(),
                    'mods': [],
                    'name_format_string': start_dict[ion_type]['name_format_string'],
                    'html_format_string': start_dict[ion_type]['html_format_string'],
                    'seq': ''
                }]
            r['pos0'][ion_type][0]['cc'] += start_dict[ion_type]['cc']
        return r

    def _fragfest(self, forward=True, start_dict=None, start_pos=None, end_pos=None, delete_pos0=True):
        """
        kwargs:

            start_pos (int) Python index position where fragmentation should start
                0 is first AA!
        """
        # print(f'Fragging {start_pos} {end_pos}')
        if start_pos is None:
            start_pos = 0
        if end_pos is None:
            end_pos = len(self.peptide)

        pos_dict = self._init_pos0(start_dict)
        alread_seen_frags = set()
        for i in range(start_pos, end_pos):
            dpos = i - start_pos
            if forward:
                translated_peptide_pos = i + 1
                # Since chemical composition has modification on N-Term, which is 0
                aa= self.peptide[i]
            else:
                translated_peptide_pos = len(self.peptide) - i
                aa = self.peptide[::-1][i]

            cc = self.upep_cc.composition_at_pos[translated_peptide_pos]
            pos_dict['pos{0}'.format(dpos + 1)] = ddict(list)
            for neutral_loss_dict in self.neutral_losses.get(aa, [{}]):
                neutral_loss_can_occure = False
                required_unimods = neutral_loss_dict.get('requires_unimod', None)

                if required_unimods is None:
                    neutral_loss_can_occure = True
                else:
                    uni_mod_at_pos = self.upep_cc.unimod_at_pos.get(
                        translated_peptide_pos, ''
                    )
                    for required_unimod in required_unimods:
                        if required_unimod == uni_mod_at_pos:
                            neutral_loss_can_occure = True

                if neutral_loss_can_occure is False:
                    continue

                nl_limited_to_specific_ion_series = False
                available_in_series = neutral_loss_dict.get('available_in_series', None)
                if available_in_series is not None:
                    nl_limited_to_specific_ion_series = True


                is_series_specific = neutral_loss_dict.get(aa,)
                for ion_type, ion_fragments in pos_dict['pos{0}'.format(dpos)].items():
                    if nl_limited_to_specific_ion_series:
                        if ion_type not in available_in_series:
                            continue
                    for charge in self.charges:
                        for ion_frag in ion_fragments:
                            new_ion_frag = copy.deepcopy(ion_frag)
                            new_ion_frag['pos'] += 1
                            new_ion_frag['cc'] += cc
                            new_ion_frag['cc'] += neutral_loss_dict.get('cc', {})
                            mod = neutral_loss_dict.get('name', None)
                            if mod is not None:
                                new_ion_frag['mods'].append(mod)
                            new_ion_frag['hill'] = new_ion_frag['cc'].hill_notation_unimod()
                            new_ion_frag['charge'] = charge
                            new_ion_frag['predicted_intensity'] = np.NAN
                            new_ion_frag['mass'] = new_ion_frag['cc']._mass()
                            new_ion_frag['mz'] = new_ion_frag['mass'] / charge + ursgal.ukb.PROTON
                            new_ion_frag['series'] = ion_type
                            new_ion_frag['modstring'] = ','.join(sorted(new_ion_frag['mods']))
                            new_ion_frag['seq'] += aa
                            new_ion_frag['name'] = new_ion_frag['name_format_string'].format(**new_ion_frag)
                            new_ion_frag['html_name'] = new_ion_frag['html_format_string'].format(**new_ion_frag)
                            _id = '{name}{modstring}{charge}'.format(**new_ion_frag)
                            if _id not in alread_seen_frags:
                                pos_dict['pos{0}'.format(dpos+1)][ion_type].append(new_ion_frag)
                            alread_seen_frags.add(_id)
        if delete_pos0:
            del pos_dict['pos0']

        return pos_dict



if __name__ == '__main__':
    mains()
