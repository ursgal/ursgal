#!/usr/bin/env python3.4
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
# import ursgal.ursgal_kb
import re
from collections import Counter, defaultdict
from copy import deepcopy as dc

# increase the field size limit to avoid crash if protein merge tags
# become too long does not work under windows
if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


DIFFERENCE_14N_15N = ursgal.ursgal_kb.DIFFERENCE_14N_15N


def main(input_file=None, output_file=None, scan_rt_lookup=None,
         params=None, search_engine=None, score_colname=None,
         upeptide_mapper=None):
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
        * All peptide Sequences are remapped to their corresponding protein,
          assuring correct start, stop, pre and post aminoacid. Thereby,
          also correct enzymatic cleavage is checked.
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
        * Selenocystein is not reported with the correct unimod modification

    MS-Amanda
        * Selenocystein is not reported with the correct unimod modification
        * multiple protein ID per peptide are splitted in two entries.
          (is done in MS-Amanda postflight)
        * short protein IDs are mapped to the full protein ID, it is checked
          which peptides map on which protein ID (is done in MS-Amanda
          postflight)

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
    psm_defining_colnames = get_psm_defining_colnames(score_colname)
    joinchar = params['protein_delimiter']
    do_not_delete = False
    created_tmp_files = []
    use15N = False

    if 'label' in params.keys():
        if params['label'] == '15N':
            use15N = True
    else:
        params['label'] = '14N'

    aa_exception_dict = params['aa_exception_dict']
    n_term_replacement = {
        'Ammonia-loss' : None,
        'Trimethyl'    : None,
        'Gly->Val'     : None,
    }
    fixed_mods = {}
    opt_mods = {}
    modname2aa = {}
    cam = False

    # mod pattern
    mod_pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )

    for modification in params['modifications']:
        aa = modification.split(',')[0]
        mod_type = modification.split(',')[1]
        pos = modification.split(',')[2]
        name = modification.split(',')[3]
        if name not in modname2aa.keys():
            modname2aa[name] = []
        modname2aa[name].append(aa)
        if 'N-term' in pos:
            n_term_replacement[name] = aa
        if mod_type == 'fix':
            fixed_mods[aa] = name
        if mod_type == 'opt':
            opt_mods[aa] = name
        if 'C,fix,any,Carbamidomethyl' in modification:
            cam = True

    cc = ursgal.ChemicalComposition()
    ursgal.GlobalUnimodMapper._reparseXML()
    de_novo_engines = ['novor', 'pepnovo', 'uninovo', 'unknown_engine']
    database_search_engines = [
        'msamanda',
        'msgf',
        'myrimatch',
        'omssa',
        'xtandem'
    ]
    de_novo = False
    database_search = False
    for de_novo_engine in de_novo_engines:
        if de_novo_engine in search_engine.lower():
            de_novo = True
    for db_se in database_search_engines:
        if db_se in search_engine.lower():
            database_search = True

    if upeptide_mapper is None:
        upapa = ursgal.UPeptideMapper()
    else:
        upapa = upeptide_mapper

    if database_search is True:
        target_decoy_peps = set()
        non_enzymatic_peps = set()
        pep_map_lookup = {}
        fasta_lookup_name = upapa.build_lookup_from_file(
            params['database'],
            force=False
        )

    psm_counter = Counter()
    # if a PSM with multiple rows is found (i.e. in omssa results), the psm
    # rows are merged afterwards

    output_file_object = open(output_file, 'w')
    protein_id_output = open(output_file + '_full_protein_names.txt', 'w')
    mz_buffer = {}
    csv_kwargs = {
        'extrasaction' : 'ignore'
    }
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'
    total_lines = len(list(csv.reader(open(input_file,'r'))))
    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader(
            in_file
        )
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
            'Protein ID',
            'Sequence Start',
            'Sequence Stop',
            'Sequence Pre AA',
            'Sequence Post AA',
        ]
        for new_fieldname in new_fieldnames:
            if new_fieldname not in output_fieldnames:
                output_fieldnames.insert(-5,new_fieldname)
        csv_output = csv.DictWriter(
            output_file_object,
            output_fieldnames,
            **csv_kwargs
        )
        csv_output.writeheader()
        print('''[ unify_cs ] parsing csv''')
        for line_nr, line_dict in enumerate(csv_input):
            if line_nr % 500 == 0:
                print(
                    '[ unify_cs ] Processing line number:    {0}/{1}'.format(
                        line_nr,
                        total_lines
                    ),
                    end='\r'
                )
            if line_dict['Spectrum Title'] != '':
                '''
                Valid for:
                    OMSSA
                    MSGF+
                    X!Tandem
                '''
                if 'RTINSECONDS=' in line_dict['Spectrum Title']:
                    line_2_split = line_dict['Spectrum Title'].split(' ')[0].strip()
                else:
                    line_2_split = line_dict['Spectrum Title']
                line_dict['Spectrum Title'] = line_2_split

                input_file_basename, spectrum_id, _spectrum_id, charge = line_2_split.split('.')

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
            line_dict['Spectrum ID'] = spectrum_id
            #we should check if data has minute format or second format...
            try:
                retention_time_in_minutes = \
                    scan_rt_lookup[ input_file_basename ][ 'scan_2_rt' ]\
                        [ spectrum_id ]
            except KeyError as e:
                error_msg = ''' Could not find scan ID {0} in scan_rt_lookup[ {1} ]
                '''.format( spectrum_id, input_file_basename )
                raise KeyError( error_msg ) from e
            if scan_rt_lookup[ input_file_basename ]['unit'] == 'second':
                rt_corr_factor = 1
            else:
                rt_corr_factor = 60
            line_dict['Retention Time (s)'] = float( retention_time_in_minutes ) * rt_corr_factor
            #
            # Modification block

            # some engines do not report fixed modifications
            # include in unified csv
            if fixed_mods != {}:
                for aa, name in fixed_mods.items():
                    for pos, aminoacid in enumerate(line_dict['Sequence']):
                        if aminoacid == aa:
                            tmp = '{0}:{1}'.format(
                                            name,
                                            pos + 1
                                        )
                            if tmp in line_dict['Modifications']:
                                # everything is ok :)
                                pass
                            else:
                                tmp_mods = line_dict['Modifications'].split(';')
                                tmp_mods.append(tmp)
                                line_dict['Modifications'] = ';'.join( tmp_mods )

            # Myrimatch and msgf+ can not handle 15N that easily
            # report all AAs moded with unknown modification
            # Note: masses are checked below to avoid any mismatch
            if use15N:
                if 'myrimatch' in search_engine.lower() or \
                        'msgf' in search_engine.lower():
                    line_dict['Modifications'] = re.sub(
                        'unknown modification:[0-9]*',
                        '',
                        line_dict['Modifications']
                    )
                if 'myrimatch' in search_engine.lower():
                    if 'Carboxymethyl' in line_dict['Modifications'] and cam == True:
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
            for modification in line_dict['Modifications'].split(';'):
                Nterm = False
                if modification == '':
                    continue
                pos, mod = None, None
                for match in mod_pattern.finditer( modification ):
                    pos = int( match.group('pos') )
                    mod = modification[ :match.start() ]
                    break
                assert pos is not None, '''
                        The format of the modification {0}
                        is not recognized by ursgal'''.format(
                            modification
                        )

                # old version, does not work with ':' in modification
                # mod = modification.split(':')[0]
                # pos = int(modification.split(':')[1])

                if pos == 0 or pos == 1:
                    Nterm = True
                    pos = 1
                aa = line_dict['Sequence'][pos-1]
                if mod in modname2aa.keys():
                    correct_mod = False
                    if aa in modname2aa[mod]:
                        # everything is ok
                        correct_mod = True
                    elif Nterm and '*' in modname2aa[mod]:
                        correct_mod = True
                        # still is ok
                    assert correct_mod == True,'''
                            A modification was reported for an aminoacid for which it was not defined
                            unify_csv cannot deal with this, please check your parameters and engine output
                            reported modification: {0} on {1}
                            modifications in parameters: {2}
                            '''.format(
                                mod,
                                aa,
                                params['modifications']
                            )
                elif 'unknown modification' == mod:
                    modification_known = False
                    if aa  in opt_mods.keys(): # fixed mods are corrected/added already
                        modification = '{0}:{1}'.format(opt_mods[aa],pos)
                        modification_known = True
                    assert modification_known == True,'''
                            unify csv does not work for the given unknown modification for
                            {0} {1}
                            maybe an unknown modification with terminal position was given?
                            '''.format(
                                line_dict['Sequence'], modification
                            )
                else:
                    try:
                        name_list = ursgal.GlobalUnimodMapper.appMass2name_list( round(float(mod), 4), decimal_places = 4 )
                    except:
                        print('''
                            A modification was reported that was not included in the search parameters
                            unify_csv cannot deal with this, please check your parameters and engine output
                            reported modification: {0}
                            modifications in parameters: {1}
                            '''.format(mod, params['modifications'])
                        )
                        raise Exception('unify_csv failed because a '\
                            'modification was reported that was not '\
                            'given in params.'
                        )
                    mapped_mod = False
                    for name in name_list:
                        if name in modname2aa.keys():
                            if aa in modname2aa[name]:
                                modification = '{0}:{1}'.format(name,pos)
                                mapped_mod = True
                            elif Nterm and '*' in modname2aa[name]:
                                modification = '{0}:{1}'.format(name,0)
                                mapped_mod = True
                            else:
                                continue
                    assert mapped_mod == True, '''
                            A mass was reported that does not map on any unimod or userdefined modification
                            or the modified aminoacid is no the specified one
                            unify_csv cannot deal with this, please check your parameters and engine output
                            reported mass: {0}
                            maps on: {1}
                            reported modified aminoacid: {2}
                            modifications in parameters: {3}
                            '''.format(
                                mod,
                                name_list,
                                aa,
                                params['modifications']
                            )
                tmp_mods.append(modification)
            line_dict['Modifications'] = ';'.join( tmp_mods )

            for unimod_name in n_term_replacement.keys():
                if '{0}:1'.format(unimod_name) in line_dict['Modifications']:
                    replace = False
                    if unimod_name in modname2aa.keys():
                        aa = modname2aa[unimod_name]
                        if aa != '*':
                            if line_dict['Sequence'][0] == aa:
                                continue
                    line_dict['Modifications'] = line_dict['Modifications'].replace(
                        '{0}:1'.format( unimod_name ),
                        '{0}:0'.format( unimod_name )
                        )

            for aa_to_replace, replace_dict in aa_exception_dict.items():
                if aa_to_replace in line_dict['Sequence']:
                    #change mods only if unimod has to be changed...
                    if 'unimod_name' in replace_dict.keys():
                        for r_pos, aa in enumerate(line_dict['Sequence']):
                            if aa == aa_to_replace:
                                index_of_U = r_pos + 1
                                unimod_name = replace_dict['unimod_name']
                                if cam:
                                    unimod_name = replace_dict['unimod_name_with_cam']
                                new_mod = '{0}:{1}'.format(
                                    unimod_name,
                                    index_of_U
                                )
                                if line_dict['Modifications'] == '':
                                    line_dict['Modifications'] += new_mod
                                else:
                                    line_dict['Modifications'] += ';{0}'.format(
                                        new_mod
                                    )
                    line_dict['Sequence'] = line_dict['Sequence'].replace(
                        aa_to_replace,
                        replace_dict['original_aa']
                    )
            # remove the double ';''
            if line_dict['Modifications'] != '':
                tmp = []
                for e in line_dict['Modifications'].split(';'):
                    if e == '':
                        # that remove the doubles ....
                        continue
                    else:
                        # other way to do it...
                        # pos_of_split_point = re.search( ':\d*\Z', e )
                        # pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )
                        for occ, match in enumerate( mod_pattern.finditer( e )):
                            mod = e[:match.start()]
                            mod_pos = e[match.start()+1:]
                            # mod, pos = e.split(':')
                            m = (int(mod_pos), mod)
                            if m not in tmp:
                                tmp.append( m )
                tmp.sort()
                line_dict['Modifications'] = ';'.join(
                    [
                        '{m}:{p}'.format( m=mod, p=pos) for pos, mod in tmp
                    ]
                )

            # caculate m/z

            upep = line_dict['Sequence'] + '#' + line_dict['Modifications']
            buffer_key = (upep, line_dict['Charge'], params['label'])
            if buffer_key not in mz_buffer.keys():
                cc.use(upep)
                if use15N:
                    number_N = dc( cc['N'] )
                    cc['15N'] = number_N
                    del cc['N']
                    if cam:
                        c_count = line_dict['Sequence'].count('C')
                        cc['14N'] = c_count
                        cc['15N'] -= c_count
                    # mass = mass + ( DIFFERENCE_14N_15N * number_N )
                mass = cc._mass()
                calc_mz = ursgal.ucore.calculate_mz(
                    mass,
                    line_dict['Charge']
                )
                mz_buffer[ buffer_key ] = calc_mz
            else:
                calc_mz = mz_buffer[ buffer_key ]
            line_dict['uCalc m/z'] = calc_mz
            if 'msamanda' in search_engine.lower():
                # ms amanda does not return calculated mz values
                line_dict['Calc m/z'] = calc_mz

            # protein block, only for database search engine

            if database_search is True:


                # remap peptides to proteins, check correct enzymatic
                # cleavage and decoy assignment
                lookup_identifier = '{0}><{1}'.format(line_dict['Sequence'], fasta_lookup_name)
                if lookup_identifier not in pep_map_lookup.keys():
                    tmp_decoy = set()
                    tmp_protein_id = {}

                    upeptide_maps = upapa.map_peptide(
                        peptide = line_dict['Sequence'],
                        fasta_name = fasta_lookup_name
                    )
                    '''
                    <><><><><><><><><><><><><>
                    '''
                    # assert upeptide_maps != [],'''
                    #         The peptide {0} could not be mapped to the
                    #         given database {1}

                    #         {2}

                    #         '''.format(
                    #             line_dict['Sequence'],
                    #             fasta_lookup_name,
                    #             ''
                    #         )
                    if upeptide_maps == []:
                        print('''
                            [ WARNING ] The peptide {0} could not be mapped to the
                            [ WARNING ] given database {1}
                            [ WARNING ] {2}
                            [ WARNING ] This PSM will be skipped.
                            '''.format(
                                line_dict['Sequence'],
                                fasta_lookup_name,
                                ''
                            ))
                    for protein in upeptide_maps:
                        allowed_aa = params['enzyme'].split(';')[0] + '-'
                        cleavage_site = params['enzyme'].split(';')[1]
                        inhibitor_aa = params['enzyme'].split(';')[2]
                        add_protein = False
                        nterm_correct = False
                        cterm_correct = False
                        if params['keep_asp_pro_broken_peps'] == True:
                            if line_dict['Sequence'][-1] == 'D' and\
                                protein['post'] == 'P':
                                cterm_correct = True
                            if line_dict['Sequence'][0] == 'P' and\
                                protein['pre'] == 'D':
                                nterm_correct = True
                        if cleavage_site == 'C':
                            if protein['pre'] in allowed_aa\
                                    or protein['start'] in [1, 2, 3]:
                                if line_dict['Sequence'][0] not in inhibitor_aa\
                                        or protein['start'] in [1, 2, 3]:
                                    nterm_correct = True
                            if protein['post'] not in inhibitor_aa:
                                if line_dict['Sequence'][-1] in allowed_aa\
                                    or protein['post'] == '-':
                                    cterm_correct = True
                        elif cleavage_site == 'N':
                            if protein['post'] in allowed_aa:
                                if line_dict['Sequence'][-1] not in inhibitor_aa\
                                    or protein['post'] == '-':
                                    cterm_correct = True
                            if protein['pre'] not in inhibitor_aa\
                                or protein['start'] in [1, 2, 3]:
                                if line_dict['Sequence'][0] in allowed_aa\
                                    or protein['start'] in [1, 2, 3]:
                                    nterm_correct = True
                        if params['semi_enzyme'] == True:
                            if cterm_correct == True or nterm_correct == True:
                                add_protein = True
                        elif cterm_correct == True and nterm_correct == True:
                            add_protein = True
                        if add_protein == True:
                            if protein['id'] not in tmp_protein_id.keys():
                                tmp_protein_id[protein['id']] = {
                                    'start' : [],
                                    'stop' : [],
                                    'pre' : [],
                                    'post' : [],
                                }
                            tmp_protein_id[protein['id']]['start'].append(str(protein['start']))
                            tmp_protein_id[protein['id']]['stop'].append(str(protein['end']))
                            tmp_protein_id[protein['id']]['pre'].append(protein['pre'])
                            tmp_protein_id[protein['id']]['post'].append(protein['post'])

                            # mzidentml-lib does not always set 'Is decoy' correctly
                            # (it's always 'false' for MS-GF+ results), this is fixed here:
                            if params['decoy_tag'] in protein['id']:
                                tmp_decoy.add('true')
                            else:
                                tmp_decoy.add('false')
                    pep_map_lookup[lookup_identifier] = (tmp_protein_id, tmp_decoy)
                else:
                    tmp_protein_id, tmp_decoy = pep_map_lookup[lookup_identifier]
                protein_id = []
                start = []
                stop = []
                pre = []
                post = []
                for prot_id in sorted(tmp_protein_id.keys()):
                    protein_id.append(prot_id)
                    start.append(';'.join(tmp_protein_id[prot_id]['start']))
                    stop.append(';'.join(tmp_protein_id[prot_id]['stop']))
                    pre.append(';'.join(tmp_protein_id[prot_id]['pre']))
                    post.append(';'.join(tmp_protein_id[prot_id]['post']))
                protein_id = joinchar.join(protein_id)
                if len(protein_id) >= 2000:
                    print('{0}: {1}'.format(line_dict['Sequence'], protein_id), file = protein_id_output)
                    protein_id = protein_id[:1990] + ' ...'
                    do_not_delete = True
                line_dict['Protein ID'] = protein_id
                line_dict['Sequence Start'] = joinchar.join(start)
                line_dict['Sequence Stop'] = joinchar.join(stop)
                line_dict['Sequence Pre AA'] = joinchar.join(pre)
                line_dict['Sequence Post AA'] = joinchar.join(post)

                if len(tmp_decoy) == 0:
                    non_enzymatic_peps.add(line_dict['Sequence'])
                    continue
                if len(tmp_decoy) >= 2:
                    target_decoy_peps.add(line_dict['Sequence'])
                    line_dict['Is decoy'] = 'true'
                else:
                    line_dict['Is decoy'] = list(tmp_decoy)[0]

                # count each PSM occurence to check whether row-merging is needed:
                psm = tuple([line_dict[x] for x in psm_defining_colnames])
                psm_counter[psm] += 1

            csv_output.writerow(line_dict)
            '''
                to_be_written_csv_lines.append( line_dict )
            '''
    output_file_object.close()

    if database_search == True:
        # upapa.purge_fasta_info( fasta_lookup_name )
        if len(non_enzymatic_peps) != 0:
            print( '''
                [ WARNING ] The following peptides could not be mapped to the
                [ WARNING ] given database {0}
                [ WARNING ] with correct enzymatic cleavage sites:
                [ WARNING ] {1}
                [ WARNING ] These PSMs were skipped.'''.format(
            params['database'],
            non_enzymatic_peps
            ))
        if len(target_decoy_peps) != 0:
            print(
                '''
                [ WARNING ] The following peptides occured in a target as well as decoy protein
                [ WARNING ] {0}
                [ WARNING ] 'Is decoy' has been set to 'True' '''.format(
                    target_decoy_peps,
                )
            )

    # if there are multiple rows for a PSM, we have to merge them aka rewrite the csv...
    if psm_counter != Counter():
        if max(psm_counter.values()) > 1:
            merge_duplicate_psm_rows(output_file, psm_counter, psm_defining_colnames, params['psm_merge_delimiter'])
            '''
            to_be_written_csv_lines = merge_duplicate_psm_rows(
                to_be_written_csv_lines,
                psm_counter
            )
            '''
        '''
        do output_file magic with to_be_written_csv_lines
        '''
    if do_not_delete == False:
        created_tmp_files.append( output_file+'_full_protein_names.txt' )
    return created_tmp_files


def get_psm_defining_colnames(score_colname):
    '''
    Returns the all PSM-defining column names (i.e spectrum & peptide,
    but also score field because sometimes the same PSMs are reported
    with different scores...
    '''
    psm = [
        'Spectrum Title',
        'Sequence',
        'Modifications',
        'Charge',
        'Is decoy',
    ]
    if score_colname:
        psm.append(score_colname)
    return psm


def merge_rowdicts(list_of_rowdicts, joinchar, alt_joinchar='<|>'):
    '''
    Merges CSV rows. If the column values are conflicting, they
    are joined with a character (joinchar).
    Special case: proteinaccessions are not joined with the joinchar,
    but rather with alt_joinchar.
    '''
    merged_d = {}
    fieldnames = list_of_rowdicts[0].keys()
    for fieldname in fieldnames:

        joinchar_used = joinchar
        # if fieldname == 'proteinacc_start_stop_pre_post_;':
        #     joinchar_used = alt_joinchar

        values = {d[fieldname] for d in list_of_rowdicts}
        if len(values) == 1:
            merged_d[fieldname] = list(values)[0]
        else:
            merged_d[fieldname] = joinchar_used.join(sorted(values))
    return merged_d


def merge_duplicate_psm_rows(unified_csv_path, psm_counter, psm_defining_colnames, joinchar):
    '''
    Rows describing the same PSM (i.e. when two proteins share the
    same peptide) are merged to one row.
    '''
    rows_to_merge_dict = defaultdict(list)

    tmp_file = unified_csv_path + ".tmp"
    os.rename(unified_csv_path, tmp_file)
    print('Merging rows of the same PSM...')
    with open(tmp_file, 'r') as tmp, open(unified_csv_path, 'w', newline='') as out:
        tmp_reader = csv.DictReader(tmp)
        writer = csv.DictWriter(out, fieldnames=tmp_reader.fieldnames)
        writer.writeheader()
        for row in tmp_reader:
            psm = tuple([row[x] for x in psm_defining_colnames])
            # each unique combination of these should only have ONE row!
            # i.e. combination of seq+spec+score
            if psm_counter[psm] == 1:
                # no duplicate = no problem, we can just write the row again
                writer.writerow(row)
            elif psm_counter[psm] > 1:
                # we have to collect all rows of this psm, and merge + write them later!
                rows_to_merge_dict[psm].append(row)
            else:
                raise Exception("This should never happen.")
        # finished parsing the old unmerged unified csv
        for rows_to_merge in rows_to_merge_dict.values():
            writer.writerow(
                merge_rowdicts(rows_to_merge, joinchar=joinchar)
            )
    os.remove(tmp_file)  # remove the old unified csv that contains duplicate rows



if __name__ == '__main__':
    if len(sys.argv) < 6:
        print(__doc__)
        exit()

    scan_rt_lookup = pickle.load(open(sys.argv[3], 'rb'))

    params = {
        'aa_exception_dict' : {
            'U' : {
                'unimod_name' : 'Delta:S(-1)Se(1)',
                'original_aa' : 'C',
                'unimod_name_with_cam': 'SecCarbamidomethyl',
            },
        },
        'modifications' : [
            'M,opt,any,Oxidation',        # Met oxidation
            'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
            '*,opt,Prot-N-term,Acetyl'    # N-Acteylation[]
        ],
        'label' : '',
    }
    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        scan_rt_lookup = scan_rt_lookup,
        params         = params,
        search_engine  = sys.argv[4],
        score_colname  = sys.argv[5]
    )
