#!/usr/bin/env python
# encoding: utf-8
"""
    Ursgal MappOrs

    :copyright: (c) 2014 by C. Fufezan, S. Schulze
    :licence: BSD, see LISCENSE for more details

"""
import ursgal
from collections import defaultdict as ddict
import multiprocessing
import os
import time

try:
    import regex as regex
    finditer_kwargs = { 'overlapped' : True }
except:
    print('[ WARNING  ] Standard re module cannot find overlapping pattern')
    print('[   INFO   ] Consider installing the regex module')
    print('[   INFO   ] pip install -r requirements.txt')
    import re as regex
    finditer_kwargs = {}


class UParamMapper( dict ):
    '''
    UParamMapper class offers interface to ursgal.uparams

    By default, the ursgal.uparams are parsed and the UParamMapper class
    is set with the ursgal_params dictionary.
    '''
    version = '0.2.0'

    def __init__( self, *args, **kwargs):
        # kwargs['engine_path'] = ursgal.__file__
        super(UParamMapper, self).__init__(*args, **kwargs)

        assert len(args) <= 1, 'Can only be initialized with max one argument'
        if len(args) == 0:
            params_dict = ursgal.uparams.ursgal_params
            # urgsal_dict
        else:
            params_dict = args[0]

        self.update( params_dict )
        self.lookup = self.group_styles()
        self._eval_functions = {
            'cpus' : {
                'max'     : multiprocessing.cpu_count(),
                'max - 1' : multiprocessing.cpu_count() - 1,
                'max-1'   : multiprocessing.cpu_count() - 1,
            }
        }

    def _assert_engine(self, engine):
        assert engine is not None, 'must define engine!'
        return

    def _eval_default_value( self, ukey, uvalue ):
        rvalue = None
        if ukey in self._eval_functions.keys():
            if uvalue in self._eval_functions[ ukey ].keys():
                rvalue = self._eval_functions[ ukey ][ uvalue ]
                if ukey == 'cpus' and rvalue == 0:
                    rvalue = 1

        return rvalue

    def mapping_dicts( self, engine_or_engine_style):
        '''yields all mapping dicts'''
        if '_style_' in engine_or_engine_style:
            lookup_key = 'style_2_params'
            style = engine_or_engine_style
        else:
            lookup_key = 'engine_2_params'
            style = self.lookup['engine_2_style'].get(engine_or_engine_style, None)

        for uparam in self.lookup[ lookup_key ].get(engine_or_engine_style, []):
            sup = self[ uparam ]

            uvalue_style_translation = sup['uvalue_translation'].get(style, {})
            assert isinstance(uvalue_style_translation, dict), '''
            Syntax error in ursgal/uparams.py at key {0}
            '''.format( uparam )
            if len(uvalue_style_translation.keys()) != 0:
                # can be translated, at least by some engine
                # and thus is not a list of elements ;)
                translated_value = uvalue_style_translation.get(
                    sup['default_value'],
                    sup['default_value']
                )
            else:
                translated_value = sup['default_value']

            if '_uevaluation_req' in sup.get('uvalue_type',''):
                re_evaluated_value = self._eval_default_value(
                    uparam,
                    translated_value
                )
                if re_evaluated_value is not None:
                    translated_value = re_evaluated_value

            template = sup.copy()
            keys_to_delete = [
                'ukey_translation',
                'uvalue_translation',
                'available_in_unode'
            ]
            for k in keys_to_delete:
                del template[ k ]
            template.update(
                {
                    'style'                    : style,
                    'ukey'                     : uparam,
                    'ukey_translated'          : sup['ukey_translation'][ style ],
                    'default_value_translated' : translated_value,
                    'uvalue_style_translation' : uvalue_style_translation,
                    'triggers_rerun'           : sup.get('triggers_rerun', True)
                }
            )

            yield template

    def get_masked_params( self, mask = None):
        '''
        Lists all uparams and the fields specified in the mask

        For example::

            upapa.get_masked_params( mask = ['uvalue_type']) will return::
                {
                    '-xmx' : {
                        'uvalue_type' : "str",
                    },
                    'aa_exception_dict' : {
                        'uvalue_type' : "dict",
                    },
                    ...
                }

        '''
        if mask is None:
            mask = []
        masked_params = {}
        for key, value in self.items():
            masked_params[ key ] = {}
            for mkey in mask:
                masked_params[ key ][ mkey ] = value.get(mkey, None)
        return masked_params


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

        The lookup build and returned looks like::

            lookup = {
                'style_2_engine' : {
                    'xtandem_style_1' : [
                        'xtandem_sledgehamer',
                        'xtandem_cylone',
                        ...
                    ],
                    'omssa_style_1' ...
                },
                # This is done during uNode initializations
                # each unode will register its style with umapmaster
                #
                'engine_2_style' : {
                    'xtandem_sledgehamer' : 'xtandem_style_1', ...
                },
                'engine_2_params' : {
                    'xtandem_sledgehamer' : [ uparam1, uparam2, ...], ...
                },
                'style_2_params' : {
                    'xtandem_style_1' : [ uparam1, uparam2, ... ], ...
                },
                'params_triggering_rerun' : {
                    'xtandem_style_1' : [ uparam1, uparam2 .... ]
                }
            }
        '''
        lookup = {
            'style_2_engine' : ddict(set),
            'engine_2_style' : {},
            # these two are not in the docu yet ...
            'engine_2_params': ddict(list),
            'style_2_params': ddict(list),
            'params_triggering_rerun' : ddict(list)
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
                    # this style 2 engine lookup is not quite right ...
                    # This function requires unode meta info for proper
                    # mapping ....
                    # lookup['style_2_engine'][ style ].add( engine )
                    lookup['engine_2_params'][ engine ].append( uparam )

                    if style not in styles_seen:
                        lookup['style_2_params'][ style ].append( uparam )
                        if udict.get('triggers_rerun', True):
                            lookup['params_triggering_rerun'][ style ].append( uparam )
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
                            sys.exit(1)
        return lookup

    def _show_params_overview( self, engine=None):
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
