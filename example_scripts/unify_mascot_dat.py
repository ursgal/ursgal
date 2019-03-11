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
import json

regexs_for_non_standard_mgfs = {
    'cz' : re.compile(r'''
        msmsid:F(?P<spec_id>[0-9]*),
        quan:(?P<quant>[0-9]*),
        start:(?P<rt_start_in_seconds>\d*\.\d+|\d+),
        end:(?P<rt_end_in_seconds>\d*\.\d+|\d+),
        survey:S(?P<survey>[0-9]*),
        parent:(?P<precursor_mz>\d*\.\d+|\d+),
    ''', re.VERBOSE)
}

def add_mascot_to_ursgal_history(file):
    """Add Mascot to history.

    Args:
        mapped_csv_search_results (str): Path to mapped search results.
    """
    mapped_json = '{0}.u.json'.format(file)
    iinfo, oinfo, params, history = json.load(open(mapped_json))
    mascot_missing = True
    for entry in history['history']:
        engine_type = entry['META_INFO'].get('engine_type', {})
        is_search_engine = engine_type.get('protein_database_search_engine', False)
        if is_search_engine and 'mascot' in entry['engine']:
            mascot_missing = False

    if mascot_missing:
        history['history'].insert(0,
            {
                "META_INFO": {
                  "engine_type": {
                    "protein_database_search_engine": True,
                    "by Hand" : True
                  }
                },
                "engine": "mascot_x_x_x"
          }
        )
        with open(mapped_json, "w") as d:
            json.dump([iinfo, oinfo, params, history], d)



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
            full_fname = f.split('=')[1]

            fname = os.path.splitext(os.path.basename(full_fname))[0]
            break
    dat_basename, ext = os.path.splitext(mascot_dat_base)

    if os.path.exists(pkl_path):
        t = pickle.load(open(pkl_path, 'rb'))
    else:
        t = {}
    if fname not in t:
        t.update(
            {
                fname : {
                    'rt_2_scan' : {},
                    'scan_2_rt' : {},
                    'unit'      : 'seconds',
                    'scan_2_mz' : {}
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
                    path, spec_id, spec_id, charge = title.split('.')
                except:
                    path = os.path.basename(fname)
                    unqstring = unquote(title)
                    charge = int(query_dict['charge'].replace('+',''))
                    for _id, pattern in regexs_for_non_standard_mgfs.items():
                        m = pattern.match(unqstring)
                        if m is not None:
                            spec_id = int(m.group('spec_id'))

                            query_dict['rtinseconds'] = float(m.group('rt_start_in_seconds'))
                            query_dict['precursor_mz'] = m.group('precursor_mz')
                            break

                rt    = query_dict['rtinseconds']
                t[fname]['rt_2_scan'][float(rt)] = int(spec_id)
                t[fname]['scan_2_rt'][int(spec_id)] = float(rt)
                t[fname]['scan_2_mz'][int(spec_id)] = float(query_dict['precursor_mz'])
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
    uc.params['csv_filter_rules'] = [
        ['Sequence', 'contains_not', 'X'],
        # ['PEP', 'lte', 0.01],
    ]
    uc.params['decoy_tag'] = '###REV###'
    uc.scan_rt_lookup_path = write_ursgal_pkl_from_mascot_dat(input_file)
    converted_unfiltered = uc.execute_unode(
        input_file,
        engine='mascot_dat2csv'
    )
    converted = uc.execute_misc_engine(
        input_file=converted_unfiltered,
        engine='filter_csv'
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
