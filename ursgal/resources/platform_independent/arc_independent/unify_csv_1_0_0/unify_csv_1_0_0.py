#!/usr/bin/env python
'''
Unifies the result csvs

usage:
    ./unify_csv_1_0_0.py <input_file> <output_file> <uberSearch_lookup.pkl> <search_engine> <score_colname>

Fixes are listed in the main function. Resulting csv have unified fields, which
is most important for consitent modification formattting.
'''

from __future__ import print_function
import sys
import os
import pickle
import csv
import ursgal
import pyqms
import pprint
# import ursgal.ukb
import re
from collections import defaultdict
from copy import deepcopy as dc
import itertools
from decimal import *

# import time
# increase the field size limit to avoid crash if protein merge tags
# become too long does not work under windows
if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


DIFFERENCE_14N_15N = ursgal.ukb.DIFFERENCE_14N_15N
MOD_POS_PATTERN = re.compile(r'(?P<modname>.*):(?P<pos>[0-9]*)$')


def main(input_file=None, output_file=None, scan_rt_lookup=None,
         params=None, search_engine=None, score_colname=None):
    '''
    Arguments:
        input_file (str): input filename of csv which should be unified
        output_file (str): output filename of csv after unifying
        scan_rt_lookup (dict): dictionary with entries of scanID to
            retention time under key 'scan_2_rt'
        force (bool): force True or False
        params (dict): params as passed by ursgal
        search_engine(str): the search engine the csv file stems from
        score_colname (str): the column names of the search engine's
            score (i.e. 'OMSSA:pvalue')

    List of fixes

    All engines
        * Retention Time (s) is correctly set using _ursgal_lookup.pkl
          During mzML conversion to mgf the retention time for every spec
          is stored in a internal lookup and used later for setting the RT.
        * All modifications are checked if they were given in
          params['modifications'], converted to the name that was given
          there and sorted according to their position.
        * Fixed modifications are added in 'Modifications', if not reported
          by the engine.
        * The monoisotopic m/z for for each line is calculated (uCalc m/z),
          since not all engines report the monoisotopic m/z
        * Mass accuracy calculation (in ppm), also taking into account that
          not always the monoisotopic peak is picked
        * Rows describing the same PSM (i.e. when two proteins share the
          same peptide) are merged to one row.

    X!Tandem
        * 'RTINSECONDS=' is stripped from Spectrum Title if present in .mgf or
          in search result.

    Myrimatch
        * Spectrum Title is corrected
        * 15N label is not formatted correctly these modifications are
          removed for further analysis.
        * When using 15N modifications on amino acids and Carbamidomethyl
          myrimatch reports sometimes Carboxymethylation on Cystein.

    MS-GF+
        * 15N label is not formatted correctly these modifications are
          removed for further analysis.
        * 'Is decoy' column is properly set to true/false
        * Carbamidomethyl is updated and set if label is 15N

    OMSSA
        * Carbamidomethyl is updated and set

    MS-Amanda
        * multiple protein ID per peptide are splitted in two entries.
          (is done in MS-Amanda postflight)

    MSFragger
        * 15N modification have to be removed from Modifications and the
          merged modifications have to be corrected.

    pGlyco
        * reformat modifications
        * reformat glycan
    '''
    print(
        '''
[ unifycsv ] Converting {0} of engine {1} to unified CSV format...
        '''.format(
            os.path.basename(input_file),
            search_engine,
        )
    )

    # get the rows which define a unique PSM (i.e. sequence+spec+score...)
    # psm_defining_colnames = get_psm_defining_colnames(score_colname, search_engine)
    joinchar              = params['translations']['protein_delimiter']
    do_not_delete         = False
    created_tmp_files     = []
    use15N                = False
    search_engine         = search_engine.lower()

    if 'label' in params.keys():
        if params['label'] == '15N':
            use15N = True
    else:
        params['label'] = '14N'

    pyqms_mz_calc = params['translations']['use_pyqms_for_mz_calculation']
    # print(use15N)
    # sys.exit(1)
    # aa_exception_dict = params['translations']['aa_exception_dict']
    n_term_replacement = {
        'Ammonia-loss' : None,
        'Trimethyl'    : None,
        'Gly->Val'     : None,
    }
    fixed_mods   = {}
    opt_mods     = {}
    mod_dict     = {}
    cam          = False

    # modification masses are rounded to allow matching to unimod
    no_decimals = params['translations']['rounded_mass_decimals']
    if 'pipi' in search_engine:
        no_decimals = 1
    if 'moda' in search_engine:
        no_decimals = 0
    mass_format_string = '{{0:3.{0}f}}'.format(no_decimals)

    # mod pattern
    mod_pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )

    for mod_type in ['fix', 'opt']:
        for modification in params['mods'][mod_type]:
            aa = modification['aa']
            pos = modification['pos']
            name = modification['name']
            if name not in mod_dict.keys():
                mod_dict[name] = {
                    'mass' : modification['mass'],
                    'aa' : set(),
                    'pos': set(),
                }
            mod_dict[name]['aa'].add(aa)
            mod_dict[name]['aa'].add(pos)
            if 'N-term' in pos:
                n_term_replacement[name] = aa
            if mod_type == 'fix':
                fixed_mods[aa] = name
                if aa == 'C' and name == 'Carbamidomethyl':
                    cam = True
                    # allow also Carbamidomnethyl on U, since the mod name gets changed
                    # already in upeptide_mapper
                    # According to unimod, the mnodification is also on Selenocystein
                    # otherwise we should change that back so that it is skipped...
                    mod_dict['Carbamidomethyl']['aa'].add('U')
                    fixed_mods['U'] = 'Carbamidomethyl'
            if mod_type == 'opt':
                opt_mods[aa] = name

    if 'msfragger' in search_engine:
        ##########################
        # msfragger mod merge block
        # calculate possbile mod combos...
        # if 15N add artifical mods...
        getcontext().prec = 8
        getcontext().rounding = ROUND_UP
        # mod_dict_list = params['mods']['opt'] + params['mods']['fix']
        if use15N:
            aminoacids_2_check = set()
            for modname in mod_dict.keys():
                aminoacids_2_check |= mod_dict[modname]['aa']
            additional_15N_modifications = []
            for aminoacid, N15_Diff in ursgal.ukb.DICT_15N_DIFF.items():
                if aminoacid not in aminoacids_2_check:
                    continue
                if '_15N_{0}'.format(aminoacid) in mod_dict.keys():
                    print('''
                        Error in unify_csv
                        New mod_name already present in mod_dict'
                        This should never happen'''
                    )
                    sys.exit(1)
                mod_dict['_15N_{0}'.format(aminoacid)] = {
                    'mass' : N15_Diff,
                    'aa' : set([aminoacid]),
                    'pos': set(['any']),
                }
                # additional_dict = {
                #     'name' : '_15N_{0}'.format(aminoacid),
                #     'mass' : N15_Diff,
                #     'aa'   : aminoacid,
                #     'pos'  : 'any'

                # }
            #     additional_15N_modifications.append(
            #         additional_dict
            #     )
            # mod_dict_list += additional_15N_modifications

        # mod_lookup = {} #d['name'] for d in self.params['mods']['opt']]
        # for mod_dict in mod_dict_list:
        #     if mod_dict['name'] not in mod_lookup.keys():
        #         mod_lookup[mod_dict['name']] = []
        #     mod_lookup[ mod_dict['name'] ].append(mod_dict)

        mod_names = []
        for mod in sorted(list(mod_dict.keys())):
            mod_names.extend(itertools.repeat(mod, len(mod_dict[mod]['aa'])))
        mass_to_mod_combo = {}
        # we cover all combocs of mods
        for iter_length in range(2, len(mod_names) + 1):
            for name_combo in itertools.combinations(mod_names, iter_length):
                mass = 0
                for name in name_combo:
                    mass += Decimal(mod_dict[name]['mass'])
                rounded_mass = mass_format_string.format(mass)
                if rounded_mass not in mass_to_mod_combo.keys():
                    mass_to_mod_combo[rounded_mass] = set()
                mass_to_mod_combo[ rounded_mass ].add( name_combo )
        # print(mass_to_mod_combo.keys())
        # sys.exit(1)
        #msfragger mod merge block end
        ##############################

    aa_exception_dict = params['translations']['aa_exception_dict']
    for unusual_aa, original_aa_dict in aa_exception_dict.items():
        if 'unimod_name' in original_aa_dict.keys():
            if original_aa_dict['unimod_name'] not in mod_dict.keys():
                mod_dict[original_aa_dict['unimod_name']] = {
                    'mass' : 0.0,
                    'aa' : set(),
                    'pos': set(),
                }
            mod_dict[original_aa_dict['unimod_name']]['aa'].update(original_aa_dict['original_aa'])

    cc = ursgal.ChemicalComposition()
    ursgal.GlobalUnimodMapper._reparseXML()
    de_novo_engines = [
        'novor',
        'pepnovo',
        'uninovo',
        'deepnovo',
        'unknown_engine'
    ]
    database_search_engines = [
        'msamanda',
        'msgf',
        'myrimatch',
        'omssa',
        'xtandem',
        'msfragger',
        'pglyco',
    ]
    open_mod_search_engines = [
        'pipi',
        'moda',
    ]
    de_novo = False
    database_search = False
    open_mod_search = False
    for de_novo_engine in de_novo_engines:
        if de_novo_engine in search_engine:
            de_novo = True
    for db_se in database_search_engines:
        if db_se in search_engine:
            database_search = True
    for om_se in open_mod_search_engines:
        if om_se in search_engine:
            open_mod_search = True

    if params['translations']['enzyme'] != 'nonspecific':
        allowed_aa, cleavage_site, inhibitor_aa = params['translations']['enzyme'].split(';')
    else:
        allowed_aa    = ''.join( list( ursgal.ukb.NITROGENS.keys() ) )
        cleavage_site = 'C'
        inhibitor_aa  = ''
    allowed_aa += '-'

    if database_search is True:
        non_enzymatic_peps = set()
        conflicting_uparams = defaultdict(set)
        fasta_lookup_name = os.path.basename(
            os.path.abspath(
                params['translations']['database']
            )
        )
        upeptide_map_sort_key   = 'Protein ID'
        upeptide_map_other_keys = [
            'Sequence Start',
            'Sequence Stop',
            'Sequence Pre AA',
            'Sequence Post AA',
        ]
    # psm_counter = Counter()
    # if a PSM with multiple rows is found (i.e. in omssa results), the psm
    # rows are merged afterwards

    output_file_object = open(output_file, 'w')
    protein_id_output  = open(output_file + '_full_protein_names.txt', 'w')
    mz_buffer          = {}
    csv_kwargs         = {
        'extrasaction' : 'ignore'
    }
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'

    ze_only_buffer = {}

    app_mass_to_name_list_buffer = {}

    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader(
            in_file
        )
        # recheck if fieldnames are correct. These are corrected in the upeptide
        # mapper but if the search engine is a de novo engine then the fields
        # might be incorrect
        output_fieldnames = list(csv_input.fieldnames)
        for remove_fieldname in [
            'proteinacc_start_stop_pre_post_;',
            'Start',
            'Stop',
            'NIST score',
            'gi',
            'Accession',
        ]:
            if remove_fieldname not in output_fieldnames:
                continue
            output_fieldnames.remove(remove_fieldname)
        new_fieldnames = [
            'uCalc m/z',
            'Accuracy (ppm)',
            'Mass Difference',
            'Protein ID',
            'Sequence Start',
            'Sequence Stop',
            'Sequence Pre AA',
            'Sequence Post AA',
            'Complies search criteria',
            'Conflicting uparam',
            'Search Engine',
        ]

        for new_fieldname in new_fieldnames:
            if new_fieldname not in output_fieldnames:
                output_fieldnames.insert( -5, new_fieldname )
        csv_output = csv.DictWriter(
            output_file_object,
            output_fieldnames,
            **csv_kwargs
        )
        csv_output.writeheader()
        print('''[ unify_cs ] Buffering csv file''')
        csv_file_buffer = []
        for line_dict in csv_input:
            csv_file_buffer.append(line_dict)
        total_lines = len(csv_file_buffer)
        print('''[ unify_cs ] Buffering csv file done''')
        all_molecules = set()
        all_charges = set()
        line_dict_collector = []
        for line_nr, line_dict in enumerate(csv_file_buffer):
            if line_nr % 500 == 0:
                print(
                    '[ unify_cs ] Processing line number: {0}/{1} '.format(
                        line_nr,
                        total_lines,
                    ),
                    end = '\r'
                )

            line_dict['Search Engine'] = search_engine
            ##########################
            # Spectrum Title block
            # reformatting Spectrum Title,
            if line_dict['Spectrum Title'] != '':
                '''
                Valid for:
                    OMSSA
                    MSGF+
                    X!Tandem
                    pGlyco
                '''
                if 'RTINSECONDS=' in line_dict['Spectrum Title']:
                    line_2_split = line_dict['Spectrum Title'].split(' ')[0].strip()
                elif line_dict['Spectrum Title'].endswith('.dta'):
                    '.'.join(line_2_split = line_dict['Spectrum Title'].split('.')[:-2])
                else:
                    line_2_split = line_dict['Spectrum Title']
                line_dict['Spectrum Title'] = line_2_split

                input_file_basename, spectrum_id, _spectrum_id, charge = line_2_split.split('.')[:4]
                pure_input_file_name = ''

            elif 'scan=' in line_dict['Spectrum ID']:
                pure_input_file_name                = os.path.basename(
                    line_dict['Raw data location']
                )
                input_file_basename = pure_input_file_name.split(".")[0]
                # not using os.path.splitext because we could have multiple file
                # extensions (i.e. ".mzml.gz")

                '''
                Valid for:
                    myrimatch
                '''
                spectrum_id = line_dict['Spectrum ID'].split('=')[-1]
                line_dict['Spectrum Title'] = '{0}.{1}.{1}.{2}'.format(
                    input_file_basename,
                    spectrum_id,
                    line_dict['Charge']
                )

            elif line_dict['Spectrum Title'] == '':
                '''
                Valid for:
                    Novor
                    DeepNovo
                    MSFragger
                '''
                pure_input_file_name = os.path.basename(
                    line_dict['Raw data location']
                )
                input_file_basename = pure_input_file_name.split(".")[0]
                spectrum_id = line_dict['Spectrum ID']
                line_dict['Spectrum Title'] = '{0}.{1}.{1}.{2}'.format(
                    input_file_basename,
                    spectrum_id,
                    line_dict['Charge']
                )
            else:
                raise Exception( 'New csv format present for engine {0}'.format( engine ) )

            #update spectrum ID from block above
            line_dict['Spectrum ID'] = spectrum_id

            # now check for the basename in the scan rt lookup
            # possible cases:
            #   - input_file_basename
            #   - input_file_basename + prefix
            #   - input_file_basename - prefix

            input_file_basename_for_rt_lookup = None
            if input_file_basename in scan_rt_lookup.keys():
                input_file_basename_for_rt_lookup = input_file_basename
            else:
                basename_with_prefix = '{0}_{1}'.format(
                    params['prefix'],
                    input_file_basename
                )
                basename_without_prefix  = input_file_basename.replace(
                    params['prefix'],
                    ''
                )
                if basename_with_prefix in scan_rt_lookup.keys():
                    input_file_basename_for_rt_lookup = basename_with_prefix
                elif basename_without_prefix in scan_rt_lookup.keys():
                    input_file_basename_for_rt_lookup = basename_without_prefix
                else:
                    print(
                        '''
[ WARNING ] Could not find scan ID {0} in scan_rt_lookup[ {1} ]
                        '''.format(
                            spectrum_id,
                            input_file_basename
                        )
                    )

            #END Spectrum Title block
            ##########################
            spectrum_id = int(spectrum_id)
            retention_time_in_minutes = \
                scan_rt_lookup[ input_file_basename_for_rt_lookup ][ 'scan_2_rt' ]\
                    [ spectrum_id ]

            # We should check if data has minute format or second format...
            if scan_rt_lookup[ input_file_basename_for_rt_lookup ]['unit'] == 'second':
                rt_corr_factor = 1
            else:
                rt_corr_factor = 60
            line_dict['Retention Time (s)'] = float( retention_time_in_minutes ) * rt_corr_factor

            # try:
            precursor_mz = scan_rt_lookup[ input_file_basename_for_rt_lookup ][
                'scan_2_mz' ][ spectrum_id ]
            # except:
            #     print('\n\n\n')
            #     print(input_file_basename_for_rt_lookup)
            #     print('spectrum_id', spectrum_id, type(spectrum_id))
            #     exit(1)
            line_dict['Exp m/z'] = round(precursor_mz, 10)

            #########################
            # Buffering corrections #
            #########################
            main_buffer_key = '{Sequence} || {Charge} || {Modifications} || '.format(
                **line_dict
            ) + params['label']
            if main_buffer_key not in ze_only_buffer.keys():
                line_dict_update = {}
                ######################
                # Modification block #
                ######################

                # check MSFragger crazy mod merge first...
                if 'msfragger' in search_engine:
                    # we have to reformat the modifications
                    # M|14$15.994915|17$57.021465 to 15.994915:14;57.021465:17
                    # reformat it in Xtandem style
                    ms_fragger_reformatted_mods = []
                    if line_dict['Modifications'] == 'M':
                        # M stand for Modifications here, not Methionine
                        line_dict['Modifications'] = ''
                    else:
                        mod_list = line_dict['Modifications']
                        for single_mod in mod_list.split('|'):
                            if single_mod in ['M','']:
                                continue
                            msfragger_pos, raw_msfragger_mass = single_mod.split('$')
                            msfragger_mass = mass_format_string.format(
                                # mass rounded as defined above
                                Decimal(raw_msfragger_mass)
                            )
                            msfragger_pos = int(msfragger_pos)
                            if msfragger_mass in mass_to_mod_combo.keys():
                                explainable_combos = []
                                for combo in mass_to_mod_combo[msfragger_mass]:
                                    combo_explainable = set([True])
                                    tmp_mods = []
                                    for new_name in combo:
                                        meta_mod_info = mod_dict[new_name]
                                        single_mod_check = set([True])
                                        '''
                                        meta_mod_info = {
                                            'aa': set of aa,
                                            'mass': 42.010565,
                                            'pos': set of pos,
                                        }
                                        '''
                                        #check aa
                                        if '*' not in meta_mod_info['aa'] and \
                                            line_dict['Sequence'][msfragger_pos] not in meta_mod_info['aa']:
                                                single_mod_check.add(False)
                                        # check pos
                                        if 'any' not in meta_mod_info['pos']:
                                            pos_to_check = set()
                                            if 'Prot-N-term' in meta_mod_info['pos'] or\
                                                'N-term' in meta_mod_info['pos']:
                                                pos_to_check.add(0)
                                            elif 'Prot-C-term' in meta_mod_info['pos'] or \
                                                'C-term' in meta_mod_info['pos']:
                                                pos_to_check.add(int(len(line_dict['Sequence'])) - 1)
                                            else:
                                                pass
                                            if pos_to_check != set():
                                                if msfragger_pos not in pos_to_check:
                                                    single_mod_check.add(False)

                                        if all(single_mod_check):
                                            # MS Frager starts counting at zero
                                            pos_in_peptide_for_format_str = msfragger_pos + 1
                                            # we keep mass here so that the
                                            # correct name is added later in already
                                            # existing code
                                            tmp_mods.append(
                                                '{0}:{1}'.format(
                                                    meta_mod_info['mass'],
                                                    pos_in_peptide_for_format_str
                                                )
                                            )
                                        else:
                                            combo_explainable.add(False)
                                    if all(combo_explainable):
                                        explainable_combos.append(tmp_mods)
                                if len(explainable_combos) > 1:
                                    print(
                                        '''
                                        [ WARNING ] Multiple modification combinations possible
                                        [ WARNING ] to explain reported modification mass
                                        [ WARNING ] The following combination was chosen to continue:
                                        [ WARNING ] {0}
                                        '''.format(
                                            sorted(explainable_combos)[0],
                                        )
                                    )
                                    # pprint.pprint(explainable_combos)
                                    # ms_fragger_reformatted_mods += sorted(explainable_combos)[0]
                                    # sys.exit(1)
                                elif len(explainable_combos) == 1:
                                    ms_fragger_reformatted_mods += sorted(explainable_combos)[0]
                                else:
                                    # no combos explainable
                                    ms_fragger_reformatted_mods.append(
                                        '{0}:{1}'.format(
                                            raw_msfragger_mass,
                                            msfragger_pos + 1
                                        )
                                    )
                            else:
                                # MS Frager starts counting at zero
                                ms_fragger_reformatted_mods.append(
                                    '{0}:{1}'.format(
                                        raw_msfragger_mass,
                                        msfragger_pos + 1
                                    )
                                )
                        # print(line_dict['Modifications'])
                        # print(mass_to_mod_combo.keys())
                        # print(ms_fragger_reformatted_mods)
                        # sys.exit(1)
                        line_dict['Modifications'] = ';'.join( ms_fragger_reformatted_mods )

                ##################################################
                # Some engines do not report fixed modifications #
                ##################################################
                if fixed_mods != {}:
                    for pos, aminoacid in enumerate(line_dict['Sequence']):
                        if aminoacid in fixed_mods.keys():
                            name = fixed_mods[aminoacid]
                            tmp = '{0}:{1}'.format(
                                name,
                                pos + 1
                            )
                            append_mod = True
                            if tmp in line_dict['Modifications']:
                                # everything is ok :)
                                append_mod = False
                            elif ':{0}'.format(pos + 1) in line_dict['Modifications']:
                                # there is a mod at that position but is it the right one ?
                                for _m in line_dict['Modifications'].split(';'):
                                    match = MOD_POS_PATTERN.search(_m)
                                    if match is not None:
                                        mod = match.group('modname')
                                        pos = match.group('pos')
                                        try:
                                            if round(mod_dict[name]['mass'], 5) == round(float(mod), 5):
                                                append_mod = False
                                        except:
                                            pass

                            if append_mod:
                                tmp_mods = line_dict['Modifications'].split(';')
                                tmp_mods.append(tmp)
                                line_dict['Modifications'] = ';'.join( tmp_mods )
                ##################################################################
                # Myrimatch, MSGF+, and MSFragger can not handle 15N that easily #
                # Report all AAs moded with unknown modification                 #
                # Note: masses are checked below to avoid any mismatch           #
                ##################################################################
                if use15N:
                    if 'myrimatch' in search_engine or \
                            'msgfplus_v9979' in search_engine:
                        for p in range(1,len(line_dict['Sequence'])+1):
                                line_dict['Modifications'] = \
                                    line_dict['Modifications'].replace(
                                        'unknown modification:{0}'.format(p),
                                        '',
                                        1,
                                    )
                    if 'myrimatch' in search_engine:
                        if 'Carboxymethyl' in line_dict['Modifications'] and cam is True:
                            line_dict['Modifications'] = line_dict['Modifications'].replace(
                                'Carboxymethyl',
                                'Carbamidomethyl'
                            )
                        elif 'Delta:H(6)C(3)O(1)' in line_dict['Modifications']:
                            line_dict['Modifications'] = line_dict['Modifications'].replace(
                                'Delta:H(6)C(3)O(1)',
                                'Carbamidomethyl'
                            )

                tmp_mods = []
                tmp_mass_diff = []
                for modification in line_dict['Modifications'].split(';'):
                    raw_modification = modification
                    Nterm = False
                    Cterm = False
                    skip_mod = False
                    if modification == '' or modification == 'null':
                        continue
                    pos, mod = None, None
                    if 'pglyco' in search_engine:
                        try:
                            pos = int(modification.split(',')[0])
                            mod_pglyco = ','.join(modification.split(',')[1:])
                            mod = mod_pglyco.split('[')[0]
                        except:
                            match = mod_pattern.search( modification )
                            pos = int( match.group('pos') )
                            mod = modification[ :match.start() ]
                    else:
                        match = mod_pattern.search( modification )
                        pos = int( match.group('pos') )
                        mod = modification[ :match.start() ]
                    assert pos is not None, '''
                            The format of the modification {0}
                            is not recognized by ursgal'''.format(
                                modification
                            )
                    if pos <= 1:
                        Nterm = True
                        new_pos = 1
                    elif pos > len(line_dict['Sequence']):
                        Cterm = True
                        new_pos = len(line_dict['Sequence'])
                    else:
                        new_pos = pos
                    aa = line_dict['Sequence'][ new_pos - 1 ].upper()
                    # if aa in fixed_mods.keys():
                    #     fixed_mods[ aminoacid ]
                    #     # fixed mods are corrected/added already
                    #     continue
                    if mod in mod_dict.keys():
                        correct_mod = False
                        if aa in mod_dict[mod]['aa']:
                            # everything is ok
                            correct_mod = True
                        elif Nterm or Cterm:
                            if '*' in mod_dict[mod]['aa']:
                                correct_mod = True
                                # still is ok
                        assert correct_mod is True,'''
                                A modification was reported for an aminoacid for which it was not defined
                                unify_csv cannot deal with this, please check your parameters and engine output
                                reported modification: {0} on {1}
                                modifications in parameters: {2}
                                '''.format(
                                    mod,
                                    aa,
                                    params['mods']
                                )
                    elif 'unknown modification' == mod:
                        modification_known = False
                        if aa in opt_mods.keys():
                            # fixed mods are corrected/added already
                            modification = '{0}:{1}'.format(opt_mods[aa],new_pos)
                            modification_known = True
                        assert modification_known == True,'''
                                unify csv does not work for the given unknown modification for
                                {0} {1} aa: {2}
                                maybe an unknown modification with terminal position was given?
                                '''.format(
                                    line_dict['Sequence'], modification, aa
                                )
                    else:
                        float_mod = float(mod)
                        masses_2_test = [float_mod]
                        if use15N:
                            substract_15N_diff = False
                            if aa in fixed_mods.keys() and 'msgfplus' in search_engine and pos != 0:
                                substract_15N_diff = True
                            if 'msfragger' in search_engine and float_mod > 4:
                                # maximum 15N labeling is 3.988 Da (R)
                                substract_15N_diff = True
                            if substract_15N_diff:
                                masses_2_test.append(float_mod - ursgal.ukb.DICT_15N_DIFF[aa])
                        # try:
                        #works always but returns empty list...
                        name_list = []
                        for mass_2_test in masses_2_test:
                            mass_buffer_key = mass_format_string.format(mass_2_test)
                            #buffer increases speed massively...
                            if mass_buffer_key not in app_mass_to_name_list_buffer.keys():
                                app_mass_to_name_list_buffer[mass_buffer_key] = ursgal.GlobalUnimodMapper.appMass2name_list(
                                    float(mass_buffer_key),
                                    decimal_places = no_decimals
                                )
                            name_list += app_mass_to_name_list_buffer[mass_buffer_key]
                        # print(name_list)
                        # except:
                        #     print('''
                        #         A modification was reported that was not included in the search parameters
                        #         unify_csv cannot deal with this, please check your parameters and engine output
                        #         reported modification: {0}
                        #         modifications in parameters: {1}
                        #         '''.format(mod, params['translations']['modifications'])
                        #     )
                        #     raise Exception('unify_csv failed because a '\
                        #         'modification was reported that was not '\
                        #         'given in params: {0}'.format(modification)
                        #     )
                        mapped_mod = False
                        for name in name_list:
                            if name in mod_dict.keys():
                                if aa in mod_dict[name]['aa']:
                                    modification = '{0}:{1}'.format(name, new_pos)
                                    mapped_mod = True
                                elif Nterm and '*' in mod_dict[name]['aa']:
                                    modification = '{0}:{1}'.format(name, 0)
                                    mapped_mod = True
                                else:
                                    continue
                            elif use15N and name in [
                                'Label:15N(1)',
                                'Label:15N(2)',
                                'Label:15N(3)',
                                'Label:15N(4)'
                            ]:
                                mapped_mod = True
                                skip_mod = True
                                break

                        if open_mod_search is True and mapped_mod is False:
                            skip_mod = True
                            tmp_mass_diff.append('{0}:{1}'.format(mod, pos))
                            continue
                        assert mapped_mod is True, '''
                                A mass was reported that does not map on any unimod or userdefined modification
                                or the modified aminoacid is not the specified one
                                unify_csv cannot deal with this, please check your parameters and engine output
                                sequence: {4}
                                reported mass: {0}
                                maps on: {1}
                                reported modified aminoacid: {2}
                                modifications in parameters: {3}
                                '''.format(
                                    mod,
                                    name_list,
                                    aa,
                                    params['mods'],
                                    line_dict['Sequence']
                                )
                    if modification in tmp_mods:
                        add_n_term_mod = False
                        _mod, _pos = modification.split(':')
                        _aa = line_dict['Sequence'][int(_pos) - 1]
                        if _aa in mod_dict[_mod]['aa']:
                            if 'N-term' in mod_dict[_mod]['aa']:
                                add_n_term_mod = True
                            elif 'Prot-N-term' in mod_dict[_mod]['aa']:
                                add_n_term_mod = True
                        if add_n_term_mod:
                            modification = modification.replace(
                                '{0}:1'.format(_mod),
                                '{0}:0'.format(_mod)
                            )
                        # else:
                        #     skip_mod = True
                    if skip_mod is True:
                        continue
                    tmp_mods.append(modification)
                if 'msfragger' in search_engine:
                    org_mass_diff = line_dict['Mass Difference']
                    tmp_mass_diff.append('{0}:n'.format(org_mass_diff))
                if 'pglyco' in search_engine:
                    line_dict['Sequence'] = line_dict['Sequence'].replace('J', 'N')
                line_dict_update['Modifications'] = ';'.join(tmp_mods)
                line_dict_update['Mass Difference'] = ';'.join(tmp_mass_diff)
                #
                # ^^--------- REPLACED MODIFICATIONS! ---------------^
                #
                for unimod_name in n_term_replacement.keys():
                    if '{0}:1'.format(unimod_name) in line_dict_update['Modifications'].split(';'):
                        if unimod_name in mod_dict.keys():
                            aa = mod_dict[unimod_name]['aa']
                            if aa != ['*']:
                                if line_dict['Sequence'][0] in aa:
                                    continue
                        line_dict_update['Modifications'] = line_dict_update['Modifications'].replace(
                            '{0}:1'.format(unimod_name),
                            '{0}:0'.format(unimod_name)
                            )
                ##########################
                # Modification block end #
                ##########################

                line_dict_update['Sequence'] = line_dict['Sequence']
                #
                # ^^--------- REPLACED SEQUENCE! ---------------^
                #
                # remove the double ';''
                if line_dict_update['Modifications'] != '':
                    tmp = []
                    positions = set()
                    for e in line_dict_update['Modifications'].split(';'):
                        if e == '':
                            # that remove the doubles ....
                            continue
                        else:
                            # other way to do it...
                            # pos_of_split_point = re.search( ':\d*\Z', e )
                            # pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )
                            for occ, match in enumerate(mod_pattern.finditer(e)):
                                mod = e[:match.start()]
                                mod_pos = e[match.start()+1:]
                                # mod, pos = e.split(':')
                                m = (int(mod_pos), mod)
                                if m not in tmp:
                                    tmp.append(m)
                                    positions.add(int(mod_pos))
                    tmp.sort()
                    line_dict_update['Modifications'] = ';'.join(
                        [
                            '{m}:{p}'.format( m=mod, p=pos) for pos, mod in tmp
                        ]
                    )
                    if len(tmp) != len(positions):
                        print(
                            '[ WARNING ] {Sequence}#{Modifications} will be skipped, because it contains two mods at the same position!'.format(
                                **line_dict_update
                            )
                        )
                        continue

                all_molecules.add(
                    '{Sequence}#{Modifications}'.format(
                        **line_dict_update
                    )
                )
                all_charges.add(int(line_dict['Charge']))


                # ------------
                # BUFFER END
                # -----------
                ze_only_buffer[ main_buffer_key ] = line_dict_update

            line_dict_update = ze_only_buffer[ main_buffer_key ]
            line_dict.update( line_dict_update )

            if 'pglyco' in search_engine:
                try:
                    Hex, HexNAc, NeuAc, NeuGc, dHex = line_dict[
                        'Glycan'].strip(' ').split(' ')
                except:
                    print(line_dict['Glycan'])
                    exit()
                line_dict['Glycan'] = 'Hex({0})HexNac({1})NeuAc({2})NeuGc({3})dHex({4})'.format(
                    Hex,
                    HexNAc,
                    NeuAc,
                    NeuGc,
                    dHex,
                )

            # protein block, only for database search engine
            if database_search is True:
                # check for correct cleavage sites and set a new field to
                # verify correct enzyme performance
                lookup_identifier = '{0}><{1}'.format(
                    line_dict['Sequence'],
                    fasta_lookup_name
                )
                if lookup_identifier not in conflicting_uparams.keys():
                    split_collector = { }
                    for key in [ upeptide_map_sort_key ] + upeptide_map_other_keys:
                        split_collector[ key ] = line_dict[key].split(joinchar)
                    sorted_upeptide_maps = []
                    for pos, protein_id in enumerate(sorted( split_collector[ upeptide_map_sort_key ] ) ):
                        dict_2_append = {
                            upeptide_map_sort_key : protein_id
                        }

                        for key in upeptide_map_other_keys:
                            dict_2_append[key] = split_collector[key][pos]
                        sorted_upeptide_maps.append(
                            dict_2_append
                        )
                    # pprint.pprint(line_dict)
                    # print(sorted_upeptide_maps)
                    # sys.exit(1)
                    if sorted_upeptide_maps == []:
                        print('''
[ WARNING ] The peptide {0} could not be mapped to the
[ WARNING ] given database {1}
[ WARNING ] {2}
[ WARNING ] This PSM will be skipped.
                            '''.format(
                                line_dict['Sequence'],
                                params['translations']['database'],
                            )
                        )
                        continue
                    peptide_fullfills_enzyme_specificity = False
                    last_protein_id = None
                    for major_protein_info_dict in sorted_upeptide_maps:
                        protein_specifically_cleaved   = False
                        nterm_correct = False
                        cterm_correct = False
                        '''
                            'Sequence Start',
                            'Sequence Stop',
                            'Sequence Pre AA',
                            'Sequence Post AA',

                        '''
                        protein_info_dict_buffer = []
                        if ';' in major_protein_info_dict['Sequence Start']:
                            tmp_split_collector =defaultdict(list)
                            for key in upeptide_map_other_keys:
                                tmp_split_collector[key] = major_protein_info_dict[key].split(';')
                            for pos, p_id in enumerate(tmp_split_collector['Sequence Start']):
                                dict_2_append = {
                                    'Protein ID' : major_protein_info_dict['Protein ID']
                                }
                                for key in tmp_split_collector.keys():
                                    dict_2_append[key] = tmp_split_collector[key][pos]
                                protein_info_dict_buffer.append(dict_2_append)
                        else:
                            protein_info_dict_buffer = [ major_protein_info_dict ]

                        for protein_info_dict in protein_info_dict_buffer:
                            if params['translations']['keep_asp_pro_broken_peps'] is True:
                                if line_dict['Sequence'][-1] == 'D' and\
                                        protein_info_dict['Sequence Post AA'] == 'P':
                                    cterm_correct = True
                                if line_dict['Sequence'][0] == 'P' and\
                                        protein_info_dict['Sequence Pre AA'] == 'D':
                                    nterm_correct = True

                            if cleavage_site == 'C':
                                if protein_info_dict['Sequence Pre AA'] in allowed_aa\
                                        or protein_info_dict['Sequence Start'] in ['1', '2', '3']:
                                    if line_dict['Sequence'][0] not in inhibitor_aa\
                                            or protein_info_dict['Sequence Start'] in ['1', '2', '3']:
                                        nterm_correct = True
                                if protein_info_dict['Sequence Post AA'] not in inhibitor_aa:
                                    if line_dict['Sequence'][-1] in allowed_aa\
                                         or protein_info_dict['Sequence Post AA'] == '-':
                                        cterm_correct = True

                            elif cleavage_site == 'N':
                                if protein_info_dict['Sequence Post AA'] in allowed_aa:
                                    if line_dict['Sequence'][-1] not in inhibitor_aa\
                                            or protein_info_dict['Sequence Post AA'] == '-':
                                        cterm_correct = True
                                if protein_info_dict['Sequence Pre AA'] not in inhibitor_aa\
                                    or protein_info_dict['Sequence Start'] in ['1', '2', '3']:
                                    if line_dict['Sequence'][0] in allowed_aa\
                                        or protein_info_dict['Sequence Start'] in ['1', '2', '3']:
                                        nterm_correct = True
                            # if line_dict['Sequence'] == 'SPRPGAAPGSR':
                            #     print(protein_info_dict)
                            #     print(nterm_correct, cterm_correct)
                            if params['translations']['semi_enzyme'] is True:
                                if cterm_correct is True or nterm_correct is True:
                                    protein_specifically_cleaved = True
                            elif cterm_correct is True and nterm_correct is True:
                                protein_specifically_cleaved = True
                            if protein_specifically_cleaved is True:
                                peptide_fullfills_enzyme_specificity = True
                                last_protein_id = protein_info_dict['Protein ID']
                    # we may test for further criteria to set this flag/fieldname
                    # e.g. the missed cleavage count etc.
                    if peptide_fullfills_enzyme_specificity is False:
                        non_enzymatic_peps.add( line_dict['Sequence'] )
                        conflicting_uparams[lookup_identifier].add(
                            'enzyme'
                        )

                    #check here if missed cleavage count is correct...
                    missed_cleavage_counter = 0
                    if params['translations']['enzyme'] != 'ACDEFGHIKLMNPQRSTVWY;C;':
                        for aa in allowed_aa:
                            if aa == '-':
                                continue
                            if cleavage_site == 'C':
                                if inhibitor_aa == '':
                                    missed_cleavage_pattern = aa
                                else:
                                    missed_cleavage_pattern = '{0}[^{1}]'.format(
                                        aa, inhibitor_aa
                                    )
                                missed_cleavage_counter += \
                                    len(re.findall(missed_cleavage_pattern, line_dict['Sequence']))
                            elif cleavage_site == 'N':
                                if inhibitor_aa == '':
                                    missed_cleavage_pattern = aa
                                else:
                                    missed_cleavage_pattern = '[^{1}]{0}'.format(
                                        aa, inhibitor_aa
                                    )
                                missed_cleavage_counter += \
                                    len(re.findall(missed_cleavage_pattern, line_dict['Sequence']))
                    if missed_cleavage_counter > params['translations']['max_missed_cleavages']:
                        conflicting_uparams[lookup_identifier].add('max_missed_cleavages')
                # count each PSM occurence to check whether row-merging is needed:
                # psm = tuple([line_dict[x] for x in psm_defining_colnames])
                # psm_counter[psm] += 1

                if len(conflicting_uparams[lookup_identifier]) == 0:
                    # all tested search criteria true
                    line_dict['Complies search criteria'] = 'true'
                else:
                    line_dict['Complies search criteria'] = 'false'
                    line_dict['Conflicting uparam'] = ';'.join(
                        sorted(conflicting_uparams[lookup_identifier])
                    )
            line_dict_collector.append(line_dict)

        # --------------------------------
        # mz calc and accuracy calc block
        # --------------------------------

        print('[ unify_cs ] calculating mz accuracies')
        # build IsotopologueLibrary
        molecule2hill_dict = {}
        for molecule in all_molecules:
            if 'X' in molecule.upper():
                cc.use(molecule.replace('X', ''))
            else:
                cc.use(molecule)
            if use15N:
                number_N = dc( cc['N'] )
                cc['15N'] = number_N
                del cc['N']
                if cam:
                    c_count = molecule.split('#')[0].count('C')
                    cc['14N'] = c_count
                    cc['15N'] -= c_count
            cc_hill = cc.hill_notation_unimod()
            molecule2hill_dict[molecule] = '+{0}'.format(cc_hill)

        if pyqms_mz_calc:
            isotopologue_dict = pyqms.IsotopologueLibrary(
                molecules=list(molecule2hill_dict.values()),
                charges=list(all_charges),
                verbose=True
            )

        # calculate m/z
        for collected_line_dict in line_dict_collector:
            molecule = '{Sequence}#{Modifications}'.format(
                **collected_line_dict
            )
            cc_hill = molecule2hill_dict[molecule].strip('+')
            charge = int(collected_line_dict['Charge'])
            if pyqms_mz_calc:
                isotopologue_mzs = isotopologue_dict[cc_hill][
                'env'][(('N', '0.000'),)][charge]['mz']

                calc_mz = round(isotopologue_mzs[0], 10)
                min_accuracy = (float(collected_line_dict['Exp m/z']) - calc_mz)/calc_mz * 1e6
                for iso_mz in isotopologue_mzs[1:]:
                    isotopologue_acc = (float(collected_line_dict['Exp m/z']) - iso_mz)/iso_mz * 1e6
                    if abs(isotopologue_acc) > abs(min_accuracy):
                        break
                    else:
                        min_accuracy = isotopologue_acc
            else:
                cc.use(molecule2hill_dict[molecule])
                mass = cc._mass()
                calc_mz = ursgal.ucore.calculate_mz(
                    mass,
                    int(collected_line_dict['Charge'])
                )
                min_accuracy = (float(collected_line_dict['Exp m/z']) - calc_mz)/calc_mz * 1e6
                for isotope in range(1,6):
                    iso_mz = ursgal.ucore.calculate_mz(
                        mass + isotope*1.008664904,
                        int(collected_line_dict['Charge'])
                    )
                    isotopologue_acc = (float(collected_line_dict['Exp m/z']) - iso_mz)/iso_mz * 1e6
                    if abs(isotopologue_acc) > abs(min_accuracy):
                        break
                    else:
                        min_accuracy = isotopologue_acc

            collected_line_dict['uCalc m/z'] = calc_mz
            if database_search is True:
                if 'Calc m/z' in collected_line_dict.keys() and\
                    collected_line_dict['Calc m/z'] == '':
                    collected_line_dict['Calc m/z'] = calc_mz

            collected_line_dict['Accuracy (ppm)'] = round(min_accuracy, 5)

            csv_output.writerow(collected_line_dict)

    output_file_object.close()

    if database_search is True:
        # upapa.purge_fasta_info( fasta_lookup_name )
        if len(non_enzymatic_peps) != 0:
            print(
                '''
                [ WARNING ] The following peptides do not reflect the enzyme
                [ WARNING ] specificity:
                [ WARNING ] {0}
                [ WARNING ] These PSMs are marked 'Complies search criteria' = 'False'
                '''.format(
                    non_enzymatic_peps
                )
            )
    # sys.exit(1)
    # if there are multiple rows for a PSM, we have to merge them aka rewrite the csv...
    # if psm_counter != Counter():
    #     if max(psm_counter.values()) > 1:
    #         merge_duplicate_psm_rows(output_file, psm_counter, psm_defining_colnames, params['translations']['psm_merge_delimiter'])
            '''
            to_be_written_csv_lines = merge_duplicate_psm_rows(
                to_be_written_csv_lines,
                psm_counter
            )
            '''
        '''
        do output_file magic with to_be_written_csv_lines
        '''
    if do_not_delete is False:
        created_tmp_files.append( output_file + '_full_protein_names.txt' )
    return created_tmp_files


# def get_psm_defining_colnames(score_colname, search_engine):
#     '''
#     Returns the all PSM-defining column names (i.e spectrum & peptide,
#     but also score field because sometimes the same PSMs are reported
#     with different scores...
#     '''
#     psm = [
#         'Spectrum Title',
#         'Sequence',
#         'Modifications',
#         'Charge',
#         'Is decoy',
#     ]
#     if 'msfragger' in search_engine:
#         psm.append('MSFragger:Neutral mass of peptide')
#     if score_colname:
#         psm.append(score_colname)
#     return psm


# def merge_rowdicts(list_of_rowdicts, joinchar, alt_joinchar='<|>'):
#     '''
#     Merges CSV rows. If the column values are conflicting, they
#     are joined with a character (joinchar).
#     Special case: proteinaccessions are not joined with the joinchar,
#     but rather with alt_joinchar.
#     '''
#     merged_d = {}
#     fieldnames = list_of_rowdicts[0].keys()
#     for fieldname in fieldnames:

#         joinchar_used = joinchar
#         # if fieldname == 'proteinacc_start_stop_pre_post_;':
#         #     joinchar_used = alt_joinchar

#         values = {d[fieldname] for d in list_of_rowdicts}
#         if len(values) == 1:
#             merged_d[fieldname] = list(values)[0]
#         else:
#             merged_d[fieldname] = joinchar_used.join(sorted(values))
#     return merged_d


# def merge_duplicate_psm_rows(unified_csv_path, psm_counter, psm_defining_colnames, joinchar):
#     '''
#     Rows describing the same PSM (i.e. when two proteins share the
#     same peptide) are merged to one row.
#     '''
#     rows_to_merge_dict = defaultdict(list)

#     tmp_file = unified_csv_path + ".tmp"
#     os.rename(unified_csv_path, tmp_file)
#     print('Merging rows of the same PSM...')
#     with open(tmp_file, 'r') as tmp, open(unified_csv_path, 'w', newline='') as out:
#         tmp_reader = csv.DictReader(tmp)
#         writer = csv.DictWriter(out, fieldnames=tmp_reader.fieldnames)
#         writer.writeheader()
#         for row in tmp_reader:
#             psm = tuple([row[x] for x in psm_defining_colnames])
#             # each unique combination of these should only have ONE row!
#             # i.e. combination of seq+spec+score
#             if psm_counter[psm] == 1:
#                 # no duplicate = no problem, we can just write the row again
#                 writer.writerow(row)
#             elif psm_counter[psm] > 1:
#                 # we have to collect all rows of this psm, and merge + write them later!
#                 rows_to_merge_dict[psm].append(row)
#             else:
#                 raise Exception("This should never happen.")
#         # finished parsing the old unmerged unified csv
#         for rows_to_merge in rows_to_merge_dict.values():
#             writer.writerow(
#                 merge_rowdicts(rows_to_merge, joinchar=joinchar)
#             )
#     os.remove(tmp_file)  # remove the old unified csv that contains duplicate rows



if __name__ == '__main__':
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(1)

    scan_rt_lookup = pickle.load(open(sys.argv[3], 'rb'))

    params = {
        'translations' : {
            # 'aa_exception_dict' : {
            #     'J' : {
            #     'original_aa' : 'L',
            #     },
            #     'O' : {
            #         'original_aa' : 'K',
            #         'unimod_name' : 'Methylpyrroline',
            #     },
            # },
            'mods' : {
                'fix': {
                    '_id': 1,
                    'aa': 'C',
                    'composition': {'C': 2, 'H': 3, 'N': 1, 'O': 1},
                    'id': '4',
                    'mass': 57.021464,
                    'name': 'Carbamidomethyl',
                    'org': 'C,fix,any,Carbamidomethyl',
                    'pos': 'any',
                    'unimod': True
                },
                'opt': {
                    '_id': 3,
                    'aa': 'M',
                    'composition': {'O': 1},
                    'id': '35',
                    'mass': 15.994915,
                    'name': 'Oxidation',
                    'org': 'M,opt,any,Oxidation',
                    'pos': 'any',
                    'unimod': True
                },
            },
            'protein_delimiter'        : '<|>',
            'enzyme'                   : 'KR;C;P',
            'keep_asp_pro_broken_peps' : True,
            'semi_enzyme'              : False,
            'decoy_tag'                : 'decoy_',
            # 'psm_merge_delimiter'      : ';',
            'precursor_mass_tolerance_plus':5,
            'precursor_mass_tolerance_minus':5,
            'precursor_isotope_range': '0,1',
            'max_missed_cleavages' : 2
        },
        # 'label'                    : '15N',
        'label' : '',
        'prefix'                   : None
    }
    params['translations']['database'] = sys.argv[6]
    # start_time = time.time()
    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        scan_rt_lookup = scan_rt_lookup,
        params         = params,
        search_engine  = sys.argv[4],
        score_colname  = sys.argv[5]
    )    # end_time = time.time()
    # print(end_time-start_time)
    # input()
