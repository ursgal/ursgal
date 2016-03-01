#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest
import pprint
from ursgal import umapmaster as umama


TEST_DICT = {
    'enzyme' : {
        'default' : 'Try',
        'available_in_unode' : ['omssa', 'xtandem'],
        'description' : 'Enzyme used for digestions',
        'ukey-translation' : {
            'omssa_style_1' : '-ot',
            'xtandem_style_1' : 'enzyme'
        },
        'uvalue-translation' : {
            'try' : {
                'omssa_style_1': 1,
                'xtandem_style_1' : 'try'
            }
        }
    },
    'frag_mass_type' : {
        'default' : 'monoisotopic',
        'available_in_unode' : ['omssa'],
        'description' : 'use chemical average or monoisotopic mass for fragment ions.',
        'ukey-translation' : {
            'omssa_style_1' : '-tom',
        },
        'uvalue-translation' : {
            'monoisotopic' : {
                'omssa_style_1': 0,
            },
            'average' : {
                'omssa_style_1': 1,
            },
        }
    },
}


class UMapMaster(unittest.TestCase):
    def setUp(self):
        self.umama = umama.UParamMapper( TEST_DICT )


    def test_get_omssa_all_params(self):
        all_omssa_params = self.umama.get_all_params( engine='omssa')
        self.assertEqual(all_omssa_params, ['enzyme', 'frag_mass_type'])


if __name__ == '__main__':
    unittest.main()
