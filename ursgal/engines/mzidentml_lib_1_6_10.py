#!/usr/bin/env python3.4
import ursgal
import sys
import os
import pprint
import subprocess

class mzidentml_lib_1_6_10( ursgal.UNode ):
    """
    MzidLib 1_6_10 UNode

    'Reisinger F, Krishna R, Ghali F, Ríos D, Hermjakob H, Vizcaíno JA, Jones AR. (2012)
    jmzIdentML API: A Java interface to the mzIdentML standard for peptide and protein identification data.'

    Java program to convert resulta to .mzIdentML and .mzIdentML to .csv

    """
    def __init__(self, *args, **kwargs):
        super(mzidentml_lib_1_6_10, self).__init__(*args, **kwargs)

    def raw2mzid( self, search_engine=None ):
        '''
        Convert raw result files into .mzid result files
        '''
        tmp_options = [
            self.exe,
            '-outputFragmentation', 'false',
            '-decoyRegex',
            '{decoy_tag}'.format(
                **self.params
            ),
            '-compress', 'false',
        ]

        if 'tandem' in search_engine:
            tmp_options += [
                '-databaseFileFormatID', 'MS:1001348',
                'massSpecFileFormatID', 'MS:1001062',
                '-idsStartAtZero', 'false'
            ]
            converter_mode = 'Tandem2mzid'
            self.print_info('Executing xtandem xml to mzid conversion')
        else:
            self.print_info('''
    Do not know how to convert search results from {input_file} to mzid
            '''.format( **self.params ),caller='Warning')
            sys.exit(1)
        tmp_command_list = [
            'java', '-Xmx{java_-Xmx}'.format( **self.params),
            '-jar', self.exe,
            converter_mode,
            os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            ),
            self.params['mzid_output_file'],
        ]

        tmp_command_list += tmp_options
        proc = subprocess.Popen(
            tmp_command_list,
            stdout=subprocess.PIPE,
        )
        for line in proc.stdout:
            print(line.strip().decode('utf'))
        return

    def preflight( self ):
        '''
        Convert .mzid result files from different search engines
        into .csv result files

        For X!Tandem result files first need to be converted into .mzid
        with raw2mzid
        '''
        #import pprint
        #pprint.pprint( self.stats )
        #exit()

        search_engine = None
        for history_step_dict in self.stats['history']:
            # print(history_step_dict)
            is_search_engine  = history_step_dict['META_INFO']['engine_type'].get(
                'search_engine',False
            )
            if is_search_engine:
                search_engine = history_step_dict['engine']

        if search_engine is None:
            raise TypeError( 'mzidentml_lib UNode: Last search engine was not found in history. Can\'t convert results without knowing which search engine was used.' )

        self.params['mzid_output_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['file_root'] + '.mzid'
        )
        if 'tandem' in search_engine:
            # xtandem uses xml outpur which has first to be converted to .mzid
            self.raw2mzid( search_engine=search_engine)
            run_mz_ident_2_csv = True
        elif 'omssa' in search_engine:
            run_mz_ident_2_csv = False
        elif 'msgf' in search_engine:
            run_mz_ident_2_csv = True
        elif 'myrimatch' in search_engine:
            run_mz_ident_2_csv = True
        elif 'msamanda' in search_engine:
            run_mz_ident_2_csv = False
        else:
            raise Exception("Don't know the search engine that created your file...")

        if run_mz_ident_2_csv:
            assert os.path.exists(self.params['mzid_output_file']), '''
                No mzident file found {0}
            '''.format( self.params['mzid_output_file'] )
            self.params[ 'command_list' ] = [
                'java', '-Xmx{java_-Xmx}'.format( **self.params),
                '-jar', self.exe,
                'Mzid2Csv',
                self.params['mzid_output_file'],
                os.path.join(
                    self.params['output_dir_path'],
                    self.params['output_file']
                ),
                '-exportType'    , 'exportPSMs' ,
                '-verboseOutput' , 'false'      ,
                '-compress'      , 'false'
            ]
        else:
            #OMSSA and MS amanda does not need a conversion
            self.params['command_list'] = []
        return
