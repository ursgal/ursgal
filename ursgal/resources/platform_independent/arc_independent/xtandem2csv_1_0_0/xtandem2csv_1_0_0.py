#!/usr/bin/env python
"""
Converts xTandem.xml files into .csv
We need to do this on our own, because mzidentml_lib
reports wrong positions for modifications
(and it is also not able to convert the piledriver.mzid into csv)

It should be noted that
- xtandem groups are not merged (since it is not the same as protein groups)
- multiple domains (multiple occurence of a peptide in the same protein) are not reported

(C)
Christian Fufezan
Stefan Schulze
"""
from __future__ import print_function
import sys, os
import csv
import math
from xml.etree import cElementTree
from collections import defaultdict as ddict
import codecs

if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)

def main(input_file = None, decoy_tag = None, output_file = None):
    '''
    Converts xTandem.xml files into .csv
    We need to do this on our own, because mzidentml_lib
    reports wrong positions for modifications
    (and it is also not able to convert the piledriver.mzid into csv)

    It should be noted that
    - xtandem groups are not merged (since it is not the same as protein groups)
    - multiple domains (multiple occurence of a peptide in the same protein) are not reported

    '''
    NEW_HEADERS = [
        'Raw data location',
        'Spectrum ID',
        'Spectrum Title',
        'Retention Time (s)',
        'Rank',
        'Calc m/z',
        'Exp m/z',
        'Charge',
        'Sequence',
        'Modifications',
        'X\!Tandem:expect',
        'X\!Tandem:hyperscore',
        'proteinacc_start_stop_pre_post_;',
        'Is decoy',
    ]
    PROTON = 1.00727646677
    protein = None
    group = None
    group_counter = 0
    protein_groups = []

    if input_file.endswith('.gz'):
        compressed = True
        # Gzipped files are not seekable
        import gzip
        # file_object = codecs.getreader("utf-8")(
        #     gzip.open(path)
        # )
        file_object = codecs.getreader("utf-8")(
            gzip.open(input_file)
        )
    else:
        file_object = codecs.open(
            input_file,
            mode     = 'r',
            encoding = 'utf-8'
        )

    csvOut     = csv.DictWriter( open( output_file , 'w', newline='') , NEW_HEADERS )
    csvOut.writeheader()

    print("Converting XTandem XML into CSV: {0}".format(input_file))
    tandemXML = iter(cElementTree.iterparse( file_object, events = ( b'start',b'end')))

    for pos, (event, element) in enumerate(tandemXML):
        if event == b'start':
            if element.tag.endswith('bioml'):
                raw_data_location = element.attrib['label'].split("'")[1]
            if element.tag.endswith('group'):
                if 'mh' in element.attrib.keys():
                    group_counter = 0
                    notes                         = ddict(set)
                    notes_key                     = None
                    group                         = {} # reset group
                    group['Raw data location']    = raw_data_location
                    group['Charge']               = element.attrib['z']
                    group['Exp m/z']              = (float(element.attrib['mh'])/float(group['Charge'])) + PROTON
                    group['X\!Tandem:expect']     = element.attrib['expect']
                    protein_groups             = []
                    domain_groups             = []
                if element.attrib['label'] == 'fragment ion mass spectrum':
                    notes_key = 'spectrum'
                if element.attrib['label'] == 'input parameters':
                    notes_key = 'parameters'
                group_counter += 1

            elif element.tag.endswith('protein'):
                protein = {} # reset protein
                notes_key = 'protein'


            elif element.tag.endswith('domain'):
                if 'seq' in element.attrib.keys():
                    domain = { header: '' for header in NEW_HEADERS } # reset domain
                    domain['Sequence']              = element.attrib['seq']
                    domain['X\!Tandem:hyperscore']  = element.attrib['hyperscore']
                    domain['Calc m/z'] = (float(element.attrib['mh'])/float(group['Charge'])) + PROTON
                    protein['Start']      = element.attrib['start']
                    protein['Stop']       = element.attrib['end']
                    protein['pre']        = element.attrib['pre'][-1]
                    protein['post']       = element.attrib['post'][0]
                    if protein['Start'] == '1':
                        protein['pre'] = '-'
                    if protein['post'] == ']':
                        protein['post'] = '-'
                    domain['proteinacc_start_stop_pre_post_;'] = '{0}_{1}_{2}_{3}_{4};'.format(
                        protein['Defline'],
                        protein['Start'],
                        protein['Stop'],
                        protein['pre'],
                        protein['post'],
                    )
                    if protein['Defline'].startswith(decoy_tag):
                        domain['Is decoy'] = True
                    else:
                        domain['Is decoy'] = False
                    domain['Rank'] = 1

            elif element.tag.endswith('aa'):
                if 'modified' not in element.attrib.keys():
                    continue
                mod = '{0}:{1}'.format(element.attrib['modified'], int(element.attrib['at']) - int(protein['Start']) + 1)
                try:
                    domain['Modifications'].append( mod )
                except:
                    domain['Modifications'] =  [ mod ]
        else:
            if element.tag.endswith('protein'):
                protein_groups.append( protein )
            if element.tag.endswith('domain'):
                for k,v in domain.items():
                    if k not in protein.keys():
                        protein[k] = v
                # domain_groups.append( domain )
            elif element.tag.endswith('note'):
                if notes_key == 'spectrum':
                    group['Spectrum Title'] = element.text.strip()
                elif notes_key == 'protein':
                    protein['Defline'] = element.text.strip()
            elif element.tag.endswith('group'):
                group_counter -= 1
                if group_counter == 0:
                    dict2write = {}
                    # proteins = []
                    for protein_group in protein_groups:
                        for key in NEW_HEADERS:
                            # if key == 'proteinacc_start_stop_pre_post_;':
                            #     proteins.append(protein_group[key])
                            #     continue
                            if key == 'Modifications' and protein_group[key] !='':
                                dict2write[key] = ';'.join(protein_group[key])
                                continue
                            try:
                                dict2write[key] = group[key]
                            except:
                                dict2write[key] = protein_group[key]
                        # dict2write['proteinacc_start_stop_pre_post_;'] = ''.join(proteins)
                        csvOut.writerow( dict2write )
                    protein_groups = []
    return

if __name__ == '__main__':
    script = main(input_file = sys.argv[1], decoy_tag = sys.argv[2], output_file = sys.argv[3])
