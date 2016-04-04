#!/usr/bin/env python3.4
import ursgal
import os


class get_http_files_1_0_0( ursgal.UNode ):
    """
    get_http_files_1_0_0 UNode

    Downloads files via http

    Args:
    def main( http_url = None, http_output_folder = None):

    """
    META_INFO = {
        'engine_type' : {
            'fetcher' : True,
        },
        # 'engine_url' : {
        #     'internal' : True,
        # },
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'get_http_files_1_0_0.py',
                },
            },
        },
        'utranslation_style'        : 'get_http_style_1',
        'in_development'            : True,
        'input_types'    : '',
        'output_suffix'  : None,
        'include_in_git' : True,
        'citation'                  : 'Kremer, L. P. M., Leufken, J., '\
            'Oyunchimeg, P., Schulze, S. & Fufezan, C. (2016) '\
            'Ursgal, Universal Python Module Combining Common Bottom-Up '\
            'Proteomics Tools for Large-Scale Analysis. '\
            'J. Proteome res. 15, 788–794.',
        # 'in_development' : True
    }

    def __init__(self, *args, **kwargs):
        super(get_http_files_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Downloads files via http

        '''
        print('[ -ENGINE- ] Executing HTTP Download ..')
        self.time_point(tag = 'execution')
        main = self.import_engine_as_python_function()
        output_path = main(
            http_url            = self.params.get('http_url', None),
            http_output_folder  = self.params.get('http_output_folder', None),
        )
        self.print_execution_time(tag='execution')
        self.io['output']['finfo']['dir']  = os.path.dirname( output_path )
        self.io['output']['finfo']['file'] = os.path.basename( output_path )
        return output_path
