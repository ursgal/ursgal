#!/usr/bin/env python3.4
import ursgal
import os
import sys
import shutil
import csv
import re
import pickle

class ptmshepherd_0_3_5(ursgal.UNode):
    """
    ptmshepherd_0_3_5 for validation and annotation of mass sifts from
    open modeification search results
    """
    META_INFO = {
        'edit_version': 1.0,
        'name': 'PTM-Shepherd',
        'version': '1.0',
        'release_date': '2020-07-30',
        'utranslation_style': 'ptmshepherd_style_1',
        'input_extensions': ['.csv'],
        'output_extensions': ['.csv'],
        'create_own_folder': False,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'validation_engine' : True,
        },
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'ptmshepherd-0.3.5.jar',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation':
            'Geiszler DJ, Kong AT, Avtonomov DM, Yu F, Leprevost FV, Nesvizhski AI.'\
            'PTM-Shepherd: analysis and summarization of post-translational and chemical modifications from open search results.'\
            'doi: https://doi.org/10.1101/2020.07.08.192583.',
    }

    def __init__(self, *args, **kwargs):
        super(ptmshepherd_0_3_5, self).__init__(*args, **kwargs)
        self.params_to_write = {}
        pass

    def preflight(self):
        '''
        Rewrite input file in tsv format.
        Write config file based on params.
        Generate command line from params.
        '''
        self.params['translations']['csv_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        n = 0
        while os.path.exists(os.path.join(
            self.params['input_dir_path'],
            'ptmshephered_tmp_{0}'.format(n)
        )):
            n += 1
        self.tmp_dir = os.path.join(
            self.params['input_dir_path'],
            'ptmshephered_tmp_{0}'.format(n)
        )
        os.mkdir(self.tmp_dir)

        tmp_input_file = self.write_input_tsv(self.params['translations']['csv_input_file'], self.tmp_dir)

        write_exclusion_list = [
            'base_mz',
        ]
        for ptmshep_param in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][ptmshep_param].items():
                if ptmshep_param in write_exclusion_list:
                    continue
                elif ptmshep_param == 'dataset':
                    print('[ PREFLGHT ] copying mzML files into tmp folder ...')
                    for mzml in param_value:
                        shutil.copyfile(
                            mzml,
                            os.path.join(
                                self.tmp_dir,
                                os.path.basename(mzml)
                            )
                        )
                    self.params_to_write['dataset'] = '01 {0} {1}'.format(
                        tmp_input_file,
                        self.tmp_dir
                    )
                elif ursgal_param_name == 'ptmshepherd_peak_picking_params':
                    for k, v in param_value.items():
                        self.params_to_write[k] = v
                elif ptmshep_param == 'precursor_tol':
                    self.params_to_write['precursor_tol'] = \
                        self.params['translations']['precursor_mass_tolerance_plus'] +\
                        self.params['translations']['precursor_mass_tolerance_minus']
                elif ptmshep_param == 'spectra_ppmtol':
                    if self.params['translations']['frag_mass_tolerance_unit'] == 'da':
                        self.params_to_write['spectra_ppmtol'] = \
                            ursgal.ucore.convert_ppm_to_dalton(
                                self.params['translations']['frag_mass_tolerance'],
                                base_mz=self.params['translations']['base_mz']
                        )
                    elif self.params['translations']['frag_mass_tolerance_unit'] == 'ppm':
                        self.params_to_write['spectra_ppmtol'] = self.params['translations']['frag_mass_tolerance']
                    else:
                        print('please add convertion of frag mass tolerance for ptmshepherd for {0}'.format(
                            self.params['translations']['frag_mass_tolerance_unit']
                        ))
                        sys.exit(1)
                elif ptmshep_param == 'varmod_masses':
                    assert len(self.params['mods']['fix']) == 0, '''
                        [ERROR] PTM-Shepherd does not support fixed modifications.
                        [ERROR] Please change the following mods to variable mods:
                        {0}
                    '''.format(self.params['mods']['fix'])
                    mod_list = []
                    for mod_dict in self.params['mods']['opt']:
                        mod_list.append('{0}:{1}'.format(
                            mod_dict['name'],
                            mod_dict['mass']
                        ))
                    self.params_to_write['varmod_masses'] = ','.join(mod_list)
                elif ptmshep_param == 'mass_offsets':
                    self.params_to_write['mass_offsets'] = '/'.join(param_value)
                elif ptmshep_param == '-Xmx':
                    xmx = '-Xmx{0}'.format(param_value)
                else:
                    self.params_to_write[ptmshep_param] = param_value

        #create param file
        self.param_file_name = self.write_params_file(self.tmp_dir)

        #command line
        self.params['command_list'] = [
            'java',
            '-jar',
            xmx,
            self.exe,
            self.param_file_name,
        ]
        print(self.params['command_list'])

        return self.params


    def postflight(self, csv_input=None):
        '''
        Take rawlocalize and rawsimrt files for PSM annotation.
        Use global.profile for modification annotation.
        Merge result with original input file.
        Rename modsummary and global.profile to keep them as summary output files.
        '''
        # Build lookup from global.profile.tsv
        internal_precision = 100000
        global_profile = 'global.profile.tsv'
        rawloc_file = '01.rawlocalize'
        rawsimrt_file = '01.rawsimrt'
        global_mod_dict = {}
        print('[ POSTFLGH ] reading global.profil.tsv')
        with open(global_profile, 'r') as gp_in:
            gp_reader = csv.DictReader(gp_in, delimiter = '\t')
            for row in gp_reader:
                lower_mass = float(row['PeakLower']) * internal_precision
                upper_mass = float(row['PeakUpper']) * internal_precision
                peak_mass = float(row['PeakApex'])
                modifications = []
                for k, v in row.items():
                    if 'Potential Modification' in k:
                        if v == '':
                            continue
                        modifications.append(v)
                modifications = ';'.join(modifications)
                for mass in range(int(lower_mass), int(upper_mass)):
                    assert mass not in global_mod_dict.keys(), '''
                    [ERROR] Overlapping mass shift annotation peaks in PTM-Shepherd.
                    {0}
                    '''.format(mass)
                    global_mod_dict[mass] = (peak_mass, modifications)

        print('[ POSTFLGH ] reading rawlocalize')
        rawloc_dict = {}
        with open(rawloc_file, 'r') as rawloc_in:
            rawloc_reader = csv.DictReader(rawloc_in, delimiter = '\t')
            for rawloc_line_dict in rawloc_reader:
                spec_pep_key = '{0}||{1}'.format(rawloc_line_dict['Spectrum'], rawloc_line_dict['Peptide'])
                if spec_pep_key not in rawloc_dict.keys():
                    rawloc_dict[spec_pep_key] = []
                tmp_dict = {}
                for k in [
                    'Localized_Pep',
                    'MaxHyper_Unloc',
                    'MaxHyper_Loc',
                    'MaxPeaks_Unloc',
                    'MaxPeaks_Loc',
                ]:
                    tmp_dict[k] = rawloc_line_dict[k]
                rawloc_dict[spec_pep_key].append(tmp_dict)

        print('[ POSTFLGH ] reading rawsimrt')
        simrt_dict = {}
        with open(rawsimrt_file, 'r') as rawsimrt_in:
            simrt_reader = csv.DictReader(rawsimrt_in, delimiter = '\t')
            for simrt_line_dict in simrt_reader:
                spec_pep_key = '{0}||{1}'.format(simrt_line_dict['Spectrum'], simrt_line_dict['Peptide'])
                if spec_pep_key not in simrt_dict.keys():
                    simrt_dict[spec_pep_key] = []
                tmp_dict = {}
                for k in [
                    'DeltaRT',
                    'nZeroSpecs_DeltaRT',
                    'Avg_Sim',
                    'Avg_ZeroSim',
                ]:
                    tmp_dict[k] = simrt_line_dict[k]
                simrt_dict[spec_pep_key].append(tmp_dict)

        print('read original input csv and writing output ...')
        if csv_input is None:
            csv_input = self.params['translations']['csv_input_file']
        csv_output = self.params['translations']['output_file_incl_path']
        #read from original input csv file
        with open(csv_input, 'r') as csv_in, \
            open(csv_output, 'w') as csv_out:
            csv_reader = csv.DictReader(csv_in)
            fieldnames = csv_reader.fieldnames
            fieldnames.extend([
                'Mass Difference Annotations',
                'PTM-Shepherd:Localized_Pep',
                'PTM-Shepherd:MaxHyper_Unloc',
                'PTM-Shepherd:MaxHyper_Loc',
                'PTM-Shepherd:MaxPeaks_Unloc',
                'PTM-Shepherd:MaxPeaks_Loc',
                'PTM-Shepherd:DeltaRT',
                'PTM-Shepherd:nZeroSpecs_DeltaRT',
                'PTM-Shepherd:Avg_Sim',
                'PTM-Shepherd:Avg_ZeroSim',
            ])
            if sys.platform == 'win32':
                lineterminator = '\n'
            else:
                lineterminator = '\r\n'
            csv_writer = csv.DictWriter(csv_out, fieldnames=fieldnames, lineterminator=lineterminator)
            csv_writer.writeheader()
            for n, line_dict in enumerate(csv_reader):
                total_mass_shift = 0
                for single_mass_shift in line_dict['Mass Difference'].split(';'):
                    if single_mass_shift == '':
                        continue
                    total_mass_shift += float(single_mass_shift.split(':')[0])
                    # break
                transformed_mass_shift = int(total_mass_shift*internal_precision)
                peak_mass, annot_modifications = global_mod_dict.get(
                    transformed_mass_shift,
                    (line_dict['Mass Difference'], '')
                )
                line_dict['Mass Difference'] = '{0}:n'.format(peak_mass)
                line_dict['Mass Difference Annotations'] = annot_modifications
                spec_pep_key = '{0}||{1}'.format(line_dict['Spectrum Title'], line_dict['Sequence'])
                # rawloc_line_dict =  next(rawloc_reader)
                # print(rawloc_line_dict)
                assert len(rawloc_dict[spec_pep_key]) == 1, '''
                [ERROR] Spectrum Title + Peptide from original input matches to multiple
                [ERROR] entries in rawlocalization output
                {0}
                '''.format(rawloc_dict[spec_pep_key])
                # for rawloc_line_dict in rawloc_dict[spec_pep_key]:
                rawloc_line_dict = rawloc_dict[spec_pep_key][0]
                line_dict['PTM-Shepherd:Localized_Pep'] = rawloc_line_dict['Localized_Pep']
                line_dict['PTM-Shepherd:MaxHyper_Unloc'] = rawloc_line_dict['MaxHyper_Unloc']
                line_dict['PTM-Shepherd:MaxHyper_Loc'] = rawloc_line_dict['MaxHyper_Loc']
                line_dict['PTM-Shepherd:MaxPeaks_Unloc'] = rawloc_line_dict['MaxPeaks_Unloc']
                line_dict['PTM-Shepherd:MaxPeaks_Loc'] = rawloc_line_dict['MaxPeaks_Loc']
                # rawsimrt_line_dict =  next(rawsimrt_reader)
                # print(rawsimrt_line_dict)
                assert len(simrt_dict[spec_pep_key]) == 1, '''
                [ERROR] Spectrum Title + Peptide from original input matches to multiple
                [ERROR] entries in rawsimrt output
                {0}
                '''.format(simrt_dict[spec_pep_key])
                rawsimrt_line_dict = simrt_dict[spec_pep_key][0]
                line_dict['PTM-Shepherd:DeltaRT'] = rawsimrt_line_dict['DeltaRT']
                line_dict['PTM-Shepherd:nZeroSpecs_DeltaRT'] = rawsimrt_line_dict['nZeroSpecs_DeltaRT']
                line_dict['PTM-Shepherd:Avg_Sim'] = rawsimrt_line_dict['Avg_Sim']
                line_dict['PTM-Shepherd:Avg_ZeroSim'] = rawsimrt_line_dict['Avg_ZeroSim']

                csv_writer.writerow(line_dict)

        shutil.copyfile(
            'global.modsummary.tsv',
            self.params['translations']['output_file_incl_path'].replace('.csv', '_modsummary.tsv')
        )
        shutil.copyfile(
            'global.profile.tsv',
            self.params['translations']['output_file_incl_path'].replace('.csv', '_profile.tsv')
        )
        self.created_tmp_files.extend([
            'global.modsummary.tsv',
            'global.profile.tsv',
            '01.histo',
            '01.locprofile.txt',
            '01.ms2counts',
            '01.rawlocalize',
            '01.rawsimrt',
            '01.simrtprofile.txt',
            'combined.histo',
            'global.locprofile.txt',
            'global.simrtprofile.txt',
        ])
        shutil.rmtree(self.tmp_dir)
        return

    def write_input_tsv(self, input_csv, tmp_dir):
        '''
        convert ursgal csv into PTM-Shepherd input tsv
        (same format as Philosopher output psms tsv)
        '''
        print('[ PREFLGHT ] writing PTM-Shepherd config file ...')
        ptmshep_input = os.path.join(
            tmp_dir,
            os.path.basename(input_csv).replace('.csv', '.tsv')
        )
        # mod pattern
        mod_pattern = re.compile( r'''(?P<name>.*):(?P<pos>[0-9]*$)''' )
        
        #convert csv file into PTM-Shepherd input file
        fieldnames_list = [ 'Spectrum',
                            'Peptide',
                            'Modified Peptide',
                            'Peptide Length',
                            'Charge',
                            'Retention',
                            'Calculated Peptide Mass',
                            'Calculated M/Z',
                            'Delta Mass',
                            'Assigned Modifications',
                            'Is Unique',
                        ]
        umama = ursgal.UnimodMapper()
        scan_rt_lookup_path = os.path.join(
            os.path.dirname(self.params['translations']['mzml_input_files'][0]),
            '_ursgal_lookup.pkl'
        )
        # with open(scan_rt_lookup_path, 'rb') as scan_rt_in:
        #     scan_rt_lookup_dict = pickle.load(scan_rt_in)

        with open(ptmshep_input, 'w', newline='') as new_csvfile, \
            open(self.params['translations']['csv_input_file'], 'r') as csv_file:
            writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames_list, delimiter='\t')
            writer.writeheader()
            csv_reader = csv.DictReader(csv_file)
            for n, row in enumerate(csv_reader):
                if n % 500 == 0:
                    print(
                        '[ PREFLGHT ] Processing line number: {0}'.format(n),
                        end = '\r'
                    )
                mass_diffs = row['Mass Difference'].split(';')
                mass_diffs_sum = 0.0
                for n, mass in enumerate(mass_diffs):
                    if mass == '':
                        continue
                    if 'moda' in row['Search Engine'] and mass.startswith('+'):
                        exp_mass = ursgal.ucore.calculate_mass(
                            float(row['Exp m/z']),
                            int(row['Charge'])
                        )
                        mass = '{}'.format(exp_mass - float(row['uCalc Mass']))
                    mass_diffs_sum += float(mass.split(':')[0])

                if '<|>' in row['Protein ID']:
                    is_unique = 'false'
                else:
                    is_unique = 'true'

                rt = row.get('Retention Time (s)','')
                if rt == '':
                    spectrum_id = int(row['Spectrum ID'])
                    raw_file_name = os.path.basename(
                        row['Raw data location']
                    )
                    input_file_basename_for_rt_lookup = raw_file_name.replace('.mgf','')
                    retention_time_in_minutes = \
                        scan_rt_lookup_dict[input_file_basename_for_rt_lookup]['scan_2_rt']\
                            [spectrum_id]
                    row['Retention Time (s)'] = retention_time_in_minutes * 60
                assert row['Retention Time (s)'] != '', '''
                [ERROR] Retention Time needs to be given for each row.
                '''
                    
                tmp_dict = {}
                tmp_dict['Spectrum'] = row['Spectrum Title']
                tmp_dict['Peptide'] = row['Sequence']
                tmp_dict['Modified Peptide'] = row['Sequence']
                tmp_dict['Peptide Length'] = len(row['Sequence'])
                tmp_dict['Charge'] = row['Charge']
                tmp_dict['Retention'] = row['Retention Time (s)']
                tmp_dict['Calculated Peptide Mass'] = row['uCalc Mass']
                tmp_dict['Calculated M/Z'] = row['uCalc m/z']
                tmp_dict['Delta Mass'] = mass_diffs_sum
                tmp_dict['Is Unique'] = is_unique

                mods = row['Modifications'].split(';')
                new_mod_list = []
                for mod in mods:
                    if mod == '':
                        continue
                    match = mod_pattern.search(mod)
                    pos = int(match.group('pos'))
                    if pos == 0:
                        aa = row['Sequence'][pos]
                    else:
                        aa = row['Sequence'][pos-1]
                    mass = umama.name2mass(match.group('name'))
                    mod_entry = '{0}{1}({2})'.format(
                        pos,
                        aa,
                        mass
                    )
                    new_mod_list.append(mod_entry)
                tmp_dict['Assigned Modifications'] = ', '.join(new_mod_list)
                writer.writerow(tmp_dict)
        print('[ PREFLGHT ] Processing done')
        return ptmshep_input

    def write_params_file(self, param_dir):
        print('[ PREFLGHT ] writing PTM-Shepherd config file ...')
        param_file_name = os.path.join(
            param_dir,
            'ptmshepherd_config.txt'
        )
        with open(param_file_name, 'w') as io:
            print('''dataset = {dataset}
threads = {threads}
histo_bindivs = {histo_bindivs}
histo_smoothbins = {histo_smoothbins}
peakpicking_promRatio = {peakpicking_promRatio}
peakpicking_mass_units = {peakpicking_mass_units}
peakpicking_width = {peakpicking_width}
peakpicking_topN = {peakpicking_topN}
precursor_mass_units = {precursor_mass_units}
precursor_tol = {precursor_tol}
spectra_ppmtol = {spectra_ppmtol}
spectra_condPeaks = {spectra_condPeaks}
spectra_condRatio = {spectra_condRatio}
varmod_masses = {varmod_masses}
localization_background = {localization_background}
mass_offsets = {mass_offsets}
isotope_error = {isotope_error}
output_extended = true
'''.format(
                **self.params_to_write),
                file=io
            )
        return param_file_name