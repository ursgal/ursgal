#!/usr/bin/env python
import ursgal
import os
import csv
import sys


class novor_1_05( ursgal.UNode ):
    """
    Novor UNode
    Parameter options at http://rapidnovor.com/

    Reference:
    Bin Ma (2015) Novor: Real-Time Peptide de Novo Sequencing Software. J Am Soc Mass Spectrom 26 (11)

    Import node for version novor_1_1beta

    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Novor',
        'version'            : '1.05',
        'release_date'       : '2015-11-10',
        'engine_type' : {
            'de_novo_search_engine' : True,
        },
        'input_extensions'   : ['.mgf'],
        'output_extensions'  : ['.csv'],
        'in_development'     : False,
        'create_own_folder'  : True,
        'include_in_git'     : False,
        'distributable'      : False,
        'utranslation_style' : 'novor_style_1',
        'engine' : {
            'linux' : {
                '64bit' : {
                    'exe' : 'novor.sh',
                }
            },
            'darwin' : {
                '64bit' : {
                    'exe' : 'novor.sh',
                }
            },
            'win32' : {
                '64bit' : {
                    'exe' : 'novor.bat',
                }
            },
        },
        'citation' : \
            'Bin Ma (2015) Novor: Real-Time Peptide de Novo Sequencing '\
            'Software. J Am Soc Mass Spectrom 26 (11)',
    }

    def __init__(self, *args, **kwargs):
        super(novor_1_05, self).__init__(*args, **kwargs)
        pass


    def preflight( self ):
        '''
        Formatting the command line via self.params

        Params.txt file will be created in the output folder

        Returns:
                dict: self.params
        '''

        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        self.params['translations']['mgf_new_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '_tmp.mgf'
        )
        self.created_tmp_files.append( self.params['translations']['mgf_new_input_file'] )

        self.params['translations']['tmp_output_file_incl_path'] = os.path.join(
            self.params['translations']['mgf_new_input_file'] + '.csv'
        )
        self.created_tmp_files.append( self.params['translations']['tmp_output_file_incl_path'] )

        self.params['translations']['params_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '_Params.txt'
        )
        self.created_tmp_files.append( self.params['translations']['params_file'])

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        print(
            '''
            [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
            [ WARNING ] need to be combined for Novor (use of symmetric tolerance window).
            [ WARNING ] The arithmetic mean is used.
            '''
        )
        self.params['translations']['precursor_mass_tolerance'] = ( float(self.params['precursor_mass_tolerance_plus']) + \
                                                            float(self.params['precursor_mass_tolerance_minus']) ) \
                                                            / 2.0

        available_mods =[
            'Acetyl (K)',
            'Acetyl (N-term)',
            'Amidated (C-term)',
            # 'Ammonia-loss (N-term C)',
            'Biotin (K)',
            'Biotin (N-term)',
            'Carbamidomethyl (C)',
            'Carbamyl (K)',
            'Carbamyl (N-term)',
            'Carboxymethyl (C)',
            # 'Deamidated (NQ)',
            # 'Dehydrated (N-term C)',
            'Dioxidation (M)',
            'Methyl (C-term)',
            'Methyl (DE)',
            'Oxidation (M)',
            'Oxidation (HW)',
            'Phospho (ST)',
            'Phospho (Y)',
            # 'Pyro-carbamidomethyl (N-term C)',
            'Pyro-Glu (E)',
            'Pyro-Glu (Q)',
            'Sodium (C-term)',
            'Sodium (DE)',
            'Sulfo (STY)',
            'Trimethyl (RK)',
        ]

        # need to check with mass
        potential_mods = {'tag': 'opt', 'mods' : []}
        fixed_mods = {'tag': 'fix', 'mods' : []}
        for mod_type in [potential_mods, fixed_mods]:
            not_available_mods = {}
            for mod in self.params[ 'mods' ][ mod_type['tag'] ]:
                if 'N-term' in mod['pos']:
                    mod[ 'aa' ] = 'N-term'
                if 'C-term' in mod['pos']:
                    mod[ 'aa' ] = 'C-term'
                if '{0} ({1})'.format(mod['name'], mod['aa']) not in available_mods:
                    if mod['name'] not in not_available_mods.keys():
                        not_available_mods[mod['name']] = []
                    not_available_mods[mod['name']].append(mod['aa'])
                    continue
                mod_type['mods'].append('{0} ({1})'.format(mod[ 'name' ], mod[ 'aa' ] ))

            for mod in not_available_mods.keys():
                if '{0} ({1})'.format(mod, ''.join(sorted(not_available_mods[mod]))) not in available_mods:
                    print('''
            [ WARNING ] Novor does not support your given modification
            [ WARNING ] Continue without modification {0} ({1})'''.format(mod, ''.join(sorted(not_available_mods[mod])))
                        )
                    continue
                else:
                    mod_type['mods'].append('{0} ({1})'.format(mod, ''.join(sorted(not_available_mods[mod]))))

        self.params['translations']['fixed_modifications'] =  ','.join( fixed_mods['mods'] )
        self.params['translations']['potential_modifications'] = ','.join( potential_mods['mods'] )

        if self.params['translations']['frag_mass_tolerance_unit'] == 'ppm':
            self.params['translations']['frag_mass_tolerance'] = \
                ursgal.ucore.convert_ppm_to_dalton(
                    self.params['translations']['frag_mass_tolerance'],
                    base_mz=self.params['translations']['base_mz']
                )

        params_file = open( self.params['translations']['params_file'], 'w', encoding = 'UTF-8' )
        params2write = [
            'enzyme = {enzyme}'.format(**self.params['translations']),
            'fragmentation = {frag_method}'.format(**self.params['translations']),
            'massAnalyzer = {instrument}'.format(**self.params['translations']),
            'fragmentIonErrorTol = {frag_mass_tolerance}Da'.format(**self.params['translations']),
            'precursorErrorTol = {precursor_mass_tolerance}{precursor_mass_tolerance_unit}'.format(**self.params['translations']),
            'variableModifications = {potential_modifications}'.format(**self.params['translations']),
            'fixedModifications = {fixed_modifications}'.format(**self.params['translations']),
            'forbiddenResidues = {forbidden_residues}'.format(**self.params['translations']),
        ]
        for param in params2write:
            print( param, file = params_file )
        params_file.close()

        mgf_org_input_file = open( self.params['translations']['mgf_input_file'], 'r', encoding = 'UTF-8' )
        lines = mgf_org_input_file.readlines()
        mgf_org_input_file.close()

        mgf_new_input_file = open( self.params['translations']['mgf_new_input_file'], 'w', encoding = 'UTF-8')
        for line in lines:
            if line.startswith('CHARGE'):
                charge = line.split('=')[1]
                print( 'CHARGE={0}+'.format(charge.strip()), file = mgf_new_input_file)
            else:
                print( line, file = mgf_new_input_file)
        mgf_new_input_file.close()

        self.params[ 'command_list' ] = [
            self.exe,
            '-p', '{params_file}'.format(**self.params['translations']),
            self.params['translations']['mgf_new_input_file'], '-f',
        ]

        return self.params

    def postflight( self ):
        '''
        Reformats the Novor output file
        '''
        regex_list = [
            ('\(Cam\)','Carbamidomethyl'),
            ('\(O\)','Oxidation'),
            ('\(N-term Acetyl\)','Acetyl'),
            ('\[Acetyl\]','Acetyl'),
            ('\(Acetyl\)','Acetyl'),
            ('\[Amidated\]','Amidated'),
            ('\[Biotin\]','Biotin'),
            ('\(Biotin\)','Biotin'),
            ('\[Carbamyl\]','Carbamyl'),
            ('\(Carbamyl\)','Carbamyl'),
            ('\(Carboxymethyl\)','Carboxymethyl'),
            ('\(Phospho\)','Phospho'),
            ('\(Deamidated\)', 'Deamidated'),
            ('\(Dioxidation\)', 'Dioxidation'),
            ('\[Methyl\]','Methyl'),
            ('\(Methyl\)','Methyl'),
            ('\(Pyro-Glu\)','Pyro-Glu'),
            ('\[Sodium\]','Sodium'),
            ('\(Sodium\)','Sodium'),
            ('\(Sulfo\)','Sulfo'),
            ('\(Trimethyl\)','Trimethyl'),
        ]

        cached_novor_output = []
        headers = None
        result_file = open( self.params['translations']['tmp_output_file_incl_path'], 'r')
        for line in result_file:
            if line.startswith('#'):
                if line.startswith('# id'):
                    headers = line.strip().split(',')
                    break
        assert headers is not None , '''Change in NOVOR output ? could not find header starting wth # id'''

        print('[ PARSING  ] Loading unformatted Novor results ...')
        non_commented_csv_lines = [ row for row in result_file if not row.startswith('#') ]
        result_file.close()
        csv_dict_reader_object = csv.DictReader(
            [ ','.join(headers) ] + non_commented_csv_lines
        )
        # extend and tanslate headers
        translated_headers = []
        header_translations = self.UNODE_UPARAMS['header_translations']['uvalue_style_translation']
        for header in headers:
            if header == '':
                continue
            translated_headers.append(
                    header_translations.get(header, header)
                )
        translated_headers += [
            'Spectrum Title',
            'Modifications',
            'Raw data location',
        ]

        new_line_dict_list = []
        for line_dict in csv_dict_reader_object:
            new_line_dict = {}
            for k, v in line_dict.items():
                if v is None:
                    continue
                if header_translations[k] == 'Sequence':
                    formated_peptide = v
                    for regex_pattern, unimod_name in regex_list:
                        formated_peptide = ursgal.ucore.reformat_peptide(
                            regex_pattern,
                            unimod_name,
                            formated_peptide
                        )
                    new_line_dict['Sequence'] = formated_peptide.split('#')[0]
                    try:
                        new_line_dict['Modifications'] = formated_peptide.split('#')[1]
                    except:
                        new_line_dict['Modifications'] = ''
                    continue
                new_line_dict[ header_translations[k] ] = v.strip()
            new_line_dict['Raw data location'] = self.params['translations']['mgf_input_file']
            new_line_dict_list.append(new_line_dict)

        new_result_file = open( self.params['translations']['output_file_incl_path'], 'w')
        csv_kwargs = {}
        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'
        csv_dict_writer_object = csv.DictWriter(
            new_result_file,
            fieldnames = translated_headers,
            **csv_kwargs
        )
        csv_dict_writer_object.writeheader()
        for line_dict in new_line_dict_list:
            csv_dict_writer_object.writerow( line_dict )
        return