#!/usr/bin/env python3.4
import ursgal


class get_ftp_files_1_0_0( ursgal.UNode ):
    """
    get_ftp_files_1_0_0 UNode

    Downloads files from FTP servers

    Args:
    def main(
        ftp_url             = None,
        folder              = None,
        login               = None,
        password            = None,
        include_ext         = None,
        output_folder       = None,
        max_number_of_files = None,
        blocksize           = None
    )
    """
    def __init__(self, *args, **kwargs):
        super(get_ftp_files_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Downloads files from FTP server

        '''
        print('[ -ENGINE- ] Executing FTP Download ..')
        self.time_point(tag = 'execution')
        main = self.import_engine_as_python_function()
        main(
            ftp_url             = self.params.get('ftp_url', None),
            folder              = self.params.get('ftp_folder', None),
            login               = self.params.get('ftp_login', None),
            password            = self.params.get('ftp_password', None),
            include_ext         = self.params.get('ftp_include_ext', None),
            output_folder       = self.params.get('ftp_output_folder', None),
            max_number_of_files = self.params.get('ftp_max_number_of_files', None),
            blocksize           = self.params.get('ftp_blocksize', None)
        )
        self.print_execution_time(tag='execution')
        return
