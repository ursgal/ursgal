#!/usr/bin/env python
import ursgal
import os
import subprocess
import sys

class msgfplus_v2016_09_16( ursgal.UNode ):
    """
    MSGF+ UNode
    Parameter options at https://omics.pnl.gov/software/ms-gf

    Reference:
        Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, Mohammed S,
        Heck AJ, Pevzner PA. (2010) The Generating Function of CID, ETD, and
        CID/ETD Pairs of Tandem Mass Spectra: Applications to Database Search.
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'MSGF+',
        'version'                     : 'v2016.09.16',
        'release_date'                : '2016-9-16',
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'            : ['.mgf', '.mzML', '.mzXML', '.ms2', '.pkl', '.dta.txt'],
        'output_extensions'           : ['.mzid'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'               : True,
        'utranslation_style'          : 'msgfplus_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'MSGFPlus.jar',
                    'url'            : 'https://omics.pnl.gov/sites/default/files/MSGFPlus.zip',
                    'zip_md5'        : '3496d299fb2423f0dd6b8b5d227588e6',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, '\
            'Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function '\
            'of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: '\
            'Applications to Database Search.',
    }

    def __init__(self, *args, **kwargs):
        super(msgfplus_v2016_09_16, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formatting the command line via self.params

        Modifications file will be created in the output folder

        Returns:
                dict: self.params
        '''

        translations = self.params['translations']['_grouped_by_translated_key']
        # import pprint
        # pprint.pprint(translations)
        # exit(1)

        self.params[ 'command_list' ] = [
            'java',
            '-jar',
            self.exe,
        ]

        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        frag_method_dict={
            '1':'CID',
            '2':'ETD',
            '3':'HCD',
        }

        frag_method=frag_method_dict[self.params['translations']['frag_method']]

        mgf_org_input_file = open( self.params['translations']['mgf_input_file'], 'r', encoding = 'UTF-8' )
        lines = mgf_org_input_file.readlines()
        mgf_org_input_file.close()

        self.params['translations']['mgf_new_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '_tmp.mgf'
        )
        self.created_tmp_files.append( self.params['translations']['mgf_new_input_file'] )

        mgf_new_input_file = open( self.params['translations']['mgf_new_input_file'], 'w', encoding = 'UTF-8')
        for line in lines:
            if line.startswith('CHARGE'):
                print( line, file = mgf_new_input_file)
                print( 'ACTIVATIONMETHOD={0}'.format(frag_method), file = mgf_new_input_file)
            else:
                print( line, file = mgf_new_input_file)
        mgf_new_input_file.close()

        translations['-s']['mgf_input_file'] = self.params['translations']['mgf_new_input_file']

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        translations['-o']['output_file_incl_path'] = \
            self.params['translations']['output_file_incl_path']

        self.params['translations']['modification_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '_Mods.txt'
        )
        self.created_tmp_files.append( self.params['translations']['modification_file'] )
        translations['-mod']['modifications'] = self.params['translations']['modification_file']

        mods_file = open( self.params['translations']['modification_file'], 'w', encoding = 'UTF-8' )
        modifications = []

        print('NumMods={0}'.format(translations['NumMods']['max_num_mods']), file = mods_file)

        if self.params['translations']['label'] == '15N':
            for aminoacid, N15_Diff in ursgal.ukb.DICT_15N_DIFF.items():
                existing = False
                for mod in self.params[ 'mods' ][ 'fix' ]:
                    if aminoacid == mod[ 'aa' ]:
                        mod[ 'mass' ] += N15_Diff
                        mod[ 'name' ] += '_15N_{0}'.format(aminoacid)
                        existing = True
                if existing == True:
                    continue
                else:
                    modifications.append( '{0},{1},fix,any,15N_{1}'.format( N15_Diff, aminoacid ) )

        for t in [ 'fix', 'opt' ]:
            for mod in self.params[ 'mods' ][ t ]:
                modifications.append( '{0},{1},{2},{3},{4}'.format(mod[ 'mass' ], mod[ 'aa' ], t, mod[ 'pos' ], mod[ 'name' ] ) )

        for mod in modifications:
            print( mod, file = mods_file )

        mods_file.close()

        translations['-t'] = {
            '-t' : '{0}{1}, {2}{1}'.format(
                translations['-t']['precursor_mass_tolerance_minus'],
                translations['-t']['precursor_mass_tolerance_unit'],
                translations['-t']['precursor_mass_tolerance_plus'],
            )
        }

        command_dict = {}

        for translated_key, translation_dict in translations.items():
            if translated_key == '-Xmx':
                self.params[ 'command_list' ].insert(1,'{0}{1}'.format(
                    translated_key,
                    list(translation_dict.values())[0]
                ))
            elif translated_key in ['label', 'NumMods', '-showQValue']:
                continue
            elif len(translation_dict) == 1:
                command_dict[translated_key] = str(list(translation_dict.values())[0])
            else:
                print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                sys.exit(1)
        for k, v in command_dict.items():
            self.params[ 'command_list' ].extend((k, v))

        return self.params

    def postflight( self ):
        pass
