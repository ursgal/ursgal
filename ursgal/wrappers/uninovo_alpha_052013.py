#!/usr/bin/env python
import ursgal
import os
import subprocess

class uninovo_alpha_052013( ursgal.UNode ):
    """
    UniNovo UNode
    http://proteomics.ucsd.edu/Software/UniNovo/

    Reference:
    Jeong K, Kim S, Pevzner PA (2013): UniNovo: a universal tool for de novo peptide sequencing.
    """
    META_INFO = {
        # see http://proteomics.ucsd.edu/Software/UniNovo/#Downloads
        'edit_version'      : 1.00,
        'name'              : 'UniNovo',
        'version'           : 'alpha.052013',
        'release_date'      : '2013-5-20',
        'engine_type' : {
            'de_novo_search_engine' : True,
        },
        'input_extensions'  : ['.mgf'],
        'output_extensions' : ['.den'],
        'create_own_folder' : True,
        'in_development'    : True,
        'include_in_git'    : None,
        'distributable'      : False,
        'utranslation_style' : 'uninovo_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'UniNovo.jar',
                    'url' : 'http://proteomics.ucsd.edu/Software/UniNovo/UniNovo.20130520.zip',
                    # 'zip_md5'        : '',
                    # 'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Jeong K, Kim S, Pevzner PA (2013): UniNovo: a universal tool for '\
            'de novo peptide sequencing.',
    }

    def __init__(self, *args, **kwargs):
        super(uninovo_alpha_052013, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formatting the command line via self.params

        Returns:
                dict: self.params
        '''

        self.params['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '.mgf'
        )

        self.params['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        print(
            '''
            [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
            [ WARNING ] need to be combined for pyQms (use of symmetric tolerance window).
            [ WARNING ] The arithmetic mean is used.
            '''
        )
        self.params['precursor_mass_tolerance'] = ( float(self.params['precursor_mass_tolerance_plus']) + \
                                                    float(self.params['precursor_mass_tolerance_minus']) ) \
                                                / 2.0

        self.params[ 'command_list' ] = [
            'pushd', self.exe.rstrip('UniNovo.jar'), '&&', #need to specify this because UniNovo searches the Pars directory in the shell working directory

            'java', '-Xmx{java_-Xmx}'.format( **self.params), '-jar', self.exe, # path 2 executable
            '-i', '{mgf_input_file}'.format( **self.params), # SpectrumFile (*.mzXML, *.mgf, *.ms2)
            '-o', '{output_file_incl_path}'.format(**self.params).rstrip('.den'), # output file prefix - UniNovo will output file named as "prefix.den"
            '-pt', '{precursor_mass_tolerance}{precursor_mass_tolerance_unit}'.format(**self.params), # precursor ion tolerance (ending in ppm or Da)
            '-t', '{frag_mass_tolerance}{frag_mass_tolerance_unit}'.format(**self.params), # ion tolerances (ending in ppm or Da)
            '-f', '{frag_method}'.format(**self.params), # fragmentation method (CID/ETD/HCD) - if -par option is specified, this option will be ignored
            '-e', '{enzyme}'.format(**self.params), # enzyme applied (0: No enzyme specificity, 1: Trypsin (default), 2: LysC)
            '-c', '{uninovo_num_13C}'.format(**self.params), # number of 13C considered (default : 0)
            #'-l', '{min_pep_length}'.format(**self.params), # minimum length of reconstructions (default : 5), in small datasets UniNovo might produce empty outputfiles, so the whole script crashes
            '-n', '{num_match_spec}'.format(**self.params), # number of de novo sequences per one spectrum (1-200 : default 100)
            '-acc', '{uninovo_accuracy}'.format(**self.params),# set accuracy threshold (0.0-0.9 : default 0.8)
            '-g', '{uninovo_num_mass_gaps}'.format(**self.params), # number of possible mass gaps per each sequence (2-10 : default 10)
            #'-par', {trained_par_file}.format(**self.params), # use user trained parameter file (see below to see how to train UniNovo)

            '&&','popd', #going back to the previous shell working directory
        ]
        #print(self.params[ 'command_list' ])
        return self.params

    def _execute(self):
        '''
        The _execute unode function

        Executes the unode executable via shell.

        Note: internal function
            Unodes that do not require execution via shell
            redefine the _execute() function in their engine
            class.

        Returns:
            None
        '''
        self.print_info('Executing command list ...', caller='eXecution')
        assert 'command_list' in self.params.keys(), '''
  No command_list was found in self.params. Convention is to define
  the command list during preflight in the uNode Engine class code or,
  alternatively, redefine uNode._execute() in the engine class altogether
        '''
        self.time_point(tag = 'execution')
        execute_answer = []
        proc = None

        if len(self.params['command_list']) != 0:
            proc = subprocess.Popen(
                self.params['command_list'],
                stdout = subprocess.PIPE,
                shell = True
            )
        else:
            print('Command list is empty, nothing to do here...')
            print('_execute failed ....', self.params['command_list'])
            execute_answer.append( 'Command list is empty' )
            self.execute_return_code = 500

        if proc is not None:
            for line in proc.stdout:
                line_decoded = line.strip().decode('utf')
                print( line_decoded )
                execute_answer.append( line_decoded )

            # catching the executable's exit code to detect crashes:
            proc.communicate()[0]
            self.execute_return_code = proc.returncode
            assert self.execute_return_code in [0, None], '''
  \n{0} crashed!

  The executable
    {1}
  terminated with Error code {2} .
  Inspect the printouts above for possible causes and verify that all input files are valid.
            '''.format( self.engine, os.path.relpath(self.exe), self.execute_return_code)

        self.print_execution_time(tag='execution')
        return

    def postflight( self ):
        return

