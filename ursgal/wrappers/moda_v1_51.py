#!/usr/bin/env python
import ursgal
import os
import subprocess
import csv
import re
import sys


class moda_v1_51(ursgal.UNode):
    """
    MODa UNode
    Check http://prix.hanyang.ac.kr/download/moda.jsp for download, new versions and contact information

    Reference:
    Na S, Bandeira N, Paek E. (2012) Fast multi-blind modification search through tandem mass spectrometry.
    """
    META_INFO = {
        'edit_version': 1.00,
        'name': 'MODa',
        'version': 'v1.51',
        'release_date': '2012-4-1',
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'input_extensions': ['.mgf', '.pkl', '.dta', '.mzXML'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'utranslation_style': 'moda_style_1',
        'engine': {
            'platform_independent': {
                'arc_independent': {
                    'exe': 'moda_v1.51.jar',
                    'url': '',
                    'zip_md5': '',
                    'additional_exe': [],
                },
            },
        },
        'citation':
        'Na S, Bandeira N, Paek E. (2012) Fast multi-blind modification '
            'search through tandem mass spectrometry.',
    }

    def __init__(self, *args, **kwargs):
        super(moda_v1_51, self).__init__(*args, **kwargs)
        pass

    def preflight(self):
        '''
        Formatting the command line via self.params

        Returns:
                dict: self.params
        '''

        translations = self.params['translations'][
            '_grouped_by_translated_key']

        self.params['translations']['params_input_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '_params.txt'
        )
        self.created_tmp_files.append(
            self.params['translations']['params_input_file'])

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        self.created_tmp_files.append(
            self.params['translations'][
                'output_file_incl_path'].replace('.csv', '.tsv')
        )
        translations['-o']['output_file_incl_path'] = \
            self.params['translations']['output_file_incl_path']

        self.params['command_list'] = [
            'java',
            '-jar',
            self.exe,
            '-i', self.params['translations']['params_input_file'],
            '-o', self.params['translations'][
                'output_file_incl_path'].replace('.csv', '.tsv'),
        ]

        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        translations['Spectra']['mgf_input_file'] = \
            self.params['translations']['mgf_input_file']

        params_input_file = open(
            self.params['translations']['params_input_file'],
            'w',
            encoding='UTF-8'
        )

        fixed_mods = []
        if self.params['translations']['label'] == '15N':
            for aminoacid, N15_Diff in ursgal.ukb.DICT_15N_DIFF.items():
                existing = False
                for mod in self.params['mods']['fix']:
                    if aminoacid == mod['aa']:
                        mod['mass'] += N15_Diff
                        mod['name'] += '_15N_{0}'.format(aminoacid)
                        existing = True
                if existing == True:
                    continue
                else:
                    fixed_mods.append('{0}, {1}'.format(aminoacid, N15_Diff))

        for mod in self.params['mods']['fix']:
            fixed_mods.append('{0}, {1}'.format(mod['aa'], mod['mass']))

        print(
            '''
            [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
            [ WARNING ] need to be combined for MODa (use of symmetric tolerance window).
            [ WARNING ] The arithmetic mean is used.
            '''
        )
        if translations['PPMTolerance']['precursor_mass_tolerance_unit'] == 'da':
            translations['PeptTolerance'] = \
                (translations['PPMTolerance']['precursor_mass_tolerance_minus'] +
                 translations['PPMTolerance']['precursor_mass_tolerance_plus']) / 2
            del translations['PPMTolerance']

        elif translations['PPMTolerance']['precursor_mass_tolerance_unit'] == 'mmu':
            translations['PeptTolerance'] = \
                10e-3 *\
                (translations['PPMTolerance']['precursor_mass_tolerance_minus'] +
                 translations['PPMTolerance']['precursor_mass_tolerance_plus']) / 2
            del translations['PPMTolerance']

        else:
            translations['PPMTolerance'] = \
                (translations['PPMTolerance']['precursor_mass_tolerance_minus'] +
                 translations['PPMTolerance']['precursor_mass_tolerance_plus']) / 2

        if translations['FragTolerance']['frag_mass_tolerance_unit'] == 'ppm':
            translations['FragTolerance'] = \
                ursgal.ucore.convert_ppm_to_dalton(
                    translations['FragTolerance']['frag_mass_tolerance'],
                    base_mz=self.params['translations']['base_mz']
            )
        elif translations['FragTolerance']['frag_mass_tolerance_unit'] == 'mmu':
            translations['FragTolerance'] = \
                translations['FragTolerance']['frag_mass_tolerance'] * 10e-3
        else:
            translations['FragTolerance'] = \
                translations['FragTolerance']['frag_mass_tolerance']

        for translated_key, translation_dict in translations.items():
            if translated_key == '-Xmx':
                self.params['command_list'].insert(1, '{0}{1}'.format(
                    translated_key,
                    list(translation_dict.values())[0]
                ))
            elif translated_key in ['-o', '-i', 'base_mz', 'label', ]:
                continue
            elif translated_key == 'ADD':
                for aa_mod in fixed_mods:
                    print('{0}={1}'.format(
                        translated_key,
                        aa_mod,
                    ),
                        file=params_input_file
                    )
            elif translated_key in ['FragTolerance', 'PPMTolerance', 'PeptTolerance']:
                print('{0}={1}'.format(
                    translated_key,
                    translations[translated_key],
                ),
                    file=params_input_file
                )
            elif len(translation_dict) == 1:
                print('{0}={1}'.format(
                    translated_key,
                    str(list(translation_dict.values())[0]),
                ),
                    file=params_input_file
                )
            else:
                print('The translatd key ', translated_key,
                      ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                sys.exit(1)

        params_input_file.close()

        return self.params

    def postflight(self):
        '''
        Rewrite ModA output .tsv into .csv so that it can be unified
        '''
        output_headers = [
            'Spectrum Title',
            'Retention Time (s)',
            'Spectrum ID',
            'Sequence',
            'Modifications',
            'Protein ID',
            'Exp m/z',
            'Calc m/z',
            'Error (exp-calc)',
            'ModA:Score',
            'ModA:probability',
            'Spectrum ID',
            'Charge',
            'Rank',
            'Raw data location',
        ]
        org_moda_out = self.params['translations'][
            'output_file_incl_path'].replace('.csv', '.tsv')
        out_line_dicts = []
        with open(org_moda_out, 'r') as org_out:
            out_reader = csv.reader(org_out, delimiter='\t')
            for row in out_reader:
                if len(row) <= 1:
                    continue
                elif '>>' in row[0]:
                    out_dict = {}
                    rank = 0
                    out_dict['Raw data location'] = row[0].strip('>>')
                    out_dict['Exp m/z'] = row[2]
                    out_dict['Charge'] = row[3]
                    out_dict['Spectrum ID'] = row[4]
                else:
                    rank += 1
                    out_dict['Calc m/z'] = row[0]
                    out_dict['Error (exp-calc)'] = row[1]
                    out_dict['ModA:Score'] = row[2]
                    out_dict['ModA:probability'] = row[3]
                    org_sequence = row[4].split('.')[1]
                    out_dict['Protein ID'] = row[5]
                    out_dict['Rank'] = rank

                    tmp_sequence = ''
                    tmp_mods = []
                    regex_pattern = '([+-]{1}[0-9]+)'
                    peptide_unimod = ursgal.ucore.reformat_peptide(
                        regex_pattern,
                        None,
                        org_sequence
                    )
                    if '#' in peptide_unimod:
                        sequence, mods = peptide_unimod.split('#')
                    else:
                        sequence = peptide_unimod
                        mods = ''
                    out_dict['Sequence'] = sequence
                    out_dict['Modifications'] = mods
                    out_line_dicts.append(out_dict.copy())

                    # prev_match = 0
                    # for match in mod_pattern.finditer(org_sequence):
                    #     mod = match.group('mod')
                    #     pos = int(match.start())
                    #     tmp_mods.append('{0}:{1}'.format(mod, pos))
                    #     tmp_sequence += org_sequence[prev_match:pos]
                    #     prev_match = pos + len(mod)
                    # sequence = tmp_sequence + \
                    #     org_sequence[prev_match:len(org_sequence)]

                    # mods = ';'.join(tmp_mods)
                    # if tmp_mods == []:
                    #     sequence = org_sequence

        output_file = self.params['translations']['output_file_incl_path']
        with open(output_file, 'w') as out_file:
            csv_writer = csv.DictWriter(out_file, fieldnames=output_headers)
            csv_writer.writeheader()
            for line_dict in out_line_dicts:
                csv_writer.writerow(line_dict)

        return output_file
