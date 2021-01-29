#!/usr/bin/env python3
# encoding: utf-8

import glob
import os
import csv
import sys
from collections import defaultdict as ddict
import pprint as pp

if __name__ == "__main__":
    print(
        """
        Converting parameter tables from csv to params dict
"""
    )
    input_file = sys.argv[1]
    output_file_name = sys.argv[1]

    # from ursgal_params import ursgal_params as urgsal_dict

    urgsal_dict = {}
    n = 0
    with open(input_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["ursgal_params"] != "":
                ukey = row["ursgal_params"]
            else:
                n += 1
                ukey = "ukey{0}".format(n)
            urgsal_dict[ukey] = {}
            description = ""
            urgsal_dict[ukey]["description"] = row["ursgal_params_description"].strip()
            urgsal_dict[ukey]["default_value"] = row["ursgal_default_params"].strip()
            available_in_unode = []
            translation = {}
            for engine in ["xtandem", "omssa", "msgfplus", "myrimatch", "msamanda"]:
                for row_key, row_value in row.items():
                    if engine in row_key and row_value != "":
                        available_in_unode.append(engine)
                        translation["{0}_style_1".format(engine)] = row_value.strip()

            urgsal_dict[ukey]["available_in_unode"] = available_in_unode
            urgsal_dict[ukey]["utag"] = ""
            urgsal_dict[ukey]["ukey_translation"] = translation
            urgsal_dict[ukey]["uvalue_type"] = ""
            urgsal_dict[ukey]["uvalue_translation"] = ""

    csvfile.close()

    output_file = open(output_file_name, "w")
    print("ursgal_params={", file=output_file)
    for param in sorted(urgsal_dict.keys()):
        print("""    '{0}':{1}""".format(param, "{"), file=output_file)
        for k, v in sorted(urgsal_dict[param].items()):
            if k == "description":
                print(
                    """        '{0}':""".format(k),
                    "'''",
                    v.strip(),
                    "''',",
                    file=output_file,
                )
                continue
            if type(v) == str:
                print("""        '{0}':"{1}",""".format(k, v), file=output_file)
            elif type(v) == dict:
                print("""        '{0}':{1}""".format(k, "{"), file=output_file)
                for k2, v2 in sorted(urgsal_dict[param][k].items()):
                    print(
                        """            '{0}':'{1}',""".format(k2, v2), file=output_file
                    )
                print("        },", file=output_file)
            elif type(v) == list:
                print("""        '{0}':{1}""".format(k, "["), file=output_file)
                for elem in sorted(v):
                    print("""            '{0}',""".format(elem), file=output_file)
                print("        ],", file=output_file)
            else:
                print("""        '{0}':'{1}',""".format(k, v), file=output_file)
        # pp.pprint(urgsal_dict, width=200, stream=output_file)
        print("    },", file=output_file)
    print("}", file=output_file)
    # pp.pprint(urgsal_dict)
    output_file.close()
