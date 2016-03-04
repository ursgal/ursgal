#!/usr/bin/env python3.4
import ursgal
import os


class msgfplus_v9979( ursgal.UNode ):
    """
    MSGF+ UNode
    Parameter options at https://bix-lab.ucsd.edu/pages/viewpage.action?pageId=13533355

    Reference:
    Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: Applications to Database Search.
    """
    META_INFO = {
        'engine_type' : {
            'search_engine' : True,
        },
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'MSGFPlus.jar',
                    'url'            : 'http://proteomics.ucsd.edu/Software/MSGFPlus/MSGFPlus.zip',
                    'zip_md5'        : '82a3e2204ff698e260ac9f89d3880b59',
                    'additional_exe' : [],
                },
            },
        },
        'utranslation_style'    : 'msgfplus_style_1',
        'compress_raw_search_results' : True,
        'output_extension'          : '.mzid',
        'input_types'               : ['.mgf', '.mzML', '.mzXML', '.ms2', '.pkl' ,'_dta.txt'],
        'create_own_folder'         : True,
        'citation'                  : 'Kim S, Mischerikow N, Bandeira N, '\
            'Navarro JD, Wich L, Mohammed S, Heck AJ, Pevzner PA. (2010) '\
            'The Generating Function of CID, ETD, and CID/ETD Pairs of '\
            'Tandem Mass Spectra: Applications to Database Search.',
        'in_development'            : False,
        'include_in_git'            : False,
    }

    def __init__(self, *args, **kwargs):
        super(msgfplus_v9979, self).__init__(*args, **kwargs)
        pass


    def preflight( self ):
        '''
        Formatting the command line via self.params

        Modifications file will be created in the output folder

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

        self.params['modification_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '_Mods.txt'
        )
        self.created_tmp_files.append( self.params['modification_file'] )

        mods_file = open( self.params['modification_file'], 'w', encoding = 'UTF-8' )
        modifications = []

        if self.params['label'] == '15N':
            for aminoacid, N15_Diff in ursgal.kb.ursgal.DICT_15N_DIFF.items():
                existing = False
                for mod in self.params[ 'mods' ][ 'fix' ]:
                    if aminoacid == mod[ 'aa' ]:
                        mod[ 'mass' ] += N15_Diff
                        mod[ 'name' ] += '_15N_{0}'.format(aminoacid)
                        existing = True
                if existing == True:
                    continue
                else:
                    modifications.append( '{0},{1},fix,any,15N_{1}'.format( N15_Diff, aminoacid ) )

        for t in [ 'fix', 'opt' ]:
            for mod in self.params[ 'mods' ][ t ]:
                modifications.append( '{0},{1},{2},{3},{4}'.format(mod[ 'mass' ], mod[ 'aa' ], t, mod[ 'pos' ], mod[ 'name' ] ) )

        for mod in modifications:
            print( mod, file = mods_file )

        mods_file.close()


        self.params[ 'command_list' ] = [
            'java', '{java_-Xmx_key}{java_-Xmx}'.format( **self.params), '-jar', self.exe, # path 2 MS-GF+ executable
            '{mgf_input_file_key}'.format( **self.params), '{mgf_input_file}'.format( **self.params), # SpectrumFile (*.mzML, *.mzXML, *.mgf, *.ms2, *.pkl or *_dta.txt)
            '{database_key}'.format(**self.params), '{database}'.format(**self.params), # DatabaseFile (*.fasta or *.fa)
            '{output_file_incl_path_key}'.format(**self.params), '{output_file_incl_path}'.format(**self.params), # OutputFile (*.mzid) (Default: SpectrumFileName.mzid)
            '{precursor_mass_tolerance_unit}'.format(**self.params), '{precursor_mass_tolerance_minus}{precursor_mass_tolerance_unit}, {precursor_mass_tolerance_plus}{precursor_mass_tolerance_unit}'.format(**self.params), # PrecursorMassTolerance] (e.g. 2.5Da, 20ppm or 0.5Da,2.5Da, Default: 20ppm)
            '-ti', '{precursor_isotope_range}'.format(**self.params), # IsotopeErrorRange (Range of allowed isotope peak errors, Default:0,1)
            '-thread', '{cpus}'.format(**self.params), # NumThreads] (Number of concurrent threads to be executed, Default: Number of available cores)
            '-tda', '0', # (0: don't search decoy database (Default), 1: search decoy database)
            '-m', '{frag_method}'.format(**self.params), # FragmentMethodID (0: As written in the spectrum or CID if no info (Default), 1: CID, 2: ETD, 3: HCD)
            '-inst', '{instrument}'.format(**self.params), # InstrumentID (0: Low-res LCQ/LTQ (Default), 1: High-res LTQ, 2: TOF, 3: Q-Exactive)
            '-e', '{enzyme}'.format(**self.params), # EnzymeID (0: unspecific cleavage, 1: Trypsin (Default), 2: Chymotrypsin, 3: Lys-C, 4: Lys-N, 5: glutamyl endopeptidase, 6: Arg-C, 7: Asp-N, 8: alphaLP, 9: no cleavage)
            '-protocol', '{msgfplus_protocol_id}' # (0: NoProtocol (Default), 1: Phosphorylation, 2: iTRAQ, 3: iTRAQPhospho)
            '-ntt', '{semi_enzyme}'.format(**self.params), #(Number of Tolerable Termini, Default: 2)
            '-mod', '{modification_file}'.format(**self.params), # ModificationFileName (Modification file, Default: standard amino acids with fixed C+57)
            '-minLength', '{min_pep_length}'.format(**self.params), # MinPepLength (Minimum peptide length to consider, Default: 6)
            '-maxLength', '{max_pep_length}'.format(**self.params), # MaxPepLength (Maximum peptide length to consider, Default: 40)
            '-minCharge', '{precursor_min_charge}'.format(**self.params), # MinCharge (Minimum precursor charge to consider if charges are not specified in the spectrum file, Default: 2)
            '-maxCharge', '{precursor_max_charge}'.format(**self.params), # MaxCharge (Maximum precursor charge to consider if charges are not specified in the spectrum file, Default: 3)
            '-n', '{num_match_spec}'.format(**self.params), # NumMatchesPerSpec (Number of matches per spectrum to be reported, Default: 1)
            '-addFeatures', '1', # (0: output basic scores only (Default), 1: output additional features)
        ]

        return self.params
