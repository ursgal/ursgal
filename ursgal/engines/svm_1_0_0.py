#!/usr/bin/env python3.4
import ursgal
import os


class svm_1_0_0( ursgal.UNode ):
    """svm_1_0_0 UNode"""
    def __init__(self, *args, **kwargs):
        super(svm_1_0_0, self).__init__(*args, **kwargs)


    def preflight(self):
        if self.params['input_file'].lower().endswith('.csv') is False:
            raise ValueError('SVM input file must be a unified CSV file!')

        assert 'validation_score_field' in self.params and \
            isinstance(self.params['validation_score_field'], str), '''
  SVM requires a quality criterion (score) for sorting purposes.
  >>> uc.params['validation_score_field'] = 'my_score_column'
  >>> uc.params['bigger_scores_better'] = False  # or True!
        '''

        score_field = self.params['validation_score_field']
        if 'bigger_scores_better' not in self.params:
            bigger_is_better = False
            print('''
  WARNING! You did not specify "bigger_scores_better" (True/False)
  in the UController params! By default, SVM assumes
  that small score values indicate PSMs of high quality (False).
            ''')
        else:
            bigger_is_better = self.params['bigger_scores_better']

        in_path = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        out_path = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        self.params['command_list'] = [
            'python3.4',
            self.exe,
            '--input_csv',
            in_path,
            '--output_csv',
            out_path,
            '--kernel',
            self.params['kernel'],
            '--fdr_cutoff',
            str(self.params['fdr_cutoff']),
            '--columns_as_features',
            self.params['columns_as_features'],
            '--sort_by',
            self.params['validation_score_field'],
            '-c',
            str(self.params['c']),
            '--mb_ram',
            str(self.params['available_RAM_in_MB']),
        ]
        if self.params.get('bigger_scores_better', False):
            self.params['command_list'].append('--bigger_scores_better')

    def postflight(self):
        return
