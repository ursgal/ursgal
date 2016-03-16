#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys

class mzml2mgf_1_0_0( ursgal.UNode ):
    """
    mzml2mgf_1_0_0 UNode

    Converts .mzML files into .mgf files
    """
    def __init__(self, *args, **kwargs):
        super(mzml2mgf_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        print('[ -ENGINE- ] Executing conversion ..')
        self.time_point(tag = 'execution')
        mzml2mgf_main = self.import_engine_as_python_function()


        try:
            tmp = mzml2mgf_main(
                mzml = os.path.join(
                    self.io['input']['finfo']['dir'],
                    self.io['input']['finfo']['file']
                ),
                mgf = os.path.join(
                    self.io['output']['finfo']['dir'],
                    self.io['output']['finfo']['file']
                ),
                i_decimals            = self.params['number_of_i_decimals'],
                mz_decimals           = self.params['number_of_mz_decimals'],
                machine_offset_in_ppm = self.params['machine_offset_in_ppm'],
                scan_exclusion_list   = self.params['scan_exclusion_list'],
                prefix                = self.params.get('prefix',None),
                scan_skip_modulo_step = self.params['scan_skip_modulo_step']
            )
        except KeyError:
            print('''

                OBO Version changed ? converter uses obo names instead of tags.
                This need to be updated in time ...

                ''')
        self.print_execution_time(tag='execution')
        return tmp
