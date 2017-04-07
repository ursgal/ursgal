#!/usr/bin/env python3.4
import ursgal


class comet_2014_02_rev_2( ursgal.UNode ):
    """
    comet_2014_02_rev_2 UNode

    Not implemented yet
    """
    META_INFO = {
        'edit_version'      : 1.00,                                             # flot, inclease number if something is changed (kaz)
        'name'              : 'Comet',                                          # str, Software name (kaz)
        'version'           : '2014_02_rev_2',                                  # str, Software version name (kaz)
        'release_date'      : '2014-1-10',                                      # None, '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' (kaz)
        'engine_type' : {
            'search_engine' : True,
        },
        'input_extensions'  : [],                                               # list, extensions (kaz)
        'input_multi_file'  : False,                                            # bool, fill true up if multiple files input is MUST like venn-diagram (kaz)
        'output_extensions' : [],                                               # list, extensions (kaz)
        'in_development'    : True,
        'include_in_git'    : None,
        'utranslation_style' : 'comet_style_1',
        'citation' : \
            '',
    }

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
