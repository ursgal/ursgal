Ursgal Descriptions
-------------------

cleavage_cterm_mass_change
^^^^^^^^^^^^^^^^^^^^^^^^^^

	| The mass added to the peptide C-terminus bz protein cleavage
	| default: *17.00305*

cleavage_nterm_mass_change
^^^^^^^^^^^^^^^^^^^^^^^^^^

	| The mass added to the peptide N-terminus bz protein cleavage
	| default: *1.00794*

semi_enzyme
^^^^^^^^^^^

	| Allows semi-enzymatic peptide ends
	| default: *False*

enzyme
^^^^^^

	| Enzyme: Rule of protein cleavage
	| default: *'trypsin'*

maximum_missed_cleavages
^^^^^^^^^^^^^^^^^^^^^^^^

	| Maximum number of missed cleavages per peptide
	| default: *2.0*

max_pep_length
^^^^^^^^^^^^^^

	| Maximal length of a peptide
	| default: *40.0*

min_pep_length
^^^^^^^^^^^^^^

	| Minimal length of a peptide
	| default: *6.0*

label
^^^^^

	| '15N' if the corresponding amino acid labeling was applied
	| default: *'14N'*

stp_bias
^^^^^^^^

	| Interpretation of peptide phosphorylation models.
	| default: *False*

search_for_saps
^^^^^^^^^^^^^^^

	| search for potential single amino acid polymorphisms
	| default: *False*

modifications
^^^^^^^^^^^^^

	| Modifications are given as a list of strings, each representing the modification of one amino acid. The string consists of four informations seperated by comma: 

'amino acid,type,position,unimod name’ 

 amino acid : specify the modified amino acid as a single letter, use '*' if the amino acid is variable

 type   : specify if it is a fixed (fix) or potential (opt) modification 

 position  : specify the position within the protein/peptide (Prot-N-term, Prot-C-term), use 'any' if the positon is variable 

 unimod name : specify the unimod PSI-MS Name (see unimod.org) 

Examples:

 [ 'M,opt,any,Oxidation' ]   - potential oxidation of Met at any position within a peptide

 [ '*,opt,Prot-N-term,Acetyl' ]  - potential acetylation of any amino acid at the N-terminus of a protein

 [ 'S,opt,any,Phospho' ]   - potential phosphorylation of Serine at any position within a peptide

 ['C,fix,any,Carbamidomethyl’, 'N,opt,any,Deamidated’, 'Q,opt,any,Deamidated’] - fixed carbamidomethylation of Cys and potential deamidation of Asn and/or Gln at any position within a peptide

Additionally, userdefined modifications can be given and are written to a userdefined_unimod.xml in ursgal/kb/ext. Userdefined modifications need to have a unique name instead of the unimod name the chemical composition needs to be given as a Hill notation on the fifth position in the string

Example:

 [ 'S,opt,any,New_mod,C2H5N1O3' ]

	| default: *['*,opt,Prot-N-term,Acetyl', 'M,opt,any,Oxidation']*

max_num_mods
^^^^^^^^^^^^

	| Maximal number of modifications per peptide
	| default: *2.0*

max_num_per_mod
^^^^^^^^^^^^^^^

	| Maximal number of modification sites per peptide for a specific modification, given as a dictionary: {unimod_name : number}
	| default: *{}*

max_mod_alternatives
^^^^^^^^^^^^^^^^^^^^

	| Maximal number of variable modification alternatives, given as C in 2^C
	| default: *6.0*

forbidden_cterm_mods
^^^^^^^^^^^^^^^^^^^^

	| List of modifications (unimod name) that are not allowed to occur at the C-terminus of a peptide
	| default: *[]*

database
^^^^^^^^

	| path/to/database/file
	| default: 

decoy_tag
^^^^^^^^^

	| decoy-specific tag to differentiate between targets and decoys
	| default: *'decoy_'*

score_a_ions
^^^^^^^^^^^^

	| Spectrum: if true, a ions are used in algorithm
	| default: *False*

score_b_ions
^^^^^^^^^^^^

	| Spectrum: if true, b ions are used in algorithm
	| default: *True*

score_c_ions
^^^^^^^^^^^^

	| Spectrum: if true, c ions are used in algorithm
	| default: *False*

score_x_ions
^^^^^^^^^^^^

	| Spectrum: if true, x ions are used in algorithm
	| default: *False*

score_y_ions
^^^^^^^^^^^^

	| Spectrum: if true, y ions are used in algorithm
	| default: *True*

score_z_ions
^^^^^^^^^^^^

	| Spectrum: if true, z ions are used in algorithm
	| default: *False*

score_-h2o_ions
^^^^^^^^^^^^^^^

	| Spectrum: if true, ions loss of H2O are respected in algorithm
	| default: *False*

score_-nh3_ions
^^^^^^^^^^^^^^^

	| Spectrum: if true, ions loss of NH3 are respected in algorithm
	| default: *False*

score_imm_ions
^^^^^^^^^^^^^^

	| Spectrum: if true, immonium ions are respected in algorithm
	| default: *False*

score_int_ions
^^^^^^^^^^^^^^

	| Spectrum: if true, internal fragment ions are respect in algorithm
	| default: *False*

score_z+1_ions
^^^^^^^^^^^^^^

	| Spectrum: if true, z ion plus 1 Da mass are used in algorithm
	| default: *False*

score_z+2_ions
^^^^^^^^^^^^^^

	| Spectrum: if true z ion plus 2 Da mass are used in algorithm
	| default: *False*

compensate_small_fasta
^^^^^^^^^^^^^^^^^^^^^^

	| compensate for very small database files.
	| default: *False*

include_reverse (not used)
^^^^^^^^^^^^^^^^^^^^^^^^^^

	| A target decoy database should be generated independently from
the search engine, e.g. by using the uNode generate_target_decoy
	| default: 

spec_dynamic_range
^^^^^^^^^^^^^^^^^^

	| Spectrum, internal normalization: The highest peak (intensity) within a spectrum is set to given value and all other peaks are normalized to this peak. If the normalized value is less than 1 he peak is rejected. 
	| default: *100.0*

precursor_mass_type
^^^^^^^^^^^^^^^^^^^

	| Precursor mass type: monoisotopic or average
	| default: *'monoisotopic', (average)*

precursor_mass_tolerance_unit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Precursor mass tolerance unit: available in ppm (parts-per-millon), Da (Dalton) or mmu (Milli mass unit)
	| default: *'ppm'*

precursor_mass_tolerance_minus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Precursor mass tolerance: lower mass tolerance of measured and calculated parent ion M+H
	| default: *5.0*

precursor_mass_tolerance_plus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Precursor mass tolerance: higher mass tolerance of measured and calculated parent ion M+H
	| default: *5.0*

precursor_isotope_range
^^^^^^^^^^^^^^^^^^^^^^^

	| Error range for incorrect carbon isotope parent ion assignment
	| default: *'0,1'*

precursor_min_mass
^^^^^^^^^^^^^^^^^^

	| minimal parent ion mass
	| default: *400.0*

precursor_min_charge
^^^^^^^^^^^^^^^^^^^^

	| minimal accepted parent ion charge
	| default: *1.0*

precursor_max_charge
^^^^^^^^^^^^^^^^^^^^

	| maximal accepted parent ion charge
	| default: *5.0*

precursor_ppm_offset
^^^^^^^^^^^^^^^^^^^^

	| Precursor offset in ppm
	| default: *None*

frag_mass_type
^^^^^^^^^^^^^^

	| Fragment mass type: monoisotopic or average
	| default: *'monoisotopic'*

frag_mass_tolerance_unit
^^^^^^^^^^^^^^^^^^^^^^^^

	| Fragment mass tolerance unit: available in ppm (parts-per-millon), Da (Dalton) or mmu (Milli mass unit)
	| default: *'ppm'*

frag_mass_tolerance
^^^^^^^^^^^^^^^^^^^

	| mass tolerance of measured and calculated fragment ions
	| default: *20.0*

frag_mass_tolerance_unit
^^^^^^^^^^^^^^^^^^^^^^^^

	| Fragment mass tolerance unit: available in ppm (parts-per-millon), Da (Dalton) or mmu (Milli mass unit)
	| default: *ppm'*

frag_mass_tolerance
^^^^^^^^^^^^^^^^^^^

	| Fragment mass type: monoisotopic or average
	| default: *'monoisotopic'*

frag_min_mz
^^^^^^^^^^^

	| minimal considered fragment ion m/z
	| default: *150.0*

frag_method
^^^^^^^^^^^

	| used fragmentatiom method. e.g. collision-induced dissociation (CID), electron-capture dissociation (ECD), electron-transfer dissociation (ETD), Higher-energy C-trap dissociation (HCD)
	| default: *'hcd'*

mininimal_required_observed_peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Mimimum number of peaks in the spectrum to be considered.
	| default: *5.0*

mininimal_required_matched_peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Mimimum number of matched ions required for a peptide to be scored
	| default: *4.0*

num_match_spec
^^^^^^^^^^^^^^

	| This parameter sets the maximum number of peptide spectrum matches to report for each spectrum
	| default: *10.0*

neutral_loss_enabled
^^^^^^^^^^^^^^^^^^^^

	| Neutral losses enabled for spectrum algorithm: set  True or False
	| default: *False*

neutral_loss_mass
^^^^^^^^^^^^^^^^^

	| Sets the centre of the window for ignoring neutral molecule losses.
	| default: *0.0*

maximal_accounted_observed_peaks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Maximum number of peaks from a spectrum used. 
	| default: *50.0*

neutral_loss_window
^^^^^^^^^^^^^^^^^^^

	| Neutral loss window: sets the width of the window for ignoring neutral molecule losses.
	| default: *0.0*

batch_size
^^^^^^^^^^

	| sets the number of sequences loaded in as a batch from the database file
	| default: *100000.0*

noise_suppression_enabled
^^^^^^^^^^^^^^^^^^^^^^^^^

	| used for noise suppresssion
	| default: *False*

decoy_generation_mode
^^^^^^^^^^^^^^^^^^^^^

	| Decoy database: Creates a target decoy database based on shuffling of peptides or complete reversing the protein sequence (reverse_protein).
	| default: *'shuffle_peptide'*

force
^^^^^

	| Force: True or False to overwrite the existing files 
	| default: *False*

cpus
^^^^

	| Cpus: set number of used cpu
	| default: *multiprocessing.cpu_count() - 1*

output_suffix
^^^^^^^^^^^^^

	| Output suffix: 'string'
	| default: *' '*

del_from_params_before_json_dump
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| parameters deleted before the json is dumped
	| default: *['grouped_psms']*

rt_pickle_name
^^^^^^^^^^^^^^

	| name of the pickle that is used to map the retention time
	| default: *_ursgal_lookup.pkl'*

json_extension
^^^^^^^^^^^^^^

	| Extention of json file
	| default: *.u.json'*

helper_extension
^^^^^^^^^^^^^^^^

	| Helper extention: 'string'
	| default: *'.u_helper'*

remove_temporary_files
^^^^^^^^^^^^^^^^^^^^^^

	| Remove temporary files: True or False
	| default: *False*

mzidentml_converter_version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| mzidentml converter version: 'version name'
	| default: *'mzidentml_lib_1_6_10'*

mzml2mgf_converter_version
^^^^^^^^^^^^^^^^^^^^^^^^^^

	| mzml to mgf converter version: 'version name'
	| default: *'mzml2mgf_1_0_0'*

unify_csv_converter_version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| unify csv converter version: 'version name'
	| default: *'unify_csv_1_0_0'*

filter_csv_converter_version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| filter csv converter version: 'version name'
	| default: *'filter_csv_1_0_0'*

show_unodes_in_development
^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Show ursgal nodes in development: False or True
	| default: *False*

search_engines_create_folders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Create folders for search engines. True or False
	| default: *True*

log_enabled
^^^^^^^^^^^

	| Will redirect sys.stdout to the logfile, default name: ursgal.log
	| default: *False*

log_file_name
^^^^^^^^^^^^^

	| This can be used to specify a different log file path
	| default: *None*

raw_ident_csv_suffix
^^^^^^^^^^^^^^^^^^^^

	| CSV suffix of raw indentification: this is the conversion result after CSV conversion but before adding retention time
	| default: *'.csv'*

ident_csv_suffix
^^^^^^^^^^^^^^^^

	| CSV suffix of identification: 'string', CSV-file which contains identifications with retention times.
	| default: *'idents.csv'*

validated_ident_csv_suffix
^^^^^^^^^^^^^^^^^^^^^^^^^^

	| CSV suffix of validated idententification:'string', CSV-file which contains PSMs validated with validation tools 
	| default: *'validated.csv'*

maximum_pep_for_ident_csv
^^^^^^^^^^^^^^^^^^^^^^^^^

	| Maximum value for PEP (posterior error probability): Threshold for identifications put in CSV-files.
	| default: *0.1*

output_file_type
^^^^^^^^^^^^^^^^

	| Output file type
	| default: *None*

input_file_type
^^^^^^^^^^^^^^^

	| Input file type
	| default: *None*

input_file
^^^^^^^^^^

	| Input file: path/to/input/file
	| default: 

java_-Xmx
^^^^^^^^^

	| set maximum Java heap size
	| default: *'13312m'*

number_of_mz_decimals
^^^^^^^^^^^^^^^^^^^^^

	| Number of decimals for m/z mass
	| default: *5.0*

number_of_i_decimals
^^^^^^^^^^^^^^^^^^^^

	| Number of decimals for intensity (peak) 
	| default: *5.0*

machine_offset_in_ppm
^^^^^^^^^^^^^^^^^^^^^

	| Machine offset 
	| default: *None*

scan_exclusion_list
^^^^^^^^^^^^^^^^^^^

	| spectra rejected during mzml2mgf conversion
	| default: *None*

scan_skip_modulo_step
^^^^^^^^^^^^^^^^^^^^^

	| include only the n'th spectrum during mzml2mgf conversion
	| default: *None*

compress_output
^^^^^^^^^^^^^^^

	| Compress output: True or False to .GZ
	| default: *False*

compress_after_post_flight
^^^^^^^^^^^^^^^^^^^^^^^^^^

	| Compress after post flight: True or False to .GZ
	| default: *False*

compress_ext_exculsion'
^^^^^^^^^^^^^^^^^^^^^^^

	| file type excluded from compression
	| default: *['.csv']*

csv_filter_rules
^^^^^^^^^^^^^^^^

	| Rules are defined as list of tuples with the first tuple element as the column name/csv fieldname, the second tuple element the rule and the third tuple element the value which should be compared
	| default: *None*

write_unfiltered_results
^^^^^^^^^^^^^^^^^^^^^^^^

	| writes rejected results if True
	| default: *False*

