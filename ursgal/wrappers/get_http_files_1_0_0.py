#!/usr/bin/env python
import ursgal
import os


class get_http_files_1_0_0( ursgal.UNode ):
    """
    get_http_files_1_0_0 UNode

    Downloads files via http

    Args:
        * http_url
        * http_output_folder
        
    Note:
        meta info param 'output_extensions' is by default txt, so that the 
        temporary txt json files get properly deleted

    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Get HTTP Files',
        'version'            : '1.0.0',
        'release_date'       : '2016-3-4',
        'engine_type' : {
            'fetcher' : True,
        },
        'input_extensions'   : [],
        'output_extensions'  : ['.txt'],
        'output_suffix'      : None,
        'in_development'     : False,
        'include_in_git'     : True,
        'distributable'      : True,
        'utranslation_style' : 'get_http_style_1',
        # 'engine_url' : {
        #     'internal' : True,
        # },
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'get_http_files_1_0_0.py',
                },
            },
        },
        'citation' : \
            'Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. & '\
            'Fufezan, C. (2016) Ursgal, Universal Python Module Combining '\
            'Common Bottom-Up Proteomics Tools for Large-Scale Analysis. J. '\
            'Proteome res. 15, 788-794.',
    }

    def __init__(self, *args, **kwargs):
        super(get_http_files_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Downloads files via http

        '''
        print('[ -ENGINE- ] Executing HTTP Download ..')
        # self.time_point(tag = 'execution')
        main = self.import_engine_as_python_function()
        output_path = main(
            http_url            = self.params.get('http_url', None),
            http_output_folder  = self.params.get('http_output_folder', None),
        )
        # self.print_execution_time(tag='execution')
        self.io['output']['finfo']['dir']  = os.path.dirname( output_path )
        self.io['output']['finfo']['file'] = os.path.basename( output_path )
        return output_path
