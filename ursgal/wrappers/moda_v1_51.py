#!/usr/bin/env python3.4
import ursgal
import os
import subprocess

class moda_v1_51( ursgal.UNode ):
    """
    MODa UNode
    Check http://prix.hanyang.ac.kr/download/moda.jsp for download, new versions and contact information

    Reference:
    Na S, Bandeira N, Paek E. (2012) Fast multi-blind modification search through tandem mass spectrometry.
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'Moda',
        'version'                     : 'v1.51',
        'release_date'                : '2012-4-1',
        'engine_type' : {
            'search_engine' : True,
        },
        'input_extensions'            : ['.mgf', '.pkl', '.dta', '.mzXML'],
        'input_multi_file'            : False,
        'output_extensions'           : ['.csv'],
        'compress_raw_search_results' : False,
        'create_own_folder'           : True,
        'in_development'              : True,
        'include_in_git'              : False,
        'utranslation_style'          : 'moda_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'moda_v1.51.jar',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Na S, Bandeira N, Paek E. (2012) Fast multi-blind modification '\
            'search through tandem mass spectrometry.',
    }

    def __init__(self, *args, **kwargs):
        super(moda_v1_51, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formatting the command line via self.params

        Returns:
                dict: self.params
        '''

        translations = self.params['translations']['_grouped_by_translated_key']
        # import pprint
        # pprint.pprint(translations)
        # exit(1)

        self.params['translations']['params_input_file'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '_params.txt'
        )
        self.created_tmp_files.append( self.params['translations']['params_input_file'] )

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        self.created_tmp_files.append(
            self.params['translations']['output_file_incl_path'].replace('.csv', '.txt')
        )
        translations['-o']['output_file_incl_path'] = \
            self.params['translations']['output_file_incl_path']

        self.params[ 'command_list' ] = [
            'java',
            '-jar',
            self.exe,
            '-i', self.params['translations']['params_input_file'],
            '-o', self.params['translations']['output_file_incl_path'].replace('.csv', '.txt'),
        ]

        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        translations['Spectra']['mgf_input_file'] = \
            self.params['translations']['mgf_input_file']

        params_input_file = open( self.params['translations']['params_input_file'], 'w', encoding = 'UTF-8' )

        fixed_mods = []
        if self.params['translations']['label'] == '15N':
            for aminoacid, N15_Diff in ursgal.ursgal_kb.DICT_15N_DIFF.items():
                existing = False
                for mod in self.params[ 'mods' ][ 'fix' ]:
                    if aminoacid == mod[ 'aa' ]:
                        mod[ 'mass' ] += N15_Diff
                        mod[ 'name' ] += '_15N_{0}'.format(aminoacid)
                        existing = True
                if existing == True:
                    continue
                else:
                    fixed_mods.append( '{0}, {1}'.format( aminoacid, N15_Diff ) )

        for mod in self.params[ 'mods' ][ 'fix' ]:
            fixed_mods.append( '{0}, {1}'.format(mod[ 'aa' ],mod[ 'mass' ] ) )

        if translations['PPMTolerance']['precursor_mass_tolerance_unit'] == 'da':
            translations['PeptTolerance'] = \
                (translations['PPMTolerance']['precursor_mass_tolerance_minus']+\
                translations['PPMTolerance']['precursor_mass_tolerance_plus'])/2
            del translations['PPMTolerance']

        elif translations['PPMTolerance']['precursor_mass_tolerance_unit'] == 'mmu':
            translations['PeptTolerance'] = \
                10e-3*\
                (translations['PPMTolerance']['precursor_mass_tolerance_minus']+\
                translations['PPMTolerance']['precursor_mass_tolerance_plus'])/2
            del translations['PPMTolerance']

        else:
             translations['PPMTolerance'] = \
                (translations['PPMTolerance']['precursor_mass_tolerance_minus']+\
                translations['PPMTolerance']['precursor_mass_tolerance_plus'])/2

        if translations['FragTolerance']['frag_mass_tolerance_unit'] == 'ppm':
            translations['FragTolerance'] = \
                ursgal.ucore.convert_ppm_to_dalton(
                    translations['FragTolerance']['frag_mass_tolerance'],
                    base_mz=self.params['translations']['base_mz']
                )
        elif translations['FragTolerance']['frag_mass_tolerance_unit'] == 'mmu':
            translations['FragTolerance'] = \
                translations['FragTolerance']['frag_mass_tolerance']*10e-3
        else:
            translations['FragTolerance'] = \
                translations['FragTolerance']['frag_mass_tolerance']

        for translated_key, translation_dict in translations.items():
            if translated_key == '-Xmx':
                self.params[ 'command_list' ].insert(1,'{0}{1}'.format(
                    translated_key,
                    list(translation_dict.values())[0]
                ))
            elif translated_key in ['-o', '-i', 'base_mz', 'label',]:
                continue
            elif translated_key == 'ADD':
                for aa_mod in fixed_mods:
                    print('{0}={1}'.format(
                            translated_key,
                            aa_mod,
                        ),
                        file = params_input_file
                    )
            elif translated_key in ['FragTolerance', 'PPMTolerance', 'PeptTolerance']:
                print('{0}={1}'.format(
                        translated_key,
                        translations[translated_key],
                    ),
                    file = params_input_file
                )
            elif len(translation_dict) == 1:
                print('{0}={1}'.format(
                        translated_key,
                        str(list(translation_dict.values())[0]),
                    ),
                    file = params_input_file
                )
            else:
                print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                exit(1)

        params_input_file.close()

        return self.params

    def postflight( self ):
        pass
