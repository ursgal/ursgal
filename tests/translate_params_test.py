#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest


class TestRun(unittest.TestCase):
    def setUp(self):
        self.R = ursgal.UController()
        self.R.USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
            'score_a_ions' : {
                True : 'translate_YES!',
                False : 'translate_PLEASE_NOT'
            }
        }
        self.R.USEARCH_PARAM_VALUE_TRANSLATIONS = {
            'trypsin' : 'trypsin_translated',  # value for enzyme
        }
        self.R.USED_USEARCH_PARAMS = set(['score_a_ions', 'enzyme'])

    def test_simple_transation(self):
        translated_params = self.R.translate_params(
            {
                'enzyme' : 'trypsin',
                'score_a_ions' : True
            }
        )
        self.assertEqual(translated_params, {
            'enzyme' : 'trypsin_translated',
            'score_a_ions' : 'translate_YES!'
        })

    def test_missing_used_params( self ):
        old_used_params = self.R.USED_USEARCH_PARAMS
        self.R.USED_USEARCH_PARAMS = set(['missing_param!'])
        with self.assertRaises(Exception):
            self.R.translate_params({})
        self.R.USED_USEARCH_PARAMS = old_used_params

if __name__ == '__main__':
    unittest.main()
