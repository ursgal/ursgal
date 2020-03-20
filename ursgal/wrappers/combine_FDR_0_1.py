#!/usr/bin/env python

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

    META_INFO = {
        'edit_version'          : 1.00,
        'name'                  : 'combine FDR',
        'version'               : '0.1',
        'release_date'          : '2009-5-1',
        'engine_type' : {
            'meta_engine' : True,
        },
        'input_extensions'      : ['.csv'],
        'output_extensions'     : ['.csv'],
        'create_own_folder'     : False,
        'in_development'        : False,
        'include_in_git'        : True,
        'distributable'      : True,
        'utranslation_style'    : 'combine_FDR_style_1',
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'combine_FDR_0_1.py',
                },
            },
        },
        'citation' : \
            'An implementation of the "combined FDR Score" algorithm, as '\
            'described in: Jones AR, Siepen JA, Hubbard SJ, Paton NW (2009) '\
            'Improving sensitivity in proteome studies by analysis of false '\
            'discovery rates for multiple search engines.',
    }

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

            search_engine = input_file_dict["last_engine"]
            score_colname = input_file_dict["last_engine_colname"]
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
            "cutoff"          : None,
            "directory"       : self.params['output_dir_path'],
            "file_info"       : file_info_for_cFDR_script,
            "output_filename" : self.params['output_file'],
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
            cutoff          = 0.01,  # only for printing
            directory       = self.command_dict["directory"],
            output_filename = self.command_dict["output_filename"],
            filter_decoys   = False,  # we have filter_csv for that purpose :)
            filter_cutoff   = False,  # we have filter_csv for that purpose :)
        )
    #self.execute_answer = self.command_dict["output_filename"]
