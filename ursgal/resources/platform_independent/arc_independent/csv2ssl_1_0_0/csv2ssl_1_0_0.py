#!/usr/bin/env python
'''
Convert unified .csv files to .ssl files.

Resulting .ssl files can be used as input for BiblioSpec

usage:
    ./csv2ssl_1_0_0.py <input_file> <output_file> <score_column_name> <score_type>

'''

import sys
import os
import csv
import ursgal
import re

if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


def main(
    input_file=None,
    output_file=None,
    score_column_name=None,
    score_type=None
):
    '''
    Convert csvs to ssl
    '''

    umama = ursgal.UnimodMapper()

    csv_kwargs = {}
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'

    output_file_object = open(output_file,'w')
    new_fieldnames = [
        'file',
        'scan',
        'charge',
        'sequence',
        'score-type',
        'score',
        'retention-time'
    ]

    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader( in_file )
        csv_output = csv.DictWriter(
            output_file_object,
            new_fieldnames,
            delimiter='\t',
            **csv_kwargs
        )
        csv_output.writeheader()

        for csv_line_dict in csv_input:
            rt = round(float(csv_line_dict['Retention Time (s)'])/60, 10)
            sequence = csv_line_dict['Sequence']
            mods = csv_line_dict['Modifications'].split(';')

            pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )
            pos2mass = {}
            for mod in mods:
                if mod == '':
                    continue
                if ':' not in mod:
                    sys.exit('This unimod: {0} requires positional information'.format( mod ))
                for occ, match in enumerate( pattern.finditer( mod )):
                    try:
                        unimod_mass = umama.name2mass(
                            mod[ :match.start() ]
                        )
                    except:
                        sys.exit(
                            'Can not map unimod {0}. extracted position argument: {1}'.format(
                                mod, match.start()
                        ))
                    position = int(match.group('pos'))
                    if position == 0:
                        position = 1
                    elif position > len(sequence):
                        position = len(sequence)
                    if position not in pos2mass:
                        pos2mass[position] = 0
                    pos2mass[ position ] += unimod_mass
                    if occ >= 1:
                        sys.exit(
                        'Incorrect regex pattern for mod: {0}'.format(
                            mod
                         ))

            seq_incl_mods = ''
            for p, aa in enumerate(sequence):
                seq_incl_mods += aa
                if p+1 in pos2mass:
                    mass = pos2mass[p+1]
                    if mass >= 0:
                        seq_incl_mods += '[+{0}]'.format(mass)
                    else:
                        seq_incl_mods += '[{0}]'.format(mass)

            ssl_line_dict = {}
            ssl_line_dict['file'] = csv_line_dict['Raw data location']
            ssl_line_dict['scan'] = csv_line_dict['Spectrum ID']
            ssl_line_dict['charge'] = csv_line_dict['Charge']
            ssl_line_dict['sequence'] = seq_incl_mods
            ssl_line_dict['score-type'] = score_type
            ssl_line_dict['score'] = csv_line_dict[score_column_name]
            ssl_line_dict['retention-time'] = rt

            csv_output.writerow( ssl_line_dict )

    output_file_object.close()
    in_file.close()
    return output_file

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    if sys.argv[3] == 'None':
        output_file_unfiltered = None
    else:
        output_file_unfiltered = sys.argv[3]


    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        score_column_name = sys.argv[3],
        score_type    = sys.argv[4],
    )
