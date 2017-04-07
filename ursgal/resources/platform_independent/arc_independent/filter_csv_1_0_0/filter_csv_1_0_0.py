#!/usr/bin/env python3.4
'''
Filters the result csvs

usage:
    ./filter_csv_1_0_0.py <input_file> <output_file>


'''

from __future__ import print_function
import sys
import os
import csv
import ursgal
import re

if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


def main( input_file=None, output_file=None, filter_rules=None, output_file_unfiltered = None):
    '''
    Filters csvs
    '''
    if filter_rules is None:
        print('No filter rules defined! Exiting now...')
        exit()
    elif len(filter_rules) == 0:
        print('No filter rules defined! Exiting now...')
        exit()
    else:
        pass

    csv_kwargs = {}
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'

    output_file_object = open(output_file,'w')

    if output_file_unfiltered is not None:
        unfiltered_output_file_object = open(
            output_file_unfiltered,
            'w'
        )

    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader( in_file )
        csv_output = csv.DictWriter(
            output_file_object,
            list(csv_input.fieldnames),
            **csv_kwargs
        )
        csv_output.writeheader()
        if output_file_unfiltered is not None:
            unfiltered_csv_output = csv.DictWriter(
                unfiltered_output_file_object,
                list(csv_input.fieldnames),
                **csv_kwargs
            )
            unfiltered_csv_output.writeheader()
        for line_dict in csv_input:

            write_row_bools = set()
            for rule_tuple in filter_rules:
                dict_key, rule, value = rule_tuple
                if dict_key not in line_dict.keys():
                    print(
                        '''Rule not recognized: {0}
                        Cause: Specified key not in csv fieldnames
                        Did you misspell the fieldname?'''.format(
                            rule_tuple
                        )
                    )
                    pass
                else:
                    if rule == 'lte':

                        if line_dict[dict_key] == '':
                            continue

                        if float(line_dict[dict_key]) <= value:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'gte':
                        # print(line_dict)
                        if float(line_dict[dict_key]) >= value:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'lt':
                        if float(line_dict[dict_key]) < value:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'gt':
                        if float(line_dict[dict_key]) > value:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'equals':
                        if line_dict[dict_key] == value:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)
                    elif rule == 'equals_not':
                        if line_dict[dict_key] != value:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'contains':
                        if value in line_dict[dict_key]:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)
                    elif rule == 'contains_not':
                        if value not in line_dict[dict_key]:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)
                    elif rule =='regex':
                        if re.search(value, line_dict[dict_key]) is not None:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)
                    elif rule == 'contains_glycosite':
                        if re.search(value, line_dict[dict_key]) is not None:
                            write_row_bools.add(True)
                        elif line_dict[dict_key][-2] == 'N' and line_dict[dict_key][-1] != 'P':
                            if 'S' in line_dict['Sequence Post AA'] or 'T' in line_dict['Sequence Post AA']:
                                write_row_bools.add(True)
                            else:
                                write_row_bools.add(False)
                        else:
                            write_row_bools.add(False)
                    elif rule == 'mod_at_glycosite':
                        mods =  line_dict[dict_key].split(';')
                        accepted = False
                        for mod in mods:
                            if value in mod:
                                pos = int(mod.split(':')[-1])
                                if line_dict['Sequence'][pos-1] != 'N':
                                    continue
                                if line_dict['Sequence'][pos] == 'P':
                                    continue
                                if pos >= len(line_dict['Sequence'])-2:
                                    if 'S' not in line_dict['Sequence Post AA'] and 'T' not in line_dict['Sequence Post AA']:
                                        continue
                                else:
                                    if line_dict['Sequence'][pos+1] not in ['S', 'T']:
                                        continue
                                accepted = True
                            else:
                                continue
                        if accepted == True:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)
                    else:
                        print('Rule: {0} not defined'.format(rule))

            if len(write_row_bools) == 1 and list(write_row_bools)[0] == True:
                csv_output.writerow( line_dict )
            elif output_file_unfiltered is not None:
                unfiltered_csv_output.writerow( line_dict )
            # break
    output_file_object.close()
    in_file.close()
    return output_file


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        exit()

    if sys.argv[3] == 'None':
        output_file_unfiltered = None
    else:
        output_file_unfiltered = sys.argv[3]


    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        filter_rules   =[
            # ('PEP','lte',0.01),
            ('Is decoy','equals_not','true'),
            # ('Sequence','contains','T'),
            # ('Sequence','contains','S'),
            # ('Sequence','contains','R'),

        ],
        output_file_unfiltered = output_file_unfiltered
    )
