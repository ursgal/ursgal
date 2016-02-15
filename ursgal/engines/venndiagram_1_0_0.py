#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import csv
import os.path

# csv.field_size_limit(sys.maxsize)

class venndiagram_1_0_0( ursgal.UNode ):
    """Venn Diagram uNode"""
    def __init__(self, *args, **kwargs):
        super(venndiagram_1_0_0, self).__init__(*args, **kwargs)


    def _execute( self ):
        '''
        Plot Venn Diagramm for a list of .csv result files (2-5)

        Arguments are set directly but passed to the engine by self.params attribute

        Keyword Arguments:
            Input files (self.params['_input_file_dicts']): list of dictionaries created by multi_run
            column_names (list)     : list of column names (str) used for the comparison
                                      columns are merged if more than one column name given
            cutoff_column_name (str)
            cutoff_column_value (str, int, float)
            header (str)
            label_list (list)       : list of label in the same order as the input files list
                                      names of last_search_engine are used if no label_list given
            opacity (float)
            output_file_name (str)  : created by self.magic_name_generator if None


        Returns:
            dict: results for the different areas e.g. dict['C-(A|B|D)']['results']

            Output file is written to the common_top_level_dir
        '''

        print('[ -ENGINE- ] Plotting Venn diagram ..')
        self.time_point(tag = 'execution')
        venndiagram_main = self.import_engine_as_python_function()

        venn_params = {
            'opacity' : self.params['opacity']
            }

        column_sets = {}

        default_label = ['label_A','label_B','label_C','label_D','label_E','label_F']

        input_file_dicts = self.params['input_file_dicts']

        data = []
        for result_file in input_file_dicts:
            for elem in ('last_search_engine','last_de_novo_engine'):
                if elem in result_file:
                    data_field = (
                        result_file[elem],
                        os.path.join(
                            result_file['dir'],
                            result_file['file']
                        )
                    )
                    data.append( data_field )
                else:
                    continue

        all_are_csv = all( [f[1].upper().endswith('.CSV') for f in data] )
        assert all_are_csv == True, "VennDiagram input files all have to be .csv"

        output_file_name = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        self.params['output_file_incl_path'] = output_file_name

        if output_file_name == None:
            head, tail = self.determine_common_common_head_tail_part_of_names( input_file_dicts=input_file_dicts)
            output_file_name = head + tail

        output_file_dir = self.params['output_dir_path']

        output_incl_path = os.path.join(
            output_file_dir,
            output_file_name
        )

        assert len(data) <= 5, "ERROR: input_file_list can only contain two to five result files, you can merge files before, if you need"

        used_labels = []

        for n, (engine, file_path) in enumerate(data):
            if self.params['label_list'] == None:
                label = engine
            else:
                label = self.params['label_list'][n]
            venn_params[default_label[n]] = label
            column_sets[ label ]     = set()
            used_labels.append(label)
            print('[ Reading  ] Venn set {0} / file #{1} : {0}'.format(
                n,
                file_path)
            )
            file_object = open(file_path, 'r')
            csv_input = csv.DictReader(
                filter(
                    lambda row: row[0] != '#', file_object
                )
            )
            for line_dict in csv_input:
                # if line_dict.get('Is decoy', 'FALSE').upper() is 'TRUE':
                #     continue

  #               cutoff_column_name = self.params['cutoff_column_name']
  #               assert cutoff_column_name in line_dict, '''
  # The column header "{0}" was not found in {1}. Please use files that have a "PEP" column
  # (i.e. Percolator-validated files) for plotting VennDiagrams, or specify another column
  # that should be used as cutoff like this:
  # >>> uc.params['cutoff_column_name'] = 'name_of_my_score_column'  
  #               '''.format( cutoff_column_name, os.path.basename(file_path) )
  #               if float( line_dict[ cutoff_column_name ] ) > self.params['cutoff_column_value']:
  #                   continue

                value = ''
                for column_name in self.params['column_names']:
                    value += '||{0}'.format( line_dict[column_name] )
                column_sets[ label ].add( value )

        in_sets = []
        for label in used_labels:
        # for label, file_set in column_sets.items():
            in_sets.append( column_sets[label] )

        return_dict = venndiagram_main(
            in_sets,
            output_file = output_incl_path,
            **venn_params
            )

        return return_dict
