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
    'output_extension'          : '.mzid',
    'input_types'               : ['.mgf', '.mzML'],
    'create_own_folder'         : True,
    'citation'                  : 'Kim S, Mischerikow N, Bandeira N, '\
        'Navarro JD, Wich L, Mohammed S, Heck AJ, Pevzner PA. (2010) '\
        'The Generating Function of CID, ETD, and CID/ETD Pairs of '\
        'Tandem Mass Spectra: Applications to Database Search.',

    'include_in_git'            : False,
}

DEFAULT_PARAMS = {
    'validation_score_field'    : 'MS-GF:SpecEValue',
    'evalue_field'              : 'MS-GF:SpecEValue',
    'validation_minimum_score'  : 1e-100,
    'bigger_scores_better'      : False,
    'max_num_mods'              : 2,
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    'nonspecific'            : 0,
    'trypsin'                : 1,
    'chymotrypsin'           : 2,
    'lysc'                   : 3,
    'lysn'                   : 4,
    'glutamyl_endopeptidase' : 5,
    'argc'                   : 6,
    'aspn'                   : 7,
    'alpha_lp'               : 8,
    'no_cleavage'            : 9,
    'cid'                    : 1,
    'etd'                    : 2,
    'hcd'                    : 3,
    'da'                     : 'Da',
    'low_res_LTQ'            : 0,
    'high_res_LTQ'           : 1,
    'tof'                    : 2,
    'q_exactive'             : 3,
}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
    'semi_enzyme' : {
        True : 1,
        False : 2
    }
}

USED_USEARCH_PARAMS = set( [
    'modifications',
    'semi_enzyme',
    'enzyme',
    'precursor_mass_tolerance_unit',
    'precursor_mass_tolerance_minus',
    'precursor_mass_tolerance_plus',
    'precursor_isotope_range',
    'instrument',
    'cpus',
    'database',
    'max_pep_length',
    'min_pep_length',
    'num_match_spec',
    'frag_method',
    'precursor_min_charge',
    'precursor_max_charge',
    'validation_score_field',
    'evalue_field',
    'validation_minimum_score',
    'bigger_scores_better',
    'max_num_mods',
    'java_-Xmx',
] )



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
