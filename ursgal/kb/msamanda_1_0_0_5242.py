META_INFO={
    'engine_type': {
        'search_engine': True,
    },
    'output_extension'          : '.csv',
    'input_types'               : ['.mgf'],
    'create_own_folder'         : True,
    'citation'                  : 'Dorfer V, Pichler P, Stranzl T, '\
        'Stadlmann J, Taus T, Winkler S, Mechtler K. (2014) MS Amanda, '\
        'a universal identification algorithm optimized for high accuracy '\
        'tandem mass spectra.',
    'include_in_git'            : None,
    'cannot_distribute'         : True,
  'in_development'            : True,
    'engine': {
        'win32' : {
            '64bit' : {
                'exe'            : 'MSAmanda.exe',
                'url'            : '',
                'zip_md5'        : None,
                'additional_exe' : [],
            },
        },
    },

}

DEFAULT_PARAMS={
    'validation_score_field'    : 'Amanda:Score',
    'evalue_field'              : 'Amanda:Weighted Probability',
    'validation_minimum_score'  : 0,
    'bigger_scores_better'      : True,
    'input_type'                : 'mgf',
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    'nonspecific'            : 'No-Enzyme',
    'trypsin'                : 'Trypsin',
    'lysc'                   : 'LysC',
    'gluc'                   : 'GluC',
    'no_cleavage'            : 'No-Cleavage',
    'da'                     : 'Da',

    'Scan Number'        : 'Spectrum ID',
    'Title'              : 'Spectrum Title',
    'Sequence'           : 'Sequence',
    'Protein Accessions' : 'proteinacc_start_stop_pre_post_;',
    'Modifications'      : 'Modifications',
    'Charge'             : 'Charge',
    'm/z'                : 'Exp m/z',
    'Amanda Score'       : 'Amanda:Score',
    'Weighted Probability' : 'Amanda:Weighted Probability',
    'Filename'           : 'Filename',
    'RT'                 : 'Retention Time (s)',
    'Rank'               : 'Rank',

    }

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
    }

USED_USEARCH_PARAMS = set( [
    'modifications',
    'enzyme',
    'maximum_missed_cleavages',
    'precursor_mass_tolerance_unit',
    'precursor_mass_tolerance_minus',
    'precursor_mass_tolerance_plus',
    'precursor_mass_type',
    'precursor_min_charge',
    'precursor_max_charge',
    'frag_mass_tolerance_unit',
    'frag_mass_tolerance',
    'score_a_ions',
    'score_b_ions',
    'score_c_ions',
    'score_x_ions',
    'score_y_ions',
    'score_z_ions',
    'score_-h2o_ions',
    'score_-nh3_ions',
    'score_imm_ions',
    'score_int_ions',
    'score_z+1_ions',
    'score_z+2_ions',
    'cpus',
    'database',
    'validation_score_field',
    'evalue_field',
    'validation_minimum_score',
    'bigger_scores_better',
    'input_type',
    ]
     )



# Usage: java -Xmx3500M -jar MSGFPlus.jar
    # -s SpectrumFile (*.mzML, *.mzXML, *.mgf, *.ms2, *.pkl or *_dta.txt)
       # Spectra should be centroided. Profile spectra will be ignored.
	# -d DatabaseFile (*.fasta or *.fa)
	# [-o OutputFile (*.mzid)] (Default: SpectrumFileName.mzid)
	# [-t PrecursorMassTolerance] (e.g. 2.5Da, 20ppm or 0.5Da,2.5Da, Default: 20ppm)
	   # Use comma to set asymmetric values. E.g. "-t 0.5Da,2.5Da" will set 0.5Da to the minus (expMass<theoMass) and 2.5Da to plus (expMass>theoMass)
	# [-ti IsotopeErrorRange] (Range of allowed isotope peak errors, Default:0,1)
	   # Takes into account of the error introduced by chooosing a non-monoisotopic peak for fragmentation.
	   # On Windows, put the range inside "" (e.g. "0,1").
	   # The combination of -t and -ti determins the precursor mass tolerance.
	   # E.g. "-t 20ppm -ti -1,2" tests abs(exp-calc-n*1.00335Da)<20ppm for n=-1, 0, 1, 2.
	# [-thread NumThreads] (Number of concurrent threads to be executed, Default: Number of available cores)
	# [-tda 0/1] (0: don't search decoy database (Default), 1: search decoy database)
	# [-m FragmentMethodID] (0: As written in the spectrum or CID if no info (Default), 1: CID, 2: ETD, 3: HCD)
	# [-inst InstrumentID] (0: Low-res LCQ/LTQ (Default), 1: High-res LTQ, 2: TOF, 3: Q-Exactive)
	# [-e EnzymeID] (0: unspecific cleavage, 1: Trypsin (Default), 2: Chymotrypsin, 3: Lys-C, 4: Lys-N, 5: glutamyl endopeptidase, 6: Arg-C, 7: Asp-N, 8: alphaLP, 9: no cleavage)
	# [-protocol ProtocolID] (0: NoProtocol (Default), 1: Phosphorylation, 2: iTRAQ, 3: iTRAQPhospho)
	# [-ntt 0/1/2] (Number of Tolerable Termini, Default: 2)
	   # E.g. For trypsin, 0: non-tryptic, 1: semi-tryptic, 2: fully-tryptic peptides only.
	# [-mod ModificationFileName] (Modification file, Default: standard amino acids with fixed C+57)
	# [-minLength MinPepLength] (Minimum peptide length to consider, Default: 6)
	# [-maxLength MaxPepLength] (Maximum peptide length to consider, Default: 40)
	# [-minCharge MinCharge] (Minimum precursor charge to consider if charges are not specified in the spectrum file, Default: 2)
	# [-maxCharge MaxCharge] (Maximum precursor charge to consider if charges are not specified in the spectrum file, Default: 3)
	# [-n NumMatchesPerSpec] (Number of matches per spectrum to be reported, Default: 1)
	# [-addFeatures 0/1] (0: output basic scores only (Default), 1: output additional features)
# Example (high-precision): java -Xmx3500M -jar MSGFPlus.jar -s test.mzXML -d IPI_human_3.79.fasta -t 20ppm -ti "-1,2" -ntt 0 -tda 1 -o testMSGFPlus.mzid
# Example (low-precision): java -Xmx3500M -jar MSGFPlus.jar -s test.mzXML -d IPI_human_3.79.fasta -t 0.5Da,2.5Da -ntt 0 -tda 1 -o testMSGFPlus.mzid

# https://bix-lab.ucsd.edu/pages/viewpage.action?pageId=13533355
