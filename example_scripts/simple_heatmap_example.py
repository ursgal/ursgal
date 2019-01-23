#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import sys
import os
import pyGCluster


def main():
    '''
    Please visit pyGCluster documentation for more information on this plotting
    function:
        http://pygcluster.github.io/usage.html#clustered-data-visualization

        - color gradients
        - box styles

    Please do not forget to cite pyGCluster and Ursgal when using this node.

    Usage:

        ./simple_heatmap_example.py <path_to_csv_file>

    Note:

        Use of force = True is recommended to cover changes in the csv input
        file.
        Default value suffix of the column name is '_mean' and '_std' for the
        error estimate.
        Please refer to the documentation for further details on parameters.

    '''
    uc = ursgal.UController(
        profile='LTQ XL low res',
        params={
            'heatmap_column_positions' : {},
            'heatmap_annotation_field_name': 'map to uniprot',
            'heatmap_identifier_field_name': 'Protein',
            'heatmap_max_value': 3,
            'heatmap_min_value': -3,
            'heatmap_color_gradient': 'RdBu',
            'heatmap_box_style': 'classic'
        }
    )
    uc.visualize(
        input_files=sys.argv[1],
        engine='plot_pygcluster',
        output_file_name='{0}_heatmap.svg'.format(
            os.path.basename(sys.argv[1])
        ),
        multi=False,
        force=True
    )
    return


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(main.__doc__)
        sys.exit(1)
    main()
