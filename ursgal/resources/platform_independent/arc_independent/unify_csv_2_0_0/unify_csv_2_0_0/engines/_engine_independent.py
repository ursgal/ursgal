import ursgal

def reformat_title(line_dict, variables):

    # we will set the following

    variables['input_file_basename'] = None
    spectrum_id = None
    variables['_spectrum_id'] = None
    variables['charge'] = None
    variables['pure_input_file_name'] = None

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

        variables['input_file_basename'], spectrum_id, _spectrum_id, _charge = line_2_split.split('.')
        variables['pure_input_file_name'] = ''

    elif 'scan=' in line_dict['Spectrum ID']:
        variables['pure_input_file_name'] = os.path.basename(
            line_dict['Raw data location']
        )
        variables['input_file_basename'] = variables['pure_input_file_name'].split(".")[0]
        # not using os.path.splitext because we could have multiple file
        # extensions (i.e. ".mzml.gz")

        '''
        Valid for:
            myrimatch
        '''
        spectrum_id = line_dict['Spectrum ID'].split('=')[-1]
        line_dict['Spectrum Title'] = '{0}.{1}.{1}.{2}'.format(
            variables['input_file_basename'],
            spectrum_id,
            line_dict['Charge']
        )

    elif line_dict['Spectrum Title'] == '':
        '''
        Valid for:
            Novor
            MSFragger
        '''
        variables['pure_input_file_name'] = os.path.basename(
            line_dict['Raw data location']
        )
        variables['input_file_basename'] = variables['pure_input_file_name'].split(".")[0]
        spectrum_id = line_dict['Spectrum ID']
        line_dict['Spectrum Title'] = '{0}.{1}.{1}.{2}'.format(
            variables['input_file_basename'],
            spectrum_id,
            line_dict['Charge']
        )
    else:
        raise Exception( 'New csv format present for engine {0}'.format( engine ) )

    #update spectrum ID from block above
    line_dict['Spectrum ID'] = spectrum_id
    return line_dict, variables

def add_missing_fixed_mods(line_dict, variables):
    for pos, aminoacid in enumerate(line_dict['Sequence']):
        if aminoacid in variables['fixed_mods'].keys():
            name = variables['fixed_mods'][aminoacid]
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
                line_dict['Modifications'] = ';'.join(tmp_mods)
    return line_dict

def adjust_15N_for_engines_that_are_not_aware_of(line_dict, variables):
    if 'myrimatch' in variables['search_engine'].lower() or \
            'msgfplus_v9979' in variables['search_engine'].lower():
        for p in range(1,len(line_dict['Sequence'])+1):
                line_dict['Modifications'] = \
                    line_dict['Modifications'].replace(
                        'unknown modification:{0}'.format(p),
                        '',
                        1,
                    )
    if 'myrimatch' in variables['search_engine'].lower():
        if 'Carboxymethyl' in line_dict['Modifications'] and \
                variables['cam'] is True:
            line_dict['Modifications'] = line_dict['Modifications'].replace(
                'Carboxymethyl',
                'Carbamidomethyl'
            )
        elif 'Delta:H(6)C(3)O(1)' in line_dict['Modifications']:
            line_dict['Modifications'] = line_dict['Modifications'].replace(
                'Delta:H(6)C(3)O(1)',
                'Carbamidomethyl'
            )
    return line_dict

def convert_mods_to_unimod_style(line_dict, variables):
    tmp_mods = []
    tmp_mass_diff = []
    for modification in line_dict['Modifications'].split(';'):
        Nterm = False
        Cterm = False
        skip_mod = False
        if modification == '':
            continue
        pos, mod = None, None
        # print(modification)
        match = variables['mod_pattern'].search( modification )
        pos = int(match.group('pos'))
        mod = modification[:match.start()]
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
        aa = line_dict['Sequence'][new_pos - 1].upper()
        # if aa in fixed_mods.keys():
        #     fixed_mods[ aminoacid ]
        #     # fixed mods are corrected/added already
        #     continue
        if mod in variables['mod_dict'].keys():
            correct_mod = False
            if aa in variables['mod_dict'][mod]['aa']:
                # everything is ok
                correct_mod = True
            elif Nterm is True or Cterm is True:
                if '*' in variables['mod_dict'][mod]['aa']:
                    correct_mod = True
                    # still is ok
            assert correct_mod is True,'''
                A modification was reported for an amino acid for which it was not defined
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
            if aa in variables['opt_mods'].keys():
                # fixed mods are corrected/added already
                modification = '{0}:{1}'.format(variables['opt_mods'][aa], new_pos)
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
            if variables['use15N']:
                substract_15N_diff = False
                if aa in fixed_mods.keys() and 'msgfplus' in variables['search_engine'].lower() and pos != 0:
                    substract_15N_diff = True
                if 'msfragger' in variables['search_engine'].lower() and float_mod > 4:
                    # maximum 15N labeling is 3.988 Da (R)
                    substract_15N_diff = True
                if substract_15N_diff:
                    masses_2_test.append(float_mod - ursgal.ukb.DICT_15N_DIFF[aa])
            # try:
            # works always but returns empty list...
            name_list = []
            for mass_2_test in masses_2_test:
                mass_buffer_key = variables['mass_format_string'].format(mass_2_test)
                #buffer increases speed massively...
                if mass_buffer_key not in  variables['app_mass_to_name_list_buffer'] .keys():
                    variables['app_mass_to_name_list_buffer'] [mass_buffer_key] = ursgal.GlobalUnimodMapper.appMass2name_list(
                        float(mass_buffer_key),
                        decimal_places = no_decimals
                    )
                name_list += variables['app_mass_to_name_list_buffer'][mass_buffer_key]
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
                if name in variables['mod_dict'].keys():
                    if aa in variables['mod_dict'][name]['aa']:
                        modification = '{0}:{1}'.format(name, new_pos)
                        mapped_mod = True
                    elif Nterm is True and '*' in variables['mod_dict'][name]['aa']:
                        modification = '{0}:{1}'.format(name,0)
                        mapped_mod = True
                    else:
                        continue
                elif variables['use15N'] is True and name in [
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
        if skip_mod is True:
            continue
        if modification in tmp_mods:
            if mod in variables['n_term_replacement'].keys() and pos == 1:
                if line_dict['Sequence'][0] in variables['mod_dict'][mod]['aa']:
                    modification.replace(
                        '{0}:1'.format(mod),
                        '{0}:0'.format(mod)
                    )
                else:
                    continue
            else:
                continue
        tmp_mods.append(modification)

    line_dict['Modifications'] = ';'.join(tmp_mods)
    line_dict['Mass Difference'] = ';'.join(tmp_mass_diff)
    return line_dict

def sort_mods_and_mod_differences(line_dict, variables):
    # let's split although we had the positions above ...
    tmp = []
    positions = set()
    for e in line_dict['Modifications'].split(';'):
        if e == '':
            # that remove the doubles ....
            continue
        else:
            # other way to do it...
            # pos_of_split_point = re.search( ':\d*\Z', e )
            # pattern = re.compile( r''':(?P<pos>[0-9]*$)''' )
            for occ, match in enumerate(variables['mod_pattern'].finditer(e)):
                mod = e[:match.start()]
                mod_pos = e[match.start()+1:]
                # mod, pos = e.split(':')
                m = (int(mod_pos), mod)
                if m not in tmp:
                    tmp.append(m)
                    positions.add(int(mod_pos))
    tmp.sort()
    line_dict['Modifications'] = ';'.join(
        [
            '{m}:{p}'.format( m=mod, p=pos) for pos, mod in tmp
        ]
    )
    if len(tmp) != len(positions):
        print(
            '[ WARNING ] {Sequence}#{Modifications} will be skipped, because it contains two mods at the same position!'.format(
                **line_dict
            )
        )

    return line_dict

def correct_mzs(line_dict, variables, params):
    # calculate m/z
    variables['cc'].use(
        '{Sequence}#{Modifications}'.format(
            **line_dict
        )
    )
    if variables['use15N']:
        number_N = dc( variables['cc']['N'] )
        variables['cc']['15N'] = number_N
        del variables['cc']['N']
        if cam:
            c_count = line_dict['Sequence'].count('C')
            variables['cc']['14N'] = c_count
            variables['cc']['15N'] -= c_count
        # mass = mass + ( DIFFERENCE_14N_15N * number_N )
    mass = variables['cc']._mass()
    calc_mz = ursgal.ucore.calculate_mz(
        mass,
        line_dict['Charge']
    )
    # mz_buffer[ buffer_key ] = calc_mz

    line_dict['uCalc m/z'] = calc_mz

    # if 'msamanda' in search_engine.lower():
        # ms amanda does not return calculated mz values
    if line_dict['Calc m/z'] == '':
        line_dict['Calc m/z'] = calc_mz

    line_dict['Accuracy (ppm)'] = \
        (float(line_dict['Exp m/z']) - line_dict['uCalc m/z'])/line_dict['uCalc m/z'] * 1e6
    prec_m_accuracy = (params['translations']['precursor_mass_tolerance_minus'] + params['translations']['precursor_mass_tolerance_plus'])/2
    i = 0
    while abs(line_dict['Accuracy (ppm)']) > prec_m_accuracy:
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
        line_dict['Accuracy (ppm)'] = \
            (float(line_dict['Exp m/z']) - calc_mz)/calc_mz * 1e6

    return line_dict
