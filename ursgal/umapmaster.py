#!/usr/bin/env python3.4
# encoding: utf-8
"""
    Ursgal MappOrs

    :copyright: (c) 2014 by C. Fufezan, S. Schulze
    :licence: BSD, see LISCENSE for more details

"""


class UParamMapper( dict ):
    '''
    '''
    def __init__( self, params_dict ):
        self._parse_params( params_dict )

    def _parse_params( self, params_dict ):
        self.clear()
        self.update( params_dict )

    def get_all_params( self, engine=None):
        assert engine is not None, 'must define engine!'
        all_params = []
        for ukey in self.keys():
            if engine in self[ ukey ]['available_in_unode']:
                all_params.append( ukey )
        return all_params

if __name__ == '__main__':
    print('Yes!')
