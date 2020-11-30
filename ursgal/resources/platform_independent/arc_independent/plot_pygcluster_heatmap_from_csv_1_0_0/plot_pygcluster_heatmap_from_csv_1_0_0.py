#!/usr/bin/env python
# encoding: utf-8
'''

'''

import os
import pyGCluster
import csv
import sys

def main(input_file=None, output_file=None, params=None):
    '''
    Arguments:
        input_file (str): input filename of csv which should be unified
        output_file (str): output filename of csv after unifying
        params (dict): params as passed by ursgal

    Note:
        Please do not forget to cite pyGCluster AND Ursgal when using this node.
        Thank you in advance!

    Please visit pyGCluster documentation for more information on this plotting
    function::

         * http://pygcluster.github.io/usage.html#clustered-data-visualization
         * color gradients
         * box styles


    Available parameters for heatmap::

        * heatmap_identifier_field_name defines the fieldname in the csv to
          appear directly right of the heatmap rows. Tipically the gene or
          protein name (Default: 'Protein')
        * heatmap_annotation_field_name defines the fieldname for an additional
          annotation in the csv to appear directly right of the object name in
          the heatmap rows. Tipically the gene or protein name
          (Default : 'map to uniprot')
        * heatmap_max_value defines the maximum value for the color scale
          (Default: 3)
        * heatmap_min_value defines the maximum value for the color scale
          (Default: -3)
        * heatmap_color_gradient defines the color gradient for the
          visualization (Default: 'Spectral')
        * heatmap_box_style defines the box style for the
          visualization (Default: 'classic')
        * heatmap_value_suffix is the suffix of the column name for columns
          holding a value (Default: '_mean')
        * heatmap_error_suffix is the suffix of the column name for columns
          holding the error to the value (Default: '_std')
        * heatmap_column_positions defines the order of the columns for plotting


    Note:

        Use of force = True is recommended to cover changes in the csv input
        file.
        Default value suffix of the column name is '_mean' and '_std' for the
        error estimate.
        Please refer to the documentation for further details on parameters.

    '''
    csv_reader = csv.DictReader(
        open(input_file, 'r')
    )
    # pprint.pprint(params)
    params['additional_labels'] = {}
    if params['heatmap_column_positions'] == {}:
        params['all_conditions']    = set()
        for fieldname in csv_reader.fieldnames:
            if fieldname.endswith(params['heatmap_value_suffix']):
                params['all_conditions'].add(
                    fieldname.replace(
                        params['heatmap_value_suffix'],
                        ''
                    )  # this tag could also go into params
                )
        params['all_conditions'] = sorted(list(params['all_conditions']))
    else:
        params['all_conditions'] = [
            params['heatmap_column_positions'][k] for k in sorted(params['heatmap_column_positions'].keys())
        ]
    plot_collector = {}
    identifiers    = []
    forbidden_character_list = [ '>', '<' ]
    for line_dict in csv_reader:
        line_name = line_dict[ params['heatmap_identifier_field_name'] ]
        for character in forbidden_character_list:
            line_name = line_name.replace( character, '__' )

        plot_collector[ line_name ] = {}

        for condition in params['all_conditions']:
            try:
                ratio =  float(
                    line_dict['{0}{1}'.format(condition,params['heatmap_value_suffix'])]
                )
                sd    = float(
                    line_dict['{0}{1}'.format(condition,params['heatmap_error_suffix'])]
                )
                plot_collector[ line_name ][condition] = (ratio, sd)
            except:
                continue
        identifiers.append(line_name)
        if params['heatmap_annotation_field_name'] in line_dict.keys():
            annotation = line_dict[params['heatmap_annotation_field_name']]
            for character in forbidden_character_list:
                annotation = annotation.replace( character, '__' )
            params['additional_labels'][ line_name ] = [ ' ', annotation ]

    cluster                      = pyGCluster.Cluster()
    folder                       = os.path.dirname(output_file)
    cluster['Working directory'] = folder
    cluster.draw_expression_map(
        data                        = plot_collector,
        identifiers                 = identifiers,
        conditions                  = params['all_conditions'],
        additional_labels           = params['additional_labels'],
        min_value_4_expression_map  = params['heatmap_min_value'],
        max_value_4_expression_map  = params['heatmap_max_value'],
        expression_map_filename     = output_file,
        box_style                   = params['heatmap_box_style'],
        color_gradient              = params['heatmap_color_gradient'],
    )

    return

if __name__ == '__main__':
    main()
