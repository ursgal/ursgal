#!/usr/bin/env python3.4


from .venndiagram_1_0_0 import venndiagram_1_0_0 as venn


class venndiagram_1_1_0( venn ):
    """Venn Diagram uNode"""
    META_INFO = {
        'edit_version'       : 1.10,
        'name'               : 'Venndiagram',
        'version'            : '1.1.0',
        'release_date'       : None,
        'engine_type' : {
            'visualizer' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.svg'],
        'output_suffix'      : 'venndiagram',
        'include_in_git'     : True,
        'in_development'     : False,
        'utranslation_style' : 'venndiagram_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'venndiagram_1_1_0.py',
                },
            },
        },
        'citation' : \
            'Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. & '\
            'Fufezan, C. (2016) Ursgal, Universal Python Module Combining '\
            'Common Bottom-Up Proteomics Tools for Large-Scale Analysis. J. '\
            'Proteome res. 15, 788-794.',
    }

    def __init__(self, *args, **kwargs):
        super(venndiagram_1_1_0, self).__init__(*args, **kwargs)
        pass
