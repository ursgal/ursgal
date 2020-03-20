#!/usr/bin/env python
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
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'Myrimatch',
        'version'                     : '2.1.138',
        'release_date'                : None,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'            : ['.mzML'],
        'output_extensions'           : ['.mzid'],
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'               : True,
        'create_own_folder'           : True,
        'utranslation_style'          : 'myrimatch_style_1',
        'engine' : {
            'linux' : {
                '64bit' : {
                    'exe'            : 'myrimatch_2_1_138',
                    'url'            : '',
                    'zip_md5'        : 'bf5df092579fe3f3d1364c835fe2f3ea',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Tabb DL, Fernando CG, Chambers MC. (2007) MyriMatch: highly '\
            'accurate tandem mass spectral peptide identification by '\
            'multivariate hypergeometric analysis.',
    }

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
            self.params['translations']['mzml_input_file'] = input_file
        elif input_file.lower().endswith('.mgf'):
            # use dark magic to find the mzml file that corresponds to the mgf:
            self.params['translations']['mzml_input_file'] = \
                self.meta_unodes['ucontroller'].get_mzml_that_corresponds_to_mgf( input_file )
            self.print_info(
                ('Since MyriMatch cannot read MGF input files, the '
                 'corresponding mzML file {0} will be used instead.'
                ).format( os.path.abspath(self.params['translations']['mzml_input_file']) ),
                caller="INFO" )
        else:
            raise Exception('MyriMatch input spec file must be in mzML format!')

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        self.params['translations']['myrimatch_ions_to_search'] = []
        for ion in ['a', 'b', 'c', 'x', 'y', 'z']:
            if ion in self.params['translations']['score_ion_list']:
                self.params['translations']['myrimatch_ions_to_search'].append(ion)
        self.params['translations']['myrimatch_ions_to_search'] = 'manual:'+','.join(self.params['translations']['myrimatch_ions_to_search'])

        self.params['translations']['myrimatch_config_file_path'] = \
            '{output_file_incl_path}_myrimatch_params.cfg'.format( **self.params['translations'])
        self.created_tmp_files.append( self.params['translations']['myrimatch_config_file_path'])
        self.write_param_file()

        self.params['command_list'] = [
            self.exe,
            '-cfg', '{myrimatch_config_file_path}'.format(**self.params['translations']),
            '{mzml_input_file}'.format(**self.params['translations']),
            '-workdir', '{output_dir_path}'.format(**self.params),
            '-cpus', '{cpus}'.format(**self.params['translations']),
            # '-dump'
        ]


    def write_param_file( self ):
        ''' Writes a file containing all parameters for the search '''

        config_file= open(self.params['translations']['myrimatch_config_file_path'], 'w') #param file must be in execution folder
        self.params['translations']['myrimatch_static_mods'] = ''
        self.params['translations']['myrimatch_dynamic_mods'] = ''

        if self.params['translations']['label'] == '15N':
            for aminoacid, N15_Diff in ursgal.ukb.DICT_15N_DIFF.items():
                existing = False
                for mod in self.params[ 'mods' ][ 'fix' ]:
                    if aminoacid == mod[ 'aa' ]:
                        mod[ 'mass' ] += N15_Diff
                        existing = True
                if existing == True:
                    continue
                self.params['translations']['myrimatch_static_mods']+= '{0} {1} '.format( aminoacid, N15_Diff )

        for mod in self.params[ 'mods' ][ 'fix' ]:
            self.params['translations']['myrimatch_static_mods'] += '{0} {1} '.format( mod[ 'aa' ], mod[ 'mass' ] )

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
            self.params['translations']['myrimatch_dynamic_mods'] += '{0} {1} {2} '.format( mod[ 'aa' ], characters[ n ], mod[ 'mass' ] )

        print(
            '''
            [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
            [ WARNING ] need to be combined for Myrimatch (use of symmetric tolerance window).
            [ WARNING ] The arithmetic mean is used.
            '''
        )
        self.params['translations']['precursor_mass_tolerance'] = ( float(self.params['translations']['precursor_mass_tolerance_plus']) + \
                                                    float(self.params['translations']['precursor_mass_tolerance_minus']) ) \
                                                / 2.0

        # temporary fix: # this should not be required anymore :)
        self.params['translations']['database'] = os.path.abspath( self.params['translations']['database'] )

        print('''
ClassSizeMultiplier = "{myrimatch_class_size_multiplier}"
CleavageRules = "{enzyme}"
ComputeXCorr = "{compute_xcorr}"
DecoyPrefix = "{decoy_tag}"
DynamicMods = "{myrimatch_dynamic_mods}"
EstimateSearchTimeOnly = "0"
FragmentMzTolerance = "{frag_mass_tolerance}{frag_mass_tolerance_unit}"
FragmentationAutoRule = "false"
FragmentationRule = "{myrimatch_ions_to_search}"
KeepUnadjustedPrecursorMz = "0"
MaxDynamicMods = "{max_num_mods}"
MaxMissedCleavages = "{max_missed_cleavages}"
MaxPeakCount = "{max_accounted_observed_peaks}"
MaxPeptideLength = "{max_pep_length}"
MaxPeptideMass = "{precursor_max_mass} Da"
MaxPeptideVariants = "{max_pep_var}"
MaxResultRank = "{num_match_spec}"
MinMatchedFragments = "{min_required_matched_peaks}"
MinPeptideLength = "{min_pep_length}"
MinPeptideMass = "{precursor_min_mass}"
MinResultScore = "{min_output_score}"
MinTerminiCleavages = "{semi_enzyme}"
MonoPrecursorMzTolerance = "{precursor_mass_tolerance}{precursor_mass_tolerance_unit}"
MonoisotopeAdjustmentSet = "{precursor_isotope_range}"
NumBatches = "{batch_size}"
NumChargeStates = "{precursor_max_charge}"
NumIntensityClasses = "{myrimatch_num_int_classes}"
NumMzFidelityClasses = "{myrimatch_num_mz_fidelity_classes}"
OutputSuffix = ""
OutputFormat = "mzIdentML"
PrecursorMzToleranceRule = "{precursor_mass_type}"
ProteinDatabase = "{database}"
ProteinSamplingTime = "{myrimatch_prot_sampl_time}"
SpectrumListFilters = "peakPicking true 2-"
StaticMods = "{myrimatch_static_mods}"
StatusUpdateFrequency = "5"
TicCutoffPercentage = "{myrimatch_tic_cutoff}"
UseSmartPlusThreeModel = "{myrimatch_smart_plus_three}"
    '''.format(**self.params['translations']), file=config_file)
        config_file.close()
        return

    def postflight(self):
        '''
        renaming MyriMatch's output file to our desired output file name
        '''
        if self.params['prefix'] is None:
            out_file_root = os.path.join(
                self.params['output_dir_path'],
                self.params['file_root']
            )
        else:
            out_file_root = os.path.join(
                self.params['output_dir_path'],
                self.params['file_root'].replace(
                    self.params['prefix'] + '_',
                    ''
                )
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
            if os.path.exists(possible_outfile):
                os.rename(
                    possible_outfile,
                    desired_output_name
                )
                break

        return
