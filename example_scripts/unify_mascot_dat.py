#!/usr/bin/env python
import pickle
import ursgal
import sys
import re
import os
from collections import defaultdict as ddict
from urllib.parse import unquote
import pprint
import re

regexs_for_crazy_mgfs = {
    'cz' : re.compile(r'''
        msmsid:F(?P<spec_id>[0-9]*),
        quan:(?P<quant>[0-9]*),
        start:(?P<rt_start_in_minutes>\d*\.\d+|\d+),
        end:(?P<rt_end_in_minutes>\d*\.\d+|\d+),
    ''', re.VERBOSE)
}

def add_mascot_to_ursgal_history(file):
    """Add Mascot to history.

    Args:
        mapped_csv_search_results (str): Path to mapped search results.
    """
    mapped_json = '{0}.u.json'.format(file)
    mascot_missing = True
    lines = []
    with open(mapped_json, 'r') as org:
        for line in org:
            if 'mascot_x_x_x' in line:
                mascot_missing = False
                break
            lines.append(line)

    if mascot_missing:
        print('MASCOT MISSING')
        print('INSERTING ...')
        with open(mapped_json, 'w') as new:
            for line in lines:
                if '"history": [' in line:
                    print('''
            "history": [
              {
                "META_INFO": {
                  "engine_type": {
                    "protein_database_search_engine": true,
                    "By Hand" : true
                  }
                },
                "engine": "mascot_x_x_x"
              },''', file = new)
                else:
                    print(line, end='', file = new)


def write_ursgal_pkl_from_mascot_dat(mascot_data_file):
    """
    Write ursgal pickle from mascot dat files

    Args:
        mascot_data_file (str): Path to mascot dat file for pickle generation.

    Returns:
        str: Path to the generated pickle file.
    """
    # rt_regex = re.compile(r'^.*rt\:(?P<rt>\d+\.\d+),.*')

    pattern = re.compile(r'Content-Type: application/x-Mascot; name="(?P<section>[a-z0-9]*)"')

    mascot_dat_base = os.path.basename(mascot_data_file)
    pkl_path = os.path.join(
        os.path.dirname(mascot_data_file),
        f'_ursgal_lookup.pkl'
    )

    sections = ddict(list)
    current_section = None
    with open(mascot_data_file) as mascot_file:
        for line in mascot_file:
            if line.strip() == '':
                continue
            match = pattern.match(line)
            if match is not None:
                current_section = match.group('section')
            else:
                sections[current_section].append(line.strip())

    for f in sections['parameters']:
        if f.startswith('FILE'):
            fname = f.split('=')[1]
            break
    dat_basename, ext = os.path.splitext(mascot_dat_base)
    if os.path.exists(pkl_path):
        t = pickle.load(open(pkl_path, 'rb'))
    else:
        t = {}
    if dat_basename not in t:
        t.update(
            {
                dat_basename : {
                    'rt_2_scan' : {},
                    'scan_2_rt' : {},
                    'unit'      : 'seconds',
                }
            }
        )

    query_dict = {}
    for entry in sections:
        if entry is not None:
            if entry.startswith('query'):
                for key in sections[entry]:
                    if '=' in key:
                        k, v = key.split('=')
                        query_dict[k] = v
                title = query_dict['title']
                try:
                    path, spec_id, spec_id, charge = title.replace('%2e', '.').split('.')
                except:
                    path = os.path.basename(fname)
                    unqstring = unquote(title)
                    charge = int(query_dict['charge'].replace('+',''))
                    for _id, pattern in regexs_for_crazy_mgfs.items():
                        m = pattern.match(unqstring)
                        if m is not None:
                            spec_id = int(m.group('spec_id'))
                            rtinminutes = m.group('rt_start_in_minutes')
                            query_dict['rtinseconds'] =  float(rtinminutes) / 60.
                            break

                rt    = query_dict['rtinseconds']
                t[dat_basename]['rt_2_scan'][float(rt)] = str(spec_id)
                t[dat_basename]['scan_2_rt'][str(spec_id)] = float(rt)
    with open(pkl_path, 'wb') as pkl:
        pickle.dump(t, pkl)
    return pkl_path


def main(input_file, database):
    """
    Usage:

    ./unify_mascot_dat.py <mascot dat file> <database>

    Note:
        Modifications are hard coded so please adjust accordingly
    """
    uc = ursgal.UController()
    uc.params['database'] = database
    uc.params['modifications'] = [
        'C,fix,any,Carbamidomethyl',
        '*,opt,Prot-N-term,Acetyl',
        'M,opt,any,Oxidation',
        '*,opt,N-term,TMT6plex',
        'K,fix,any,TMT6plex',
    ]
    uc.scan_rt_lookup_path = write_ursgal_pkl_from_mascot_dat(input_file)

    converted = uc.execute_unode(
        input_file,
        engine='mascot_dat2csv'
    )
    mapped = uc.map_peptides_to_fasta(
        converted
    )
    add_mascot_to_ursgal_history(mapped)
    unified = uc.unify_csv(mapped)
    print(unified)

if __name__ == '__main__':
    if len(sys.argv) !=3:
        print(main.__doc__)
    else:
        main(sys.argv[1], sys.argv[2])
