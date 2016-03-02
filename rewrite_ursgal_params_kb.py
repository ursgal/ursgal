#!/usr/bin/env python3.4
# encoding: utf-8

import csv
import sys

if __name__ == '__main__':
    print('''
        Rewriting params dict
''')
    output_file_name = sys.argv[1]

    from ursgal_params import ursgal_params as urgsal_dict

    output_file = open(output_file_name, 'w')
    print('ursgal_params={', file=output_file)
    for param in sorted(urgsal_dict.keys()):
        print('''    '{0}':{1}'''.format(param, '{'), file=output_file )
        for k, v in sorted(urgsal_dict[param].items()):
            if k == 'description':
                print('''        '{0}':'''.format(k), "'''", v.strip(), "''',", file=output_file)
                continue
            if type(v) == str:
                print('''        '{0}':"{1}",'''.format(k,v), file=output_file)
            elif type(v) == dict:
                print('''        '{0}':{1}'''.format(k, '{'), file=output_file)
                for k2, v2 in sorted(urgsal_dict[param][k].items()):
                    print('''            '{0}':'{1}','''.format(k2,v2), file=output_file)
                print('        },', file=output_file)
            elif type(v) == list:
                print('''        '{0}':{1}'''.format(k, '['), file=output_file)
                for elem in sorted(v):
                    print('''            '{0}','''.format(elem), file=output_file)
                print('        ],', file=output_file)
            else:
                print('''        '{0}':'{1}','''.format(k,v), file=output_file)
        print('    },', file=output_file)
    print('}', file=output_file)
    output_file.close()