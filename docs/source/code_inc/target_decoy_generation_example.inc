.. code-block:: python

	#!/usr/bin/env python3.4
	# encoding: utf-8
	
	import ursgal
	import os
	
	
	def main():
	    '''
	    Simple example script how to generate a target decoy databse.
	
	    usage:
	
	        ./target_decoy_generation_example.py
	
	    '''
	    params = {
	        'enzyme'                : 'trypsin',
	        'decoy_generation_mode' : 'reverse_protein',
	    }
	
	    fasta_database_list = [
	        os.path.join(
	            os.pardir,
	            'example_data',
	            'BSA.fasta'
	        )
	    ]
	
	    uc = ursgal.UController(
	        params = params
	    )
	
	    new_target_decoy_db_name = uc.generate_target_decoy(
	        input_files       = fasta_database_list,
	        output_file_name = 'my_BSA_target_decoy.fasta',
	    )
	    print('Generated target decoy database: {0}'.format(new_target_decoy_db_name))
	
	if __name__ == '__main__':
	    main()
