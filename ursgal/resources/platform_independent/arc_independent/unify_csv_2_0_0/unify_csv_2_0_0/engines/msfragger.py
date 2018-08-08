import decimal
import ursgal.ucore


def translate_headers(line_dict, variables):

    return line_dict, variables


def convert_mass_to_mz_values(line_dict, variables):
    '''
    'Precursor neutral mass (Da)' : '',
    'Neutral mass of peptide' : 'Calc m/z',

    Masses include  any variable modifications (Da)
    '''

    exp_mz = ursgal.ucore.calculate_mz(
        line_dict['MSFragger:Precursor neutral mass (Da)'],
        line_dict['Charge']
    )
    calc_mz = ursgal.ucore.calculate_mz(
        line_dict['MSFragger:Neutral mass of peptide'],
        line_dict['Charge']
    )

    line_dict['Exp m/z'] = exp_mz
    line_dict['Calc m/z'] = calc_mz

    return line_dict, variables


def reformat_modifications(line_dict, variables):
    '''
    We have to reformat the modifications
    M|14$15.994915|17$57.021465 to 15.994915:14;57.021465:17
    reformat it in X!tandem/Ursgal format
    '''
    ms_fragger_reformatted_mods = []
    # M stand for Modifications here, not Methionine
    if line_dict['Modifications'] == 'M':
        line_dict['Modifications'] = ''
    else:
        mod_list = line_dict['Modifications']
        for single_mod in mod_list.split('|'):
            if single_mod in ['M','']:
                continue
            msfragger_pos, raw_msfragger_mass = single_mod.split('$')
            msfragger_mass      = variables['mass_format_string'].format(
                # mass rounded as defined above
                decimal.Decimal(raw_msfragger_mass)
            )
            msfragger_pos       = int(msfragger_pos)
            if msfragger_mass in variables['mass_to_mod_combo'].keys():
                explainable_combos = []
                for combo in variables['mass_to_mod_combo'][msfragger_mass]:
                    combo_explainable = set([True])
                    tmp_mods = []
                    for new_name in combo:
                        meta_mod_info = variables['mod_dict'][new_name]
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
                                pos_to_check.add(
                                    int(len(line_dict['Sequence'])) - 1
                                )
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
        line_dict['Modifications'] = ';'.join( ms_fragger_reformatted_mods )
    return line_dict, variables
