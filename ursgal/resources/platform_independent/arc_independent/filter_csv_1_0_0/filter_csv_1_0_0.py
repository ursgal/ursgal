#!/usr/bin/env python
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
import operator

if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


def main( input_file=None, output_file=None, filter_rules=None, output_file_unfiltered = None):
    '''
    Filters csvs
    '''
    if filter_rules is None:
        print('No filter rules defined! Exiting now...')
        sys.exit(1)
    elif len(filter_rules) == 0:
        print('No filter rules defined! Exiting now...')
        sys.exit(1)
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
        for line_pos, line_dict in enumerate(csv_input):
            write_row_bools = set()
            for rule_tuple in filter_rules:
                dict_key, rule, value = rule_tuple
                if dict_key not in line_dict.keys():
                    print(
                        '''Rule not recognized: {0}
Input file: {1}
headers : {2}
Cause: Specified key not in csv fieldnames
Did you misspell the field name?'''.format(
                            rule_tuple,
                            input_file,
                            csv_input.fieldnames,

                        )
                    )
                    raise Exception
                else:
                    if rule in ['lte', 'gte', 'lt' , 'gt']:
                        # requires not None! and to be floatable
                        if line_dict[ dict_key ] is None:
                            write_row_bools.add(False)

                        elif rule == 'lte':
                            cpm_method = operator.__le__
                        elif rule == 'gte':
                            cpm_method = operator.__ge__
                        elif rule == 'lt':
                            cpm_method = operator.__lt__
                        elif rule == 'gt':
                            cpm_method = operator.__gt__

                        try:
                            floated_value = float(line_dict[dict_key])
                        except:
                            if line_dict[ dict_key ] is '':
                                floated_value = None
                            else:
                                print('[ ERROR ] Value to be filtered could not be converted to float')
                                print('Value:'+line_dict[dict_key])
                                sys.exit(1)
                                
                        if floated_value is None:
                            write_row_bools.add(False)
                        elif cpm_method( floated_value, value):
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'equals':
                        if value == line_dict[dict_key]:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'equals_not':
                        if value != line_dict[dict_key]:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'contains':
                        if value in line_dict[dict_key]:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'contains_not':
                        if line_dict[dict_key] is None:
                            write_row_bools.add(True)
                        elif value not in line_dict[dict_key]:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'regex':
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
                        if accepted is True:
                            write_row_bools.add(True)
                        else:
                            write_row_bools.add(False)

                    elif rule == 'contains_element_of_list':
                        assert type(value) == list, '''
                        The value for the filter rule 'contains_element_of_list'
                        needs to be a list. You specified:
                        {0}
                        '''.format(value)
                        write = False
                        for element in value:
                            if element in line_dict[dict_key]:
                                write = True
                        write_row_bools.add(write)

                    else:
                        print('Rule: {0} not defined'.format(rule))
                        raise Exception

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
        sys.exit(1)

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
