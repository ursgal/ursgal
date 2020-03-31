#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys

def main(mzML_file=None):
    '''
    '''
    R = ursgal.UController(
    	params={
    		'signal_to_noise_threshold': 1.5,
    		# 'scan_inclusion_list': [x for x in range(0,100)]
    	}
	)
    mgf_file = R.convert(
        input_file=mzML_file, 
        engine='mzml2mgf_2_0_0'
    )

if __name__ == '__main__':
    main(mzML_file=sys.argv[1])