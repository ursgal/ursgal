#!/usr/bin/env python
import ursgal
import os
from collections import defaultdict as ddict
import csv
import itertools
import sys

class pglyco_fdr_2_2_0(ursgal.UNode):
    """
    Unode for pGlycoFDR included in pGlyco 2.2.0
    This node allows post-processing of pGlyco results

    Note:
        Please download pGlycoFDR manually as part of pGlyco 2.2.0
        https://github.com/pFindStudio/pGlyco2

    Reference:
    Liu MQ, Zeng WF,, Fang P, Cao WQ, Liu C, Yan GQ, Zhang Y, Peng C, Wu JQ,
    Zhang XJ, Tu HJ, Chi H, Sun RX, Cao Y, Dong MQ, Jiang BY, Huang JM, Shen HL,
    Wong CCL, He SM, Yang PY. (2017) pGlyco 2.0 enables precision N-glycoproteomics
    with comprehensive quality control and one-step mass spectrometry
    for intact glycopeptide identification.
    Nat Commun 8(1)
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'pGlycoFDR',
        'version': '2.2.0',
        'release_date': '2019-01-01',
        'utranslation_style': 'pglyco_fdr_style_1',
        'input_extensions': ['.csv'],
        'output_extensions': ['.csv'],
        'create_own_folder': False,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'validation_engine': True,
        },
        'engine': {
            'win32' : {
                '64bit' : {
                    'exe'            : 'pGlycoFDR.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation':
        'Liu MQ, Zeng WF,, Fang P, Cao WQ, Liu C, Yan GQ, Zhang Y, Peng C, Wu JQ,'
            'Zhang XJ, Tu HJ, Chi H, Sun RX, Cao Y, Dong MQ, Jiang BY, Huang JM, Shen HL,'
            'Wong CCL, He SM, Yang PY. (2017) pGlyco 2.0 enables precision N-glycoproteomics '
            'with comprehensive quality control and one-step mass spectrometry'
            'for intact glycopeptide identification.'
            'Nat Commun 8(1)'
    }

    def __init__(self, *args, **kwargs):
        super(pglyco_fdr_2_2_0, self).__init__(*args, **kwargs)
        pass

    def preflight(self):
        '''
        Formatting the command line and writing the param input file via 
        self.params

        Returns:
            dict: self.params
        '''
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        search_result_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        print(search_result_file)

        self.param_file_name = search_result_file.strip('.csv') + '_pGlyco.cfg'

        self.params['command_list'] = [
            self.exe,
            '-p',
            self.param_file_name,
            '-r',
            os.path.join(
                self.params['input_dir_path'],
                'pGlycoDB-GP.txt',
            ),
        ]

        return self.params

    def postflight(self):
        # '''
        # Reads pGlycoFDR txt output and write final csv output file.

        # Adds:
        #     * Raw data location, since this can not be added later

        # '''
        pglyco_header = [
            'GlySpec',
            'PepSpec',
            'RawName',
            'Scan',
            'RT',
            'PrecursorMH',
            'PrecursorMZ',
            'Charge',
            'Rank',
            'Peptide',
            'Mod',
            'PeptideMH',
            'Glycan(H,N,A,G,F)',
            'PlausibleStruct',
            'GlyID',
            'GlyFrag',
            'GlyMass',
            'GlySite',
            'TotalScore',
            'PepScore',
            'GlyScore',
            'CoreMatched',
            'CoreFuc',
            'MassDeviation',
            'PPM',
            'GlyIonRatio',
            'PepIonRatio',
            'GlyDecoy',
            'PepDecoy',
            'GlycanFDR',
            'PeptideFDR',
            'TotalFDR',
        ]

        translated_headers = []
        header_translations = self.UNODE_UPARAMS[
            'header_translations']['uvalue_style_translation']
        # import pprint
        # pprint.pprint(self.meta_unodes['pglyco_fdr_2_2_0'].UNODE_UPARAMS)
        for original_header_key in pglyco_header:
            ursgal_header_key = header_translations[original_header_key]
            translated_headers.append(ursgal_header_key)

        csv_kwargs = {}
        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'
        csv_writer = csv.DictWriter(
            open(self.params['translations']['output_file_incl_path'], 'w'),
            fieldnames=translated_headers,
            **csv_kwargs
        )

        pglyco_output = os.path.join(
            self.params['output_dir_path'],
            'pGlycoDB-GP-FDR.txt'
        )
        csv_reader = csv.DictReader(
            open(pglyco_output, 'r'),
            fieldnames=translated_headers,
            delimiter='\t',
        )
        # self.created_tmp_files.append(pglyco_output)

        csv_writer.writeheader()
        for n, line_dict in enumerate(csv_reader):
            if n == 0:
                continue
            csv_writer.writerow(line_dict)
        return
