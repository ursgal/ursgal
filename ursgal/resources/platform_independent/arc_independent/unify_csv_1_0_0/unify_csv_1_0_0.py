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
        * The monoisotopic m/z for for each line is calculated (uCalc m/z),
          since not all engines report the monoisotopic m/z
        * Mass accuracy calculation (in ppm), also taking into account that
          not always the monoisotopic peak is picked
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
    joinchar              = params['translations']['protein_delimiter']
    do_not_delete         = False
    created_tmp_files     = []
    use15N                = False

    if 'label' in params.keys():
        if params['label'] == '15N':
            use15N = True
    else:
        params['label'] = '14N'
    # print(use15N)
    # exit()
    aa_exception_dict = params['translations']['aa_exception_dict']
    n_term_replacement = {
        'Ammonia-loss' : None,
        'Trimethyl'    : None,
        'Gly->Val'     : None,
    }
    fixed_mods = {}
    opt_mods   = {}
    modname2aa = {}
    cam        = False

    # mod pattern
    mod_pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )

    for modification in params['translations']['modifications']:
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
            params['translations']['database'],
            force  = False,
        )
    # print('Cached!')
    # input()
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
    ze_only_buffer = {}

    if params['translations']['enzyme'] != 'nonspecific':
        allowed_aa, cleavage_site, inhibitor_aa = params['translations']['enzyme'].split(';')
    else:
        allowed_aa    = ''.join( list( ursgal.ursgal_kb.NITROGENS.keys() ) )
        cleavage_site = 'C'
        inhibitor_aa  = ''
    allowed_aa += '-'

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
            'Accuracy (ppm)',
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
        import time
        for line_nr, line_dict in enumerate(csv_input):
            if line_nr % 500 == 0:
                print(
                    '[ unify_cs ] Processing line number: {0}/{1} .. '.format(
                        line_nr,
                        total_lines,
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
Could not find scan ID {0} in scan_rt_lookup[ {1} ]
                        '''.format(
                            spectrum_id,
                            input_file_basename
                        )
                    )

            retention_time_in_minutes = \
                scan_rt_lookup[ input_file_basename_for_rt_lookup ][ 'scan_2_rt' ]\
                    [ spectrum_id ]

            #we should check if data has minute format or second format...
            if scan_rt_lookup[ input_file_basename ]['unit'] == 'second':
                rt_corr_factor = 1
            else:
                rt_corr_factor = 60
            line_dict['Retention Time (s)'] = float( retention_time_in_minutes ) * rt_corr_factor

            #
            # now lets buffer for real !! :)
            #
            _ze_ultra_buffer_key_ = '{Sequence} || {Charge} || {Modifications} || '.format( **line_dict ) + params['label']
            if _ze_ultra_buffer_key_ not in ze_only_buffer.keys():
                line_dict_update = {}
                #
                # Modification block

                # some engines do not report fixed modifications
                # include in unified csv
                if fixed_mods != {}:
                    for pos, aminoacid in enumerate(line_dict['Sequence']):
                        if aminoacid in fixed_mods.keys():
                            name = fixed_mods[ aminoacid ]
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
                            'msgfplus_v9979' in search_engine.lower():
                        for p in range(1,len(line_dict['Sequence'])+1):
                                line_dict['Modifications'] = \
                                    line_dict['Modifications'].replace(
                                        'unknown modification:{0}'.format(p),
                                        '',
                                        1,
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
                    Cterm = False
                    skip_mod = False
                    if modification == '':
                        continue
                    pos, mod = None, None
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
                    if mod in modname2aa.keys():
                        correct_mod = False
                        if aa in modname2aa[mod]:
                            # everything is ok
                            correct_mod = True
                        elif Nterm or Cterm:
                            if '*' in modname2aa[mod]:
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
                                    params['translations']['modifications']
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
                        if aa in fixed_mods.keys() and use15N \
                            and 'msgfplus' in search_engine.lower():
                            if pos != 0:
                                mod = float(mod) - ursgal.ursgal_kb.DICT_15N_DIFF[aa]
                        try:
                            name_list = ursgal.GlobalUnimodMapper.appMass2name_list(
                                round(float(mod), 3), decimal_places = 3
                            )
                        except:
                            print('''
                                A modification was reported that was not included in the search parameters
                                unify_csv cannot deal with this, please check your parameters and engine output
                                reported modification: {0}
                                modifications in parameters: {1}
                                '''.format(mod, params['translations']['modifications'])
                            )
                            raise Exception('unify_csv failed because a '\
                                'modification was reported that was not '\
                                'given in params.'
                                '{0}'.format(modification)
                            )
                        mapped_mod = False
                        for name in name_list:
                            if name in modname2aa.keys():
                                if aa in modname2aa[name]:
                                    modification = '{0}:{1}'.format(name,new_pos)
                                    mapped_mod = True
                                elif Nterm and '*' in modname2aa[name]:
                                    modification = '{0}:{1}'.format(name,0)
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
                        assert mapped_mod is True, '''
                                A mass was reported that does not map on any unimod or userdefined modification
                                or the modified aminoacid is not the specified one
                                unify_csv cannot deal with this, please check your parameters and engine output
                                reported mass: {0}
                                maps on: {1}
                                reported modified aminoacid: {2}
                                modifications in parameters: {3}
                                '''.format(
                                    mod,
                                    name_list,
                                    aa,
                                    params['translations']['modifications']
                                )
                    if modification in tmp_mods or skip_mod is True:
                        continue
                    tmp_mods.append(modification)
                line_dict_update['Modifications'] = ';'.join( tmp_mods )
                #
                # ^^--------- REPLACED MODIFICATIONS! ---------------^
                #
                for unimod_name in n_term_replacement.keys():
                    if '{0}:1'.format(unimod_name) in line_dict_update['Modifications'].split(';'):
                        if unimod_name in modname2aa.keys():
                            aa = modname2aa[unimod_name]
                            if aa != ['*']:
                                if line_dict['Sequence'][0] in aa:
                                    continue
                        line_dict_update['Modifications'] = line_dict_update['Modifications'].replace(
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
                                    if cam and replace_dict['original_aa'] == 'C':
                                        unimod_name = replace_dict['unimod_name_with_cam']
                                    new_mod = '{0}:{1}'.format(
                                        unimod_name,
                                        index_of_U
                                    )
                                    if line_dict_update['Modifications'] == '':
                                        line_dict_update['Modifications'] += new_mod
                                    else:
                                        line_dict_update['Modifications'] += ';{0}'.format(
                                            new_mod
                                        )
                        line_dict['Sequence'] = line_dict['Sequence'].replace(
                            aa_to_replace,
                            replace_dict['original_aa']
                        )

                line_dict_update['Sequence'] = line_dict['Sequence']
                #
                # ^^--------- REPLACED SEQUENCE! ---------------^
                #
                # remove the double ';''
                if line_dict_update['Modifications'] != '':
                    tmp = []
                    for e in line_dict_update['Modifications'].split(';'):
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
                    line_dict_update['Modifications'] = ';'.join(
                        [
                            '{m}:{p}'.format( m=mod, p=pos) for pos, mod in tmp
                        ]
                    )

                # calculate m/z
                cc.use(
                    '{Sequence}#{Modifications}'.format(
                        **line_dict_update
                    )
                )
                if use15N:
                    number_N = dc( cc['N'] )
                    cc['15N'] = number_N
                    del cc['N']
                    if cam:
                        c_count = line_dict_update['Sequence'].count('C')
                        cc['14N'] = c_count
                        cc['15N'] -= c_count
                    # mass = mass + ( DIFFERENCE_14N_15N * number_N )
                mass = cc._mass()
                calc_mz = ursgal.ucore.calculate_mz(
                    mass,
                    line_dict['Charge']
                )
                # mz_buffer[ buffer_key ] = calc_mz

                line_dict_update['uCalc m/z'] = calc_mz
                # if 'msamanda' in search_engine.lower():
                    # ms amanda does not return calculated mz values
                if line_dict['Calc m/z'] == '':
                    line_dict_update['Calc m/z'] = calc_mz

                line_dict_update['Accuracy (ppm)'] = \
                    (float(line_dict['Exp m/z']) - line_dict_update['uCalc m/z'])/line_dict_update['uCalc m/z'] * 1e6
                prec_m_accuracy = (params['translations']['precursor_mass_tolerance_minus'] + params['translations']['precursor_mass_tolerance_plus'])/2
                i = 0
                while abs(line_dict_update['Accuracy (ppm)']) > prec_m_accuracy:
                    i += 1
                    if i > len(params['translations']['precursor_isotope_range'].split(','))-1:
                        break
                    isotope = params['translations']['precursor_isotope_range'].split(',')[i]
                    isotope = int(isotope)
                    if isotope == 0:
                        continue
                    calc_mz = ursgal.ucore.calculate_mz(
                        mass + isotope*1.008664904,
                        line_dict['Charge']
                    )
                    line_dict_update['Accuracy (ppm)'] = \
                        (float(line_dict['Exp m/z']) - calc_mz)/calc_mz * 1e6

                # ------------
                # BUFFER END
                # -----------
                ze_only_buffer[ _ze_ultra_buffer_key_ ] = line_dict_update

            line_dict_update = ze_only_buffer[ _ze_ultra_buffer_key_ ]
            line_dict.update( line_dict_update )

            # protein block, only for database search engine
            if database_search is True:
                # remap peptides to proteins, check correct enzymatic
                # cleavage and decoy assignment
                lookup_identifier = '{0}><{1}'.format(
                    line_dict['Sequence'],
                    fasta_lookup_name
                )
                if lookup_identifier not in pep_map_lookup.keys():
                    tmp_decoy = set()
                    # tmp_protein_id = {}

                    upeptide_maps = upapa.map_peptide(
                        peptide    = line_dict['Sequence'],
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
                            )
                        )
                        continue

                    sorted_upeptide_maps = [ protein_dict for protein_dict in sorted( upeptide_maps, key=lambda x: x['id'] ) ]
                    # sorted(bacterial_protein_collector[race].items(),key=lambda x: x[1]['psm_count'])
                    # print()
                    # print(line_dict['Sequence'])
                    # print(sorted_upeptide_maps)
                    protein_mapping_dict = None
                    last_protein_id = None
                    for protein in sorted_upeptide_maps:
                        # print(line_dict)
                        # print(protein)
                        add_protein   = False
                        nterm_correct = False
                        cterm_correct = False
                        if params['translations']['keep_asp_pro_broken_peps'] is True:
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

                        if params['translations']['semi_enzyme'] is True:
                            if cterm_correct is True or nterm_correct is True:
                                add_protein = True
                        elif cterm_correct is True and nterm_correct is True:
                            add_protein = True

                        if add_protein is True:
                            # print(add_protein)
                            # print(cterm_correct, nterm_correct)
                            if protein_mapping_dict is None:
                                protein_mapping_dict = {
                                    'Protein ID'       : protein['id'],
                                    'Sequence Start'   : str(protein['start']),
                                    'Sequence Stop'    : str(protein['end']),
                                    'Sequence Pre AA'  : protein['pre'],
                                    'Sequence Post AA' : protein['post'],
                                }
                            else:
                                if protein['id'] == last_protein_id:
                                    tmp_join_char = ';'
                                else:
                                    tmp_join_char = joinchar

                                    protein_mapping_dict['Protein ID' ] += '{0}{1}'.format(tmp_join_char, protein['id'])

                                protein_mapping_dict['Sequence Start'   ] += '{0}{1}'.format(tmp_join_char, str(protein['start']))
                                protein_mapping_dict['Sequence Stop'    ] += '{0}{1}'.format(tmp_join_char, str(protein['end']))
                                protein_mapping_dict['Sequence Pre AA'  ] += '{0}{1}'.format(tmp_join_char, protein['pre'])
                                protein_mapping_dict['Sequence Post AA' ] += '{0}{1}'.format(tmp_join_char, protein['post'])

                            # print(protein_mapping_dict['Protein ID' ])
                            last_protein_id = protein['id']

                            # mzidentml-lib does not always set 'Is decoy' correctly
                            # (it's always 'false' for MS-GF+ results), this is fixed here:
                            if params['translations']['decoy_tag'] in protein['id']:
                                tmp_decoy.add('true')
                            else:
                                tmp_decoy.add('false')

                    if protein_mapping_dict is None:
                        non_enzymatic_peps.add(line_dict['Sequence'])
                        continue

                    if len(protein_mapping_dict['Protein ID']) >= 2000:
                        print(
                            '{0}: {1}'.format(
                                line_dict['Sequence'],
                                protein_mapping_dict['Protein ID']
                            ),
                            file = protein_id_output
                        )
                        protein_mapping_dict['Protein ID'] = protein_mapping_dict['Protein ID'][:1990] + ' ...'
                        do_not_delete = True

                    if len(tmp_decoy) >= 2:
                        target_decoy_peps.add(line_dict['Sequence'])
                        protein_mapping_dict['Is decoy'] = 'true'
                    else:
                        protein_mapping_dict['Is decoy'] = list(tmp_decoy)[0]

                    pep_map_lookup[ lookup_identifier ] = protein_mapping_dict

                buffered_protein_mapping_dict = pep_map_lookup[lookup_identifier]
                line_dict.update( buffered_protein_mapping_dict )
                # count each PSM occurence to check whether row-merging is needed:
                psm = tuple([line_dict[x] for x in psm_defining_colnames])
                psm_counter[psm] += 1

            csv_output.writerow(line_dict)
            '''
                to_be_written_csv_lines.append( line_dict )
            '''
    output_file_object.close()

    if database_search is True:
        # upapa.purge_fasta_info( fasta_lookup_name )
        if len(non_enzymatic_peps) != 0:
            print( '''
                [ WARNING ] The following peptides could not be mapped to the
                [ WARNING ] given database {0}
                [ WARNING ] with correct enzymatic cleavage sites:
                [ WARNING ] {1}
                [ WARNING ] These PSMs were skipped.'''.format(
            params['translations']['database'],
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
            merge_duplicate_psm_rows(output_file, psm_counter, psm_defining_colnames, params['translations']['psm_merge_delimiter'])
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
    if len(sys.argv) < 7:
        print(__doc__)
        exit()

    scan_rt_lookup = pickle.load(open(sys.argv[3], 'rb'))

    params = {
        'translations' : {
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
                '*,opt,Prot-N-term,Acetyl',    # N-Acteylation[]
                'K,opt,any,Label:13C(5)15N(1)',
                'K,opt,any,Label:13C(6)15N(2)',
            ],
            'protein_delimiter'        : '<|>',
            'enzyme'                   : 'KR;C;P',
            'keep_asp_pro_broken_peps' : True,
            'semi_enzyme'              : False,
            'decoy_tag'                : 'decoy_',
            'psm_merge_delimiter'      : ';',
            'precursor_mass_tolerance_plus':5,
            'precursor_mass_tolerance_minus':5,
            'precursor_isotope_range': '0,1'
        },
        # 'label'                    : '15N',
        'label' : '',
        'prefix'                   : None
    }
    params['translations']['database'] = sys.argv[6]
    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        scan_rt_lookup = scan_rt_lookup,
        params         = params,
        search_engine  = sys.argv[4],
        score_colname  = sys.argv[5]
    )
