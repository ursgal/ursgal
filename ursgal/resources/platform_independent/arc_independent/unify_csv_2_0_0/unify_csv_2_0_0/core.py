#!/usr/bin/env python3.4
'''
Unifies the result csvs

usage:
    ./unify_csv_2_0_0.py <input_file> <output_file> <uberSearch_lookup.pkl> <search_engine> <score_colname>

Fixes are listed in the main function. Resulting csv have unified fields, which
is most important for consitent modification formattting.
'''

from __future__ import print_function
import sys
import os
import pickle
import csv
import copy

import ursgal
# ^---- why does a standalone program require ursgal ?
import pprint
import re
from collections import defaultdict
from copy import deepcopy as dc
import itertools
# from decimal import *
# ^--- be explicit! or
import decimal
import unify_csv_2_0_0


def reformat_ursgal_mods(params=None, variables=None):
    #
    for mod_type in ['fix', 'opt']:
        for modification in params['mods'][mod_type]:
            aa = modification['aa']
            pos = modification['pos']
            name = modification['name']
            if variables['mod_dict'] is None:
                variables['mod_dict'] = {}

            if name not in variables['mod_dict'].keys():
                variables['mod_dict'][name] = {
                    'mass' : modification['mass'],
                    'aa' : set(),
                    'pos': set(),
                }
            variables['mod_dict'][name]['aa'].add(aa)
            variables['mod_dict'][name]['aa'].add(pos)
            if 'N-term' in pos:
                variables['n_term_replacement'][name] = aa
            if mod_type == 'fix':
                if variables['fixed_mods'] is None:
                    variables['fixed_mods'] = {}

                variables['fixed_mods'][aa] = name
                if aa == 'C' and name == 'Carbamidomethyl':
                    cam = True
                    # allow also Carbamidomnethyl on U, since the mod name gets changed
                    # already in upeptide_mapper
                    # According to unimod, the mnodification is also on Selenocystein
                    # otherwise we should change that back so that it is skipped...
                    variables['mod_dict']['Carbamidomethyl']['aa'].add('U')
                    variables['fixed_mods']['U'] = 'Carbamidomethyl'
            if mod_type == 'opt':
                if variables['opt_mods'] is None:
                    variables['opt_mods'] = {}
                variables['opt_mods'][aa] = name
    return variables


def main(
    input_file=None,
    output_file=None,
    scan_rt_lookup=None,
    params=None,
    search_engine=None,
    score_colname=None
):
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

    '''

    # from unify_csv_2_0_0.engines import _engine_independent


    # import time
    # increase the field size limit to avoid crash if protein merge tags
    # become too long does not work under windows
    if sys.platform != 'win32':
        csv.field_size_limit(sys.maxsize)

    # DIFFERENCE_14N_15N = ursgal.ukb.DIFFERENCE_14N_15N
    # ^--- has to be in main scope as main is imported by ursgal directly ..
    # is actually not used anymore

    print(
        '''
[ unifycsv ] Converting {0} of engine {1} to unified CSV format...
        '''.format(
            os.path.basename(input_file),
            search_engine,
        )
    )

    # NOTE: since we refactor the loops a lot, we need to keep track of all
    #       variables.
    # PROPOSAL: let's use a centralized dict for all variable so we can pass
    #           it through the functions as well, let's say variables

    variables = {
        'scan_rt_lookup' : scan_rt_lookup,
        'params'         : params
    }
    # get the rows which define a unique PSM (i.e. sequence+spec+score...)
    # psm_defining_colnames = get_psm_defining_colnames(score_colname, search_engine)
    joinchar              = params['translations']['protein_delimiter']
    do_not_delete         = False
    created_tmp_files     = []

    variables['use15N']   = False
    variables['search_engine'] = search_engine.lower()
    variables['joinchar'] = joinchar

    # ^--- sooner or later this should end up in variables ...

    if 'label' in params.keys():
        if params['label'] == '15N':
            variables['use15N'] = True
    else:
        params['label'] = '14N'
    # print(variables['use15N'])
    # sys.exit(1)
    # aa_exception_dict = params['translations']['aa_exception_dict']
    variables['n_term_replacement'] = {
        'Ammonia-loss' : None,
        'Trimethyl'    : None,
        'Gly->Val'     : None,
    }
    # fixed_mods   = {}
    # opt_mods     = {}
    # mod_dict     = {}
    # cam          = False

    variables['fixed_mods'] = None
    variables['opt_mods'] = None
    variables['mod_dict'] = None
    variables['cam'] = False
    variables['app_mass_to_name_list_buffer'] = {}
    variables['cc'] = ursgal.ChemicalComposition()

    # modification masses are rounded to allow matching to unimod
    no_decimals = params['translations']['rounded_mass_decimals']
    variables['no_decimals'] = no_decimals

    if 'pipi' in search_engine.lower():
        no_decimals = 1
    if 'moda' in search_engine.lower():
        no_decimals = 0
    variables['mass_format_string'] = '{{0:3.{0}f}}'.format(no_decimals)

    # mod pattern
    variables['mod_pattern'] = re.compile( r''':(?P<pos>[0-9]*$)''' )

    variables = reformat_ursgal_mods(
        params=params,
        variables=variables
    )
    # for mod_type in ['fix', 'opt']:
    #     for modification in params['mods'][mod_type]:
    #         aa = modification['aa']
    #         pos = modification['pos']
    #         name = modification['name']
    #         if name not in mod_dict.keys():
    #             mod_dict[name] = {
    #                 'mass' : modification['mass'],
    #                 'aa' : set(),
    #                 'pos': set(),
    #             }
    #         mod_dict[name]['aa'].add(aa)
    #         mod_dict[name]['aa'].add(pos)
    #         if 'N-term' in pos:
    #             n_term_replacement[name] = aa
    #         if mod_type == 'fix':
    #             fixed_mods[aa] = name
    #             if aa == 'C' and name == 'Carbamidomethyl':
    #                 cam = True
    #                 # allow also Carbamidomnethyl on U, since the mod name gets changed
    #                 # already in upeptide_mapper
    #                 # According to unimod, the mnodification is also on Selenocystein
    #                 # otherwise we should change that back so that it is skipped...
    #                 mod_dict['Carbamidomethyl']['aa'].add('U')
    #                 fixed_mods['U'] = 'Carbamidomethyl'
    #         if mod_type == 'opt':
    #             opt_mods[aa] = name

    if 'msfragger' in search_engine.lower():
        ##########################
        # msfragger mod merge block
        # calculate possbile mod combos...
        # if 15N add artifical mods...
        decimal.getcontext().prec = 8
        decimal.getcontext().rounding = decimal.ROUND_UP
        # mod_dict_list = params['mods']['opt'] + params['mods']['fix']
        if variables['use15N']:
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
                    mass += decimal.Decimal(mod_dict[name]['mass'])
                rounded_mass = mass_format_string.format(mass)
                if rounded_mass not in mass_to_mod_combo.keys():
                    mass_to_mod_combo[rounded_mass] = set()
                mass_to_mod_combo[ rounded_mass ].add( name_combo )
        # print(mass_to_mod_combo.keys())
        # sys.exit(1)
        #msfragger mod merge block end
        ##############################

    ursgal.GlobalUnimodMapper._reparseXML()
    de_novo_engines = [
        'novor',
        'pepnovo',
        'uninovo',
        'unknown_engine'
    ]
    database_search_engines = [
        'msamanda',
        'msgf',
        'myrimatch',
        'omssa',
        'xtandem',
        'msfragger',
    ]
    open_mod_search_engines = [
        'pipi',
        'moda',
    ]
    variables['de_novo'] = False
    variables['database_search'] = False
    variables['open_mod_search'] = False
    for de_novo_engine in de_novo_engines:
        if de_novo_engine in search_engine.lower():
            variables['de_novo'] = True
    for db_se in database_search_engines:
        if db_se in search_engine.lower():
            variables['database_search'] = True
    for om_se in open_mod_search_engines:
        if om_se in search_engine.lower():
            variables['open_mod_search'] = True

    if params['translations']['enzyme'] != 'nonspecific':
        allowed_aa, cleavage_site, inhibitor_aa = params['translations']['enzyme'].split(';')
    else:
        allowed_aa    = ''.join( list( ursgal.ukb.NITROGENS.keys() ) )
        cleavage_site = 'C'
        inhibitor_aa  = ''
    allowed_aa += '-'

    variables['cleavage_site'] = cleavage_site
    variables['allowed_aa']    = allowed_aa
    variables['inhibitor_aa']  = inhibitor_aa


    if variables['database_search'] is True:
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
        variables['upeptide_map_sort_key'] = 'Protein ID'
        variables['upeptide_map_other_keys'] = upeptide_map_other_keys
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



    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader(
            in_file
        )
        csv_fieldnames = list(csv_input.fieldnames)
        variables['fieldnames'] = copy.deepcopy(
            csv_fieldnames
        )
        # recheck if fieldnames are correct. These are corrected in the upeptide
        # mapper but if the search engine is a de novo engine then the fields
        # might be incorrect
        for remove_fieldname in [
            'proteinacc_start_stop_pre_post_;',
            'Start',
            'Stop',
            'NIST score',
            'gi',
            'Accession',
        ]:
            if remove_fieldname not in csv_fieldnames:
                continue
            csv_fieldnames.remove(remove_fieldname)
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
        ]

        for new_fieldname in new_fieldnames:
            if new_fieldname not in csv_fieldnames:
                csv_fieldnames.insert(
                    -5, # why minus 5?
                    new_fieldname
                )
        csv_output = csv.DictWriter(
            output_file_object,
            csv_fieldnames,
            **csv_kwargs
        )
        csv_output.writeheader()
        print('''[ unify_cs ] Buffering csv file''')
        csv_file_buffer = []
        for line_dict in csv_input:
            csv_file_buffer.append(line_dict)
        total_lines = len(csv_file_buffer)
        print('''[ unify_cs ] Buffering csv file done''')
        for line_nr, line_dict in enumerate(csv_file_buffer):
            if line_nr % 500 == 0:
                print(
                    '[ unify_cs ] Processing line number: {0}/{1} '.format(
                        line_nr,
                        total_lines,
                    ),
                    end = '\r'
                )
            # Example
            # if search_engine == 'ommsa_2_1_9':
            #     # can we solve this more elegantly since we know the engine
            #     # already...
            #     line_dict, variables = unify_csv_2_0_0.engines.ommsa_2_1_9\
            #         .replacement_for_postflight(
            #             line_dict,
            #             variables
            #         )

            ##########################
            # Spectrum Title block   #
            ##########################
            # reformatting Spectrum Title,
            line_dict, variables = unify_csv_2_0_0.engines._engine_independent\
                .reformat_title(
                    line_dict,
                    variables
                )

            ##########################
            #END Spectrum Title block#
            ##########################

            ##########################
            # RT insert block        #
            ##########################
            line_dict, variables = unify_csv_2_0_0.engines._engine_independent\
                .add_retention_time(
                    line_dict,
                    variables
            )
            # if line_dict['Sequence'] == 'YICDNQDTISSK' and line_dict['Spectrum ID']  =='2590':
            #     print(line_dict)
            #     exit()
            ##########################
            # END RT insert block    #
            ##########################

            #########################
            # Buffering corrections #
            #########################
            main_buffer_key = '{Sequence} || {Charge} || {Modifications} || {0}'.format(
                params['label'],
                **line_dict
            )

            # if line_dict['Sequence'] == 'YICDNQDTISSK' and line_dict['Spectrum ID']  =='2590':
            #     print(line_dict)
            #     exit()
            if main_buffer_key not in ze_only_buffer.keys():
                # THIS MUST NOT BE DEEPCOPIED, CEATE EMPTY DICT!!!! and pass both dicts to the dunction
                line_dict_update = {}

                ######################
                # Modification block #
                ######################
                # check MSFragger crazy mod merge first...
                if 'msfragger' in search_engine.lower():
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
                            msfragger_mass      = mass_format_string.format(
                                # mass rounded as defined above
                                decimal.Decimal(raw_msfragger_mass)
                            )
                            msfragger_pos       = int(msfragger_pos)
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

                if variables['fixed_mods'] is not None:
                    line_dict = unify_csv_2_0_0.engines._engine_independent\
                        .add_missing_fixed_mods(
                            line_dict,
                            variables
                        )
                 
                ##################################################################
                # Myrimatch, MSGF+, and MSFragger can not handle 15N that easily #
                # Report all AAs moded with unknown modification                 #
                # Note: masses are checked below to avoid any mismatch           #
                ##################################################################
                if variables['use15N']:
                    line_dict = unify_csv_2_0_0.engines._engine_independent\
                        .adjust_15N_for_engines_that_are_not_aware_of(
                            line_dict,
                            variables
                        )

                ##
                # Reformatting mods
                ##

                line_dict, variables, line_dict_update = unify_csv_2_0_0.engines._engine_independent\
                    .convert_mods_to_unimod_style(
                        line_dict,
                        variables,
                        line_dict_update
                    )

                #
                # ^^--------- REPLACED MODIFICATIONS! ---------------^
                #

                # Convert N-terms
                line_dict_update = unify_csv_2_0_0.engines._engine_independent\
                    .convert_n_terms(
                        line_dict_update,
                        variables
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
                    line_dict_update = unify_csv_2_0_0.engines._engine_independent\
                        .sort_mods_and_mod_differences(
                            line_dict_update,
                            variables
                        )


                # calculate m/z
                line_dict_update['Charge']     = line_dict['Charge']
                #Charge and Calc m/z is neede for mz calculation
                line_dict_update, variables = unify_csv_2_0_0.engines._engine_independent\
                    .correct_mzs(
                        line_dict_update,
                        variables,
                        line_dict
                    )

                # ------------
                # BUFFER END
                # -----------
                ze_only_buffer[ main_buffer_key ] = line_dict_update

            line_dict_update = ze_only_buffer[ main_buffer_key ]
            line_dict.update( line_dict_update )

            # protein block, only for database search engine
            if variables['database_search'] is True:
                # check for correct cleavage sites and set a new field to
                # verify correct enzyme performance
                lookup_identifier = '{0}><{1}'.format(
                    line_dict['Sequence'],
                    fasta_lookup_name
                )
                if lookup_identifier not in conflicting_uparams.keys():
                    #############################
                    # check peptide mapping     #
                    #############################
                    line_dict, variables = unify_csv_2_0_0.engines._engine_independent\
                        .check_if_peptide_was_mapped(
                            line_dict,
                            variables
                        )

                    if variables['sorted_upeptide_maps'] == []:
                        print('''
                [ WARNING ] The peptide {0} could not be mapped to the
                [ WARNING ] given database {1}
                [ WARNING ] This PSM will be skipped.
                            '''.format(
                                line_dict['Sequence'],
                                params['database'],
                            )
                        )
                        continue
                    #############################
                    # END checkpeptide mapping  #
                    #############################

                    #############################
                    # check enzyme specificity  #
                    #############################
                    line_dict, variables = unify_csv_2_0_0.engines._engine_independent\
                        .verify_cleavage_specificity(
                            line_dict,
                            variables
                        )
                    if variables['peptide_fullfills_enzyme_specificity'] is False:
                        non_enzymatic_peps.add(
                            line_dict['Sequence']
                        )
                        conflicting_uparams[lookup_identifier].add(
                            'enzyme'
                        )
                    ###############################
                    # END check enzyme specificity#
                    ###############################

                    #############################
                    # check missed cleavages    #
                    #############################
                    line_dict, variables = unify_csv_2_0_0.engines._engine_independent\
                        .count_missed_cleavages(
                            line_dict,
                            variables
                        )
                    
                    if variables['missed_cleavage_counter'] > variables['params']['translations']['max_missed_cleavages']:
                        conflicting_uparams[lookup_identifier].add(
                            'max_missed_cleavages'
                        )
                    #############################
                    #END check missed cleavages #
                    #############################

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
            csv_output.writerow(
                line_dict
            )
            '''
                to_be_written_csv_lines.append( line_dict )
            '''
    output_file_object.close()

    if variables['database_search'] is True:
        # upapa.purge_fasta_info( fasta_lookup_name )
        if len(non_enzymatic_peps) != 0:
            print('''
[ WARNING! ] The following peptides do not reflect the enzyme
[ WARNING! ] specificity:
[ WARNING! ] {0}
[ WARNING! ] These PSMs are marked 'Complies search criteria' = 'False'
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
#     if 'msfragger' in search_engine.lower():
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
