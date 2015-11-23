#!/usr/bin/env python3.4
import ursgal
import os
import subprocess


class pepnovo_3_1( ursgal.UNode ):
    """
    PepNovo v3.1 UNode
    http://proteomics.ucsd.edu/Software/UniNovo/

    Reference:
    Ari M. Frank, Mikhail M. Savitski, Michael L. Nielsen, Roman A. Zubarev, and Pavel A. Pevzner (2007) De Novo Peptide Sequencing and Identification with Precision Mass Spectrometry, J. Proteome Res. 6:114-123.
    """
    def __init__(self, *args, **kwargs):
        super(pepnovo_3_1, self).__init__(*args, **kwargs)
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

        if self.params['precursor_mass_tolerance_unit'] == 'ppm':
            self.params['precursor_mass_tolerance_plus'] = ursgal.ucore.convert_ppm_to_dalton( self.params['precursor_mass_tolerance_plus'], base_mz=self.params['base_mz'] )
            self.params['precursor_mass_tolerance_minus'] = ursgal.ucore.convert_ppm_to_dalton( self.params['precursor_mass_tolerance_minus'], base_mz=self.params['base_mz'] )
        self.params['precursor_mass_tolerance'] = ( float(self.params['precursor_mass_tolerance_plus']) + \
                                                    float(self.params['precursor_mass_tolerance_minus']) ) \
                                                / 2.0

        if self.params['frag_mass_tolerance_unit'] == 'ppm':
            self.params['frag_mass_tolerance'] = ursgal.ucore.convert_ppm_to_dalton( self.params['frag_mass_tolerance'], base_mz=self.params['base_mz'] )

        if self.params['pepnovo_model_dir'] == None:
            self.params['pepnovo_model_dir'] = os.path.dirname(self.exe) + '/Models'

        available_mods = {
            'Carbamidomethyl': {'fix': ('C', '+57'),
                               'opt': ('HDE', '+57'),
                               'N-term': 'NT+CAM'},
            'Trp->Kynurenin': {'opt': ('W', '+4')},
            'Cation:K': {'opt': ('SKNPLRVIEMDGA', '+38')},
            'Cation:Na': {'opt': ('QVPNYTHDESFAMILG', '+22')},
            'Acetyl': {'opt': ('LTSYGVMPDAK', '+42'),
                       'N-term': '^+42'},
            'Carbamyl': {'opt': ('PANMETGDLFIQSVK', '+43')},
            'Dehydrated': {'opt': ('EDST', '-18')},
            'Dimethyl': {'opt': ('K', '+28')},
            'Dioxidation': {'opt': ('MW', '+32')},
            'Formyl': {'opt': ('ST', '+28')},
            'Oxidation': {'opt': ('MHWDKNP', '+16')},
            'Deamidated': {'opt': ('NQ', '+1')},
            'Methyl': {'opt': ('CHKNQR', '+14'),
                       'N-term': '^+14'},
            'Phospho': {'opt': ('STY', '+80')},
            'Gln->pyro-Glu': {'opt': ('Q', '-17')},
            'Amidated': {'C-term': '$-1'},
            'Label:18O(1)': {'C-term': '$+2'},
            }

        modifications = []
        for mod in self.params[ 'mods' ][ 'fix' ]:
            if mod['name'] in available_mods.keys():
                if 'fix' in available_mods[ mod['name'] ].keys():
                    if mod['aa'] in available_mods[ mod['name'] ]['fix'][0]:
                        modifications.append(mod['aa'] + available_mods[ mod['name'] ]['fix'][1])

        for mod in self.params[ 'mods' ][ 'opt' ]:
            if mod['name'] in available_mods.keys():
                for term in ['N-term', 'C-term']:
                    if term in mod['pos']:
                        if term in available_mods[ mod['name'] ].keys():
                            modifications.append(available_mods[ mod['name'] ][term])
                if 'opt' in available_mods[ mod['name'] ].keys():
                    if mod['aa'] in available_mods[ mod['name'] ]['opt'][0]:
                        modifications.append(mod['aa'] + available_mods[ mod['name'] ]['opt'][1])


        self.params[ 'command_list' ] = [
            self.exe, # path 2 executable
            '-file', '{mgf_input_file}'.format( **self.params), # SpectrumFile (*.mzXML, *.mgf, *.ms2)
            '-model', '{pepnovo_model}'.format( **self.params), # (currently only CID_IT_TRYP is available)
            '-fragment_tolerance', '{frag_mass_tolerance}'.format(**self.params), # ion tolerances (in Da)
            '-pm_tolerance', '{precursor_mass_tolerance}'.format(**self.params), # precursor ion tolerance (in Da)
            '-digest', '{enzyme}'.format(**self.params),
            '-num_solutions', '{num_match_spec}'.format(**self.params),
            '-model_dir', '{pepnovo_model_dir}'.format(**self.params),  # - directory where model files are kept (default ./Models)
            '-PTMs', ':'.join(modifications),  # - separated by a colons (no spaces) e.g., M+16:S+80:N+1
        ]
        if self.params['pepnovo_tag_length']:
            if self.params['pepnovo_tag_length'] >= 3 and self.params['pepnovo_tag_length'] <= 6:
                self.params[ 'command_list' ].extend([
                    '-tag_length', '{pepnovo_tag_length}'.format(**self.params)
                    ]) # < 3-6> - returns peptide sequence of the specified length (only lengths 3-6 are allowed).

        for param in [
            'output_cum_probs', 
            'output_aa_probs',
            'prm',
            'prm_norm',
            'correct_pm',
            'use_spectrum_charge',
            'use_spectrum_mz',
            'no_quality_filter',
        ]:
            if self.params[param] == True:
                self.params[ 'command_list' ].append( '-{0}'.format(param) )

        if self.params['min_filter_prob'] >= 0 and self.params['min_filter_prob'] <= 1.0:
            self.params[ 'command_list' ].extend([ '-min_filter_prob', '{min_filter_prob}'.format(**self.params) ])

        return self.params

    def _execute(self):
        if len(self.params['command_list']) != 0:
            proc = subprocess.Popen(
                self.params['command_list'],
                stdout = subprocess.PIPE,
            )
        else:
            print('Command list is empty, nothing to do here...')
            print('_execute failed ....', self.params['command_list'])
            execute_answer.append( 'Command list is empty' )
            self.execute_return_code = 500

        if proc is not None:
            output_file = open(self.params['output_file_incl_path'], 'w')
            # pint('Printing output to file, this can take a while ...')
            for line in proc.stdout:
                if line.startswith(b'>>'):
                    print(
                        'processing spectrum number: ',
                        line.strip().decode('utf').split('.')[1],
                        end = '\r'
                    )

                line_decoded = line.strip().decode('utf')
                print( line_decoded, file = output_file )
            output_file.close()

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
