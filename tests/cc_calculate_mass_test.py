#!/usr/bin/env python3.2
# encoding: utf-8
'''
Small test to verify the correct function of the isotope mass calculation
in chemical_composition
'''
import ursgal

TESTS = [
    {
        'composition_1' : {
            '14N' : 1,
            '12C' : 1
        },
        'composition_2' : {
            'N' : 1,
            'C' : 1
        },
    },
    {
        'composition_1' : {
            'N'   : 1,
            '14N' : 1,
            '12C' : 1
        },
        'composition_2' : {
            'N' : 2,
            'C' : 1
        },
    },
]

cc_1 = ursgal.ChemicalComposition()
cc_2 = ursgal.ChemicalComposition()


def pepitde_with_unimod_test():
    for test_id, test_dict in enumerate( TESTS ):
        yield mass_checker, test_dict


def mass_checker( test_dict ):

    cc_1.add_chemical_formula(
        test_dict['composition_1']
    )
    cc_2.add_chemical_formula(
        test_dict['composition_2']
    )
    assert cc_1._mass() == cc_2._mass()
    cc_1.clear()
    cc_2.clear()


if __name__ == '__main__':
    print(__doc__)
    pepitde_with_unimod_test()
