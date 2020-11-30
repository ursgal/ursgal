#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle
import shutil


class filter_csv_1_0_0(ursgal.UNode):
    """filter_csv_1_0_0 UNode

    Filters .csv files row-wise according to user-defined rules.

    The filter rules have to be defined in the params. See the engine
    documentation for further information ( :meth:`.filter_csv_1_0_0._execute` ).
    """

    META_INFO = {
        'edit_version'           : 1.00,
        'name'                   : 'Filter CSV',
        'version'                : '1.0.0',
        'release_date'           : None,
        'engine_type' : {
            'misc_engine' : True
        },
        'input_extensions'       : ['.csv'],
        'output_extensions'      : ['.csv'],
        'output_suffix'          : 'accepted',
        'rejected_output_suffix' : 'rejected',
        'in_development'         : False,
        'include_in_git'         : True,
        'distributable'      : True,
        'utranslation_style'     : 'filter_csv_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'filter_csv_1_0_0.py',
                },
            },
        },
        'citation' :
        '',
    }

    def __init__(self, *args, **kwargs):
        super(filter_csv_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        '''
        Result files (.csv) are filtered for defined filter parameters.

        Input file has to be a .csv

        Creates a _accepted.csv file and returns its path. If defined also
        rejected entries are written to _rejected.csv.

        Note:

            To write the rejected entries define 'write_unfiltered_results' as
            True in the parameters.

        Available rules:

            * lte
            * gte
            * lt
            * gt
            * contains
            * contains_not
            * equals
            * equals_not
            * regex

        Example:

            >>> params = {
            >>>     'csv_filter_rules':[
            >>>         ['PEP', 'lte', 0.01],
            >>>         ['Is decoy', 'equals', 'false']
            >>>     ]
            >>>}

        The example above would filter for posterior error probabilities lower
        than or equal to 0.01 and filter out all decoy proteins.

        Rules are defined as list of lists with the first list element as the
        column name/csv fieldname, the second list element the rule and the
        third list element the value which should be compared. Multiple rules
        can be applied, see example above. If the same fieldname should be
        filtered multiply (E.g. Sequence should not contain 'T' and 'Y'), the
        rules have to be defined separately.

        Example:

            >>> params = {
            >>>     'csv_filter_rules':[
            >>>         ['Sequence','contains_not','T'],
            >>>         ['Sequence','contains_not','Y']
            >>>     ]
            >>>}



        lte:

            'lower than or equal' (<=) value has to comparable i.e. float or
            int. Values are accepted if they are lower than or equal to the
            defined value. E.g. ['PEP','lte',0.01]

        gte:

            'greater than or equal' (>=) value has to comparable
            i.e. float or int. Values are accepted if they are greater than or
            equal to the defined value. E.g. ['Exp m/z','gte',180]

        lt:

            'lower than' (<=) value has to comparable
            i.e. float or int. Values are accepted if they are lower than
            the defined value. E.g. ['PEP','lt',0.01]

        gt:

            'greater than' (>=) value has to comparable
            i.e. float or int. Values are accepted if they are greater than
            the defined value. E.g. ['PEP','gt',0.01]

        contains:

            Substrings are checked if they are present in the the full string.
            E.g. ['Modifications','contains','Oxidation']

        contains_not:

            Substrings are checked if they are present in the the full string.
            E.g. ['Sequence','contains_not','M']

        equals:

            String comparison (==). Comparison has to be an exact match to pass.
            E.g. ['Is decoy','equals','false']. Floats and ints are not compared
            at the moment!

        equals_not:

            String comparison (!=). Comparisons differing will be rejected.
            E.g. ['Is decoy','equals_not','true']. Floats and ints are not
            compared at the moment!

        regex:

            Any regular expression matching is possible E.g. CT and CD motif
            search ['Sequence','regex','C[T|D]']


        Note:

            Some spreadsheet tools interpret False and True and show them as
            upper case when opening the files, even if they are actually
            written in lower case. This is especially important for target and
            decoy filtering, i.e. ['Is decoy','equals','false'].
            'false' has to be lower case, even if the spreadsheet tool displays
            it as 'FALSE'.

        '''
        print('[ -ENGINE- ] Executing conversion ..')
        # self.time_point(tag = 'execution')
        filter_csv_main = self.import_engine_as_python_function()
        if self.params['output_file'].lower().endswith('.csv') is False:
            raise ValueError('Trying to filter a non-csv file')

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        if self.params['translations']['write_unfiltered_results'] is False:
            output_file_unfiltered = None
        else:
            file_extension = self.META_INFO.get(
                'output_suffix',
                None
            )
            new_file_extension = self.META_INFO.get(
                'rejected_output_suffix',
                None
            )
            output_file_unfiltered = output_file.replace(
                file_extension,
                new_file_extension
            )
            shutil.copyfile(
                '{0}.u.json'.format(output_file),
                '{0}.u.json'.format(output_file_unfiltered)
            )

        filter_csv_main(
            input_file=input_file,
            output_file=output_file,
            filter_rules=self.params['translations']['csv_filter_rules'],
            output_file_unfiltered=output_file_unfiltered,
        )
        if output_file_unfiltered is not None:
            self.fix_md5_and_file_in_json(
                json_path='{0}.u.json'.format(output_file_unfiltered)
            )

        # self.print_execution_time(tag='execution')
        return output_file
