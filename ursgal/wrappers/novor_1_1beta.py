#!/usr/bin/env python3.4
import ursgal
import os
import csv


class novor_1_1beta( ursgal.UNode ):
    """
    Novor UNode
    Parameter options at http://rapidnovor.com/

    Reference:
    Bin Ma (2015) Novor: Real-Time Peptide de Novo Sequencing Software.
    """
    META_INFO = {
        'engine_type' : {
            'denovo_engine' : True,
        },
        'engine' : {
            'linux' : {
                '64bit' : {
                    'exe'            :'novor.sh',
                }
            },
            'darwin' : {
                '64bit' : {
                    'exe'            :'novor.sh',
                }
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'novor.bat',
                }
            },
        },
        'in_development'            : True,
        'output_extension'          : '.csv',
        'input_types'               : ['.mgf'],
        'create_own_folder'         : True,
        'citation'                  : \
            'Bin Ma (2015) Novor: Real-Time Peptide de Novo Sequencing Software.',
        'include_in_git'            : False,
    }

    def __init__(self, *args, **kwargs):
        super(novor_1_1beta, self).__init__(*args, **kwargs)
        pass


    def preflight( self ):
        '''
        Formatting the command line via self.params

        Params.txt file will be created in the output folder

        Returns:
                dict: self.params
        '''

        self.params['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '.mgf'
        )

        self.params['mgf_new_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '_tmp.mgf'
        )
        self.created_tmp_files.append( self.params['mgf_new_input_file'] )

        self.params['output_file_incl_path'] = os.path.join(
            self.params['mgf_new_input_file'] + '.csv'
        )
        self.created_tmp_files.append( self.params['output_file_incl_path'] )

        self.params['params_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '_Params.txt'
        )
        self.created_tmp_files.append( self.params['params_file'])

        self.params['new_output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        self.params['precursor_mass_tolerance'] = ( float(self.params['precursor_mass_tolerance_plus']) + \
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
            'Deamidated (NQ)',
            # 'Dehydrated (N-term C)',
            'Dioxidation (M)',
            'Methyl (C-term)',
            # 'Methyl (DE)',
            'Oxidation (M)',
            'Oxidation (HW)',
            'Phospho (ST)',
            'Phospho (Y)',
            # 'Pyro-carbamidomethyl (N-term C)',
            'Pyro-Glu (E)',
            'Pyro-Glu (Q)',
            'Sodium (C-term)',
            # 'Sodium (DE)',
            # 'Sulfo (STY)',
            # 'Trimethyl (RK)',
        ]

        # need to adapt for more than one aa with same mod
        # check with mass
        potential_mods = []
        fixed_mods = []
        for mod in self.params[ 'mods' ][ 'fix' ]:
            if 'N-term' in mod['pos']:
                mod[ 'aa' ] = 'N-term'
            if 'C-term' in mod['pos']:
                mod[ 'aa' ] = 'C-term'
            if '{0} ({1})'.format(mod['name'], mod['aa']) not in available_mods:
                print('''
        [ WARNING ] Novor does not support your given modification
        [ WARNING ] Continue without modification {0} '''.format(mod)
                    )
                continue
            fixed_mods.append('{0} ({1})'.format(mod[ 'name' ], mod[ 'aa' ] ))

        for mod in self.params[ 'mods' ][ 'opt' ]:
            if 'N-term' in mod['pos']:
                mod[ 'aa' ] = 'N-term'
            if 'C-term' in mod['pos']:
                mod[ 'aa' ] = 'C-term'
            if '{0} ({1})'.format(mod['name'], mod['aa']) not in available_mods:
                print('''
        [ WARNING ] Novor does not support your given modification
        [ WARNING ] Continue without modification {0} '''.format(mod)
                    )
                continue
            potential_mods.append(
                '{0} ({1})'.format(mod[ 'name' ], mod[ 'aa' ] )
            )
        self.params['fixed_modifications'] =  ','.join( fixed_mods )
        self.params['potential_modifications'] = ','.join( potential_mods )

        params_file = open( self.params['params_file'], 'w', encoding = 'UTF-8' )
        params2write = [
            'enzyme = {enzyme}'.format(**self.params),
            'fragmentation = {frag_method}'.format(**self.params),
            'massAnalyzer = {instrument}'.format(**self.params),
            'fragmentIonErrorTol = {frag_mass_tolerance}{frag_mass_tolerance_unit}'.format(**self.params),
            'precursorErrorTol = {precursor_mass_tolerance}{precursor_mass_tolerance_unit}'.format(**self.params),
            'variableModifications = {potential_modifications}'.format(**self.params),
            'fixedModifications = {fixed_modifications}'.format(**self.params),
            'forbiddenResidues = {novor_forbidden_residues}'.format(**self.params),
        ]
        for param in params2write:
            print( param, file = params_file )
        params_file.close()

        mgf_org_input_file = open( self.params['mgf_input_file'], 'r', encoding = 'UTF-8' )
        lines = mgf_org_input_file.readlines()
        mgf_org_input_file.close()

        mgf_new_input_file = open( self.params['mgf_new_input_file'], 'w', encoding = 'UTF-8')
        for line in lines:
            if line.startswith('CHARGE'):
                charge = line.split('=')[1]
                print( 'CHARGE={0}+'.format(charge.strip()), file = mgf_new_input_file)
            else:
                print( line, file = mgf_new_input_file)
        mgf_new_input_file.close()

        self.params[ 'command_list' ] = [
            self.exe,
            '-p', '{params_file}'.format(**self.params),
            self.params['mgf_new_input_file'], '-f',
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

        ]

        cached_novor_output = []
        headers = None
        result_file = open( self.params['output_file_incl_path'], 'r')
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
        for header in headers:
            if header == '':
                continue
            translated_headers.append(
                self.USEARCH_PARAM_VALUE_TRANSLATIONS.get(header, header)
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
                if self.USEARCH_PARAM_VALUE_TRANSLATIONS[k] == 'Sequence':
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
                new_line_dict[ self.USEARCH_PARAM_VALUE_TRANSLATIONS[k] ] = v.strip()
            new_line_dict['Raw data location'] = self.params['mgf_input_file']
            new_line_dict_list.append(new_line_dict)

        new_result_file = open( self.params['new_output_file_incl_path'], 'w')
        csv_dict_writer_object = csv.DictWriter(
            new_result_file,
            fieldnames = translated_headers
        )
        csv_dict_writer_object.writeheader()
        for line_dict in new_line_dict_list:
            csv_dict_writer_object.writerow( line_dict )
        return
