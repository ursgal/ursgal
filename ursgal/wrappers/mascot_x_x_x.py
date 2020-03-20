#!/usr/bin/env python
import ursgal


class mascot_x_x_x( ursgal.UNode ):
    """
    Dummy to merge mascot data into usgal workflow
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'Mascot',
        'version'                     : '2017',
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'output_extensions'           : ['.xml'],
        'create_own_folder'           : True,
        'utranslation_style'          : 'mascot_style_1',
        'citation'                    : 'www.matrixscience.com',
        'in_development'              : True,
        'include_in_git'              : True,
        'input_extensions'            : [],
        'release_date'                : None
    }

    def __init__(self, *args, **kwargs):
        super(mascot_x_x_x, self).__init__(*args, **kwargs)
