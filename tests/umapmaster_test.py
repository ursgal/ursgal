#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest
import pprint
from ursgal import umapmaster as umama


TEST_DICT = {
    'enzyme' : {
        'default_value' : 'trypsin',
        'available_in_unode' : ['omssa', 'xtandem'],
        'description' : 'Enzyme used for digestions',
        'ukey_translation' : {
            'omssa_style_1' : '-ot',
            'xtandem_style_1' : 'enzyme'
        },
        'uvalue_translation' : {
            'omssa_style_1' : {
                'trypsin' : 1
            },
            'xtandem_style_1' : {
                'trypsin' : '[KR]|{P}'
            }
        }
    },
    'frag_mass_type' : {
        'default_value' : 'monoisotopic',
        'available_in_unode' : ['omssa'],
        'description' : 'use chemical average or monoisotopic mass for fragment ions.',
        'ukey_translation' : {
            'omssa_style_1' : '-tom',
        },
        'uvalue_translation' : {
            'omssa_style' : {
                'monoisotopic' : 0,
                'average' : 1
            }
        }
    },
}


class UMapMaster(unittest.TestCase):
    def setUp(self):
        self.umama_small = umama.UParamMapper( TEST_DICT )
        self.umama_default = umama.UParamMapper()

    def test_all_mappings_by_style(self):
        results = []
        for mDict in self.umama_small.mapping_dicts('omssa'):
            results.append( (mDict['ukey'], mDict['default_value']) )
        self.assertEqual(
            sorted(results),
            sorted([
                ('enzyme', 'trypsin'),
                ('frag_mass_type', 'monoisotopic' )
            ])
        )

    def test_get_masked_params( self ):
        mask = ['default_value', 'description']
        masked_params = self.umama_small.get_masked_params(mask=mask)
        self.assertEqual(
            len(masked_params.keys()),
            len(TEST_DICT.keys())
        )
        self.assertEqual(
             len(masked_params['enzyme'].keys()), len(mask)
        )
        self.assertEqual(
            list(sorted(masked_params['enzyme'].keys())), sorted(mask)
        )




if __name__ == '__main__':
    unittest.main()
