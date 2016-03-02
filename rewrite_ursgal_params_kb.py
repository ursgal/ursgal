#!/usr/bin/env python3.4
# encoding: utf-8

import csv
import sys
import json

if __name__ == '__main__':
    print('''
        Rewriting params dict
''')
    output_file_name = sys.argv[1]
    # input_file_name = sys.argv[1]
    # output_file_name = sys.argv[2]
    # urgsal_dict = json.load( open( input_file_name, 'r' ) )

    # print(j_content)
    # exit()

    from ursgal_params import ursgal_params as urgsal_dict

    # with open( output_file_name , 'w') as output_file:
    #         json.dump(
    #             urgsal_dict,
    #             output_file,
    #             sort_keys = True,
    #             indent = 4
    #         )


    output_file = open(output_file_name, 'w')
    print('ursgal_params={', file=output_file)
    for param in sorted(urgsal_dict.keys()):
        # print(param)
        # if param != 'force':
        #     continue
        # print(urgsal_dict[param])
        print('''    '{0}':{1}'''.format(param, '{'), file=output_file )
        for k, v in sorted(urgsal_dict[param].items()):
            # print(k, type(v))
            if k == 'description':
                print('''        '{0}':'''.format(k), "'''", v.strip(), "''',", file=output_file)
            elif type(v) == str:
                print('''        '{0}':"{1}",'''.format(k,v), file=output_file)
            elif type(v) == dict:
                print('''        '{0}':{1}'''.format(k, '{'), file=output_file)
                for k2, v2 in sorted(urgsal_dict[param][k].items()):
                    if type(v2) == dict:
                        print('''            '{0}':{1}'''.format(k2, '{'), file=output_file)
                        for k3, v3 in sorted(urgsal_dict[param][k][k2].items()):
                            print('''                '{0}':'{1}','''.format(k3,v3), file=output_file)
                        print('            },', file=output_file)
                    else:
                        print('''            '{0}':'{1}','''.format(k2,v2), file=output_file)
                print('        },', file=output_file)
            elif type(v) == list:
                print('''        '{0}':{1}'''.format(k, '['), file=output_file)
                for elem in sorted(v):
                    print('''            '{0}','''.format(elem), file=output_file)
                print('        ],', file=output_file)
            else:
                print('''        '{0}':"{1}",'''.format(k,v), file=output_file)
        # exit()
        print('    },', file=output_file)
    print('}', file=output_file)
    output_file.close()