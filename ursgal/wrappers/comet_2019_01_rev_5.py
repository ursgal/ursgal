import os
import ursgal
import csv
import xml.etree.ElementTree as ET

# 'comet_2019_01_rev_5',
# 'comet_style_2'


class comet_2019_01_rev_5(ursgal.UNode):
    """
    MODa UNode
    Check http://comet-ms.sourceforge.net/ for download, new versions and contact information

    Not implemented yet
    """
    META_INFO = {
        'edit_version': 1.00,
        'name': 'Comet',
        'version': '2019_01_rev_5',
        'release_date': '2020-04-06',
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'input_extensions': ['.mgf', '.mzML', '.mzXML', '.ms2'],
        'output_extensions': ['.csv', '.txt', '.xml', ],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': None,
        'distributable': False,
        'utranslation_style': 'comet_style_2',
        'citation':
            ' - A Deeper Look into Comet - Implementation and Features. '
            '   Eng JK, Hoopmann MR, Jahan TA, Egertson JD, Noble WS, MacCoss MJ. '
            '   J Am Soc Mass Spectrom. 2015 Jun 27. doi: 10.1007/s13361-015-1179-x'
            ' - Comet: an open source tandem mass spectrometry sequence database search tool. '
            '   Eng JK, Jahan TA, Hoopmann MR. '
            '   Proteomics. 2012 Nov 12. doi: 10.1002/pmic.201200439',

        'engine': {
            'darwin': {
                '64bit': {
                    'exe': 'comet.2019015.linux.exe',
                    'url': '',
                    'zip_md5': '4b62c06b9885753a4c9ee2586fd072d8',
                    'additional_exe': [],
                },
            },
            'linux': {
                '64bit': {
                    'exe': 'comet.2019015.linux.exe',
                    'url': '',
                    'zip_md5': '4b62c06b9885753a4c9ee2586fd072d8',
                    'additional_exe': [],
                },
            },
            'win32': {
                '64bit': {
                    'exe': 'comet.2019015.win64.exe',
                    'url': '',
                    'zip_md5': '4b62c06b9885753a4c9ee2586fd072d8',
                    'additional_exe': [],
                },
                '32bit': {
                    'exe': 'comet.2019015.win32.exee',
                    'url': '',
                    'zip_md5': '4b62c06b9885753a4c9ee2586fd072d8',
                    'additional_exe': [],
                },
            },
        }

    }

    def __init__(self, *args, **kwargs):
        super(comet_2019_01_rev_5, self).__init__(*args, **kwargs)

    def preflight(self):
        """
        Create comet.params file and format command line via self.params

        return:   dict: self.params
        """

        # self.params['command_list'] += self.params['options']
        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        self.params['translations']['tmp_output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'].replace('.csv', '.pep.xml') # + '.pep.xml'
        )

        self.params['translations']['parameter_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['file_root'] + '.params'
        )
        alternate_output_base_name = self.params['translations']['tmp_output_file_incl_path'].replace('.pep.xml', '')
        self.params['translations']['alternate_output_base_name'] = alternate_output_base_name

        # self.params['translations']['output_file_incl_path'] =

        ## ADDING IONS
        self.ursgal2comet_ions()
        ## ADDING VARIABLE MODS
        self.ursgal2comet_mods()

        parameter_file_template = self.format_template()
        # print(parameter_file_template)
        with open(self.params['translations']['parameter_file'], 'w') as io:
            print(parameter_file_template, file=io)

        self.params['command_list'] = [
            self.exe,
            '{mgf_input_file}'.format(**self.params['translations']),
            '-P{parameter_file}'.format(**self.params['translations']),
            '-D{database}'.format(**self.params),
            '-N{alternate_output_base_name}'.format(**self.params['translations']),
        ]

        print("\nCommand line:")
        print(' '.join(self.params['command_list']))
        print("")
        return self.params

    def postflight(self):
        """Convert xml dict to csv"""
        rows_dict = self.cometxml2dict()
        # print(rows_dict)
        output_file = self.params['translations']['tmp_output_file_incl_path'].replace('.pep.xml', '.csv')
        print(f"[{'Write':^10s}] Writing file: {output_file}")
        raw_input_file = os.path.abspath(self.params['input_file'])
        #
        NEW_HEADERS = [
            'Raw data location',
            'Spectrum ID',
            'Spectrum Title',
            'Retention Time (s)',
            'Rank',
            'Calc m/z',
            'Exp m/z',
            'Charge',
            'Sequence',
            'Modifications',
            'Comet:evalue',
            'Comet:xcorr',
            'Comet:spscore',
            'Comet:deltacn',
            'proteinacc_start_stop_pre_post_;',
            'Is decoy',
            'Start',
            'Stop',
        ]

        PROTON = 1.00727646677
        decoy_tag = self.params.get('decoy_tag', 'decoy_')

        with open(output_file, 'w') as result_file:
            self.print_info(
                'Writing Comet results, this can take a while...',
                caller='Info'
            )
            csv_dict_write_object = csv.DictWriter(result_file, fieldnames=NEW_HEADERS)
            csv_dict_write_object.writeheader()
            total_docs = len(rows_dict)
            padding = len(str(total_docs))
            self.print_info(f"Total number of lines: {total_docs}", caller='info')
            for cache_pos, row_info in rows_dict.items():
                line_dict = {}
                for header, new_header in  self.UNODE_UPARAMS['header_translations']['uvalue_style_translation'].items():
                    line_dict[new_header] = row_info.get(header, None)
                line_dict['Modifications'] = row_info.get('Modifications', None)
                line_dict['Exp m/z'] = (float(row_info['precursor_neutral_mass']) / float(
                    row_info['assumed_charge'])) + PROTON
                line_dict['Calc m/z'] = (float(row_info['calc_neutral_pep_mass']) / float(
                    row_info['assumed_charge'])) + PROTON

                line_dict['Is decoy'] = decoy_tag in line_dict['proteinacc_start_stop_pre_post_;']
                line_dict['Raw data location'] = raw_input_file
                csv_dict_write_object.writerow(line_dict)
                if cache_pos % 500 == 0:
                    print(f"[{'Info':^10s}] Processing line number: {cache_pos:>{padding}}/{total_docs:>{padding}}",  end='\r')

        return output_file




    def cometxml2dict(self):
        """Convert pep.xml to dict"""
        xml_input_file = self.params['translations']['tmp_output_file_incl_path']
        print(f"[{'Sub':^10s}] Extracting info from XML file; {xml_input_file}")
        tree = ET.parse(xml_input_file)
        row = 0
        out = {}
        for elem in tree.getroot():
            for spectrum_query in elem:
                if 'spectrum_query' not in spectrum_query.tag:
                    continue

                for search_result in spectrum_query:

                    n_search_hits = len(search_result)
                    if n_search_hits == 0:
                        continue

                    # General information about the Spectrum
                    info_spectrum_query = spectrum_query.attrib
                    for search_hit in search_result:
                        row += 1

                        search_hit_info = search_hit.attrib
                        # Protein ID
                        proteins = [search_hit_info['protein']]

                        for search_hit_entry in search_hit:
                            # Peptide Modifications
                            tmp_mods = []
                            # Entry name
                            search_hit_tag = search_hit_entry.tag
                            if 'modification_info' in search_hit_tag:
                                # Extract all peptide modifications
                                for modification_entry in search_hit_entry:
                                    modification_entry_info = modification_entry.attrib
                                    position = modification_entry_info['position']
                                    mod_mass = modification_entry_info[
                                        'variable'] if 'variable' in modification_entry_info else \
                                        modification_entry_info['static']
                                    # mod_name = mass2unimod_name[mod_mass]
                                    # Formatting modification
                                    new_mod = '{0}:{1}'.format(mod_mass, position)
                                    # new_mod = '{0}:{1}'.format(mod_name, position)
                                    tmp_mods.append(new_mod)
                                # Concatenate into a string
                                modifications_ursgal_format = ';'.join(tmp_mods)
                                search_hit_info = {**search_hit_info, **{'Modifications': modifications_ursgal_format}}
                            elif 'search_score' in search_hit_tag:
                                score_info = search_hit_entry.attrib
                                search_hit_info = {**search_hit_info, **{score_info['name']: score_info['value']}}
                            elif 'alternative_protein' in search_hit_tag:
                                proteins.append(search_hit_entry.attrib['protein'])

                        out[row] = {**info_spectrum_query, **search_hit_info, **{'protein': ';'.join(proteins)}}

                        if row % 500 == 0:
                            print(f"[{'Info':^10s}] Processing line number: {row}",  end='\r')

            if out:
                print(f"[{'Ok':^10s}] All good with information extraction!")
        return out

    def ursgal2comet_ions(self):
        """Format ions"""
        comet_ions = ['a', 'b', 'c', 'x', 'y', 'z']
        active_ions = self.params['translations']['score_ion_list']
        for ion in comet_ions:
            value = 0
            if ion in active_ions:
                value = 1
            ion_key = 'use_{ion_name}_ions'.format(ion_name=ion.upper())
            self.params['translations'][ion_key] = value

    def ursgal2comet_mods(self):
        """Format ursgal modifications to Comet"""
        um = ursgal.UnimodMapper()
        residues = [
            'G', 'A', 'S', 'P', 'V', 'T', 'C', 'L', 'I', 'N',
            'D', 'Q', 'K', 'E', 'M', 'H', 'F', 'R', 'Y',
            'W',
        ]
        variable_mods_lines = ''
        for n, mod in enumerate(self.params['translations']['modifications'], 1):
            if mod == 'C,fix,any,Carbamidomethyl':
                continue

            aa_name, aa_type, mod_pos, mod_name = mod.split(',')
            mod_mass = None
            second_entry = ''
            third_entry = 0
            fourth_entry = -1
            fifth_entry = self.params['translations']['max_num_per_mod']
            sixth_entry = 0
            seventh_entry = 0
            eigth_entry = 0.0

            if mod_name.isdigit():
                mod_mass = um.id2mass(int(mod_name))
            else:
                mod_mass = um.name2mass(mod_name)
            if not mod_mass:
                raise RuntimeError("Expected Unimod or id")

            if aa_name in residues:
                second_entry = aa_name
            elif aa_name == '*':
                pass
            else:
                raise SyntaxError(f"Expected * or any residues of the following {' '.join(residues)}")

            se_prefix = ''
            if mod_pos == 'Prot-N-term':
                se_prefix = 'n'
            elif mod_pos == 'Prot-C-term':
                se_prefix = 'c'
            second_entry = se_prefix + second_entry

            fdict = {
                'n': str(n).zfill(2),
                'first_entry': mod_mass,
                'second_entry': second_entry,
                'third_entry': third_entry,
                'fourth_entry': fourth_entry,
                'fifth_entry': fifth_entry,
                'sixth_entry': sixth_entry,
                'seventh_entry': seventh_entry,
                'eigth_entry': eigth_entry
            }
            formatted_mod = "variable_mod{n} = {first_entry:>10.7f} {second_entry} {third_entry:1d} {fourth_entry:>2d} {fifth_entry:d} {sixth_entry:1d} {seventh_entry:1d} {eigth_entry:.7f}\n".format(
                **fdict)
            variable_mods_lines += formatted_mod
        self.params['translations']['variable_mods_lines'] = variable_mods_lines

    def format_template(self):
        """comet.params template"""
        template = '''# comet_version 2019.01 rev. 5
# Comet MS/MS search engine parameters file.
# Everything following the '#' symbol is treated as a comment.

database_name = {database}
decoy_search = 0                       # 0=no (default), 1=concatenated search, 2=separate search
peff_format = 0                        # 0=no (normal fasta, default), 1=PEFF PSI-MOD, 2=PEFF Unimod
peff_obo =                             # path to PSI Mod or Unimod OBO file

num_threads = {cpus}                       # 0=poll CPU to set num threads; else specify num threads directly (max 128)

#
# masses
#
peptide_mass_tolerance = 20.00
peptide_mass_units = {precursor_mass_tolerance_unit}                 # 0=amu, 1=mmu, 2=ppm
mass_type_parent = {precursor_mass_type}                   # 0=average masses, 1=monoisotopic masses
mass_type_fragment = {frag_mass_type}                 # 0=average masses, 1=monoisotopic masses
precursor_tolerance_type = 1           # 0=MH+ (default), 1=precursor m/z; only valid for amu/mmu tolerances
isotope_error = 3                      # 0=off, 1=0/1 (C13 error), 2=0/1/2, 3=0/1/2/3, 4=-8/-4/0/4/8 (for +4/+8 labeling)

#
# search enzyme
#
search_enzyme_number = {enzyme}              # choose from list at end of this params file
search_enzyme2_number = 0              # second enzyme; set to 0 if no second enzyme
num_enzyme_termini = {semi_enzyme}                 # 1 (semi-digested), 2 (fully digested, default), 8 C-term unspecific , 9 N-term unspecific
allowed_missed_cleavage = {max_missed_cleavages}           # maximum value is 5; for enzyme search

#
# Up to 9 variable modifications are supported
# format:  <mass> <residues> <0=variable/else binary> <max_mods_per_peptide> <term_distance> <n/c-term> <required> <neutral_loss>
#     e.g. 79.966331 STY 0 3 -1 0 0 97.976896
{variable_mods_lines}
max_variable_mods_in_peptide = {max_mod_alternatives}
require_variable_mod = 0

#
# fragment ions
#
# ion trap ms/ms:  1.0005 tolerance, 0.4 offset (mono masses), theoretical_fragment_ions = 1
# high res ms/ms:    0.02 tolerance, 0.0 offset (mono masses), theoretical_fragment_ions = 0, spectrum_batch_size = 10000
#
fragment_bin_tol = 0.02                # binning to use on fragment ions
fragment_bin_offset = 0.0              # offset position to start the binning (0.0 to 1.0)
theoretical_fragment_ions = 0          # 0=use flanking peaks, 1=M peak only
use_A_ions = {use_A_ions}
use_B_ions = {use_B_ions}
use_C_ions = {use_C_ions}
use_X_ions = {use_X_ions}
use_Y_ions = {use_Y_ions}
use_Z_ions = {use_Z_ions}
use_NL_ions = {neutral_loss_enabled}                       # 0=no, 1=yes to consider NH3/H2O neutral loss peaks

#
# output
#
output_sqtstream = 0                   # 0=no, 1=yes  write sqt to standard output
output_sqtfile = 0                     # 0=no, 1=yes  write sqt file
output_txtfile = 1                     # 0=no, 1=yes  write tab-delimited txt file
output_pepxmlfile = 1                  # 0=no, 1=yes  write pep.xml file
output_percolatorfile = 0              # 0=no, 1=yes  write Percolator tab-delimited input file
print_expect_score = 1                 # 0=no, 1=yes to replace Sp with expect in out & sqt
num_output_lines = 5                   # num peptide results to show
show_fragment_ions = 0                 # 0=no, 1=yes for out files only

sample_enzyme_number = 1               # Sample enzyme which is possibly different than the one applied to the search.
                                       # Used to calculate NTT & NMC in pepXML output (default=1 for trypsin).

#
# mzXML parameters
#
scan_range = 0 0                       # start and end scan range to search; either entry can be set independently
precursor_charge = {precursor_min_charge} {precursor_max_charge}                 # precursor charge range to analyze; does not override any existing charge; 0 as 1st entry ignores parameter
override_charge = 0                    # 0=no, 1=override precursor charge states, 2=ignore precursor charges outside precursor_charge range, 3=see online
ms_level = {ms_level}                           # MS level to analyze, valid are levels 2 (default) or 3
activation_method = ALL                # activation method; used if activation method set; allowed ALL, CID, ECD, ETD, ETD+SA, PQD, HCD, IRMPD

#
# misc parameters
#
digest_mass_range = {precursor_min_mass} {precursor_max_mass}           # MH+ peptide mass range to analyze
peptide_length_range = {min_pep_length} {max_pep_length}            # minimum and maximum peptide length to analyze (default 1 63; max length 63)
num_results = 100                      # number of search hits to store internally
max_duplicate_proteins = 20            # maximum number of protein names to report for each peptide identification; -1 reports all duplicates
skip_researching = 1                   # for '.out' file output only, 0=search everything again (default), 1=don't search if .out exists
max_fragment_charge = {frag_max_charge}                # set maximum fragment charge state to analyze (allowed max 5)
max_precursor_charge = {precursor_max_charge}               # set maximum precursor charge state to analyze (allowed max 9)
nucleotide_reading_frame = 0           # 0=proteinDB, 1-6, 7=forward three, 8=reverse three, 9=all six
clip_nterm_methionine = 0              # 0=leave sequences as-is; 1=also consider sequence w/o N-term methionine
spectrum_batch_size = 15000            # max. # of spectra to search at a time; 0 to search the entire scan range in one loop
decoy_prefix = {decoy_tag}                  # decoy entries are denoted by this string which is pre-pended to each protein accession
equal_I_and_L = 1                      # 0=treat I and L as different; 1=treat I and L as same
output_suffix =                        # add a suffix to output base names i.e. suffix "-C" generates base-C.pep.xml from base.mzXML input
mass_offsets =                         # one or more mass offsets to search (values substracted from deconvoluted precursor mass)
precursor_NL_ions =                    # one or more precursor neutral loss masses, will be added to xcorr analysis

#
# spectral processing
#
minimum_peaks = {min_required_observed_peaks}                     # required minimum number of peaks in spectrum to search (default 10)
minimum_intensity = 0                  # minimum intensity value to read in
remove_precursor_peak = 0              # 0=no, 1=yes, 2=all charge reduced precursor peaks (for ETD), 3=phosphate neutral loss peaks
remove_precursor_tolerance = 1.5       # +- Da tolerance for precursor removal
clear_mz_range = 0.0 0.0               # for iTRAQ/TMT type data; will clear out all peaks in the specified m/z range

#
# additional modifications
#

add_Cterm_peptide = 0.0
add_Nterm_peptide = 0.0
add_Cterm_protein = 0.0
add_Nterm_protein = 0.0

add_G_glycine = 0.0000                 # added to G - avg.  57.0513, mono.  57.02146
add_A_alanine = 0.0000                 # added to A - avg.  71.0779, mono.  71.03711
add_S_serine = 0.0000                  # added to S - avg.  87.0773, mono.  87.03203
add_P_proline = 0.0000                 # added to P - avg.  97.1152, mono.  97.05276
add_V_valine = 0.0000                  # added to V - avg.  99.1311, mono.  99.06841
add_T_threonine = 0.0000               # added to T - avg. 101.1038, mono. 101.04768
add_C_cysteine = 57.021464             # added to C - avg. 103.1429, mono. 103.00918
add_L_leucine = 0.0000                 # added to L - avg. 113.1576, mono. 113.08406
add_I_isoleucine = 0.0000              # added to I - avg. 113.1576, mono. 113.08406
add_N_asparagine = 0.0000              # added to N - avg. 114.1026, mono. 114.04293
add_D_aspartic_acid = 0.0000           # added to D - avg. 115.0874, mono. 115.02694
add_Q_glutamine = 0.0000               # added to Q - avg. 128.1292, mono. 128.05858
add_K_lysine = 0.0000                  # added to K - avg. 128.1723, mono. 128.09496
add_E_glutamic_acid = 0.0000           # added to E - avg. 129.1140, mono. 129.04259
add_M_methionine = 0.0000              # added to M - avg. 131.1961, mono. 131.04048
add_O_ornithine = 0.0000               # added to O - avg. 132.1610, mono  132.08988
add_H_histidine = 0.0000               # added to H - avg. 137.1393, mono. 137.05891
add_F_phenylalanine = 0.0000           # added to F - avg. 147.1739, mono. 147.06841
add_U_selenocysteine = 0.0000          # added to U - avg. 150.0379, mono. 150.95363
add_R_arginine = 0.0000                # added to R - avg. 156.1857, mono. 156.10111
add_Y_tyrosine = 0.0000                # added to Y - avg. 163.0633, mono. 163.06333
add_W_tryptophan = 0.0000              # added to W - avg. 186.0793, mono. 186.07931
add_B_user_amino_acid = 0.0000         # added to B - avg.   0.0000, mono.   0.00000
add_J_user_amino_acid = 0.0000         # added to J - avg.   0.0000, mono.   0.00000
add_X_user_amino_acid = 0.0000         # added to X - avg.   0.0000, mono.   0.00000
add_Z_user_amino_acid = 0.0000         # added to Z - avg.   0.0000, mono.   0.00000

#
# COMET_ENZYME_INFO _must_ be at the end of this parameters file
#
[COMET_ENZYME_INFO]
0.  No_enzyme              0      -           -
1.  Trypsin                1      KR          P
2.  Trypsin/P              1      KR          -
3.  Lys_C                  1      K           P
4.  Lys_N                  0      K           -
5.  Arg_C                  1      R           P
6.  Asp_N                  0      D           -
7.  CNBr                   1      M           -
8.  Glu_C                  1      DE          P
9.  PepsinA                1      FL          P
10. Chymotrypsin           1      FWYL        P
11. Chymotrypsin/P         1      FWYL        -
12. Elastase			   1      AGILV       P
        '''.format(**self.params['translations'])
        return template
