#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import pprint
sys.path.insert(0, os.path.abspath('../'))
from ursgal.uparams import ursgal_params
from collections import defaultdict as ddict
import dash
import dash_core_components as dcc
import dash_html_components as html


def sort_params(uparams, sort_by=None):
    if sort_by is None:
        return uparams
    sorted_params = {}
    for ukey in uparams.keys():
        if type(uparams[ukey][sort_by]) in [list, dict]:
            for element in uparams[ukey][sort_by]:
                if element not in sorted_params.keys():
                    sorted_params[element] = {}
                sorted_params[element][ukey] = uparams[ukey]
        else:
            element = uparams[ukey][sort_by]
            if element not in sorted_params.keys():
                sorted_params[element] = {}
            sorted_params[element][ukey] = uparams[ukey]
    return sorted_params

app = dash.Dash()

colors = {
    'background_header': '#297FB8',
    'text_header': '#FCFFFF'
}

available_engines = []
unode_sorted_uparams = sort_params(ursgal_params, sort_by='available_in_unode')
for unode in sorted(unode_sorted_uparams.keys()):
    available_engines.append(unode)

available_tags = []
utag_sorted_uparams = sort_params(ursgal_params, sort_by='utag')
for utag in sorted(utag_sorted_uparams):
    available_tags.append(utag)

app.layout = html.Div([
    html.Div([
        dcc.Markdown(
            '''
.
''',
            containerProps={
                'style': {
                    'color': 'rgb(30, 120, 210)',
                }, })
    ], style={
        'backgroundColor': 'rgb(30, 120, 210)',
    },),

    html.Div([
        dcc.Markdown('''
# Ursgal Parameters
A searchable list of all parameters in Ursgal.
Use the dropdown options to select one or multiple engines or tags \
for which the corresponding parameters should be displayed

        ''',
                     containerProps={
                         'style': {
                             'color': 'rgb(35, 35, 35)',
                         }, })
    ], style={
        'marginLeft': 10,
        'marginRight': 10,
    }),

    html.Div([
        dcc.Markdown('**UParams**'),
        dcc.RadioItems(
            id='uparams_radio',
            options=[
                {'label': 'All uparams', 'value': 'all_uparams'},
                {'label': 'Select uparams', 'value': 'select_uparams'},
            ],
            value='all_uparams',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='params',
            value='all_uparams',
            multi=True
        ),
    ], style={
        'width': '32%',
        'marginLeft': 10,
        'marginRight': 10,
        'display': 'inline-block',
        'backgroundColor': 'rgb(250, 250, 250)',
        'color': 'rgb(35, 35, 35)',
    }),

    html.Div([
        dcc.Markdown('**Engines**'),
        dcc.RadioItems(
            id='engines_radio',
            options=[
                {'label': 'All engines', 'value': 'all_engines'},
                {'label': 'Select engines', 'value': 'select_engines'},
            ],
            value='all_engines',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='engine',
            value='all_engines',
            multi=True
        ),
    ], style={
        'width': '32%',
        'marginLeft': 10,
        'display': 'inline-block',
        'backgroundColor': 'rgb(250, 250, 250)',
        'color': 'rgb(35, 35, 35)',
    }),

    html.Div([
        dcc.Markdown('**Tags**'),
        dcc.RadioItems(
            id='tags_radio',
            options=[
                {'label': 'All tags', 'value': 'all_tags'},
                {'label': 'Select tags', 'value': 'select_tags'},
            ],
            value='all_tags',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='tag',
            value='all_tags',
            multi=True
        ),
    ], style={
        'width': '32%',
        'display': 'inline-block',
        'backgroundColor': 'rgb(250, 250, 250)',
        'color': 'rgb(35, 35, 35)',
    }),

    html.Div([
        dcc.Checklist(
            id='text_options',
            options=[
                {'label': 'Show UNodes for each parameter',
                    'value': 'available_unodes'},
                {'label': 'Show Ursgal tags',
                    'value': 'show_utags'},
                {'label': 'Show Ursgal value translations',
                    'value': 'uvalue_translation'},
                {'label': 'Show Ursgal key translations',
                    'value': 'ukey_translation'},
            ],
            values=['available_unodes'],
            # labelStyle={'display': 'inline-block'}
        ),
    ], style={
        'marginLeft': 10,
        'marginRight': 10,
        'backgroundColor': 'rgb(250, 250, 250)',
        'color': 'rgb(35, 35, 35)',
    },),

    html.Div([
        dcc.Markdown(
            '''
.
''',
            containerProps={
                'style': {
                    'color': 'rgb(30, 120, 210)',
                }, })
    ], style={
        'backgroundColor': 'rgb(30, 120, 210)',
    },),

    html.Div([
        dcc.Markdown(
            id='selected_params',
            containerProps={
                'style': {
                    'color': 'rgb(37, 37, 37)',
                },
            },
        ),
    ], style={
        'marginLeft': 30,
        'marginRight': 10,
        'backgroundColor': 'rgb(250, 250, 250)',
    },)
], style={
    'backgroundColor': 'rgb(250, 250, 250)'
},)


@app.callback(
    dash.dependencies.Output('params', 'options'),
    [dash.dependencies.Input('uparams_radio', 'value'), ])
def set_uparams_dropdown(selected_uparams):
    if selected_uparams == 'all_uparams':
        return [{'disabled': True}]
    if selected_uparams == 'select_uparams':
        return [{'label': i, 'value': i} for i in sorted(ursgal_params) if i != '']


@app.callback(
    dash.dependencies.Output('params', 'disabled'),
    [dash.dependencies.Input('uparams_radio', 'value'), ])
def set_uparams_dropdown(selected_uparams):
    if selected_uparams == 'all_uparams':
        return True
    if selected_uparams == 'select_uparams':
        return False


@app.callback(
    dash.dependencies.Output('params', 'value'),
    [dash.dependencies.Input('uparams_radio', 'value'), ])
def set_engines_value(selected_uparams):
    if selected_uparams == 'all_uparams':
        return 'all_uparams'
    if selected_uparams == 'select_uparams':
        return []


@app.callback(
    dash.dependencies.Output('engine', 'options'),
    [dash.dependencies.Input('engines_radio', 'value'), ])
def set_engines_dropdown(selected_engines):
    if selected_engines == 'all_engines':
        return [{'disabled': True}]
    if selected_engines == 'select_engines':
        return [{'label': i, 'value': i} for i in sorted(available_engines) if i != '']


@app.callback(
    dash.dependencies.Output('engine', 'disabled'),
    [dash.dependencies.Input('engines_radio', 'value'), ])
def set_engines_dropdown(selected_engines):
    if selected_engines == 'all_engines':
        return True
    if selected_engines == 'select_engines':
        return False


@app.callback(
    dash.dependencies.Output('engine', 'value'),
    [dash.dependencies.Input('engines_radio', 'value'), ])
def set_engines_value(selected_engines):
    if selected_engines == 'all_engines':
        return 'all_engines'
    if selected_engines == 'select_engines':
        return []


@app.callback(
    dash.dependencies.Output('tag', 'options'),
    [dash.dependencies.Input('tags_radio', 'value'), ])
def set_engines_dropdown(selected_tags):
    if selected_tags == 'all_tags':
        return [{'disabled': True}]
    if selected_tags == 'select_tags':
        return [{'label': i, 'value': i} for i in sorted(available_tags) if i != '']


@app.callback(
    dash.dependencies.Output('tag', 'disabled'),
    [dash.dependencies.Input('tags_radio', 'value'), ])
def set_engines_dropdown(selected_tags):
    if selected_tags == 'all_tags':
        return True
    if selected_tags == 'select_tags':
        return False


@app.callback(
    dash.dependencies.Output('tag', 'value'),
    [dash.dependencies.Input('tags_radio', 'value'), ])
def set_engines_dropdown(selected_tags):
    if selected_tags == 'all_tags':
        return 'all_tags'
    if selected_tags == 'select_tags':
        return []


@app.callback(
    dash.dependencies.Output('selected_params', 'children'),
    [dash.dependencies.Input('engine', 'value'),
     dash.dependencies.Input('params', 'value'),
     dash.dependencies.Input('tag', 'value'),
     dash.dependencies.Input('text_options', 'values'), ])
def update_text(selected_engines, selected_uparams, selected_tags, selected_text_options):
    if selected_uparams == 'all_uparams':
        uparams = ursgal_params
    else:
        uparams = {}
        for ukey in selected_uparams:
            uparams[ukey] = ursgal_params[ukey]
    if selected_engines == 'all_engines':
        engine_params = uparams
    else:
        engine_params = {}
        for unode in selected_engines:
            for ukey in unode_sorted_uparams[unode]:
                if ukey not in uparams.keys():
                    continue
                if ukey not in engine_params.keys():
                    engine_params[ukey] = ursgal_params[ukey]
                else:
                    continue
    if selected_tags == 'all_tags':
        tag_engine_params = engine_params
    else:
        tag_engine_params = {}
        for utag in selected_tags:
            for ukey in utag_sorted_uparams[utag]:
                if ukey not in engine_params.keys():
                    continue
                if ukey not in tag_engine_params.keys():
                    tag_engine_params[ukey] = ursgal_params[ukey]
                else:
                    continue

    text = []
    for ursgal_param, udict in sorted(tag_engine_params.items()):
        if isinstance(udict['default_value'], dict):
            default_value = str(sorted(udict['default_value'])).strip()
        else:
            default_value = str(udict['default_value']).strip()
        text.append(
            '''
## {0}

{desc}

**Default value**: {default_value} \n
**type**: {type} \n
**triggers rerun**: {rerun} \n
'''.format(
                ursgal_param,
                desc=udict['description'].strip(),
                default_value=default_value,
                type=udict.get('uvalue_type', ''),
                rerun=udict.get('trigger_rerun', 'False')
            )
        )
        if 'available_unodes' in selected_text_options:
            text.append(
                '''
### Available in UNodes:
''')
            for unode in udict['available_in_unode']:
                text.append('* {0}'.format(unode))

        if 'show_utags' in selected_text_options:
            text.append(
                '''
### Ursgal tags:
''')
            for utag in udict['utag']:
                text.append('* {0}'.format(utag))

        if 'ukey_translation' in selected_text_options:
            text.append('''
### Ursgal key translations for {0}:
'''.format(ursgal_param)
            )
            for style, translation in sorted(udict['ukey_translation'].items()):
                text.append('* {0}: {1}'.format(
                    style,
                    translation)
                )

        if 'uvalue_translation' in selected_text_options:
            text.append('''
### Ursgal value translations for {0}:
'''.format(ursgal_param)
            )
            for style, translation in sorted(udict['uvalue_translation'].items()):
                if type(translation) is dict:
                    text.append(
                        '''* {0}: {1}'''.format(
                            style,
                            translation)
                    )
        text.append(
            '---------------')
    return '\n'.join(text)

if __name__ == '__main__':
    print('Collecting uparams ...')
    print(len(ursgal_params))
    app.run_server(debug=True)
