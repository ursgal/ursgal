#!/usr/bin/env python
# encoding: utf-8
"""
plot.py

by
    Stefan Schulze
    Anna Niehues
    Johannes Barth
    Till Bald
    Daniel Jaeger
    Christian Fufezan

"""
from __future__ import print_function
import os
import sys
import bisect
import math
import codecs

def main( *args, **kwargs ):
    """
    Creates a simple SVG VennDiagram
    requires 2, 3, 4 or 5 sets as arguments

    Keyword Arguments:

        output_file

        header

        label_A
        label_B
        label_C
        label_D
        label_E

        color_A:  e.g. #FF8C00
        color_B
        color_C
        color_D
        color_E

        font

    the function returns a dict with the following keys were the results
    can be accesse by e.g. dict['C-(A|B|D)']['results']

        'A&B-(C|D)'
        'C&D-(A|B)'
        'B&C-(A|D)'
        'A&B&C&D'
        'A&C-(B|D)'
        'B&D-(A|C)'
        'A&D-(B|C)'
        '(A&C&D)-B'
        '(A&B&D)-C'
        '(A&B&C)-D'
        '(B&C&D)-A'
        'A-(B|C|D)'
        'D-(A|B|C)'
        'B-(A|C|D)'
        'C-(A|B|D)'

    or for 2 or 3  or 5 VennDiagrams the appropriate combinations ...

    """

    assert len(args) >= 2, "2 Sets (A, B ) are minimal arguments ! :)"
    for _ in args:
        assert isinstance(_, set) , "Input args have to be Python sets, got ... {0}".format( type(_))

    defaultValues = {
        'output_file'            : 'VennDiagram.svg',
        'header'                 : 'ursgal Venn Diagram',
        'width'                  : 1200,
        'height'                 : 1200,
        'label_A'                : 'A',
        'label_B'                : 'B',
        'label_C'                : 'C',
        'label_D'                : 'D',
        'label_E'                : 'E',
        'cx'                     : 600,
        'cy'                     : 400,
        'label font-size header' : 31,
        'label font-size major'  : 25,
        'label font-size minor'  : 20,
        'label font-size venn'   : 20,
        'demo'                   : False,
        'font'                   : 'Helvetica',
        'stroke-width'           : 2,
        'opacity'                : 0.3
    }

    for k, v in defaultValues.items():
        if k not in kwargs.keys():
            kwargs[ k ] = v
    
    A = args[0]
    B = args[1]
    if len(args) == 2:
        C = set()
        D = set()
        E = set()
        kwargs['total-pos-cy'] = kwargs['cy'] + 220
    elif len(args) == 3:
        C = args[2]
        D = set()
        E = set()
        kwargs['total-pos-cy'] = kwargs['cy'] + 320
    elif len(args) == 4:
        C = args[2]
        D = args[3]
        E = set()
        kwargs['total-pos-cy'] = kwargs['cy'] + 320
    elif len(args) == 5:
        C = args[2]
        D = args[3]
        E = args[4]
        kwargs['total-pos-cy'] = kwargs['cy'] + 410
    else:
        exit('WooT?')

    kwargs['total_n'] = len(A | B | C | D | E)

    vdLen = len( args )
    vdTypeSpecific = {
        2 : {   'A' : { 'color'         : '#e41a1c',
                        'cx'            : kwargs['cx'] - 80,
                        'cy'            : kwargs['cy'],
                        'rx'            : 170,
                        'ry'            : 170,
                        'rot'           : 0,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'] - 280,
                        'text-pos-y'    : kwargs['cy'] - 170,
                        # 'set'           : sets['A'],
                        },
                'B' : { 'color'         : '#377eb8',
                        'cx'            : kwargs['cx'] + 80,
                        'cy'            : kwargs['cy'],
                        'rx'            : 170,
                        'ry'            : 170,
                        'rot'           : 0,
                        'text-anchor'   : 'start',
                        'text-pos-x'    : kwargs['cx'] + 280,
                        'text-pos-y'    : kwargs['cy'] - 170,
                        }
                },
        3 : {   'A' : { 'color'         : '#e41a1c',
                        'cx'            : kwargs['cx'] - 80,
                        'cy'            : kwargs['cy'] + 80,
                        'rx'            : 220,
                        'ry'            : 130,
                        'rot'           : 50,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'] - 300,
                        'text-pos-y'    : kwargs['cy'] - 70,
                        },
                'B' : { 'color'         : '#377eb8',
                        'cx'            : kwargs['cx'],
                        'cy'            : kwargs['cy'] - 25,
                        'rx'            : 220,
                        'ry'            : 130,
                        'rot'           : 90,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'],
                        'text-pos-y'    : kwargs['cy'] - 310,
                        },
                'C' : { 'color'         : '#4daf4a',
                        'cx'            : kwargs['cx'] + 80,
                        'cy'            : kwargs['cy'] + 80,
                        'rx'            : 220,
                        'ry'            : 130,
                        'rot'           : -50,
                        'text-anchor'   : 'start',
                        'text-pos-x'    : kwargs['cx'] + 300,
                        'text-pos-y'    : kwargs['cy'] - 70,
                        }
                },
        4 : {   'A' : { 'color'         : '#e41a1c', # '#FF8C00',
                        'cx'            : kwargs['cx'] - 80,
                        'cy'            : kwargs['cy'] + 80,
                        'rx'            : 220,
                        'ry'            : 130,
                        'rot'           : 50,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'] - 300,
                        'text-pos-y'    : kwargs['cy'] - 70,
                        },
                'B' : { 'color'         : '#377eb8', # '#FF1493',
                        'cx'            : kwargs['cx'],
                        'cy'            : kwargs['cy'],
                        'rx'            : 220,
                        'ry'            : 130,
                        'rot'           : +50,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'] - 200,
                        'text-pos-y'    : kwargs['cy'] - 200,
                        },
                'C' : { 'color'         : '#4daf4a', # '#7D26CD',
                        'cx'            : kwargs['cx'],
                        'cy'            : kwargs['cy'],
                        'rx'            : 220,
                        'ry'            : 130,
                        'rot'           : -50,
                        'text-anchor'   : 'start',
                        'text-pos-x'    : kwargs['cx'] + 200,
                        'text-pos-y'    : kwargs['cy'] - 200,
                        },
                'D' : { 'color'         : '#984ea3', # '#00CED1',
                        'cx'            : kwargs['cx'] + 80,
                        'cy'            : kwargs['cy'] + 80,
                        'rx'            : 220,
                        'ry'            : 130,
                        'rot'           : -50,
                        'text-anchor'   : 'start',
                        'text-pos-x'    : kwargs['cx'] + 300,
                        'text-pos-y'    : kwargs['cy'] - 70,
                        }
                },
        5 : {   'A' : { 'color'         : '#e41a1c',
                        'cx'            : kwargs['cx'] - 70,
                        'cy'            : kwargs['cy'] + 20,
                        'rx'            : 280,
                        'ry'            : 160,
                        'rot'           : 14,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'] - 360,
                        'text-pos-y'    : kwargs['cy'] - 60,
                },
                'B' : { 'color'         : '#377eb8',
                        'cx'            : kwargs['cx'] + 10,
                        'cy'            : kwargs['cy'] ,
                        'rx'            : 280,
                        'ry'            : 160,
                        'rot'           : 86,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'] + 0,
                        'text-pos-y'    : kwargs['cy'] - 320,

                },
                'C' : { 'color'         : '#4daf4a',
                        'cx'            : kwargs['cx'] + 50,
                        'cy'            : kwargs['cy'] + 65,
                        'rx'            : 280,
                        'ry'            : 160,
                        'rot'           : 158,
                        'text-anchor'   : 'start',
                        'text-pos-x'    : kwargs['cx'] + 330,
                        'text-pos-y'    : kwargs['cy'] - 60,
                },
                'D' : { 'color'         : '#984ea3',
                        'cx'            : kwargs['cx'] + 5,
                        'cy'            : kwargs['cy'] + 125,
                        'rx'            : 280,
                        'ry'            : 160,
                        'rot'           : 230,
                        'text-anchor'   : 'start',
                        'text-pos-x'    : kwargs['cx'] + 210,
                        'text-pos-y'    : kwargs['cy'] + 350,
                },
               'E' : { 'color'         : '#ff7f00',
                        'cx'            : kwargs['cx'] - 75,
                        'cy'            : kwargs['cy'] + 105,
                        'rx'            : 280,
                        'ry'            : 160,
                        'rot'           : 302,
                        'text-anchor'   : 'end',
                        'text-pos-x'    : kwargs['cx'] - 270,
                        'text-pos-y'    : kwargs['cy'] + 350,
                }
            },
    }
    for k, v in vdTypeSpecific[ vdLen ].items():
        vdTypeSpecific[ vdLen ][ k ]['label']   = kwargs['label_{0}'.format(k)]
        vdTypeSpecific[ vdLen ][ k ]['setSize'] = len( eval(k) )
        vdTypeSpecific[ vdLen ][ k ]['label font-size major'] = \
            kwargs['label font-size major']
        vdTypeSpecific[ vdLen ][ k ]['label font-size minor'] = \
            kwargs['label font-size minor']
        vdTypeSpecific[ vdLen ][ k ]['label font-size venn']  = \
            kwargs['label font-size venn']

        if k not in kwargs.keys():
            kwargs[ k ] = v
    #updating color:
    for setIdentifier in ['A','B','C','D','E']:
        if 'color_{0}'.format( setIdentifier ) in kwargs.keys():
            vdTypeSpecific[ vdLen ][ setIdentifier ]['color'] = kwargs[ 'color_{0}'.format( setIdentifier ) ]

    io = open( kwargs['output_file'], 'w' )
    print("""
<svg xmlns="http://www.w3.org/2000/svg" version="1.1"
width="{width}" height="{height}"
style="position:relative; top:0; left:0; z-index:-1;">
<title>{header}</title>
<g font-family="{font}" >
<text transform="translate({cx} 40)" font-size="{label font-size header}" text-anchor="middle">{header}</text>
<text transform="translate({cx} {total-pos-cy})"  font-size="{label font-size major}" text-anchor="middle">Total</text>
<text transform="translate({cx} {y2})"  font-size="{label font-size minor}" text-anchor="middle" font-style="italic">n = {total_n}</text>
</g>    """.format(
                    y2 = kwargs['total-pos-cy'] + 30,
                    **kwargs
            ), file = io)

    for setKey in sorted( vdTypeSpecific[ len(args) ].keys() ):
        # Why do we have multiple storages ?
        kwargs[ setKey ]['opacity'] =  kwargs['opacity']
        kwargs[ setKey ]['stroke-width'] =  kwargs['stroke-width']
        # -----
        print('''
        <ellipse rx="{rx}" ry="{ry}" transform="translate({cx} {cy}) rotate({rot})" style="fill:{color};fill-opacity:{opacity};stroke:{color};stroke-width:{stroke-width}" />
        '''.format( **kwargs[ setKey ]), file = io )

    print('<g font-family="{font}" >'.format( **kwargs), file = io)

    for setKey in sorted( vdTypeSpecific[ len(args) ].keys() ):
        print('''
        <text transform="translate({text-pos-x} {text-pos-y})"  font-size="{label font-size major}" text-anchor="{text-anchor}">{label}</text>
        <text transform="translate({text-pos-x} {y2})"  font-size="{label font-size minor}" text-anchor="{text-anchor}" font-style="italic">n = {setSize}</text>
        '''.format(
                    y2 = kwargs[ setKey ]['text-pos-y']+30,
                    **kwargs[ setKey ]
                    # **kwargs
            ),  file = io )
    print('</g>', file = io)

    if len(args) == 2:
        returnDict = {
            'A&B'       : {
                'value'  : 'A.B',
                'x'      : kwargs['cx'] ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
            'B-A'       : {
                'value'  : 'B.C',
                'x'      : kwargs['cx'] + 170 ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
            'A-B'       : {
                'value'  : 'A.C',
                'x'      : kwargs['cx'] - 170 ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
        }
    elif len(args) == 3:
        returnDict = {
            'A&B-C'     : {
                'value'  : 'A.B',
                'x'      : kwargs['cx'] - 90  ,
                'y'      : kwargs['cy']        ,
                'results': None, 
            },
            'B&C-A'     : {
                'value'  : 'B.C',
                'x'      : kwargs['cx'] + 90  ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
            'A&C-B'     : {
                'value'  : 'A.C',
                'x'      : kwargs['cx']       ,
                'y'      : kwargs['cy'] + 240  ,
                'results': None,
            },
            'A&B&C'     : {
                'value'  : 'A.B.C',
                'x'      : kwargs['cx']       ,
                'y'      : kwargs['cy'] + 100  ,
                'results': None,
            },
            'A-(B|C)'   : {
                'value'  : 'A',
                'x'      : kwargs['cx'] - 190 ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
            'C-(A|B)'   : {
                'value'  : 'C',
                'x'      : kwargs['cx'] + 190 ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
            'B-(A|C)'   : {
                'value'  : 'B',
                'x'      : kwargs['cx']       ,
                'y'      : kwargs['cy'] - 140  ,
                'results': None,
            },
        }
    elif len(args) == 4:
        returnDict = {
            'A&B-(C|D)' : {
                'value'  : 'A.B',
                'x'      : kwargs['cx'] - 140 ,
                'y'      : kwargs['cy'] - 70   ,
                'results': None,
            },
            'C&D-(A|B)' : {
                'value'  : 'C.D',
                'x'      : kwargs['cx'] + 140 ,
                'y'      : kwargs['cy'] - 70   ,
                'results': None,
            },
            'B&C-(A|D)' : {
                'value'  : 'B.C',
                'x'      : kwargs['cx']       ,
                'y'      : kwargs['cy'] - 70   ,
                'results': None,
            },
            'A&B&C&D'   : {
                'value'  : 'A.B.C.D',
                'x'      : kwargs['cx']       ,
                'y'      : kwargs['cy'] + 100  ,
                'results': None,
            },
            'A&C-(B|D)' : {
                'value'  : 'A.C',
                'x'      : kwargs['cx'] - 125 ,
                'y'      : kwargs['cy'] + 135  ,
                'results': None,
            },
            'B&D-(A|C)' : {
                'value'  : 'B.D',
                'x'      : kwargs['cx'] + 125 ,
                'y'      : kwargs['cy'] + 135  ,
                'results': None,
            },
            'A&D-(B|C)' : {
                'value'  : 'A.D',
                'x'      : kwargs['cx']       ,
                'y'      : kwargs['cy'] + 240  ,
                'results': None,
            },
            '(A&C&D)-B' : {
                'value'  : 'A.C.D',
                'x'      : kwargs['cx'] - 55  ,
                'y'      : kwargs['cy'] + 170  ,
                'results': None,
            },
            '(A&B&D)-C' : {
                'value'  : 'A.B.D',
                'x'      : kwargs['cx'] + 55  ,
                'y'      : kwargs['cy'] + 170  ,
                'results': None,
            },
            '(A&B&C)-D' : {
                'value'  : 'A.B.C',
                'x'      : kwargs['cx'] - 95  ,
                'y'      : kwargs['cy'] + 30   ,
                'results': None,
            },
            '(B&C&D)-A' : {
                'value'  : 'B.C.D',
                'x'      : kwargs['cx'] + 95  ,
                'y'      : kwargs['cy'] + 30   ,
                'results': None,
            },
            'A-(B|C|D)' : {
                'value'  : 'A',
                'x'      : kwargs['cx'] - 200 ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
            'D-(A|B|C)' : {
                'value'  : 'D',
                'x'      : kwargs['cx'] + 200 ,
                'y'      : kwargs['cy']        ,
                'results': None,
            },
            'B-(A|C|D)' : {
                'value'  : 'B',
                'x'      : kwargs['cx'] - 95  ,
                'y'      : kwargs['cy'] - 140  ,
                'results': None,
            },
            'C-(A|B|D)' : {
                'value'  : 'C',
                'x'      : kwargs['cx'] + 95  ,
                'y'      : kwargs['cy'] - 140  ,
                'results': None,
            },
        }
    elif len(args) == 5:
        returnDict = {
            'A-(B|C|D|E)'       : {'value' : 'A',         'x': kwargs['cx'] - 270  , 'y' : kwargs['cy'] - 30   , 'results': None },
            'D-(A|B|C|E)'       : {'value' : 'D',         'x': kwargs['cx'] + 130  , 'y' : kwargs['cy'] + 300  , 'results': None },
            'B-(A|C|D|E)'       : {'value' : 'B',         'x': kwargs['cx']        , 'y' : kwargs['cy'] - 200  , 'results': None },
            'C-(A|B|D|E)'       : {'value' : 'C',         'x': kwargs['cx'] + 240  , 'y' : kwargs['cy'] - 10   , 'results': None },
            'E-(B|C|D|A)'       : {'value' : 'E',         'x': kwargs['cx'] - 180  , 'y' : kwargs['cy'] + 300  , 'results': None },
            'A&B-(C|D|E)'       : {'value' : 'A.B',       'x': kwargs['cx'] - 110  , 'y' : kwargs['cy'] - 120  , 'results': None },
            'C&D-(A|B|E)'       : {'value' : 'C.D',       'x': kwargs['cx'] + 170  , 'y' : kwargs['cy'] + 170  , 'results': None },
            'B&C-(A|D|E)'       : {'value' : 'B.C',       'x': kwargs['cx'] + 135  , 'y' : kwargs['cy'] - 70   , 'results': None },
            'E&C-(A|D|B)'       : {'value' : 'C.E',       'x': kwargs['cx'] - 175  , 'y' : kwargs['cy'] + 190  , 'results': None },
            'B&E-(A|D|C)'       : {'value' : 'B.E',       'x': kwargs['cx'] + 40   , 'y' : kwargs['cy'] - 120  , 'results': None },
            'A&E-(B|D|C)'       : {'value' : 'A.E',       'x': kwargs['cx'] - 230  , 'y' : kwargs['cy'] + 90   , 'results': None },
            'E&D-(A|C|B)'       : {'value' : 'D.E',       'x': kwargs['cx'] - 50   , 'y' : kwargs['cy'] + 275  , 'results': None },
            'A&C-(B|D|E)'       : {'value' : 'A.C',       'x': kwargs['cx'] + 185  , 'y' : kwargs['cy'] + 80   , 'results': None },
            'B&D-(A|C|E)'       : {'value' : 'B.D',       'x': kwargs['cx'] + 50   , 'y' : kwargs['cy'] + 260  , 'results': None },
            'A&D-(B|C|E)'       : {'value' : 'A.D',       'x': kwargs['cx'] - 175  , 'y' : kwargs['cy'] - 60   , 'results': None },
            '(A&C&D)-(B|E)'     : {'value' : 'A.C.D',     'x': kwargs['cx'] + 175  , 'y' : kwargs['cy'] + 125  , 'results': None },
            '(A&B&D)-(C|E)'     : {'value' : 'A.B.D',     'x': kwargs['cx'] - 130  , 'y' : kwargs['cy'] - 90   , 'results': None },
            '(A&B&C)-(D|E)'     : {'value' : 'A.B.C',     'x': kwargs['cx'] + 150  , 'y' : kwargs['cy'] + 10   , 'results': None },
            '(B&C&D)-(A|E)'     : {'value' : 'B.C.D',     'x': kwargs['cx'] + 90   , 'y' : kwargs['cy'] + 205  , 'results': None },
            '(B&D&E)-(A|C)'     : {'value' : 'B.D.E',     'x': kwargs['cx'] - 15   , 'y' : kwargs['cy'] + 260  , 'results': None },
            '(E&B&C)-(A|D)'     : {'value' : 'B.C.E',     'x': kwargs['cx'] + 85   , 'y' : kwargs['cy'] - 95   , 'results': None },
            '(C&D&E)-(A|B)'     : {'value' : 'C.D.E',     'x': kwargs['cx'] - 105  , 'y' : kwargs['cy'] + 220  , 'results': None },
            '(A&B&E)-(D|C)'     : {'value' : 'A.B.E',     'x': kwargs['cx'] - 10   , 'y' : kwargs['cy'] - 105  , 'results': None },
            '(A&D&E)-(B|C)'     : {'value' : 'A.D.E',     'x': kwargs['cx'] - 180  , 'y' : kwargs['cy'] + 10   , 'results': None },
            '(A&E&C)-(D|B)'     : {'value' : 'A.C.E',     'x': kwargs['cx'] - 200  , 'y' : kwargs['cy'] + 130  , 'results': None },
            '(A&B&C&D)-E'       : {'value' : 'A.B.C.D',   'x': kwargs['cx'] + 120  , 'y' : kwargs['cy'] + 140  , 'results': None },
            '(A&B&C&E)-D'       : {'value' : 'A.B.C.E',   'x': kwargs['cx'] + 75   , 'y' : kwargs['cy'] - 60   , 'results': None },
            '(A&B&D&E)-C'       : {'value' : 'A.B.D.E',   'x': kwargs['cx'] - 110  , 'y' : kwargs['cy'] - 55   , 'results': None },
            '(A&C&D&E)-B'       : {'value' : 'A.C.D.E',   'x': kwargs['cx'] - 170  , 'y' : kwargs['cy'] + 90   , 'results': None },
            '(B&C&D&E)-A'       : {'value' : 'B.C.D.E',   'x': kwargs['cx'] - 20   , 'y' : kwargs['cy'] + 220  , 'results': None },
            'A&B&C&D&E'         : {'value' : 'A.B.C.D.E', 'x': kwargs['cx'] - 10   , 'y' : kwargs['cy'] + 50   , 'results': None },
            }
    else:
        print('''
            NOT SURE WHAT YOU WANT TO DO WITH MORE THAN 5 SETS ...
        ''')
    # exit(1)
    for k in returnDict.keys():
        r                          = eval( k )
        if kwargs['demo'] == False:
            returnDict[ k ]['value']   = len( r )
        returnDict[ k ]['results'] = r
    print('<g font-family="{font}" font-size="{label font-size venn}" >'.format(**kwargs), file = io)
    for labelDict in returnDict.values():
        print('<text transform="translate({x} {y})" text-anchor="middle" stroke="#777777" stroke-width="0.5" >{value}</text>'.format(**labelDict),file=io)
    print('</g>', file=io)
    print("</svg>", file = io)
    print('Saved VennDiagram as {output_file}'.format(**kwargs ))
    return returnDict

if __name__ == '__main__':
    main(
        set( [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9              ] ),
        set( [    1,                 7, 8, 9, 10         ] ),
        set( [    1,    3,                   10, 15      ] ),
        set( [    1,                                 100 ] ),
        set( [ 0, 1,    3,    5,    7,               100 ] ),
        demo = False
    )
