#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest


class TestRun(unittest.TestCase):
    def setUp(self):
        self.uc = ursgal.UController()
        self.uc.params['translations'] = {}
        self.uc.UNODE_UPARAMS.update(
            {
                'test_ions' : {
                    'style'                    : 'test_style_1',
                    'ukey'                     : 'test_ions',
                    'ukey_translated'          : '__test_00000_ions',
                    'default_value'            : 'Yes',
                    'default_value_translated' : True,
                    'uvalue_style_translation' : {
                        'Yes' : True,
                        'No'  : False
                    },
                    'triggers_rerun'           : True
                },
                'score_test_ions' : {
                    'style'                    : 'test_style_1',
                    'ukey'                     : 'score_test_ions',
                    'ukey_translated'          : '__test_00000_ions',
                    'default_value'            : True,
                    'default_value_translated' : 'Please yes translate',
                    'uvalue_style_translation' : {
                        True : 'Please yes translate',
                        False: 'No please leave me alone'
                    },
                    'triggers_rerun'           : True
                },
                'list_of_things' : {
                    'style'                    : 'test_style_1',
                    'ukey'                     : 'list_of_things',
                    'ukey_translated'          : 'list_of_things',
                    'default_value'            : [ True, True, True],
                    'default_value_translated' : [ True, True, True],
                    'uvalue_style_translation' : {},
                    'triggers_rerun'           : True
                }
            }
        )

    def test_key_and_value_translation(self):
        untranslated_params, translated_params = self.uc.collect_and_translate_params(
            {
                'test_ions' : 'No',
            }
        )
        self.assertEqual(
            translated_params['test_ions_key'], '__test_00000_ions'
        )
        self.assertEqual(
            translated_params['test_ions'], False
        )


    def test_bool_translation(self):
        untranslated_params, translated_params = self.uc.collect_and_translate_params(
            {
                'score_test_ions' : False,
            }
        )
        self.assertEqual(
            translated_params['score_test_ions'], 'No please leave me alone'
        )
    def test_empty_translation_return_default(self):
        untranslated_params, translated_params = self.uc.collect_and_translate_params({})
        self.assertEqual(
            translated_params['score_test_ions'], 'Please yes translate'
        )
    def test_list_ov_values_is_kept(self):
        untranslated_params, translated_params = self.uc.collect_and_translate_params(
            {'list_of_things' : [False, False, False]}
        )
        self.assertEqual(
            translated_params['list_of_things'], [False, False, False]
        )

    def test_grouping_on_translated_keys(self):
        untranslated_params, translated_params = self.uc.collect_and_translate_params({})
        self.assertEqual(
            len(
                translated_params['_grouped_by_translated_key']['__test_00000_ions']
            ),
            2
        )


if __name__ == '__main__':
    unittest.main()
