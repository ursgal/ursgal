#!/usr/bin/env python
import ursgal
import os

class crux_2_1( ursgal.UNode ):
    """
    crux_2_1 UNode

    Not implemented yet
    """

    META_INFO = {
        'edit_version'      : 1.00,
        'name'              : 'Crux',
        'version'           : '2.1',
        'release_date'      : None,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'  : [],
        'output_extensions' : [],
        'in_development'    : True,
        'include_in_git'    : None,
        'distributable'      : False,
        'utranslation_style' : 'crux_style_1',
        'citation' : \
            '',
    }


    def __init__(self, *args, **kwargs):
        super(crux_2_1, self).__init__(*args, **kwargs)

        pass

    def print_param_line(self,key, value, io):
        '''
        '''
        print(
            '{0}={1}'.format(
                key,
                value),
            file=io
        )
        return


    def write_param_file(self):
        self.params['param_file'] = self.params['output_file_basename_incl_path'] + '_crux_params.txt'
        cam_mod = ursgal.ukb.CAM_MOD
        io = open(self.params['param_file'],'w')

        cam = False
        for mod in self.params[ 'mods' ][ 'fix' ]:
            if self.params['label'] == '15N' and mod[ 'aa' ] == 'C' and mod[ 'name' ] == 'Carbamidomethyl':
                cam = True
                continue
            print_param_line( mod[ 'aa' ], mod[ 'mass' ])

        potential_modifications = ''
        n_term_mods = ''
        for mod in self.params[ 'mods' ][ 'opt' ]:
            if mod[ 'pos' ] != 'any':
                continue
            potential_modifications += '{0}:{1}:10,'.format(mod[ 'mass' ], mod[ 'aa' ] )
        if potential_modifications != '':
            print_param_line( 'mod=', potential_modifications )

        for aminoacid, modification in ursgal.ukb.DICT_15N_DIFF.items():
            if aminoacid == 'C':
                if cam == True:
                    if self.params['label'] == '15N':
                        modification += cam_mod
                    else:
                        modification = cam_mod
                else:
                    modification = 0
                print_param_line(
                    aminoacid,
                    modification,
                    io
                )
            elif self.params['label'] == '15N':
                print_param_line(
                    aminoacid,
                    modification,
                    io
                )
        self.params_list =[
            ('spectrum-min-mz','150.000000'),
            ('min-peaks','15'),
            ('precursor-window','5'),
            ('precursor-window-type','ppm'),

        ]
        # if self.params['machine'] == 'QExactive+':
        #     self.params_list.append(('precursor-window','5'))
        #     # self.params['product_ion_tolerance'] = '0.02'

        # elif self.params['machine'] == 'LTQ XL':
        #     # self.params['ions_to_search'] = '1,4'
        #     # self.params['product_ion_tolerance'] = '0.5'
        #     pass


        for key, value in self.params_list:
            print_param_line(key, value, io)

        io.close()
        # return


    def preflight( self ):
        '''
        CRUX param options:
        http://cruxtoolkit.sourceforge.net/default.params


        CRUX tide-index options:
        http://cruxtoolkit.sourceforge.net/tide-index.html

        CRUX tide-seach options:
        http://cruxtoolkit.sourceforge.net/tide-search.html

        '''

        self.params['output_file'] = self.params['output_file_basename_incl_path']+'{0}.csv'.format(self.params['ident_csv_suffix'])

        self.params['fileroot'] = os.path.basename( self.params['output_file_basename_incl_path' ] )
        self.write_param_file()
        pprint.pprint(self.params)
        exit()
        # building command_list !
        #
        print('  Building database index for tide ...')
        self.params['command_list'] = [
            # creating the index
            '{executable_path}'.format(**self.params),
            'tide-index',
            '{database}'.format( **self.params ),
            '--decoy-format', #none|shuffle|peptide-reverse|protein-reverse
            'none',
            '{database}_crux_dbindex'.format(**self.params),
            '--overwrite', 'T',  #Replace existing files if true (T) or fail when trying to overwrite a file if false (F)
            '--parameter-file', #A file containing command-line or additional parameters
            '{param_file}'.format(**self.params),
            '--output-dir', #The name of the directory where output files will be created
            '{output_folder}'.format(**self.params),
            '--fileroot',   #The fileroot string will be added as a prefix to all output file names
            '{fileroot}'.format(**self.params)
        ]
        _run( self.params )

        self.params['command_list'] =[
            #tide-search
           '{executable_path}'.format(**self.params),
            'tide-search',
            '{mgf_input_file}'.format(**self.params),
            '{database}_crux_dbindex'.format(**self.params),
            '--overwrite', 'T',    #Replace existing files if true (T) or fail when trying to overwrite a file if false (F)
            # '--txt-output', 'T',#Output an txt fiel results file to the output directory
            '--pin-output', 'T',
            # '--mzid-output', 'T',
            '--concat', 'T',  #report target and decoy hits
            '--parameter-file', #A file containing command-line or additional parameters
            '{param_file}'.format(**self.params),
            '--output-dir', #The name of the directory where output files will be created
            '{output_folder}'.format(**self.params),
            '--fileroot',   #The fileroot string will be added as a prefix to all output file names
            '{fileroot}'.format(**self.params)

        ]


    def postflight( self ):
        '''
        links mzid default name to our specific name

        we  create now tab delimited ouput fr easier parsing and correct conversion
        '''
        pass

        # print('Creating symbolic link for output result...')
        # default_suffix = '.tide-search.mzid'
        # default_file_name = os.path.join(
        #     self.params['output_folder'],
        #     '{0}{1}'.format(
        #         self.params['fileroot'],
        #         default_suffix
        #     )
        # )
        # try:
        #     os.symlink(
        #         default_file_name,
        #         default_file_name.replace(
        #             default_suffix,
        #             '.mzid'
        #         )
        #     )
        # except:
        #     pass

