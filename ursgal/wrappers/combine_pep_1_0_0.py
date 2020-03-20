#!/usr/bin/env python

import ursgal
import os.path


class combine_pep_1_0_0(ursgal.UNode):
    '''
    combine_pep_1_0_0 UNode

    Combining Multiengine Search Results with "Combined PEP"

    "Combined PEP" is a hybrid approach combining elements of the
    "combined FDR" approach (Jones et al., 2009), elements of PeptideShaker,
    and elements of Bayes' theorem. Similar to "combined FDR", "combined PEP"
    groups the PSMs. For each search engine, the reported PSMs are treated
    as a set and the logical combinations of all sets are treated separately
    as done in the "combined FDR" approach. For instance, three search engines
    would result in seven PSM groups, which can be visualized by the seven
    intersections of a three-set Venn diagram. Typically, a PSM group that is
    shared by multiple engines contains fewer decoy hits and thus represents a
    higher quality subset and thus its PSMs receive a higher score. This
    approach is based on the assumption that the search engines agree on the
    decoys and false-positives as they agree on the targets.

    The combined PEP approach uses Bayes' theorem to calculate a multiengine
    PEP (MEP) for each PSM based on the PEPs reported by, for example,
    Percolator for different search engines, that is

    .. image:: http://pubs.acs.org/appl/literatum/publisher/achs/journals/content/jprobs/2016/jprobs.2016.15.issue-3/acs.jproteome.5b00860/20160229/images/pr-2015-00860d_m001.gif
       :target: http://pubs.acs.org/doi/full/10.1021/acs.jproteome.5b00860#_i2
       :align: center

    This is done for each PSM group separately.

    Then, the combined PEP (the final score) is computed similar to PeptideShaker
    using a sliding window over all PSMs within each group (sorted by MEP). Each
    PSM receives a PEP based on the target/decoy ratio of the surrounding PSMs.

    .. image:: http://pubs.acs.org/appl/literatum/publisher/achs/journals/content/jprobs/2016/jprobs.2016.15.issue-3/acs.jproteome.5b00860/20160229/images/pr-2015-00860d_m002.gif
       :target: http://pubs.acs.org/doi/full/10.1021/acs.jproteome.5b00860#_i2
       :align: center

    Finally, all groups are merged and the results reported in one output,
    including all the search result scores from the individual search engines
    as well as the FDR based on the "combined PEP".

    The sliding window size can be defined by adjusting the Ursgal parameter
    "window_size" (default is 249).

    Input should be multiple CSV files from different search engines. Each
    CSV requires a PEP column, for instance by post-processing with Percolator.

    Returns a merged CSV file with all PSMs that were found and two added
    columns:

    - column "Bayes PEP":
        The multi-engine PEP, see explanation above
    - column "combined PEP":
        The PEP as computed within the engine combination PSMs

    For optimal ranking, PSMs should be sorted by combined PEP.
    Ties can be resolved by sorting them by Bayes PEP.
    '''

    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Combine PEP',
        'version'            : '1.0.0',
        'release_date'       : '2009-5-1',
        'engine_type' : {
            'meta_engine' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'in_development'     : False,
        'include_in_git'     : True,
        'distributable'      : True,
        'utranslation_style' : 'combine_pep_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'combine_pep_1_0_0.py',
                },
            },
        },
        'citation' : \
            'Combines PEP scores from different search engines.',
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
            'pep_colname': 'PEP',
            # The size of the sliding window for PEP calculation:
            'window_size': self.params['translations']['window_size'],
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
            input_csvs           = self.command_dict['input_csvs'],
            input_engines        = self.command_dict['input_engines'],
            output_csv           = self.command_dict['output_csv'],
            columns_for_grouping = self.command_dict['columns_for_grouping'],
            input_sep            = self.command_dict['input_sep'],
            output_sep           = self.command_dict['output_sep'],
            join_sep             = self.command_dict['join_sep'],
            pep_colname          = self.command_dict['pep_colname'],
            window_size          = self.command_dict['window_size'],
        )
