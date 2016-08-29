#!/usr/bin/env python3.4
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

    Please visit pyGCluster documentation for more information on this plotting
    function
         * http://pygcluster.github.io/usage.html#clustered-data-visualization
         * color gradients
         * box styles


    Available parameters for heatmap
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

    Please do not forget to cite pyGCluster and Ursgal when using this node.

    '''
    csv_reader =  csv.DictReader(
        open(input_file, 'r')
    )
    params['all_conditions']    = set()
    params['additional_labels'] = {}

    for fieldname in csv_reader.fieldnames:
        if fieldname.endswith('_mean'):
            params['all_conditions'].add(
                fieldname.replace('_mean', '') # this tag could also go into params
            )
    params['all_conditions'] = sorted(list(params['all_conditions']))
    plot_collector = {}
    identifiers    = []
    for line_dict in csv_reader:
        line_name = line_dict[params['heatmap_identifier_field_name']]

        plot_collector[ line_name ] = {}

        for condition in params['all_conditions']:
            try:
                ratio =  float(line_dict['{0}_mean'.format(condition)])
                sd    = float(line_dict['{0}_std'.format(condition)])
                plot_collector[ line_name ][condition] = (ratio, sd)
            except:
                continue
        identifiers.append(line_name)
        try:
            params['additional_labels'][ line_name ] = [' ', line_dict[params['heatmap_annotation_field_name']]]
        except:
            pass
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
