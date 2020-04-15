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
import subprocess
# from .msgfplus_C_mzid2csv_v2017_07_04 import msgfplus_C_mzid2csv_v2017_07_04 as msgfc


class msgfplus2csv_v1_2_1( ursgal.UNode ):
    """
    msgfplus2csv_v1.2.1 UNode
    Parameter options at https://omics.pnl.gov/software/ms-gf

    Reference:
    Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: Applications to Database Search.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'msgfplus_C_mzid2csv',
        'version'            : 'v1.2.1',
        'release_date'       : '2018-03-28',
        'engine_type' : {
            'converter'     : True
        },
        'input_extensions'   : ['.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : None,
        'include_in_git'     : False,
        'in_development'     : False,
        'distributable'      : False,
        'utranslation_style' : 'msgfplus_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'MzidToTsvConverter.exe',
                    'url'     : '',
                    'zip_md5' : 'bddd04bcba2a72429f7d892a09e98ded'
                },
            },
        },
        'citation' : \
            'Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, '\
            'Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function '\
            'of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: '\
            'Applications to Database Search.',
    }
    def __init__(self, *args, **kwargs):
        super(msgfplus2csv_v1_2_1, self).__init__(*args, **kwargs)
        if sys.platform in ['win32']:
            self.dependencies_ok = True
        else:
            try:
                proc = subprocess.Popen( ['mono', '-V'], stdout = subprocess.PIPE)
            except FileNotFoundError:
                print(
                    '''
        ERROR: MSGF+ mzid C converter requires Mono.
        Installation: http://www.mono-project.com/download
                    '''
                )
                self.dependencies_ok = False

    def preflight( self ):
        '''
        mzid result files from MS-GF+ are converted to CSV
        using the MzIDToTsv converter from MS-GF+

        Input file has to be a .mzid or .mzid.gz

        Creates a .csv file and returns its path

        Mzid to Tsv Converter
        Usage: MzidToTsvConverter -mzid:"mzid path" [-tsv:"tsv output path"] [-unroll|-u] [-showDecoy|-sd]
          Required parameters:
            '-mzid:path' - path to mzid[.gz] file; if path has spaces, it must be in quotes.
          Optional parameters:
            '-tsv:path' - path to tsv file to be written; if not specified, will be output to same location as mzid
            '-unroll|-u' signifies that results should be unrolled - one line per unique peptide/protein combination in each spectrum identification
            '-showDecoy|-sd' signifies that decoy results should be included in the result tsv


        '''
        input_file_incl_path = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        # pprint.pprint(self.params)
        # exit()
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        if sys.platform in ['win32']:
            self.params['command_list'] = []
        else:
            self.params['command_list'] = ['mono']
        self.params['command_list'] += [
            # 'mono',
            self.exe,
            '-mzid:{0}'.format(input_file_incl_path),
            '-tsv:{0}'.format(self.params['translations']['output_file_incl_path'].strip('.csv')+'.tsv'),
            '-showDecoy',
            '-unroll',
            # '-skipDupIds',
            # '-singleResult',
        ]
        self.created_tmp_files.append(self.params['translations']['output_file_incl_path'].strip('.csv')+'.tsv')

        return self.params['translations']['output_file_incl_path']

    def postflight( self ):
        '''
        Convert .tsv result file to .csv and translates headers
        '''

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
                'Spectrum Title',
                'Modifications',
                'Retention Time (s)',
                'Start',
                'Stop',
                'Sequence Pre AA',
                'Sequence Post AA',
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

                # pre_aa, sequence, post_aa = dict_2_write['Sequence'].split('.')
                dict_2_write['Sequence Pre AA']   = dict_2_write['Sequence'][0]
                dict_2_write['Sequence Post AA']  = dict_2_write['Sequence'][-1]
                dict_2_write['Sequence']          = dict_2_write['Sequence'][2:-2]

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
                dict_2_write['Modifications']     = ';'.join( extracted_mods )
                dict_2_write['Raw data location'] = dict_2_write['Raw data location'].replace('_tmp.mgf', '').replace('.mgf', '').replace('.mzML', '')
                dict_2_write['Spectrum Title']    = '{0}.{1}.{1}.{2}'.format(
                    dict_2_write['Raw data location'],
                    dict_2_write['Spectrum ID'],
                    dict_2_write['Charge']
                )
                csv_dict_writer_object.writerow( dict_2_write )
        print('[ INFO  ] Writing MS-GF+ results done!')
        return