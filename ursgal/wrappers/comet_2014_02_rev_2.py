#!/usr/bin/env python3.4
import ursgal


class comet_2014_02_rev_2( ursgal.UNode ):
    """
    comet_2014_02_rev_2 UNode

    Not implemented yet
    """
    def __init__(self, *args, **kwargs):
        super(comet_2014_02_rev_2, self).__init__(*args, **kwargs)

    def preflight( self ):
        self.params[ 'command_list' ] = [
            'java', '-Xmx{java_-Xmx}'.format( **self.params),
            '-jar', '{executable_path}'.format(**self.params),
        ]
        self.params[ 'command_list' ] += self.params['options']

    def postflight( self ):
        pass
