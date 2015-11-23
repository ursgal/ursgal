#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import pickle

class unify_csv_1_0_0( ursgal.UNode ):
    """unify_csv_1_0_0 UNode"""
    def __init__(self, *args, **kwargs):
        super(unify_csv_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Result files from search engines are unified
        to contain the same informations in the same style

        Input file has to be a .csv

        Creates a _unified.csv file and returns its path

        '''
        print('[ -ENGINE- ] Executing conversion ..')
        self.time_point(tag = 'execution')
        unify_csv_main = self.import_engine_as_python_function()
        if self.params['output_file'].lower().endswith('.csv') is False:
            raise ValueError('Trying to unify a non-csv file')

        output_file = os.path.join(
                self.params['output_dir_path'],
                self.params['output_file']
            )
        input_file  = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        scan_rt_lookup_path = self.meta_unodes['ucontroller'].scan_rt_lookup_path

        assert os.path.isfile( scan_rt_lookup_path ), """
Could not load RT lookup dict from this location: {0}
        """.format( scan_rt_lookup_path )

        scan_rt_lookup_dict = pickle.load(
            open( scan_rt_lookup_path, 'rb' )
        )

        last_engine = None
        for engine_type in ['search_engine', 'denovo_engine']:
            if last_engine == None:
                last_engine = self.get_last_engine(
                history = self.stats['history'],
                engine_type = engine_type,
            )


        unify_csv_main(
            input_file     = input_file,
            output_file    = output_file,
            scan_rt_lookup = scan_rt_lookup_dict,
            params         = self.params,
            search_engine  = last_engine,
        )

        self.print_execution_time(tag='execution')
        return output_file
