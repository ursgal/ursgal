#!/usr/bin/env python3.4
import ursgal
import os


class uninovo_alpha_052013( ursgal.UNode ):
    """
    UniNovo UNode
    http://proteomics.ucsd.edu/Software/UniNovo/

    Reference:
    Jeong K, Kim S, Pevzner PA (2013): UniNovo: a universal tool for de novo peptide sequencing.
    """
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
        
        self.params['precursor_mass_tolerance'] = ( float(self.params['precursor_mass_tolerance_plus']) + \
                                                    float(self.params['precursor_mass_tolerance_minus']) ) \
                                                / 2.0

        self.params[ 'command_list' ] = [
            'java', '-Xmx{java_-Xmx}'.format( **self.params), '-jar', self.exe, # path 2 executable
            '-i', '{mgf_input_file}'.format( **self.params), # SpectrumFile (*.mzXML, *.mgf, *.ms2)
            '-o', '{output_file_incl_path}'.format(**self.params), # output file prefix - UniNovo will output file named as "prefix.den" 
            '-pt', '{precursor_mass_tolerance}{precursor_mass_tolerance_unit}'.format(**self.params), # precursor ion tolerance (ending in ppm or Da)
            '-t', '{frag_mass_tolerance}{frag_mass_tolerance_unit}'.format(**self.params), # ion tolerances (ending in ppm or Da)
            '-f', '{frag_method}'.format(**self.params), # fragmentation method (CID/ETD/HCD) - if -par option is specified, this option will be ignored
            '-e', '{enzyme}'.format(**self.params), # enzyme applied (0: No enzyme specificity, 1: Trypsin (default), 2: LysC)
            '-c', '{uninovo_num_13C}'.format(**self.params), # number of 13C considered (default : 0)
            '-l', '{min_pep_length}'.format(**self.params), # minimum length of reconstructions (default : 5)
            '-n', '{num_match_spec}'.format(**self.params), # number of de novo sequences per one spectrum (1-200 : default 100)
            '-acc', '{uninovo_accuracy}'.format(**self.params),# set accuracy threshold (0.0-0.9 : default 0.8)
            '-g', '{uninovo_num_mass_gaps}'.format(**self.params), # number of possible mass gaps per each sequence (2-10 : default 10)
             # '-par', {trained_par_file}.format(**self.params), # use user trained parameter file (see below to see how to train UniNovo)
        ]

        return self.params
