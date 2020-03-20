#!/usr/bin/env python
import ursgal
import os


class mascot_dat2csv_1_0_0(ursgal.UNode):
    """
    Dummy to merge mascot data into usgal workflow
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'mascot_dat2csv',
        'version'                     : '1.0.0',
        'engine_type' : {
            'converter': True
        },
        'output_extensions'           : ['.csv'],
        'create_own_folder'           : False,
        'utranslation_style'          : 'mascot_style_1',
        'citation'                    : 'www.matrixscience.com',
        'in_development'              : False,
        'include_in_git'              : True,
        'input_extensions'            : ['.dat'],
        'release_date'                : None,
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'mascot_dat2csv_1_0_0.py',
                },
            },
        },
        'citation' : '',
    }

    def __init__(self, *args, **kwargs):
        super(mascot_dat2csv_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        dat2csv = self.import_engine_as_python_function()

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        dat2csv(input_file, output_file)
        # self._add_mascot_to_ursgal_history(output_file)
        return output_file

    def _add_mascot_to_ursgal_history(self, file):
        """Add Mascot to history.

        Args:
            mapped_csv_search_results (str): Path to mapped search results.
        """
        # print('CHECKING HISTORY')
        mapped_json = '{0}.u.json'.format(file)
        mascot_missing = True
        lines = []
        with open(mapped_json, 'r') as org:
            for line in org:
                if 'mascot_x_x_x' in line:
                    mascot_missing = False
                    break
                lines.append(line)

        if mascot_missing:
            with open(mapped_json, 'w') as new:
                for line in lines:
                    if '"history": [' in line:
                        print('''
                "history": [
                  {
                    "META_INFO": {
                      "engine_type": {
                        "protein_database_search_engine": true,
                        "By Hand" : true
                      }
                    },
                    "engine": "mascot_x_x_x"
                  },''', file = new)
                    else:
                        print(line, end='', file = new)
