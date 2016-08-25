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
    '''
    csv_reader =  csv.DictReader(
        open(input_file, 'r')
    )
    params['all_conditions']    = set()
    params['additional_labels'] = {}

    for fieldname in csv_reader.fieldnames:
        if fieldname.endswith('_mean'):
            params['all_conditions'].add( fieldname.replace('_mean', ''))
    params['all_conditions'] = sorted(list(params['all_conditions']))
    plot_collector = {}
    identifiers    = []
    for line_dict in csv_reader:
        line_name = line_dict[params['heatmap_object_field_name']]

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
