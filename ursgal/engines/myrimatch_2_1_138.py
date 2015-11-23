#!/usr/bin/env python3.4
import ursgal
import os
import os.path


class myrimatch_2_1_138( ursgal.UNode ):
    """
    Myrimatch UNode

    Myrimatch options:
    http://forge.fenchurch.mc.vanderbilt.edu/scm/viewvc.php/*checkout*/trunk/doc/index.html?root=myrimatch

    Reference:
    Tabb DL, Fernando CG, Chambers MC. (2007) MyriMatch: highly accurate tandem mass spectral peptide identification by multivariate hypergeometric analysis.
    """
    def __init__(self, *args, **kwargs):
        super(myrimatch_2_1_138, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formatting the command line
        '''
        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        if input_file.lower().endswith('.mzml') or \
            input_file.lower().endswith('.mzml.gz'):
            self.params['mzml_input_file'] = input_file
        elif input_file.lower().endswith('.mgf'):
            # use dark magic to find the mzml file that corresponds to the mgf:
            self.params['mzml_input_file'] = \
                self.meta_unodes['ucontroller'].get_mzml_that_corresponds_to_mgf( input_file )
            self.print_info(
                ('Since MyriMatch cannot read MGF input files, the '
                 'corresponding mzML file {0} will be used instead.'
                ).format( os.path.relpath(self.params['mzml_input_file']) ),
                caller="INFO" )
        else:
            raise Exception('MyriMatch input spec file must be in mzML format!')

        self.params['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        self.params['myrimatch_ions_to_search'] = []
        for ion in ['a','b','c','x','y','z']:
            ion_2_add = self.params['score_{0}_ions'.format(ion)]
            if ion_2_add != '':
                self.params['myrimatch_ions_to_search'].append( ion_2_add )
        self.params['myrimatch_ions_to_search'] = 'manual:'+','.join(self.params['myrimatch_ions_to_search'] )

        self.params['myrimatch_config_file_path'] = \
            '{output_file_incl_path}_myrimatch_params.cfg'.format( **self.params )
        self.created_tmp_files.append( self.params['myrimatch_config_file_path'] )
        self.write_param_file( )

        self.params['command_list'] = [
            self.exe,
            '-cfg', '{myrimatch_config_file_path}'.format(**self.params),
            '{mzml_input_file}'.format(**self.params),
            '-workdir', "{output_dir_path}".format( **self.params ),
            '-cpus', '{cpus}'.format( **self.params ),
            '-OutputFormat', 'mzIdentML',
            # '-OutputSuffix', '_{0}'.format( self.engine ),
            # '-dump'
            '-FragmentationAutoRule', 'false' #it should be false,
            #If true, MyriMatch will automatically choose the fragmentation rule based on the activation type of each MSn spectrum.
        ]


    def write_param_file( self ):
        ''' Writes a file containing all parameters for the search '''

        config_file= open(self.params['myrimatch_config_file_path'], 'w') #param file must be in execution folder
        # param_io = open('config_file','w')
        self.params['myrimatch_static_mods'] = ''
        # self.params['cam_mod_mass'] = ursgal.kb.ursgal.CAM_MOD
        self.params['myrimatch_dynamic_mods'] = ''
        # cam = False

        # if self.params['label'] == '15N':
        #     for aminoacid, modification in ursgal.kb.ursgal.DICT_15N_DIFF.items():
        #         if aminoacid == 'C' and cam == True:
        #             self.params['myrimatch_static_mods']+= '{0} {1} '.format( aminoacid, modification + ursgal.kb.ursgal.CAM_MOD )
        #         else:
        #             self.params['myrimatch_static_mods']+= '{0} {1} '.format( aminoacid, modification )

        if self.params['label'] == '15N':
            for aminoacid, N15_Diff in ursgal.kb.ursgal.DICT_15N_DIFF.items():
                existing = False
                for mod in self.params[ 'mods' ][ 'fix' ]:
                    if aminoacid == mod[ 'aa' ]:
                        mod[ 'mass' ] += N15_Diff
                        existing = True
                if existing == True:
                    continue
                self.params['myrimatch_static_mods']+= '{0} {1} '.format( aminoacid, N15_Diff )
            
        for mod in self.params[ 'mods' ][ 'fix' ]:
            # if self.params['label'] == '15N' and mod[ 'aa' ] == 'C' and mod[ 'name' ] == 'Carbamidomethyl':
            #     cam = True
            #     continue
            self.params['myrimatch_static_mods'] += '{0} {1} '.format( mod[ 'aa' ], mod[ 'mass' ] )
            
        characters = ['$', '%', '^', '&', '*', '_', '<', '>', '|', ':', ';' ]
        for n, mod in enumerate( self.params[ 'mods' ][ 'opt' ] ):
            if n >= len(characters)-1:
                print( 
                    '''
                    [ WARNING ] To many potential modifications. Ran out of characters.
                    [ WARNING ] Continues without modification: {0}'''.format(mod)
                )
                continue
            if mod[ 'pos' ] != 'any':
                print( 
                    '''
                    [ WARNING ] myrimatch does only support "any" as position of modifications.
                    [ WARNING ] Continues without modification: {0}'''.format(mod)
                )
                continue
            self.params['myrimatch_dynamic_mods'] += '{0} {1} {2} '.format( mod[ 'aa' ], characters[ n ], mod[ 'mass' ] )


# MinResultScore = "9.9999999999999995e-08" original
# MaxPeptideLength: 30, was 75

        # temporary fix: # this should not be required anymore :)
        self.params['database'] = os.path.abspath( self.params['database'] )

        print('''AvgPrecursorMzTolerance = "1.5m/z"
ClassSizeMultiplier = "2"
CleavageRules = "{enzyme}"
ComputeXCorr = "1"
DecoyPrefix = "{decoy_tag}"
DynamicMods = "{myrimatch_dynamic_mods}"
EstimateSearchTimeOnly = "0"
FragmentMzTolerance = "{frag_mass_tolerance}{frag_mass_tolerance_unit}"
FragmentationAutoRule = "false"
FragmentationRule = "{myrimatch_ions_to_search}"
KeepUnadjustedPrecursorMz = "0"
MaxDynamicMods = "10"
MaxFragmentChargeState = "0"
MaxMissedCleavages = "-{maximum_missed_cleavages}"
MaxPeakCount = "{maximal_accounted_observed_peaks}"
MaxPeptideLength = "{max_pep_length}"
MaxPeptideMass = "10000 Da"
MaxPeptideVariants = "1000000"
MaxResultRank = "{num_match_spec}"
MinMatchedFragments = "5"
MinPeptideLength = "{min_pep_length}"
MinPeptideMass = "{precursor_min_mass}"
MinResultScore = "9.9999999999999995e-08"
MinTerminiCleavages = "{semi_enzyme}"
MonoPrecursorMzTolerance = "{precursor_mass_tolerance_minus}{precursor_mass_tolerance_unit}"
MonoisotopeAdjustmentSet = "{precursor_isotope_range}"
NumBatches = "50"
NumChargeStates = "{precursor_max_charge}"
NumIntensityClasses = "3"
NumMzFidelityClasses = "3"
OutputSuffix = ""
PrecursorMzToleranceRule = "{precursor_mass_type}"
PreferIntenseComplements = "1"
ProteinDatabase = "{database}"
ProteinListFilters = ""
ProteinSamplingTime = "15"
ResultsPerBatch = "{batch_size}"
SpectrumListFilters = "peakPicking true 2-"
StaticMods = "{myrimatch_static_mods}"
StatusUpdateFrequency = "5"
TicCutoffPercentage = "0.97999999999999998"
UseSmartPlusThreeModel = "1"
    '''.format( **self.params ), file=config_file)
        config_file.close()
        return

    def postflight(self):
        '''
        renaming MyriMatch's output file to our desired output file name
        '''
        out_file_root = os.path.join(
            self.params['output_dir_path'],
            self.params['file_root']
        )

        # when the input file is gzipped,
        # myrimatch does not trim the "mzml"-part of
        # the file extension, so sometimes the output
        # file might end with .mzML.mzid ...
        # in any case, we rename it to our desired name
        possible_outfiles = [
            out_file_root + '.mzid',  # most likely case, unless input was gzipped
            out_file_root + '.mzML.mzid',
            out_file_root + '.mzml.mzid',
            out_file_root + '.MZML.mzid',
        ]
        desired_output_name = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        for possible_outfile in possible_outfiles:
            if os.path.exists( possible_outfile ):
                os.rename(
                    possible_outfile,
                    desired_output_name
                )
                break

        return
