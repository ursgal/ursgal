#!/usr/bin/env python3.4

import ursgal
import os.path


class combine_pep_1_0_0(ursgal.UNode):
    '''
    combine_pep_1_0_0 UNode

    Combine_PEP is a variation of the combined FDR score algorithm
    (Jones et al., 2009). Instead of sorting PSMs by the average FDR
    score (AFS), PSMs are sorted by their multi-engine PEP as computed
    from the single-engine PEPs using Bayes’ theorem.
    For instance, consider a PSM that received three different PEPs
    (a, b and c) from three different search engines. The multi-engine
    PEP can then be computed:

                                a*b*c
    multi-engine PEP = -------------------------
                       a*b*c + (1-a)*(1-b)*(1-c)

    For each combination of search engines, all PSMs that were found
    by these engines are then scored separately. First, they are sorted
    by their multi-engine PEP. Then their combined PEPs are computed by
    iterating a sliding window over the sorted PSMs. Each PSM receives
    a PEP based on the target/decoy ratio of the surrounding PEPs:

    PEP = (2 * number_of_decoys_in_window) / number_of_total_PSMs_in_window

    The window_size can be defined by adjusting the Ursgal parameter
    'cPEP:window_size', default is 249.

    Input should be multiple CSV files from different search engines. Each
    CSV requires a PEP column, for instance by post-processing with Percolator.

    Returns a merged CSV file with all PSMs that were found and two added
    columns:
    - column 'Bayes PEP':
        The multi-engine PEP, see explanation above
    - column 'combined PEP':
        The PEP as computed within the engine combination PSMs

    For optimal ranking, PSMs should be sorted by combined PEP.
    Ties can be resolved by sorting them by Bayes PEP.
    '''

    META_INFO = {
        'engine_type'    : {
            'controller'        : False,
            'converter'         : False,
            'validation_engine' : False,
            'search_engine'     : False,
            'meta_engine'       : True,
        },
        'in_development'            : True,
        'input_types'               : ['.csv'],
        'output_extension'          : '.csv',
        'create_own_folder'         : False,
        #'citation' : 'Combines PEP scores from different search engines.',
        'include_in_git'            : True,

        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'combine_pep_1_0_0.py',
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        super(combine_pep_1_0_0, self).__init__(*args, **kwargs)
        pass


    def preflight( self ):
        '''
        Building the list of parameters that will be passed to the
        combine_pep_1_0_0 main function.

        These parameters are stored in self.command_dict

        Returns:
                None
        '''
        input_file_list_for_cPEP = []
        search_engine_list_for_cPEP = []
        # careful, these must have the same order!

        for input_file_dict in self.params["input_file_dicts"]:
            input_file_path = os.path.join(
                input_file_dict['dir'],
                input_file_dict['file']
            )
            input_file_list_for_cPEP.append(input_file_path)
            search_engine = input_file_dict["last_engine"]
            search_engine_list_for_cPEP.append(search_engine)

        features_that_define_unique_psm = \
            ['Sequence', 'Modifications', 'Spectrum Title', 'Is decoy']#, 'Charge', 'Is decoy']

        output_csv_full_path = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'],
        )

        self.command_dict = {
            'input_csvs': input_file_list_for_cPEP,
            'input_engines': search_engine_list_for_cPEP,
            'output_csv': output_csv_full_path,
            'columns_for_grouping': features_that_define_unique_psm,
            'input_sep': ',',  # input csv separating char
            'output_sep': ',',  # output csv separating char
            'join_sep': ';',  # char to join multiple values in same field
            'pep_colname': self.params['cPEP:pep_colname'],
            # The size of the sliding window for PEP calculation:
            'window_size': self.params['cPEP:window_size'],
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
        cPEP_main = self.import_engine_as_python_function()

        print('''

Executing main() function from {scriptpath} with the following parameters:

>>> {script}.main(
...     input_csvs = {input_csvs},
...     input_engines = {input_engines},
...     output_csv = '{output_csv}',
...     columns_for_grouping = {columns_for_grouping},
...     input_sep = '{input_sep}',
...     output_sep = '{output_sep}',
...     join_sep = '{join_sep}',
...     pep_colname = '{pep_colname}',
...     window_size = {window_size},
... )

        '''.format(
            scriptpath = os.path.relpath(self.exe),
            script = os.path.basename(self.exe),
            **self.command_dict
            )
        )

        # executing main function of the combine_PEP script
        cPEP_main(
            input_csvs = self.command_dict['input_csvs'],
            input_engines = self.command_dict['input_engines'],
            output_csv = self.command_dict['output_csv'],
            columns_for_grouping = self.command_dict['columns_for_grouping'],
            input_sep = self.command_dict['input_sep'],
            output_sep = self.command_dict['output_sep'],
            join_sep = self.command_dict['join_sep'],
            pep_colname = self.command_dict['pep_colname'],
            window_size = self.command_dict['window_size'],
        )
