#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle
import csv
import copy
import re
import pprint
import gzip


class msgfplus2csv_v2016_09_16( ursgal.UNode ):
    """
    msgfplus2csv_v2016_09_16 UNode
    Parameter options at https://omics.pnl.gov/software/ms-gf

    Reference:
    Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: Applications to Database Search.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'msgfplus2csv',
        'version'            : 'v2016.09.16',
        'release_date'       : '2016-9-16',
        'engine_type' : {
            'converter'     : True
        },
        'input_extensions'   : ['.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : None,
        'include_in_git'     : False,
        'in_development'     : False,
        'distributable'  : False,
        'utranslation_style' : 'msgfplus_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'MSGFPlus.jar',
                    'url'     : '',
                    'zip_md5' : '',
                },
            },
        },
        'citation' : \
            'Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, '\
            'Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function '\
            'of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: '\
            'Applications to Database Search.',
        'uses_unode' : 'msgfplus_v2016_09_16',
    }

    def __init__(self, *args, **kwargs):
        super(msgfplus2csv_v2016_09_16, self).__init__(*args, **kwargs)

    def preflight( self ):
        '''
        mzid result files from MS-GF+ are converted to CSV
        using the MzIDToTsv converter from MS-GF+

        Input file has to be a .mzid

        Creates a .csv file and returns its path

        '''
        input_file_incl_path = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        if self.io['input']['finfo']['is_compressed']:
            self.params['translations']['mzidentml_compress'] = True
            with gzip.open(input_file_incl_path, 'rt') as fin:
                path, ext = os.path.splitext(input_file_incl_path)
                with open(path, 'wt') as fout:
                    for line in fin:
                        fout.write(line)
            input_file_incl_path = path
            self.params['translations']['tmp_uncompressed_mzid'] = path

        self.params['command_list'] = [
            'java',
            '-Xmx{0}'.format(self.params['translations']['-xmx']),
            '-cp',
            self.exe,
            'edu.ucsd.msjava.ui.MzIDToTsv',
            '-i', input_file_incl_path,
            '-o','{0}'.format(self.params['translations']['output_file_incl_path'].strip('.csv')+'.tsv'),
            '-showQValue','{0}'.format(self.params['translations']['output_q_values']),
            '-showDecoy', '1',
            '-unroll','0',
        ]
        self.created_tmp_files.append(self.params['translations']['output_file_incl_path'].strip('.csv')+'.tsv')

        return self.params['translations']['output_file_incl_path']

    def postflight( self ):
        '''
        Convert .tsv result file to .csv
        '''
        # remove temp mzid
        if self.params['translations'].get('tmp_uncompressed_mzid', None) is not None:
            os.remove(self.params['translations']['tmp_uncompressed_mzid'])

        cached_msgfplus_output = []
        with open(self.params['translations']['output_file_incl_path'].strip('.csv')+'.tsv', 'r') as result_file:
            headers = []
            for h in result_file.readline()[1:].split('\t'):
                headers.append(h.strip())
            ignore_columns = [
                'SpecID',
                'FragMethod',
                'IsotopeError',
                'PrecursorError(ppm)',
            ]

            translated_headers = []
            for header in headers:
                if header in ignore_columns:
                    continue
                translated_headers.append(
                    self.UNODE_UPARAMS['header_translations']['uvalue_style_translation'].get(header, header)
                )
            translated_headers += [
                'Modifications',
                'Retention Time (s)',
                'Start',
                'Stop',
                'Calc m/z',
                'Is decoy',
            ]
            print('[ PARSING  ] Loading unformatted MS-GF+ results ...')
            for row in result_file:
                line_dict = {}
                for n, field in enumerate(row.split('\t')):
                    line_dict[headers[n]] = field.strip()
                cached_msgfplus_output.append( line_dict )
        print('[ PARSING  ] Done')

        mod_pattern = re.compile( r'''[+-][0-9]{1,}[\.,][0-9]{1,}''' )

        with open(
            os.path.join(
                self.params['output_dir_path'],
                self.params['output_file'],
            ),
            'w'
        ) as result_file:
            if sys.platform == 'win32':
                lineterminator = '\n'
            else:
                lineterminator = '\r\n'
            csv_dict_writer_object = csv.DictWriter(
                result_file,
                fieldnames = translated_headers,
                lineterminator = lineterminator
            )
            csv_dict_writer_object.writeheader()
            print('[ INFO  ] Writing MS-GF+ results')
            csv_write_list = []

            total_docs = len(cached_msgfplus_output)

            for cache_pos, m in enumerate(cached_msgfplus_output):
                tmp = {}
                for header in headers:
                    if header in ignore_columns:
                        continue
                    translated_header = self.UNODE_UPARAMS['header_translations']['uvalue_style_translation'].get(header, header)
                    tmp[ translated_header ] = m[ header ]

                if cache_pos % 500 == 0:
                    print(
                        '[ INFO ] Processing line number:    {0}/{1}'.format(
                            cache_pos,
                            total_docs
                        ),
                        end = '\r'
                    )
                dict_2_write = copy.deepcopy( tmp )

                for k in [
                    'Charge',
                    'MS-GF:DeNovoScore',
                    'MS-GF:EValue',
                    'MS-GF:RawScore',
                    'Exp m/z',
                    'MS-GF:SpecEValue',
                ]:
                    dict_2_write[k] = dict_2_write[k].replace(',', '.')

                dict_2_write['Raw data location'] = os.path.abspath(
                    #hahahahha
                    dict_2_write['Raw data location']
                )

                extracted_mods = []

                match = mod_pattern.search(dict_2_write['Sequence'])
                while match != None:
                    start, stop = match.span()
                    mod = dict_2_write['Sequence'][start:stop].replace(',', '.')
                    extracted_mods.append('{0}:{1}'.format(mod, start))
                    dict_2_write['Sequence'] = \
                        dict_2_write['Sequence'][:start] \
                        + dict_2_write['Sequence'][stop:]
                    match = mod_pattern.search(dict_2_write['Sequence'])

                dict_2_write['Modifications'] = ';'.join( extracted_mods )
                csv_dict_writer_object.writerow( dict_2_write )
        print('[ INFO  ] Writing MS-GF+ results done!')
        return
