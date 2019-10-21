#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle
import shutil


class csv2counted_results_1_0_0(ursgal.UNode):
    """csv2counted_results_1_0_0 UNode"""

    META_INFO = {
        'edit_version': 1.00,
        'name': 'Summarize Results as Tables',
        'version': '1.0.0',
        'release_date': None,
        'engine_type': {
            'converter': True
        },
        'output_extensions': ['.csv'],
        'input_extensions': ['.csv'],
        'output_suffix': 'counted',
        'in_development': False,
        'utranslation_style': 'csv2counted_results_style_1',
        'include_in_git': True,
        'distributable': True,
        'engine': {
            'platform_independent': {
                'arc_independent': {
                    'exe': 'csv2counted_results_1_0_0.py',
                },
            },
        },
        'citation': '',
    }

    def __init__(self, *args, **kwargs):
        super(csv2counted_results_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        '''
        Results (.csv) are summarized as table (.csv) containing all identified
        proteins, peptides, or other specified identifiers. For each sample,
        the peptide or spectral count for each identifier is given.

        Input file has to be a .csv

        Creates a _counted.csv file and returns its path.

        Columns containing the elements that should be counted (identifiers)
        are given as a list of headers using uc.params["identifier_column_names"].
        Columns defining a unique countable element (e.g. "Sequence", "Spectrum ID")
        are given as a list of headers using uc.params["count_column_names"].

        This can be used to create a SFINX (http://sfinx.ugent.be/) input file, 
        using: 
            uc.params["convert_to_sfinx"]=True
            uc.params["identifier_colum_names"]=["Protein ID"]
            uc.params["count_column_names"]=["Sequence"]

        '''

        print('[ -ENGINE- ] Executing conversion ..')
        self.time_point(tag='execution')
        csv2count_main = self.import_engine_as_python_function()
        if self.params['input_file'].lower().endswith('.csv') is False:
            raise ValueError('Trying to convert a non-csv file')

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        csv2count_main(
            input_file=input_file,
            output_file=output_file,
            identifier_colum_names=self.params['translations']['identifier_column_names'],
            count_column_names=self.params['translations']['count_column_names'],
            count_by_file=self.params['translations']['count_by_file'],
            convert2sfinx=self.params['translations']['convert_to_sfinx'],
            keep_column_names=self.params['translations']['keep_column_names'],
        )

        self.print_execution_time(tag='execution')
        return output_file
