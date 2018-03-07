#!/usr/bin/env python3.4
# encoding: utf-8

import sys
import os
import pprint
sys.path.insert(0, os.path.abspath('../'))
from ursgal.uparams import ursgal_params
from collections import defaultdict as ddict

_table_headers = ['style', 'translation', 'translated value', 'ursgal value']

minimal_width = max([ len(t) for t in _table_headers])

PARAMS_FILE = open('source/parameter.txt', 'w')

def create_format_string( number_of_columns = 1 ):
    fmt = ''
    for n in range(number_of_columns):
        fmt += ' {' + str(n) + ': <{width}}'
    return fmt


def determine_longest_string( fdict ):
    len_longest = minimal_width
    for k, value in fdict.items():
        if isinstance(k, bool):
            k = 'False'
        # print(k,value)
        if len(str(k)) > len_longest:
            len_longest = len(k)
        if isinstance(value, dict):
            # value translations
            len_in_nested = determine_longest_string( value)
            if len_in_nested > len_longest:
                len_longest = len_in_nested
        elif isinstance(value, bool):
            pass
        elif value is None:
            pass
        elif isinstance(value, float):
            pass
        elif isinstance(value, int):
            pass
        elif isinstance(value, tuple):
            pass
        else:
            if len(value) > len_longest:
                len_longest = len(value)
    return len_longest


def uprint( string ):
    print( string, file = PARAMS_FILE)
    # print( string )
    return

def print_error( udict, syntax_error_at='unkown' ):
    pprint.pprint( udict )
    print('Syntax error @ {0}'.format( syntax_error_at ))


if __name__ == '__main__':
    print(
        'Converting ursgal.uparams to sphinx. [ source/parameter.txt ] '
    )
    uprint('''
.. _parameters:

Ursgal Parameters
*****************

A Dash script has been built in order to make it easier to explore uparams.
It allows for searching for specific uparams, filtering by UNodes (i.e. engines),
and filtering by utags. 
To install Dash, follow the instructions on 
    | https://dash.plot.ly/

Afterwards, just go to the docs folder and execute the script::

    user@localhost:~/ursgal/docs$ python3.4 uparams_to_sphinx_docu.py

A local server will be created and view the interactive page: 
    | http://127.0.0.1:8050/

Besides this, all uparams are still listed here as part of the documentation.


.. note:: This sphinx source file was **auto-generated** using
    ursgal/docs/uparams_to_sphinx_docu.py, which parses ursgal/ursgal/uparams.py
    Please **do not** modify this file directly, but commit changes to ursgal.uparams.


''')
    for ursgal_param, udict in sorted(ursgal_params.items()):
        # if len(udict['available_in_unode']) <= 5:
        #     continue
        if isinstance(udict['default_value'], dict):
            default_value = str(sorted(udict['default_value'])).strip()
        else:
            default_value = str(udict['default_value']).strip()
        uprint('''
.. raw:: html

      <hr />

{0}
{1}


{desc}

:Default value: {default_value}
:type: {type}
:triggers rerun: {rerun}
            '''.format(
            ursgal_param,
            '#' * (len(ursgal_param) + 11),
            desc = udict['description'].strip(),
            default_value = default_value,
            type = udict.get('uvalue_type', ''),
            rerun = udict.get('triggers_rerun', 'False')
        ))

        uprint('''
Available in unodes
"""""""""""""""""""
''')
        for unode in udict['available_in_unode']:
            uprint('* {0}'.format( unode ))
        uprint('''
Ursgal key translations for *{0}*
""""""""""""""""""""""""""""""{1}
'''.format( ursgal_param, '"'*len(ursgal_param)))
        len_longest = determine_longest_string( udict['ukey_translation']  )
        fmt = create_format_string( number_of_columns = 2 )
        delimiter_text = ['=' * len_longest ] * 2
        try:
            uprint( fmt.format(*delimiter_text, width=len_longest))
        except:
            print( delimiter_text )
            print( udict['ukey_translation'])
            exit(1)
        uprint( fmt.format('Style', 'Translation', width=len_longest))
        uprint( fmt.format(*delimiter_text, width=len_longest))
        for style, translation in sorted(udict['ukey_translation'].items()):
            try:
                uprint( fmt.format(style, '{0}'.format(translation), width=len_longest))
            except:
                print( fmt , style, translation, len_longest )
                exit(1)
        uprint( fmt.format(*delimiter_text, width=len_longest))

        if len( udict['uvalue_translation'] ) == 0:
            continue
        uprint('''
Ursgal value translations
"""""""""""""""""""""""""
''')
        len_longest = determine_longest_string( udict['uvalue_translation']  )
        fmt = create_format_string(
            number_of_columns =  len(udict['uvalue_translation'].keys()) + 1
        )
        nmbr_of_val_translations = len(udict['uvalue_translation'].keys())
        delimiter_text = ['=' * len_longest ] * ( nmbr_of_val_translations + 1)
        header_text_1 = [
            '{0: <{1}}'.format('Ursgal Value', len_longest),
            '{0: <{1}}'.format('Translated Value', len_longest),
        ] + [''] * (nmbr_of_val_translations - 1)

        header_text_2 = [
            '{0: >{1}}'.format('-' * (len_longest), len_longest),
            '{0}'.format(
                '-'.join(
                    ['-' * len_longest] * len(udict['uvalue_translation'].keys())
                )
            ),
        ] + [''] * (nmbr_of_val_translations )
        header_text_3 = ['{0: <{1}}'.format('.', len_longest)]
        row_predicts = {}
        for style, fdict in sorted(udict['uvalue_translation'].items()):
            header_text_3.append(
                '{0: <{1}}'.format(style, len_longest),
            )
            try:
                for uvalue_unformated, translated_value in sorted(fdict.items()):
                    # header_text_3.append( '{0: <{1}}'.format(uvalue_unformated, len_longest) )
                    if translated_value is None:
                        translated_value = 'None'
                    uvalue = '{0: <{1}}'.format(uvalue_unformated, len_longest)
                    if uvalue not in row_predicts.keys():
                        row_predicts[ uvalue ] = {
                            s : 'n/t' for s in udict['uvalue_translation'].keys()
                        }
                    row_predicts[ uvalue ][ style ] = '{0: <{1}}'.format(
                        translated_value, len_longest
                    )
            except:
                print(fdict)
                print_error( udict, syntax_error_at = 'uvalue_translation' )
                # for uvalue_unformated, translated_value in sorted(fdict.items()):
                #     # header_text_3.append( '{0: <{1}}'.format(uvalue_unformated, len_longest) )
                #     uvalue = '{0: <{1}}'.format(uvalue_unformated, len_longest)
                #     if uvalue not in row_predicts.keys():
                #         row_predicts[ uvalue ] = {
                #             s : 'n/t' for s in udict['uvalue_translation'].keys()
                #         }
                #     row_predicts[ uvalue ][ style ] = '{0: <{1}}'.format(
                #         translated_value, len_longest
                #     )
                exit(1)
        uprint( fmt.format(*delimiter_text, width=len_longest))
        uprint( fmt.format(*header_text_1, width=len_longest))
        uprint( fmt.format(*header_text_2, width=len_longest).rstrip())
        uprint( fmt.format(*header_text_3, width=len_longest))
        uprint( fmt.format(*delimiter_text, width=len_longest))

        for uvalue, fdict in sorted( row_predicts.items() ):
            row = [ uvalue ]
            for k, v in sorted(fdict.items()):
                row.append( v )
            uprint( fmt.format(*row, width=len_longest))
        uprint( fmt.format(*delimiter_text, width=len_longest))
uprint('''

.. params ending on _ are links ... one can escape them with \_ but well well

.. _score:
   http://http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/

.. _proteinacc_start_stop_pre_post:
    http://http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/

.. _decoy:
    http://http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/

    ''')
