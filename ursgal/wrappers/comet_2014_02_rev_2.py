#!/usr/bin/env python
import ursgal


class comet_2014_02_rev_2( ursgal.UNode ):
    """
    comet_2014_02_rev_2 UNode

    Not implemented yet
    """
    META_INFO = {
        'edit_version'      : 1.00,
        'name'              : 'Comet',
        'version'           : '2014_02_rev_2',
        'release_date'      : '2014-1-10',
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'  : [],
        'output_extensions' : [],
        'in_development'    : True,
        'include_in_git'    : None,
        'distributable'      : False,
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
