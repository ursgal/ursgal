ursgal_params=
{'batch_size': {'AVAILABLE_IN_UNODE': ['xtandem'],
                'BUTTOM_TYPE': '',
                'DEFAULT_VALUE': '100000',
                'DESCRIPTION': 'sets the number of sequences loaded in as a '
                               'batch from the database file',
                'TRANSLATION': {'xtandem': 'spectrum, sequence batch size'},
                'VALUE_RANGE': ''},
 'cleavage_cterm_mass_change': {'AVAILABLE_IN_UNODE': ['xtandem'],
                                'BUTTOM_TYPE': '',
                                'DEFAULT_VALUE': '17.00305',
                                'DESCRIPTION': 'The mass added to the peptide '
                                               'C-terminus bz protein cleavage',
                                'TRANSLATION': {'xtandem': 'protein, cleavage '
                                                           'C-terminal mass '
                                                           'change'},
                                'VALUE_RANGE': ''},
 'cleavage_nterm_mass_change': {'AVAILABLE_IN_UNODE': ['xtandem'],
                                'BUTTOM_TYPE': '',
                                'DEFAULT_VALUE': '1.00794',
                                'DESCRIPTION': 'The mass added to the peptide '
                                               'N-terminus bz protein cleavage',
                                'TRANSLATION': {'xtandem': 'protein, cleavage '
                                                           'N-terminal mass '
                                                           'change'},
                                'VALUE_RANGE': ''},
 'compensate_small_fasta': {'AVAILABLE_IN_UNODE': ['xtandem'],
                            'BUTTOM_TYPE': '',
                            'DEFAULT_VALUE': 'False',
                            'DESCRIPTION': 'compensate for very small database '
                                           'files.',
                            'TRANSLATION': {'xtandem': 'scoring, cyclic '
                                                       'permutation'},
                            'VALUE_RANGE': ''},
 'compress_after_post_flight': {'AVAILABLE_IN_UNODE': [],
                                'BUTTOM_TYPE': '',
                                'DEFAULT_VALUE': 'False',
                                'DESCRIPTION': 'Compress after post flight: '
                                               'True or False to .GZ',
                                'TRANSLATION': {},
                                'VALUE_RANGE': ''},
 "compress_ext_exculsion'": {'AVAILABLE_IN_UNODE': [],
                             'BUTTOM_TYPE': '',
                             'DEFAULT_VALUE': "['.csv']",
                             'DESCRIPTION': 'file type excluded from '
                                            'compression',
                             'TRANSLATION': {},
                             'VALUE_RANGE': ''},
 'compress_output': {'AVAILABLE_IN_UNODE': [],
                     'BUTTOM_TYPE': '',
                     'DEFAULT_VALUE': 'False',
                     'DESCRIPTION': 'Compress output: True or False to .GZ',
                     'TRANSLATION': {},
                     'VALUE_RANGE': ''},
 'cpus': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa', 'msgfplus', 'myrimatch'],
          'BUTTOM_TYPE': '',
          'DEFAULT_VALUE': 'multiprocessing.cpu_count() - 1',
          'DESCRIPTION': 'Cpus: set number of used cpu',
          'TRANSLATION': {'msgfplus': '-thread',
                          'myrimatch': '-cpus <integer>',
                          'omssa': '-nt',
                          'xtandem': 'spectrum, threads'},
          'VALUE_RANGE': ''},
 'csv_filter_rules': {'AVAILABLE_IN_UNODE': [],
                      'BUTTOM_TYPE': '',
                      'DEFAULT_VALUE': 'None',
                      'DESCRIPTION': 'Rules are defined as list of tuples with '
                                     'the first tuple element as the column '
                                     'name/csv fieldname, the second tuple '
                                     'element the rule and the third tuple '
                                     'element the value which should be '
                                     'compared',
                      'TRANSLATION': {},
                      'VALUE_RANGE': ''},
 'database': {'AVAILABLE_IN_UNODE': ['omssa', 'msgfplus', 'myrimatch'],
              'BUTTOM_TYPE': '',
              'DEFAULT_VALUE': '',
              'DESCRIPTION': 'path/to/database/file',
              'TRANSLATION': {'msgfplus': '-d',
                              'myrimatch': '-ProteinDatabase <string>',
                              'omssa': '-d'},
              'VALUE_RANGE': ''},
 'decoy_generation_mode': {'AVAILABLE_IN_UNODE': [],
                           'BUTTOM_TYPE': '',
                           'DEFAULT_VALUE': "'shuffle_peptide'",
                           'DESCRIPTION': 'Decoy database: Creates a target '
                                          'decoy database based on shuffling '
                                          'of peptides or complete reversing '
                                          'the protein sequence '
                                          '(reverse_protein).',
                           'TRANSLATION': {},
                           'VALUE_RANGE': ''},
 'decoy_tag': {'AVAILABLE_IN_UNODE': [],
               'BUTTOM_TYPE': '',
               'DEFAULT_VALUE': "'decoy_'",
               'DESCRIPTION': 'decoy-specific tag to differentiate between '
                              'targets and decoys',
               'TRANSLATION': {},
               'VALUE_RANGE': ''},
 'del_from_params_before_json_dump': {'AVAILABLE_IN_UNODE': [],
                                      'BUTTOM_TYPE': '',
                                      'DEFAULT_VALUE': "['grouped_psms']",
                                      'DESCRIPTION': 'parameters deleted '
                                                     'before the json is '
                                                     'dumped',
                                      'TRANSLATION': {},
                                      'VALUE_RANGE': ''},
 'enzyme': {'AVAILABLE_IN_UNODE': ['xtandem',
                                   'omssa',
                                   'msgfplus',
                                   'myrimatch',
                                   'msamanda'],
            'BUTTOM_TYPE': '',
            'DEFAULT_VALUE': "'trypsin'",
            'DESCRIPTION': 'Enzyme: Rule of protein cleavage',
            'TRANSLATION': {'msamanda': 'enzyme specificity',
                            'msgfplus': '-e',
                            'myrimatch': '-CleavageRules<str>',
                            'omssa': '-e',
                            'xtandem': 'protein, cleavage site'},
            'VALUE_RANGE': ''},
 'filter_csv_converter_version': {'AVAILABLE_IN_UNODE': [],
                                  'BUTTOM_TYPE': '',
                                  'DEFAULT_VALUE': "'filter_csv_1_0_0'",
                                  'DESCRIPTION': 'filter csv converter '
                                                 "version: 'version name'",
                                  'TRANSLATION': {},
                                  'VALUE_RANGE': ''},
 'forbidden_cterm_mods': {'AVAILABLE_IN_UNODE': ['xtandem'],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': '[]',
                          'DESCRIPTION': 'List of modifications (unimod name) '
                                         'that are not allowed to occur at the '
                                         'C-terminus of a peptide',
                          'TRANSLATION': {'xtandem': 'residue, potential '
                                                     'modification mass'},
                          'VALUE_RANGE': ''},
 'force': {'AVAILABLE_IN_UNODE': [],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': 'False',
           'DESCRIPTION': 'Force: True or False to overwrite the existing '
                          'files',
           'TRANSLATION': {},
           'VALUE_RANGE': ''},
 'frag_mass_tolerance': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa'],
                         'BUTTOM_TYPE': '',
                         'DEFAULT_VALUE': "'monoisotopic'",
                         'DESCRIPTION': 'Fragment mass type: monoisotopic or '
                                        'average',
                         'TRANSLATION': {'omssa': '-to',
                                         'xtandem': 'spectrum, fragment '
                                                    'monoisotopic mass error'},
                         'VALUE_RANGE': ''},
 'frag_mass_tolerance_unit': {'AVAILABLE_IN_UNODE': ['xtandem'],
                              'BUTTOM_TYPE': '',
                              'DEFAULT_VALUE': "ppm'",
                              'DESCRIPTION': 'Fragment mass tolerance unit: '
                                             'available in ppm '
                                             '(parts-per-millon), Da (Dalton) '
                                             'or mmu (Milli mass unit)',
                              'TRANSLATION': {'xtandem': 'spectrum, fragment '
                                                         'monoisotopic mass '
                                                         'error units'},
                              'VALUE_RANGE': ''},
 'frag_mass_type': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': "'monoisotopic'",
                    'DESCRIPTION': 'Fragment mass type: monoisotopic or '
                                   'average',
                    'TRANSLATION': {'omssa': '-tom',
                                    'xtandem': 'spectrum, fragment mass type'},
                    'VALUE_RANGE': ''},
 'frag_method': {'AVAILABLE_IN_UNODE': ['msgfplus', 'myrimatch'],
                 'BUTTOM_TYPE': '',
                 'DEFAULT_VALUE': "'hcd'",
                 'DESCRIPTION': 'used fragmentatiom method. e.g. '
                                'collision-induced dissociation (CID), '
                                'electron-capture dissociation (ECD), '
                                'electron-transfer dissociation (ETD), '
                                'Higher-energy C-trap dissociation (HCD)',
                 'TRANSLATION': {'msgfplus': '-m',
                                 'myrimatch': '-FragmentationRule<str>'},
                 'VALUE_RANGE': ''},
 'frag_min_mz': {'AVAILABLE_IN_UNODE': ['xtandem'],
                 'BUTTOM_TYPE': '',
                 'DEFAULT_VALUE': '150',
                 'DESCRIPTION': 'minimal considered fragment ion m/z',
                 'TRANSLATION': {'xtandem': 'spectrum, minimum fragment mz'},
                 'VALUE_RANGE': ''},
 'helper_extension': {'AVAILABLE_IN_UNODE': [],
                      'BUTTOM_TYPE': '',
                      'DEFAULT_VALUE': "'.u_helper'",
                      'DESCRIPTION': "Helper extention: 'string'",
                      'TRANSLATION': {},
                      'VALUE_RANGE': ''},
 'ident_csv_suffix': {'AVAILABLE_IN_UNODE': [],
                      'BUTTOM_TYPE': '',
                      'DEFAULT_VALUE': "'idents.csv'",
                      'DESCRIPTION': "CSV suffix of identification: 'string', "
                                     'CSV-file which contains identifications '
                                     'with retention times.',
                      'TRANSLATION': {},
                      'VALUE_RANGE': ''},
 'include_reverse (not used)': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                       'msgfplus',
                                                       'msamanda'],
                                'BUTTOM_TYPE': '',
                                'DEFAULT_VALUE': '',
                                'DESCRIPTION': 'A target decoy database should '
                                               'be generated independently '
                                               'from\n'
                                               'the search engine, e.g. by '
                                               'using the uNode '
                                               'generate_target_decoy',
                                'TRANSLATION': {'msamanda': 'generate_decoy',
                                                'msgfplus': '-tda',
                                                'xtandem': 'scoring, include '
                                                           'reverse'},
                                'VALUE_RANGE': ''},
 'input_file': {'AVAILABLE_IN_UNODE': ['xtandem', 'msgfplus'],
                'BUTTOM_TYPE': '',
                'DEFAULT_VALUE': '',
                'DESCRIPTION': 'Input file: path/to/input/file',
                'TRANSLATION': {'msgfplus': '-s', 'xtandem': 'spectrum, path'},
                'VALUE_RANGE': ''},
 'input_file_type': {'AVAILABLE_IN_UNODE': ['xtandem'],
                     'BUTTOM_TYPE': '',
                     'DEFAULT_VALUE': 'None',
                     'DESCRIPTION': 'Input file type',
                     'TRANSLATION': {'xtandem': 'spectrum, path type'},
                     'VALUE_RANGE': ''},
 'java_-Xmx': {'AVAILABLE_IN_UNODE': [],
               'BUTTOM_TYPE': '',
               'DEFAULT_VALUE': "'13312m'",
               'DESCRIPTION': 'set maximum Java heap size',
               'TRANSLATION': {},
               'VALUE_RANGE': ''},
 'json_extension': {'AVAILABLE_IN_UNODE': [],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': ".u.json'",
                    'DESCRIPTION': 'Extention of json file',
                    'TRANSLATION': {},
                    'VALUE_RANGE': ''},
 'label': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa'],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': "'14N'",
           'DESCRIPTION': "'15N' if the corresponding amino acid labeling was "
                          'applied',
           'TRANSLATION': {'omssa': '-tem / -tom',
                           'xtandem': 'protein, modified residue mass file'},
           'VALUE_RANGE': ''},
 'log_enabled': {'AVAILABLE_IN_UNODE': [],
                 'BUTTOM_TYPE': '',
                 'DEFAULT_VALUE': 'False',
                 'DESCRIPTION': 'Will redirect sys.stdout to the logfile, '
                                'default name: ursgal.log',
                 'TRANSLATION': {},
                 'VALUE_RANGE': ''},
 'log_file_name': {'AVAILABLE_IN_UNODE': [],
                   'BUTTOM_TYPE': '',
                   'DEFAULT_VALUE': 'None',
                   'DESCRIPTION': 'This can be used to specify a different log '
                                  'file path',
                   'TRANSLATION': {},
                   'VALUE_RANGE': ''},
 'machine_offset_in_ppm': {'AVAILABLE_IN_UNODE': [],
                           'BUTTOM_TYPE': '',
                           'DEFAULT_VALUE': 'None',
                           'DESCRIPTION': 'Machine offset',
                           'TRANSLATION': {},
                           'VALUE_RANGE': ''},
 'max_mod_alternatives': {'AVAILABLE_IN_UNODE': ['xtandem'],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': '6',
                          'DESCRIPTION': 'Maximal number of variable '
                                         'modification alternatives, given as '
                                         'C in 2^C',
                          'TRANSLATION': {'xtandem': 'protein, ptm complexity'},
                          'VALUE_RANGE': ''},
 'max_num_mods': {'AVAILABLE_IN_UNODE': ['msgfplus'],
                  'BUTTOM_TYPE': '',
                  'DEFAULT_VALUE': '2',
                  'DESCRIPTION': 'Maximal number of modifications per peptide',
                  'TRANSLATION': {'msgfplus': 'NumMods'},
                  'VALUE_RANGE': ''},
 'max_num_per_mod': {'AVAILABLE_IN_UNODE': ['xtandem'],
                     'BUTTOM_TYPE': '',
                     'DEFAULT_VALUE': '{}',
                     'DESCRIPTION': 'Maximal number of modification sites per '
                                    'peptide for a specific modification, '
                                    'given as a dictionary: {unimod_name : '
                                    'number}',
                     'TRANSLATION': {'xtandem': 'residue, potential '
                                                'modification mass'},
                     'VALUE_RANGE': ''},
 'max_pep_length': {'AVAILABLE_IN_UNODE': ['omssa', 'msgfplus', 'myrimatch'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': '40',
                    'DESCRIPTION': 'Maximal length of a peptide',
                    'TRANSLATION': {'msgfplus': '-maxLength',
                                    'myrimatch': '-MaxPeptideLength<int>',
                                    'omssa': '-nox'},
                    'VALUE_RANGE': ''},
 'maximal_accounted_observed_peaks': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                             'myrimatch'],
                                      'BUTTOM_TYPE': '',
                                      'DEFAULT_VALUE': '50',
                                      'DESCRIPTION': 'Maximum number of peaks '
                                                     'from a spectrum used.',
                                      'TRANSLATION': {'myrimatch': '-MaxPeakCount',
                                                      'xtandem': 'spectrum, '
                                                                 'total peaks'},
                                      'VALUE_RANGE': ''},
 'maximum_missed_cleavages': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                     'myrimatch',
                                                     'msamanda'],
                              'BUTTOM_TYPE': '',
                              'DEFAULT_VALUE': '2',
                              'DESCRIPTION': 'Maximum number of missed '
                                             'cleavages per peptide',
                              'TRANSLATION': {'msamanda': 'missed_cleavages',
                                              'myrimatch': '-MaxMissedCleavages<int>',
                                              'xtandem': 'scoring, maximum '
                                                         'missed cleavage '
                                                         'sites'},
                              'VALUE_RANGE': ''},
 'maximum_pep_for_ident_csv': {'AVAILABLE_IN_UNODE': [],
                               'BUTTOM_TYPE': '',
                               'DEFAULT_VALUE': '0.1',
                               'DESCRIPTION': 'Maximum value for PEP '
                                              '(posterior error probability): '
                                              'Threshold for identifications '
                                              'put in CSV-files.',
                               'TRANSLATION': {},
                               'VALUE_RANGE': ''},
 'min_pep_length': {'AVAILABLE_IN_UNODE': ['omssa', 'msgfplus', 'myrimatch'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': '6',
                    'DESCRIPTION': 'Minimal length of a peptide',
                    'TRANSLATION': {'msgfplus': '-minLength',
                                    'myrimatch': '-MinPeptideLength<int>',
                                    'omssa': '-no'},
                    'VALUE_RANGE': ''},
 'mininimal_required_matched_peaks': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                             'omssa'],
                                      'BUTTOM_TYPE': '',
                                      'DEFAULT_VALUE': '4',
                                      'DESCRIPTION': 'Mimimum number of '
                                                     'matched ions required '
                                                     'for a peptide to be '
                                                     'scored',
                                      'TRANSLATION': {'omssa': '-hm',
                                                      'xtandem': 'scoring, '
                                                                 'minimum ion '
                                                                 'count'},
                                      'VALUE_RANGE': ''},
 'mininimal_required_observed_peaks': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                              'omssa'],
                                       'BUTTOM_TYPE': '',
                                       'DEFAULT_VALUE': '5',
                                       'DESCRIPTION': 'Mimimum number of peaks '
                                                      'in the spectrum to be '
                                                      'considered.',
                                       'TRANSLATION': {'omssa': '-hs',
                                                       'xtandem': 'spectrum, '
                                                                  'minimum '
                                                                  'peaks'},
                                       'VALUE_RANGE': ''},
 'modifications': {'AVAILABLE_IN_UNODE': ['xtandem',
                                          'omssa',
                                          'msgfplus',
                                          'myrimatch',
                                          'msamanda'],
                   'BUTTOM_TYPE': '',
                   'DEFAULT_VALUE': "['*,opt,Prot-N-term,Acetyl', "
                                    "'M,opt,any,Oxidation']",
                   'DESCRIPTION': 'Modifications are given as a list of '
                                  'strings, each representing the modification '
                                  'of one amino acid. The string consists of '
                                  'four informations seperated by comma: \n'
                                  '\n'
                                  "'amino acid,type,position,unimod name’ \n"
                                  '\n'
                                  ' amino acid : specify the modified amino '
                                  "acid as a single letter, use '*' if the "
                                  'amino acid is variable\n'
                                  '\n'
                                  ' type   : specify if it is a fixed (fix) or '
                                  'potential (opt) modification \n'
                                  '\n'
                                  ' position  : specify the position within '
                                  'the protein/peptide (Prot-N-term, '
                                  "Prot-C-term), use 'any' if the positon is "
                                  'variable \n'
                                  '\n'
                                  ' unimod name : specify the unimod PSI-MS '
                                  'Name (see unimod.org) \n'
                                  '\n'
                                  'Examples:\n'
                                  '\n'
                                  " [ 'M,opt,any,Oxidation' ]   - potential "
                                  'oxidation of Met at any position within a '
                                  'peptide\n'
                                  '\n'
                                  " [ '*,opt,Prot-N-term,Acetyl' ]  - "
                                  'potential acetylation of any amino acid at '
                                  'the N-terminus of a protein\n'
                                  '\n'
                                  " [ 'S,opt,any,Phospho' ]   - potential "
                                  'phosphorylation of Serine at any position '
                                  'within a peptide\n'
                                  '\n'
                                  " ['C,fix,any,Carbamidomethyl’, "
                                  "'N,opt,any,Deamidated’, "
                                  "'Q,opt,any,Deamidated’] - fixed "
                                  'carbamidomethylation of Cys and potential '
                                  'deamidation of Asn and/or Gln at any '
                                  'position within a peptide\n'
                                  '\n'
                                  'Additionally, userdefined modifications can '
                                  'be given and are written to a '
                                  'userdefined_unimod.xml in ursgal/kb/ext. '
                                  'Userdefined modifications need to have a '
                                  'unique name instead of the unimod name the '
                                  'chemical composition needs to be given as a '
                                  'Hill notation on the fifth position in the '
                                  'string\n'
                                  '\n'
                                  'Example:\n'
                                  '\n'
                                  " [ 'S,opt,any,New_mod,C2H5N1O3' ]",
                   'TRANSLATION': {'msamanda': 'modification protein=true '
                                               'cterm=true',
                                   'msgfplus': '-mod',
                                   'myrimatch': '-StaticMods<str>',
                                   'omssa': '-mv',
                                   'xtandem': 'protein, C-terminal residue '
                                              'modification mass'},
                   'VALUE_RANGE': ''},
 'mzidentml_converter_version': {'AVAILABLE_IN_UNODE': [],
                                 'BUTTOM_TYPE': '',
                                 'DEFAULT_VALUE': "'mzidentml_lib_1_6_10'",
                                 'DESCRIPTION': 'mzidentml converter version: '
                                                "'version name'",
                                 'TRANSLATION': {},
                                 'VALUE_RANGE': ''},
 'mzml2mgf_converter_version': {'AVAILABLE_IN_UNODE': [],
                                'BUTTOM_TYPE': '',
                                'DEFAULT_VALUE': "'mzml2mgf_1_0_0'",
                                'DESCRIPTION': 'mzml to mgf converter version: '
                                               "'version name'",
                                'TRANSLATION': {},
                                'VALUE_RANGE': ''},
 'neutral_loss_enabled': {'AVAILABLE_IN_UNODE': ['xtandem'],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': 'False',
                          'DESCRIPTION': 'Neutral losses enabled for spectrum '
                                         'algorithm: set  True or False',
                          'TRANSLATION': {'xtandem': 'spectrum, use neutral '
                                                     'loss window'},
                          'VALUE_RANGE': ''},
 'neutral_loss_mass': {'AVAILABLE_IN_UNODE': ['xtandem'],
                       'BUTTOM_TYPE': '',
                       'DEFAULT_VALUE': '0',
                       'DESCRIPTION': 'Sets the centre of the window for '
                                      'ignoring neutral molecule losses.',
                       'TRANSLATION': {'xtandem': 'spectrum, neutral loss '
                                                  'mass'},
                       'VALUE_RANGE': ''},
 'neutral_loss_window': {'AVAILABLE_IN_UNODE': ['xtandem'],
                         'BUTTOM_TYPE': '',
                         'DEFAULT_VALUE': '0',
                         'DESCRIPTION': 'Neutral loss window: sets the width '
                                        'of the window for ignoring neutral '
                                        'molecule losses.',
                         'TRANSLATION': {'xtandem': 'spectrum, neutral loss '
                                                    'window'},
                         'VALUE_RANGE': ''},
 'noise_suppression_enabled': {'AVAILABLE_IN_UNODE': ['xtandem'],
                               'BUTTOM_TYPE': '',
                               'DEFAULT_VALUE': 'False',
                               'DESCRIPTION': 'used for noise suppresssion',
                               'TRANSLATION': {'xtandem': 'spectrum, use noise '
                                                          'suppression'},
                               'VALUE_RANGE': ''},
 'num_match_spec': {'AVAILABLE_IN_UNODE': ['omssa',
                                           'msgfplus',
                                           'myrimatch',
                                           'msamanda'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': '10',
                    'DESCRIPTION': 'This parameter sets the maximum number of '
                                   'peptide spectrum matches to report for '
                                   'each spectrum',
                    'TRANSLATION': {'msamanda': 'Specify the number of matches '
                                                'to report for each spectrum',
                                    'msgfplus': 'number of matches per '
                                                'spectrum to be reported',
                                    'myrimatch': 'This parameter sets the '
                                                 'maximum rank of '
                                                 'peptide-spectrum-matches to '
                                                 'report for each spectrum',
                                    'omssa': 'maximum number of hits retained '
                                             'per precursor charge state per '
                                             'spectrum'},
                    'VALUE_RANGE': ''},
 'number_of_i_decimals': {'AVAILABLE_IN_UNODE': [],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': '5',
                          'DESCRIPTION': 'Number of decimals for intensity '
                                         '(peak)',
                          'TRANSLATION': {},
                          'VALUE_RANGE': ''},
 'number_of_mz_decimals': {'AVAILABLE_IN_UNODE': [],
                           'BUTTOM_TYPE': '',
                           'DEFAULT_VALUE': '5',
                           'DESCRIPTION': 'Number of decimals for m/z mass',
                           'TRANSLATION': {},
                           'VALUE_RANGE': ''},
 'output_file_type': {'AVAILABLE_IN_UNODE': [],
                      'BUTTOM_TYPE': '',
                      'DEFAULT_VALUE': 'None',
                      'DESCRIPTION': 'Output file type',
                      'TRANSLATION': {},
                      'VALUE_RANGE': ''},
 'output_suffix': {'AVAILABLE_IN_UNODE': [],
                   'BUTTOM_TYPE': '',
                   'DEFAULT_VALUE': "' '",
                   'DESCRIPTION': "Output suffix: 'string'",
                   'TRANSLATION': {},
                   'VALUE_RANGE': ''},
 'precursor_isotope_range': {'AVAILABLE_IN_UNODE': ['xtandem', 'msgfplus'],
                             'BUTTOM_TYPE': '',
                             'DEFAULT_VALUE': "'0,1'",
                             'DESCRIPTION': 'Error range for incorrect carbon '
                                            'isotope parent ion assignment',
                             'TRANSLATION': {'msgfplus': '-ti',
                                             'xtandem': 'spectrum, parent '
                                                        'monoisotopic mass '
                                                        'isotope error'},
                             'VALUE_RANGE': ''},
 'precursor_mass_tolerance_minus': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                           'omssa',
                                                           'msgfplus',
                                                           'myrimatch',
                                                           'msamanda'],
                                    'BUTTOM_TYPE': '',
                                    'DEFAULT_VALUE': '5',
                                    'DESCRIPTION': 'Precursor mass tolerance: '
                                                   'lower mass tolerance of '
                                                   'measured and calculated '
                                                   'parent ion M+H',
                                    'TRANSLATION': {'msamanda': 'ms1_tol',
                                                    'msgfplus': '-t',
                                                    'myrimatch': '-MonoPrecursorMzTolerance',
                                                    'omssa': '-te',
                                                    'xtandem': 'spectrum, '
                                                               'parent '
                                                               'monoisotopic '
                                                               'mass error '
                                                               'minus'},
                                    'VALUE_RANGE': ''},
 'precursor_mass_tolerance_plus': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                          'omssa',
                                                          'msamanda'],
                                   'BUTTOM_TYPE': '',
                                   'DEFAULT_VALUE': '5',
                                   'DESCRIPTION': 'Precursor mass tolerance: '
                                                  'higher mass tolerance of '
                                                  'measured and calculated '
                                                  'parent ion M+H',
                                   'TRANSLATION': {'msamanda': 'ms1_tol',
                                                   'omssa': '-te',
                                                   'xtandem': 'spectrum, '
                                                              'parent '
                                                              'monoisotopic '
                                                              'mass error '
                                                              'plus'},
                                   'VALUE_RANGE': ''},
 'precursor_mass_tolerance_unit': {'AVAILABLE_IN_UNODE': ['xtandem',
                                                          'omssa',
                                                          'msamanda'],
                                   'BUTTOM_TYPE': '',
                                   'DEFAULT_VALUE': "'ppm'",
                                   'DESCRIPTION': 'Precursor mass tolerance '
                                                  'unit: available in ppm '
                                                  '(parts-per-millon), Da '
                                                  '(Dalton) or mmu (Milli mass '
                                                  'unit)',
                                   'TRANSLATION': {'msamanda': 'ms1_tol unit',
                                                   'omssa': '-teppm',
                                                   'xtandem': 'spectrum, '
                                                              'parent '
                                                              'monoisotopic '
                                                              'mass error '
                                                              'units'},
                                   'VALUE_RANGE': ''},
 'precursor_mass_type': {'AVAILABLE_IN_UNODE': ['omssa',
                                                'myrimatch',
                                                'msamanda'],
                         'BUTTOM_TYPE': '',
                         'DEFAULT_VALUE': "'monoisotopic', (average)",
                         'DESCRIPTION': 'Precursor mass type: monoisotopic or '
                                        'average',
                         'TRANSLATION': {'msamanda': 'monoisotopic',
                                         'myrimatch': '-PrecursorMzToleranceRule '
                                                      '<str>',
                                         'omssa': '-tem'},
                         'VALUE_RANGE': ''},
 'precursor_max_charge': {'AVAILABLE_IN_UNODE': ['omssa',
                                                 'msgfplus',
                                                 'myrimatch',
                                                 'msamanda'],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': '5',
                          'DESCRIPTION': 'maximal accepted parent ion charge',
                          'TRANSLATION': {'msamanda': 'considered_charges',
                                          'msgfplus': '-maxCharge',
                                          'myrimatch': '-NumChargeStates '
                                                       '<interger>',
                                          'omssa': '-zh'},
                          'VALUE_RANGE': ''},
 'precursor_min_charge': {'AVAILABLE_IN_UNODE': ['omssa',
                                                 'msgfplus',
                                                 'msamanda'],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': '1',
                          'DESCRIPTION': 'minimal accepted parent ion charge',
                          'TRANSLATION': {'msamanda': 'considered_charges',
                                          'msgfplus': '-minCharge',
                                          'omssa': '-zl'},
                          'VALUE_RANGE': ''},
 'precursor_min_mass': {'AVAILABLE_IN_UNODE': ['xtandem', 'myrimatch'],
                        'BUTTOM_TYPE': '',
                        'DEFAULT_VALUE': '400',
                        'DESCRIPTION': 'minimal parent ion mass',
                        'TRANSLATION': {'myrimatch': '-MinPeptideMass <real>',
                                        'xtandem': 'spectrum, minimum parent '
                                                   'm+h -sets the minimum '
                                                   'parent M+H required for a '
                                                   'spectrum to be '
                                                   'considered.'},
                        'VALUE_RANGE': ''},
 'precursor_ppm_offset': {'AVAILABLE_IN_UNODE': [],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': 'None',
                          'DESCRIPTION': 'Precursor offset in ppm',
                          'TRANSLATION': {},
                          'VALUE_RANGE': ''},
 'prefix': {'AVAILABLE_IN_UNODE': [],
            'BUTTOM_TYPE': '',
            'DEFAULT_VALUE': 'None',
            'DESCRIPTION': '',
            'TRANSLATION': {},
            'VALUE_RANGE': ''},
 'raw_ident_csv_suffix': {'AVAILABLE_IN_UNODE': [],
                          'BUTTOM_TYPE': '',
                          'DEFAULT_VALUE': "'.csv'",
                          'DESCRIPTION': 'CSV suffix of raw indentification: '
                                         'this is the conversion result after '
                                         'CSV conversion but before adding '
                                         'retention time',
                          'TRANSLATION': {},
                          'VALUE_RANGE': ''},
 'remove_temporary_files': {'AVAILABLE_IN_UNODE': [],
                            'BUTTOM_TYPE': '',
                            'DEFAULT_VALUE': 'False',
                            'DESCRIPTION': 'Remove temporary files: True or '
                                           'False',
                            'TRANSLATION': {},
                            'VALUE_RANGE': ''},
 'rt_pickle_name': {'AVAILABLE_IN_UNODE': [],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': "_ursgal_lookup.pkl'",
                    'DESCRIPTION': 'name of the pickle that is used to map the '
                                   'retention time',
                    'TRANSLATION': {},
                    'VALUE_RANGE': ''},
 'scan_exclusion_list': {'AVAILABLE_IN_UNODE': [],
                         'BUTTOM_TYPE': '',
                         'DEFAULT_VALUE': 'None',
                         'DESCRIPTION': 'spectra rejected during mzml2mgf '
                                        'conversion',
                         'TRANSLATION': {},
                         'VALUE_RANGE': ''},
 'scan_skip_modulo_step': {'AVAILABLE_IN_UNODE': [],
                           'BUTTOM_TYPE': '',
                           'DEFAULT_VALUE': 'None',
                           'DESCRIPTION': "include only the n'th spectrum "
                                          'during mzml2mgf conversion',
                           'TRANSLATION': {},
                           'VALUE_RANGE': ''},
 'score_-h2o_ions': {'AVAILABLE_IN_UNODE': ['msamanda'],
                     'BUTTOM_TYPE': '',
                     'DEFAULT_VALUE': 'False',
                     'DESCRIPTION': 'Spectrum: if true, ions loss of H2O are '
                                    'respected in algorithm',
                     'TRANSLATION': {'msamanda': 'series'},
                     'VALUE_RANGE': ''},
 'score_-nh3_ions': {'AVAILABLE_IN_UNODE': ['msamanda'],
                     'BUTTOM_TYPE': '',
                     'DEFAULT_VALUE': 'False',
                     'DESCRIPTION': 'Spectrum: if true, ions loss of NH3 are '
                                    'respected in algorithm',
                     'TRANSLATION': {'msamanda': 'series'},
                     'VALUE_RANGE': ''},
 'score_a_ions': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa', 'msamanda'],
                  'BUTTOM_TYPE': '',
                  'DEFAULT_VALUE': 'False',
                  'DESCRIPTION': 'Spectrum: if true, a ions are used in '
                                 'algorithm',
                  'TRANSLATION': {'msamanda': 'series',
                                  'omssa': '-i',
                                  'xtandem': 'scoring, a ions'},
                  'VALUE_RANGE': ''},
 'score_b_ions': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa', 'msamanda'],
                  'BUTTOM_TYPE': '',
                  'DEFAULT_VALUE': 'True',
                  'DESCRIPTION': 'Spectrum: if true, b ions are used in '
                                 'algorithm',
                  'TRANSLATION': {'msamanda': 'series',
                                  'omssa': '-i',
                                  'xtandem': 'scoring, b ions'},
                  'VALUE_RANGE': ''},
 'score_c_ions': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa', 'msamanda'],
                  'BUTTOM_TYPE': '',
                  'DEFAULT_VALUE': 'False',
                  'DESCRIPTION': 'Spectrum: if true, c ions are used in '
                                 'algorithm',
                  'TRANSLATION': {'msamanda': 'series',
                                  'omssa': '-i',
                                  'xtandem': 'scoring, c ions'},
                  'VALUE_RANGE': ''},
 'score_imm_ions': {'AVAILABLE_IN_UNODE': ['msamanda'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': 'False',
                    'DESCRIPTION': 'Spectrum: if true, immonium ions are '
                                   'respected in algorithm',
                    'TRANSLATION': {'msamanda': 'series'},
                    'VALUE_RANGE': ''},
 'score_int_ions': {'AVAILABLE_IN_UNODE': ['msamanda'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': 'False',
                    'DESCRIPTION': 'Spectrum: if true, internal fragment ions '
                                   'are respect in algorithm',
                    'TRANSLATION': {'msamanda': 'series'},
                    'VALUE_RANGE': ''},
 'score_x_ions': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa', 'msamanda'],
                  'BUTTOM_TYPE': '',
                  'DEFAULT_VALUE': 'False',
                  'DESCRIPTION': 'Spectrum: if true, x ions are used in '
                                 'algorithm',
                  'TRANSLATION': {'msamanda': 'series',
                                  'omssa': '-i',
                                  'xtandem': 'scoring, x ions'},
                  'VALUE_RANGE': ''},
 'score_y_ions': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa', 'msamanda'],
                  'BUTTOM_TYPE': '',
                  'DEFAULT_VALUE': 'True',
                  'DESCRIPTION': 'Spectrum: if true, y ions are used in '
                                 'algorithm',
                  'TRANSLATION': {'msamanda': 'series',
                                  'omssa': '-i',
                                  'xtandem': 'scoring, y ions'},
                  'VALUE_RANGE': ''},
 'score_z+1_ions': {'AVAILABLE_IN_UNODE': ['msamanda'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': 'False',
                    'DESCRIPTION': 'Spectrum: if true, z ion plus 1 Da mass '
                                   'are used in algorithm',
                    'TRANSLATION': {'msamanda': 'series'},
                    'VALUE_RANGE': ''},
 'score_z+2_ions': {'AVAILABLE_IN_UNODE': ['msamanda'],
                    'BUTTOM_TYPE': '',
                    'DEFAULT_VALUE': 'False',
                    'DESCRIPTION': 'Spectrum: if true z ion plus 2 Da mass are '
                                   'used in algorithm',
                    'TRANSLATION': {'msamanda': 'series'},
                    'VALUE_RANGE': ''},
 'score_z_ions': {'AVAILABLE_IN_UNODE': ['xtandem', 'omssa', 'msamanda'],
                  'BUTTOM_TYPE': '',
                  'DEFAULT_VALUE': 'False',
                  'DESCRIPTION': 'Spectrum: if true, z ions are used in '
                                 'algorithm',
                  'TRANSLATION': {'msamanda': 'series',
                                  'omssa': '-i',
                                  'xtandem': 'scoring, z ions'},
                  'VALUE_RANGE': ''},
 'search_engines_create_folders': {'AVAILABLE_IN_UNODE': [],
                                   'BUTTOM_TYPE': '',
                                   'DEFAULT_VALUE': 'True',
                                   'DESCRIPTION': 'Create folders for search '
                                                  'engines. True or False',
                                   'TRANSLATION': {},
                                   'VALUE_RANGE': ''},
 'search_for_saps': {'AVAILABLE_IN_UNODE': ['xtandem'],
                     'BUTTOM_TYPE': '',
                     'DEFAULT_VALUE': 'False',
                     'DESCRIPTION': 'search for potential single amino acid '
                                    'polymorphisms',
                     'TRANSLATION': {'xtandem': 'protein, saps'},
                     'VALUE_RANGE': ''},
 'semi_enzyme': {'AVAILABLE_IN_UNODE': ['xtandem',
                                        'omssa',
                                        'msgfplus',
                                        'myrimatch',
                                        'msamanda'],
                 'BUTTOM_TYPE': '',
                 'DEFAULT_VALUE': 'False',
                 'DESCRIPTION': 'Allows semi-enzymatic peptide ends',
                 'TRANSLATION': {'msamanda': 'enzyme specificity',
                                 'msgfplus': '-ntt',
                                 'myrimatch': '-MinTerminiCleavages<int>',
                                 'omssa': '-e',
                                 'xtandem': 'protein, cleavage semi'},
                 'VALUE_RANGE': ''},
 'show_unodes_in_development': {'AVAILABLE_IN_UNODE': [],
                                'BUTTOM_TYPE': '',
                                'DEFAULT_VALUE': 'False',
                                'DESCRIPTION': 'Show ursgal nodes in '
                                               'development: False or True',
                                'TRANSLATION': {},
                                'VALUE_RANGE': ''},
 'spec_dynamic_range': {'AVAILABLE_IN_UNODE': ['xtandem'],
                        'BUTTOM_TYPE': '',
                        'DEFAULT_VALUE': '100',
                        'DESCRIPTION': 'Spectrum, internal normalization: The '
                                       'highest peak (intensity) within a '
                                       'spectrum is set to given value and all '
                                       'other peaks are normalized to this '
                                       'peak. If the normalized value is less '
                                       'than 1 he peak is rejected.',
                        'TRANSLATION': {'xtandem': 'spectrum, dynamic range'},
                        'VALUE_RANGE': ''},
 'stp_bias': {'AVAILABLE_IN_UNODE': ['xtandem'],
              'BUTTOM_TYPE': '',
              'DEFAULT_VALUE': 'False',
              'DESCRIPTION': 'Interpretation of peptide phosphorylation '
                             'models.',
              'TRANSLATION': {'xtandem': 'protein, stP bias'},
              'VALUE_RANGE': ''},
 'ukey1': {'AVAILABLE_IN_UNODE': ['xtandem', 'msamanda'],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': '',
           'DESCRIPTION': '',
           'TRANSLATION': {'msamanda': 'modification protein=true nterm=true',
                           'xtandem': 'protein, N-terminal residue '
                                      'modification mass'},
           'VALUE_RANGE': ''},
 'ukey2': {'AVAILABLE_IN_UNODE': ['xtandem'],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': '',
           'DESCRIPTION': '',
           'TRANSLATION': {'xtandem': 'protein, quick acetyl'},
           'VALUE_RANGE': ''},
 'ukey3': {'AVAILABLE_IN_UNODE': ['xtandem'],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': '',
           'DESCRIPTION': '',
           'TRANSLATION': {'xtandem': 'protein, quick pyrolidone'},
           'VALUE_RANGE': ''},
 'ukey4': {'AVAILABLE_IN_UNODE': ['xtandem', 'msamanda'],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': '',
           'DESCRIPTION': '',
           'TRANSLATION': {'msamanda': 'modification fix=true',
                           'xtandem': 'residue, modification mass'},
           'VALUE_RANGE': ''},
 'ukey5': {'AVAILABLE_IN_UNODE': ['xtandem', 'msamanda'],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': '',
           'DESCRIPTION': '',
           'TRANSLATION': {'msamanda': 'modification fix=false',
                           'xtandem': 'residue, potential modification mass'},
           'VALUE_RANGE': ''},
 'ukey6': {'AVAILABLE_IN_UNODE': ['xtandem'],
           'BUTTOM_TYPE': '',
           'DEFAULT_VALUE': '',
           'DESCRIPTION': '',
           'TRANSLATION': {'xtandem': 'residue, potential modification motif'},
           'VALUE_RANGE': ''},
 'unify_csv_converter_version': {'AVAILABLE_IN_UNODE': [],
                                 'BUTTOM_TYPE': '',
                                 'DEFAULT_VALUE': "'unify_csv_1_0_0'",
                                 'DESCRIPTION': 'unify csv converter version: '
                                                "'version name'",
                                 'TRANSLATION': {},
                                 'VALUE_RANGE': ''},
 'use_refine': {'AVAILABLE_IN_UNODE': [],
                'BUTTOM_TYPE': '',
                'DEFAULT_VALUE': 'False',
                'DESCRIPTION': '',
                'TRANSLATION': {},
                'VALUE_RANGE': ''},
 'validated_ident_csv_suffix': {'AVAILABLE_IN_UNODE': [],
                                'BUTTOM_TYPE': '',
                                'DEFAULT_VALUE': "'validated.csv'",
                                'DESCRIPTION': 'CSV suffix of validated '
                                               "idententification:'string', "
                                               'CSV-file which contains PSMs '
                                               'validated with validation '
                                               'tools',
                                'TRANSLATION': {},
                                'VALUE_RANGE': ''},
 'write_unfiltered_results': {'AVAILABLE_IN_UNODE': [],
                              'BUTTOM_TYPE': '',
                              'DEFAULT_VALUE': 'False',
                              'DESCRIPTION': 'writes rejected results if True',
                              'TRANSLATION': {},
                              'VALUE_RANGE': ''}}
