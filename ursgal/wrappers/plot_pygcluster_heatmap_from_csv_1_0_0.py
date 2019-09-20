#!/usr/bin/env python
import ursgal
import os


class plot_pygcluster_heatmap_from_csv_1_0_0( ursgal.UNode ):
    """plot_pygcluster_heatmap_from_csv_1_0_0 UNode"""
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Plot pyGCluster Heatmap from CSV',
        'version'            : '1.0.0',
        'release_date'       : '2014-3-15',
        'engine_type' : {
            'visualizer' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.svg'],
        'output_suffix'      : '',
        'include_in_git'     : True,
        'in_development'     : True,
        'distributable'      : True,
        'utranslation_style' : 'heatmap_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'plot_pygcluster_heatmap_from_csv_1_0_0.py',
                },
            },
        },
        'citation' : \
            'Jaeger D, Barth J, Niehues A, Fufezan C (2014) pyGCluster, a '\
            'novel hierarchical clustering approach. Bioinformatics 30 896 898',
    }

    def __init__(self, *args, **kwargs):
        super(plot_pygcluster_heatmap_from_csv_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        '''
        print('[ -ENGINE- ] Executing plotting ..')
        # self.time_point(tag = 'execution')
        unify_csv_main = self.import_engine_as_python_function()
        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        input_file  = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        unify_csv_main(
            input_file      = input_file,
            output_file     = output_file,
            params          = self.params['translations'],
        )
        # self.print_execution_time(tag='execution')
        return output_file
