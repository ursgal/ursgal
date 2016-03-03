#!/usr/bin/env python3.4
# encoding: utf-8
"""
    Ursgal MappOrs

    :copyright: (c) 2014 by C. Fufezan, S. Schulze
    :licence: BSD, see LISCENSE for more details

"""
from ursgal.uparams import ursgal_params as urgsal_dict
from collections import defaultdict as ddict


class UParamMapper( dict ):
    '''
    '''
    version = '0.2.0'

    def __init__( self, *args ):
        assert len(args) <= 1, 'Can only be initialized with max one argument'
        if len(args) == 0:
            params_dict = urgsal_dict
        else:
            params_dict = args[0]

        self.update( params_dict )
        self.lookup = self.group_styles()

    def _assert_engine(self, engine):
        assert engine is not None, 'must define engine!'
        return

    def mapping_dicts( self, engine_or_engine_style):
        '''yields all mapping dicts'''
        if '_style_' in engine_or_engine_style:
            lookup_key = 'style_2_params'
            style = engine_or_engine_style
        else:
            lookup_key = 'engine_2_params'
            style = self.lookup['engine_2_style'].get(engine_or_engine_style,  None)

        for uparam in self.lookup[ lookup_key ].get(engine_or_engine_style, []):
            sup = self[ uparam ]

            yield {
                'ukey'   : uparam,
                'style'  : style,
                'default_value' : sup['default_value'],
                'ukey_translated' : sup['ukey_translation'][ style ],
                'uvalue_style_translation' : sup['uvalue_translation'].get(style, {})
            }

    def get_all_params( self, engine=None):
        self._assert_engine( engine )
        all_params = []
        for ukey in self.keys():
            if engine in self[ ukey ]['available_in_unode']:
                all_params.append( ukey )
        return all_params

    def group_styles(self):
        '''
        Parses self.items() and build up lookups.
        Additionally, consistency check is performed to guarantee that each
        engine is mapping only on one style.

        The lookup build and returned looks like

        lookup = {
            'style_2_engine' : {
                'xtandem_style_1' : [
                    'xtandem_sledgehamer',
                    'xtandem_cylone',
                    ...
                ],
                'omssa_style_1' ...
            }
            'engine_2_style' : {
                'xtandem_sledgehamer' : 'xtandem_style_1', ...
            },
            'engine_2_params' : {
                'xtandem_sledgehamer' : [ uparam1, uparam2, ...], ...
            },
            'style_2_params' : {
                'xtandem_style_1' : [ uparam1, uparam2, ... ], ...
            }
        }
        '''
        lookup = {
            'style_2_engine' : ddict(set),
            'engine_2_style' : {},
            # these two are not in the docu yet ...
            'engine_2_params': ddict(list),
            'style_2_params': ddict(list)
        }
        for uparam, udict in sorted(self.items()):
            # print( uparam, end = '\t')
            # if uparam == 'force':
            #     print(udict)
            for style in udict['ukey_translation'].keys():
                try:
                    style_basename, style_version = style.split('_style_')
                except:
                    print('Syntax Error @ uparam {0}'.format(uparam))
                    print('style : {0}'.format( style ))
                    exit(1)
                vvv = False
                if style_basename == 'ucontroller':
                    vvv = True
                    # print('UController params {0}'.format( uparam ))
                # else:
                    # print()
                styles_seen = set()
                for engine in udict['available_in_unode']:
                    # if vvv:
                    #     print(engine )
                    if style_basename not in engine:
                        continue

                    lookup['style_2_engine'][ style ].add( engine )
                    lookup['engine_2_params'][ engine ].append( uparam )

                    if True: # style not in styles_seen:
                        lookup['style_2_params'][ style ].append( uparam )
                        styles_seen.add( style )

                    parsed_e2s = lookup['engine_2_style'].get( engine, None)
                    if parsed_e2s is None:
                        lookup['engine_2_style'][ engine ] = style
                    else:
                        if parsed_e2s != style:
                            print(
                                '{0} was found to map on style {1} and {2}'.format(
                                    engine, parsed_e2s, style
                                )
                            )
        return lookup

    def show_params_overview( self, engine=None):
        self._assert_engine( engine )
        # This can be done differently with the lookups now ...
        for param in sorted(self.get_all_params( engine=engine)):
            udefault_value     = self[ param ]['default_value']

            ukey_translation   = self[ param ]['ukey_translation'].get(
                'msgfplus_style_1', '??'
            )
            uvalue_translation = self[ param ]['uvalue_translation'].get(
                'msgfplus_style_1', {}
            )
            try:
                translated_default_param_value = uvalue_translation.get( param, 'n/d')
            except:
                translated_default_param_value = 'complex type'
            try:

                print(
                    'uParams {0: >30} : {1: <20} {2: >30} : {3: <20}'.format(
                        param,
                        udefault_value,
                        ukey_translation,
                        translated_default_param_value,
                    )
                )
            except:

                print('Failed on: ' , param)


if __name__ == '__main__':
    print('Yes!')
