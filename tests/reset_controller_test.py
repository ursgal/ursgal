#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest
import pprint

class ResetController(unittest.TestCase):
    def setUp(self):
        self.R = ursgal.UController(
            params = {
                'TEST_PARAMS' : 'New',
                # this will score score_ion_list ! :)
            },
            profile  = 'LTQ XL high res'
        )
        pprint.pprint( self.R.params )

    def test_params_setting( self ):
        self.R.params['TEST_PARAMS'] = '2nd'
        self.assertEqual(self.R.params['TEST_PARAMS'] , '2nd')

    def test_profile_was_set( self ):
        self.assertEqual(self.R.params['score_ion_list'] , ['a', 'b', 'y'])

    def test_profile_was_set2( self ):
        self.R.reset_controller()
        self.R.set_profile( 'LTQ XL low res' )

        self.assertEqual(self.R.params['instrument'] , 'low_res_ltq')

    def test_profile_was_set3( self ):
        self.R.reset_controller()
        self.R.set_profile( 'LTQ XL low res' )
        self.R.reset_controller()

        self.assertEqual(self.R.params['instrument'] , 'low_res_ltq')

    def test_reset_none_default_params(self):
        self.R.params['TEST_PARAMS_2nd'] = '2nd'
        self.R.reset_controller()
        self.assertEqual(self.R.params['TEST_PARAMS_2nd'] , '2nd')

    def test_reset_none_default_params_twice(self):
        self.R.params['TEST_PARAMS'] = '2nd'
        self.R.reset_controller()
        self.R.params['TEST_PARAMS'] = '3nd'
        self.R.reset_controller()
        self.assertEqual(self.R.params['TEST_PARAMS'] , '3nd')

    def test_reset_default_params(self):
        self.R.params['enzyme'] = 'trypsin'
        self.R.reset_controller()
        self.assertEqual(self.R.params['enzyme'] , 'trypsin')

    def test_reset_default_params_to_something(self):
        self.R.params['enzyme'] = 'argc'
        self.R.reset_controller()
        self.assertEqual(self.R.params['enzyme'] , 'argc')

    def test_sweep_params(self):
        '''Not going back to default'''
        for ppm_error in range(-100, 110, 1):
            with self.subTest(ppm_error = ppm_error):
                self.R.params['frag_mass_tolerance'] = ppm_error
                self.assertEqual(
                    self.R.params['frag_mass_tolerance'],
                    ppm_error
                )

    def test_reset_default_params_twice_incl_back_to_default(self):
        '''
        Setting back to default ...
        '''
        self.R.params['enzyme'] = 'argc'
        self.R.reset_controller()
        self.R.params['enzyme'] = 'trypsin'
        self.R.reset_controller()
        self.assertEqual(self.R.params['enzyme'] , 'trypsin')

    def test_reset_default_params_twice_incl_back_to_default_none(self):
        self.R.params['machine_offset_in_ppm'] = 10
        self.R.reset_controller()
        self.R.params['machine_offset_in_ppm'] = None
        self.R.reset_controller()
        self.assertEqual(
            self.R.params['machine_offset_in_ppm'],
            None
        )

    def test_reset_default_params_twice_incl_back_to_default2(self):
        self.R.params['prefix'] = 'REALLY_'
        self.R.reset_controller()
        self.R.params['prefix'] = None
        self.R.reset_controller()
        self.assertEqual(self.R.params['prefix'] , None)

if __name__ == '__main__':
    unittest.main()
