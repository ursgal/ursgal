#!/usr/bin/env python3.4

import ursgal
import os.path


class combine_FDR_0_1( ursgal.UNode ):
    '''
    combine FDR 0_1 UNode

    An implementation of the "combined FDR Score" algorithm, as described in:
    Jones AR, Siepen JA, Hubbard SJ, Paton NW (2009):
    "Improving sensitivity in proteome studies by analysis of false discovery
    rates for multiple search engines."
    
    Input should be multiple CSV files from different search engines. Each
    CSV requires a PEP column, for instance by post-processing with Percolator.

    Returns a merged CSV file with all PSMs that were found and an added
    column "Combined FDR Score".
    '''
    def __init__(self, *args, **kwargs):
        super(combine_FDR_0_1, self).__init__(*args, **kwargs)
        pass


    def preflight( self ):
        '''
        Building the list of parameters that will be passed to the
        combine_FDR_0_1 main function.

        These parameters are stored in self.command_dict

        Returns:
                None
        '''
        input_file_list_for_cFDR_script = []
        file_info_for_cFDR_script       = {}

        input_file_search_engines = set()
        for input_file_dict in self.params["input_file_dicts"]:
            input_file_path = os.path.join(
                input_file_dict['dir'],
                input_file_dict['file']
            )
            input_file_list_for_cFDR_script.append( input_file_path )

            search_engine = input_file_dict["last_search_engine"]
            score_colname = input_file_dict["last_search_engine_colname"]
            input_file_search_engines.add( search_engine )

            file_info_for_cFDR_script[ input_file_path ] = {
                "engine_name"    : search_engine,                # i.e. "xtandem_sledgehammer"
                "engine_colname" : score_colname.split(":")[0],  # i.e. "X\!Tandem"
            }

        assert len(input_file_search_engines) == len(self.params["input_file_dicts"]) \
        and len(self.params["input_file_dicts"]) > 1, '''
        All {0} input files must be search results from *different* search engines.
        You specified {1} input files:
        {2}
        ...but they are all from {3} engine(s).
        If want to analyze multiple files from the same engine, merge them beforehand with
        merge_csvs().'''.format(
            os.path.basename( self.exe ),
            len(self.params["input_file_dicts"]),
            input_file_list_for_cFDR_script,
            len(input_file_search_engines)
        )

        self.command_dict = {
            "input_file_list" : input_file_list_for_cFDR_script,
            "cutoff"          : self.params['combined_FDR_cutoff'],
            "directory"       : self.params['output_dir_path'],
            "file_info"       : file_info_for_cFDR_script,
            "output_filename" : self.params['output_file'],
            "filter_decoys"   : self.params['filter_decoys'],
            "filter_cutoff"   : self.params['apply_combined_FDR_cutoff'],
        }


    def _execute( self ):
        '''
        Executing the combine_FDR_0_1 main function with parameters
        that were defined in preflight (stored in self.command_dict)

        The main function is imported and then executed using the
        parameters from command_dict.

        Returns:
                None
        '''
        combine_FDR_main = self.import_engine_as_python_function()

        print('''

Executing main() function from {scriptpath}.py with the following parameters:

>>> {script}.main(
...
...     input_file_list = \t{input_file_list},
...
...     file_info       = \t{file_info},
...
...     directory       = {directory},
...     output_filename = {output_filename},
...     cutoff          = {cutoff},
...     filter_cutoff   = {filter_cutoff},
...     filter_decoys   = {filter_decoys},
... )

        '''.format(
            scriptpath = os.path.relpath( self.exe ),
            script     = os.path.basename( self.exe ),
            **self.command_dict
            )
        )

        # executing main function of the FDR combiner script
        combine_FDR_main(
            input_file_list = self.command_dict["input_file_list"],
            file_info       = self.command_dict["file_info"],
            cutoff          = self.command_dict["cutoff"],
            directory       = self.command_dict["directory"],
            output_filename = self.command_dict["output_filename"],
            filter_decoys   = self.command_dict["filter_decoys"],
            filter_cutoff   = self.command_dict["filter_cutoff"],
        )
    #self.execute_answer = self.command_dict["output_filename"]
