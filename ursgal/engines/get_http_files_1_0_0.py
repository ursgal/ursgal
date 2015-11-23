#!/usr/bin/env python3.4
import ursgal


class get_http_files_1_0_0( ursgal.UNode ):
    """
    get_http_files_1_0_0 UNode

    Downloads files via http

    Args:
    def main( http_url = None, http_output_folder = None):

    """
    def __init__(self, *args, **kwargs):
        super(get_http_files_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Downloads files via http

        '''
        print('[ -ENGINE- ] Executing HTTP Download ..')
        self.time_point(tag = 'execution')
        main = self.import_engine_as_python_function()
        main(
            http_url            = self.params.get('http_url', None),
            http_output_folder  = self.params.get('http_output_folder', None),
        )
        self.print_execution_time(tag='execution')
        return
