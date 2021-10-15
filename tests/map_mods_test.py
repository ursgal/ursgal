#!/usr/bin/env python3
# encoding: utf-8
"""

Test the filter_csv function for xtandem engine

"""
import ursgal
import csv
import os


R = ursgal.UController()


TESTS = [
    {
        "modifications": ["M,opt,any,Oxidation"],
        "type": "opt",
        "result_dict": {
            "_id": 0,
            "aa": "M",
            "mass": 15.994915,
            "pos": "any",
            "name": "Oxidation",
            "composition": {"O": 1},
            "org": "M,opt,any,Oxidation",
            "id": "35",
            "unimod": True,
        },
    },
    {
        "modifications": ["C,fix,any,Carbamidomethyl"],
        "type": "fix",
        "result_dict": {
            "_id": 0,
            "aa": "C",
            "mass": 57.021464,
            "pos": "any",
            "name": "Carbamidomethyl",
            "composition": {"O": 1, "N": 1, "C": 2, "H": 3},
            "org": "C,fix,any,Carbamidomethyl",
            "id": "4",
            "unimod": True,
        },
    },
    {
        "modifications": ["K,fix,any,TEST,+13C(10)15N(3)C(2)H(20)O(2)-N(1)"],
        "type": "fix",
        "result_dict": {
            "_id": 0,
            "aa": "K",
            "mass": 237.17713092699998,
            "pos": "any",
            "name": "TEST",
            "composition": {"13C": 10, "15N": 3, "C": 2, "H": 20, "O": 2, "N": -1},
            "org": "K,fix,any,TEST,+13C(10)15N(3)C(2)H(20)O(2)-N(1)",
            "unimod": False,
        },
    },
]


def map_mods_test():
    for test_id, test_dict in enumerate(TESTS):
        yield map_mods, test_dict


def map_mods(test_dict):
    file_exists = False
    usermods_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "ursgal",
        "resources",
        "platform_independent",
        "arc_independent",
        "ext",
        "userdefined_unimod.xml",
    )
    if os.path.exists(usermods_file):
        import shutil

        tmp_usermods_file = usermods_file.replace(".xml", "_tmp.xml")
        shutil.copy(usermods_file, tmp_usermods_file)
        file_exists = True
    R = ursgal.UController(params={"modifications": test_dict["modifications"]})
    ursgal.UNode.map_mods(R)
    map_mod_dict = R.params["mods"][test_dict["type"]][0]
    for k, v in test_dict["result_dict"].items():
        assert v == map_mod_dict[k]

    if file_exists:
        shutil.copy(tmp_usermods_file, usermods_file)
        os.remove(tmp_usermods_file)
    elif os.path.exists(usermods_file):
        os.remove(usermods_file)


if __name__ == "__main__":
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        map_mods(test_dict)
