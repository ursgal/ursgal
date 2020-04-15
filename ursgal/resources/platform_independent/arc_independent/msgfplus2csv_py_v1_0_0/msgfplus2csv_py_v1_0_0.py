#!/usr/bin/env python
import gzip
import xml.etree.ElementTree as ElementTree
import csv
import os
import sys


def main(mzid_file, csv_file):
    """Convert msgfplus mzid file to csv.

    Args:
        mzid_file (str): file path to input mzid
        csv_file (str): file path to output csv

    Raises:
        Exception: Description
    """
    if mzid_file.endswith('.gz'):
        open_func = gzip.open
    else:
        open_func = open

    headers = [
        'Raw data location',
        'Spectrum ID',
        'Spectrum Title',
        'Exp m/z',
        'Charge',
        'Sequence',
        'proteinacc_start_stop_pre_post_;',
        'MS-GF:DeNovoScore',
        'MS-GF:RawScore',
        'MS-GF:SpecEValue',
        'MS-GF:EValue',
        'Modifications',
        'Retention Time (s)',
        'Start',
        'Stop',
        'Calc m/z',
        'Is decoy',
        'rank'
    ]
    pep_lookup = {}
    with open_func(mzid_file) as fin, open(csv_file, 'wt') as fout:
        csv_writer = csv.DictWriter(fout, fieldnames=headers)
        csv_writer.writeheader()
        tree = ElementTree.iterparse(fin, events=('end', 'start'))
        for event, element in tree:
            if element.tag.endswith('}Inputs') and event == 'end':
                for e in element:
                    if e.attrib.get('id') == 'SID_1':
                        input_filepath = e.attrib['location']
                        input_filename = e.attrib['name']
            if element.tag.endswith('}Peptide') and event == 'end':
                key = element.attrib['id']
                if key not in pep_lookup:
                    pep_lookup[key] = {}
                    pep_lookup[key]['mods'] = []
                else:
                    raise Exception('Duplicate key {key}'.format(key=key))

                for e in element:
                    if e.tag.endswith('}PeptideSequence'):
                        seq = e.text
                        pep_lookup[key]['sequence'] = seq
                    elif e.tag.endswith('}Modification'):
                        pos = e.attrib['location']
                        delta = e.attrib['monoisotopicMassDelta']
                        for mod_e in e:
                            new = {}
                            new['pos'] = pos
                            new['delta'] = delta
                            new['name'] = mod_e.attrib['name']
                            pep_lookup[key]['mods'].append(new)

            if element.tag.endswith('}SpectrumIdentificationResult') and event == 'end':
                for ele in element[::-1]:
                    if ele.attrib.get('name', None) == 'spectrum title':
                        spec_title = ele.attrib['value']
                        spec_id = spec_title.split('.')[1]
                    elif ele.tag.endswith('}SpectrumIdentificationItem'):
                        attrib = ele.attrib
                        ref = attrib['peptide_ref']

                        peptide_data = pep_lookup[ref]

                        mods = []
                        for m in peptide_data['mods']:
                            pos  = m['pos']
                            delta = m['delta']
                            string = '{delta}:{pos}'.format(
                                delta=delta,
                                pos=pos
                            )
                            mods.append(string)

                        mods = ';'.join(mods)
                        input_filename_stem, ext = os.path.splitext(
                            input_filename
                        )
                        charge = attrib['chargeState']
                        new_psm = {
                            'Spectrum ID'      : spec_id,
                            'Spectrum Title'   : spec_title,
                            'Exp m/z'          : attrib['experimentalMassToCharge'],
                            'Charge'           : charge,
                            'Raw data location': input_filepath,
                            'Sequence'         : peptide_data['sequence'],
                            'rank'             : attrib['rank'],
                            'Modifications'    : mods,
                        }

                        for e in ele:
                            name = e.attrib.get('name', None)
                            if name in headers:
                                new_psm[name] = e.attrib['value']
                        csv_writer.writerow(new_psm)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
