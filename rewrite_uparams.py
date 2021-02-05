#!/usr/bin/env python3
# encoding: utf-8

import csv
import sys
import re
import pprint
import os


def main():
    """
    Rewrites uparams.py, thereby checking for duplicates and sorting the dictionary.
    Note:
        uparams.py will be overwritten, if you are not sure, if your changes to uparams.py are correct, you can use another output_file_name

    Usage:
        ./rewrite_uparams.py <output_file_name(optional)>
    """

    input_file_name = os.path.join("ursgal", "uparams.py")
    try:
        output_file_name = sys.argv[1]
    except:
        output_file_name = input_file_name

    print(
        """
        Testing params dict for duplicates
    """
    )

    params = set()
    duplicates = []
    with open(input_file_name, "r") as input_file:
        for line in input_file:
            if line.startswith("    '") and line[4] == "'":
                hit = re.match("    '.{1,}'", line)
                param = hit.group(0).strip()
                if param not in params:
                    params.add(param)
                else:
                    duplicates.append(param)
    if duplicates == []:
        print("no duplicates were found")
    else:
        print("remove duplicates for:", duplicates)
        sys.exit(1)

    print(
        """
        Rewriting params dict
    """
    )
    from ursgal.uparams import ursgal_params as urgsal_dict

    print(len(urgsal_dict.keys()), " parameters")
    output_file = open(output_file_name, "w")
    print("ursgal_params = {", file=output_file)
    for param in sorted(urgsal_dict.keys()):
        # print(param)
        # if param != 'force':
        #     continue
        # print(urgsal_dict[param])
        print("""    '{0}' : {1}""".format(param, "{"), file=output_file)
        for k, v in sorted(urgsal_dict[param].items()):
            # print(k, type(v))
            if k == "description":
                print(
                    """        '{0}' : """.format(k),
                    repr(v.strip()),
                    ",",
                    file=output_file,
                )
            elif type(v) == str:
                print("""        '{0}' : "{1}",""".format(k, v), file=output_file)
            elif type(v) == dict:
                print("""        '{0}' : {1}""".format(k, "{"), file=output_file)
                for k2, v2 in sorted(urgsal_dict[param][k].items()):
                    if type(v2) == dict:
                        print(
                            """            '{0}' : {1}""".format(k2, "{"),
                            file=output_file,
                        )
                        for k3, v3 in sorted(urgsal_dict[param][k][k2].items()):
                            if k3 in [True, False]:
                                if type(v3) != str:
                                    print(
                                        """                {0} : {1},""".format(k3, v3),
                                        file=output_file,
                                    )
                                else:
                                    print(
                                        """                {0} : '{1}',""".format(
                                            k3, v3
                                        ),
                                        file=output_file,
                                    )
                            elif type(v3) != str:
                                print(
                                    """                '{0}' : {1},""".format(k3, v3),
                                    file=output_file,
                                )
                            else:
                                print(
                                    """                '{0}' : '{1}',""".format(k3, v3),
                                    file=output_file,
                                )
                        print("            },", file=output_file)
                    elif type(v2) != str:
                        print(
                            """            '{0}' : {1},""".format(k2, v2),
                            file=output_file,
                        )
                    else:
                        print(
                            """            '{0}' : '{1}',""".format(k2, v2),
                            file=output_file,
                        )
                print("        },", file=output_file)
            elif type(v) == list:
                print("""        '{0}' : {1}""".format(k, "["), file=output_file)
                for elem in sorted(v):
                    print("""            '{0}',""".format(elem), file=output_file)
                print("        ],", file=output_file)
            else:
                print("""        '{0}' : {1},""".format(k, v), file=output_file)
        # sys.exit(1)
        # print('''        'trigger_rerun' : True,''', file=output_file)
        print("    },", file=output_file)
    print("}", file=output_file)
    output_file.close()


if __name__ == "__main__":
    main()
