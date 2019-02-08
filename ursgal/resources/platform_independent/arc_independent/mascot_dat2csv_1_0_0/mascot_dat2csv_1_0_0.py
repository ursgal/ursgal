#!/usr/bin/env python
import re
from collections import defaultdict as ddict
import csv
from urllib.parse import unquote
import os

pattern = re.compile(
    r'Content-Type: application/x-Mascot; name="(?P<section>[a-z0-9]*)"'
)
peptide_match_pattern = re.compile(
    r'''
    q(?P<query>[0-9]*)_
    p(?P<rank>[0-9]*)=
    (?P<missed_cleavages>[-+0-9]*),
    (?P<peptide_mass>[0-9\.]*),
    (?P<delta>[-0-9\.]*),
    (?P<number_of_ions_matched>[0-9]*),
    (?P<sequence>[A-Z]*),
    (?P<peaks_used_from_ions1>[0-9]*),
    (?P<var_mod_string>[0-9]*),
    (?P<score>[.0-9]*),
    (?P<ion_series_found>[0-9]*),
    ''',
    re.VERBOSE
)


regexs_for_crazy_mgfs = {
    'cz' : re.compile(r'''
        msmsid:F(?P<spec_id>[0-9]*),
        quan:(?P<quant>[0-9]*),
        start:(?P<rt_start_in_minutes>\d*\.\d+|\d+),
        end:(?P<rt_end_in_minutes>\d*\.\d+|\d+),
    ''', re.VERBOSE)
}

PROTON = 1.007276466


class MascotDatParser(object):

    def __init__(self, mascot_dat_file):
        """Parse idents from mascot dat file.

        Args:
            mascot_dat_file (str): Path to mascot dat file.
        """
        self.mascot_dat_file = mascot_dat_file
        self.search_file = self._get_search_file()
        self.section_dict = self._parse_mascot_sections(self.mascot_dat_file)
        self.mods         = self._parse_mods()
        self.peptide_dict = self._assemble_peptide_info(self.section_dict)
        self.peptides     = self._create_final_lookup(
            self.peptide_dict,
            self.section_dict
        )
        self._iter = self._iter_idents()

    def _get_search_file(self):
        with open(self.mascot_dat_file) as fin:
            for line in fin:
                if line.startswith('FILE='):
                    file = line.split('=')[1].strip()
                    break
        return file

    def _parse_mascot_sections(self, in_file):
        sections = ddict(list)
        current_section = None

        with open(in_file) as mascot_file:
            for line in mascot_file:
                if line.strip() == '':
                    continue
                match = pattern.match(line)
                if match is not None:
                    current_section = match.group('section')
                else:
                    sections[current_section].append(line.strip())
        return sections

    def _assemble_peptide_info(self, section_dict):
        pep_info = {}
        for line in section_dict['peptides']:
            if line.strip() == '':
                continue
            if line.startswith('--'):
                continue
            k, v = line.strip().split('=')
            k_splitted = k.split('_')
            if len(k_splitted) == 2:
                if v == '-1':
                    continue
                else:
                    m = peptide_match_pattern.match(line)
                    if m is None:
                        print(line)
                        print('????')
                        break
                    mdict = m.groupdict()
                    section_key = '_q{query}_p{rank}'.format(**mdict)
                    pep_info[section_key] = mdict
            else:
                if 'terms' in k:
                    continue
                elif '_primary_nl' in k:
                    q, p, primary, nl = k.split('_')
                    pep_info['_{0}_{1}'.format(q, p)]['primary_nl'] = v
                elif '_subst' in k:
                    q, p, subst = k.split('_')
                    if pep_info['_{0}_{1}'.format(q, p)].get(
                        'substitution',
                        None
                    ) is None:
                        pep_info['_{0}_{1}'.format(q, p)]['substitution'] = []
                    pep_info['_{0}_{1}'.format(q, p)]['substitution'].append(v)
                elif '_db'in k:
                    # merged database stuff
                    continue
                else:
                    raise Exception(
                        'Do not know what to do with this line'
                        '\n{line}'.format(line=line)
                    )
        return pep_info

    def _create_final_lookup(self, pep_info, section_info):
        global_params = {}
        peptides      = {}
        for pair in section_info['parameters']:
            k_v = pair.split('=')
            if len(k_v) == 2:
                k, v = k_v
                global_params[k] = v
        for query_with_rank in pep_info:
            info_dict = pep_info[query_with_rank]
            mods = self._format_mods(info_dict)

            query_dict = {}
            query = query_with_rank.strip('_q').split('_')[0]
            query_list = self.section_dict['query{0}'.format(query)]
            for q in query_list:
                k_v = q.split('=')
                if len(k_v) == 2:
                    k, v = k_v
                    query_dict[k] = v

            if query_dict['title'].startswith('msmsid'):
                # CZ Title
                unqstring = unquote(query_dict['title'])
                m = regexs_for_crazy_mgfs['cz'].match(unqstring)
                if m is not None:
                    spec_id = int(m.group('spec_id'))
                    rtinminutes = m.group('rt_start_in_minutes')
                    query_dict['retention_time'] =  float(rtinminutes) / 60.
                    charge = query_dict['charge'].replace("+","")
                    query_dict['title'] = '{0}.{1}.{1}.{2}'.format(
                        os.path.splitext(
                            os.path.basename(self.search_file)
                        )[0],
                        spec_id,
                        charge
                    )
                    query_dict['spectrum_id'] = spec_id
                else:
                    print('Do not understand title {title}'.format(**query_dict))
                    exit(1)
                # title_dict = self._format_cz_title(query_dict['title'])
                # spec_id    = int(title_dict['msmsid'].strip('F'))
                # query_dict['spectrum_id'] = spec_id
                # query_dict['retention_time'] = float(title_dict['peak_rt'])
                # # del query_dict['peak_rt']
            else:
                # TPP style (as used by msconvert)
                title_dict = {}
                spec_id    = int(query_dict['scans'])
                query_dict['spectrum_id'] = spec_id
                query_dict['retention_time'] = query_dict['rtinseconds']
                del query_dict['rtinseconds']

            query_dict.update(info_dict)
            query_dict['mods'] = mods
            if spec_id not in peptides:
                peptides[spec_id] = []
            peptides[spec_id].append(query_dict)
        return peptides

    def _parse_mods(self):
        mods = {
            'variable' : {},
            'fixed'    : {}
        }
        for entry in self.section_dict['masses']:
            if 'delta' in entry:
                delta, delta_entry = entry.strip().split('=')
                mods['variable'][delta.replace('delta', '')] = delta_entry
            if 'fixed' in entry.lower():
                delta, delta_entry = entry.strip().split('=')
        return mods

    def _format_mods(self, pepdict):
        mods = []
        subs = pepdict.get('substitution', None)
        for pos, mod in enumerate(pepdict['var_mod_string']):
            if mod == '0':
                continue
            if subs is not None:
                for entry in subs:
                    splitted_list = entry.split(',')
                    for i in range(0, len(splitted_list), 3):
                        sub_pos, old_aa, new_aa = splitted_list[i:i + 3]
                        if int(sub_pos) == pos:
                            mods.append('Subst({mod}):{pos}'.format(
                                mod=new_aa,
                                pos=int(sub_pos)
                            ))
            var_mod_string = self.mods['variable'].get(mod, None)

            if var_mod_string is not None:
                var_mass, var_mod = var_mod_string.split(',')
                var_mass = float(var_mass.strip())
                var_mod = var_mod.split(' ')[0]
                mods.append('{mod}:{pos}'.format(
                    mod=var_mod,
                    pos=pos
                ))

            fix_mod_string = self.mods['fixed'].get(mod, None)
            if fix_mod_string is not None:
                fix_mass, fix_mod = fix_mod_string.split(',')
                fix_mass = float(fix_mass.strip())
                fix_mod  = fix_mod.split(' ')[0]
                mods.append('{mod}:{pos}'.format(
                    mod=fix_mod,
                    pos=pos
                ))
        return mods

    def _format_cz_title(self, title):
        title_info = {}
        # under linux, we have hexadecimals
        # under windows, its unicode
        #
        entry_list = title.split('%2c')
        if len(entry_list) == 1:
            raise Exception(
                'reading mgf with CZ title under windows is not'
                'supported now due to strange hex strings'
                'Title string supplied: {title}'.format(title=title)
            )
        for e in entry_list:
            k_v = e.split('%3a')
            if len(k_v) == 2:
                k, v = k_v
                if '%2e' in v:
                    v = v.replace('%2e', '.')
                title_info[k] = v
        return title_info

    def __getitem__(self, spectrum_id):
        return self.peptides[spectrum_id]

    def _iter_idents(self):
        for key in self.peptides:
            yield self.peptides[key]

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)


def main(input_file, output_file):

    ursgal_headers = [
        'Raw data location', 'Spectrum ID', 'Spectrum Title',
        'Exp m/z', 'Charge', 'Sequence',
        'proteinacc_start_stop_pre_post_;',
        'Mascot:Score', 'Modifications', 'Retention Time (s)',
        'Start', 'Stop', 'Calc m/z',
        'Is decoy', 'rank'
    ]

    parser = MascotDatParser(input_file)
    with open(output_file, 'wt') as fout:
        csv_writer = csv.DictWriter(fout, fieldnames=ursgal_headers)
        csv_writer.writeheader()
        for spec_id in parser.peptides:
            for ident in parser.peptides[spec_id]:
                charge = int(ident['charge'].strip('+'))
                title = ident['title']
                if '%2e' in title:
                    # where do these hexs come from?
                    title = title.replace('%2e', '.')
                d = {
                    'Raw data location': parser.search_file,
                    'Spectrum Title': title,
                    'Spectrum ID': int(ident['spectrum_id']),
                    'Exp m/z': (float(ident['peptide_mass']) / charge) + PROTON,
                    'Charge': charge,
                    'Sequence': ident['sequence'],
                    'Mascot:Score': ident['score'],
                    'Modifications': ';'.join(ident['mods']),
                    'Retention Time (s)': ident['retention_time'],
                    'rank': ident['rank']
                }
                csv_writer.writerow(d)
