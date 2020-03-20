#!/usr/bin/env python
'''
    usage:
        svm.py unified_input.csv engine_score_column_name
    i.e. :
        svm.py omssa_2_1_6_unified.csv 'OMSSA:pvalue'

    Writes a new file with added column "SVMscore" which is the distance to
    the separating hyperplane of a Percolator-like support vector machine.
'''
import numpy as np
import sklearn
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import Imputer
from collections import Counter, defaultdict
from random import random
import csv
import re
import os
import argparse

from misc import (get_score_colname_and_order, field_to_float,
                  unify_sequence,calc_FDR, scale_scores, row_is_decoy,
                  field_to_bayes_float, get_mz_values)






SCALER = sklearn.preprocessing.RobustScaler()  # RobustScaler() seems to be most robust ;)
PROTON = 1.00727646677


class SVMWrapper(dict):
    def __init__(self):
        self._svm_score_name = 'SVMscore'
        self.counter = {  # counting the # of possible training PSMs
            'target': 0,
            'decoy': 0,
            'positive': 0,
            'negative': 0,
            'unknown': 0,
            'parsed PSMs': 0,
        }
        self.results  = {}
        self.shitty_decoy_seqs = set()  # is overwritten by find_shitty_decoys()
        self.mgf_lookup = {}
        self.pep_to_mz = {}

        if __name__ == '__main__':
            self.parse_options()  # parse command line args and set options
            self.set_input_csv()

        self.observed_charges = set()
        self.used_extra_fields = set()
        self.decoy_train_prob = None  # probability to include decoy PSMs as negative training examples
        self.maximum_proteins_per_line = 0
        self.tryptic_aas = set(['R', 'K', '-'])
        self.delim_regex = re.compile(r'<\|>|\;')  # regex to split a line by both ";" and "<|>"
        return


    def parse_options(self):
        '''
        parses the command line args for options/parameters
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-i', '--input_csv', type=str, help='Input CSV path(s)',
            required=True, nargs='+')
        parser.add_argument(
            '-o', '--output_csv', type=str, help='Output CSV path',
            required=True)
        parser.add_argument(
            '-k', '--kernel', type=str, default='rbf',
            help='SVM kernel type ("rbf", "linear", "poly" or "sigmoid")')
        parser.add_argument(
            '-c', type=float, default=1.0,
            help='Penalty parameter C of the error term')
        parser.add_argument(
            '-g', '--gamma', type=str, default='auto',
            help='Gamma parameter of the SVM.')
        parser.add_argument(
            '-r', '--mb_ram', type=float, default=4000,
            help='Available RAM in megabytes, for SVM calculation')
        parser.add_argument(
            '-f', '--fdr_cutoff', type=float, default=0.01, 
            help='Target PSMs with a lower FDR will be used as a '\
                 'positive training set')
        parser.add_argument(
            '-x', '--columns_as_features', type=str, nargs='+', default=[
                'MS-GF:RawScore',
                'MS-GF:DeNovoScore',
                'MS-GF:SpecEValue',
                'MS-GF:EValue',
                'OMSSA:evalue',
                'OMSSA:pvalue',
                'X\!Tandem:expect',
                'X\!Tandem:hyperscore',
            ],
            help='Columns that should be used as a feature directly '\
                 '(e.g. secondary scores). Will be converted to float')
        parser.add_argument(
            '-d', '--dump_svm_matrix', type=str, default=False,
            help='Dump SVM matrix in PIN (Percolator input) format '
                 'to the specified path, mostly for debugging '
                 'and benchmarking.')

        arg_dict = vars(parser.parse_args())  # convert to dict
        self.update(arg_dict)
        try:
            self['gamma'] = float(self['gamma'])
        except ValueError:
            assert self['gamma'] == 'auto', 'Invalid gamma param: '\
                '"{0}", using "auto" instead.'.format(self['gamma'])


    def set_input_csv(self):
        '''
        distinguishes one vs. many unified input csv files and either
        sets the single csv as input, or merges all csvs and sets
        the merged csv as input.
        '''
        if len(self['input_csv']) > 1:
            raise Exception('You must only specify *one* unified CSV file!')
        self.csv_path = self['input_csv'][0]
        print('Using input file', self.csv_path)


    def find_shitty_decoys(self):
        '''
        Finds and notes decoys that share their sequence with a target PSM.
        
        Also counts the number of targets and decoys to get a quick estimate
        of how many positive/negative training examples can be "claimed".
        '''
        target_seqs = set()
        decoy_seqs = set()
        with open(self.csv_path, 'r') as f:

            reader = csv.DictReader(f)

            sorted_reader = sorted(
                reader, reverse=self['bigger_scores_better'],
                key=lambda d: float(d[self.col_for_sorting])
            )

            for row in sorted_reader:
                self.observed_charges.add(int(row['Charge']))
                if row_is_decoy(row):
                    decoy_seqs.add(unify_sequence(row['Sequence']))
                    self.counter['decoy'] += 1
                else:
                    target_seqs.add(unify_sequence(row['Sequence']))
                    self.counter['target'] += 1

        self.shitty_decoy_seqs = target_seqs.intersection(decoy_seqs)
        if len(self.shitty_decoy_seqs) > 0:
            print(
                'Warning! Found {0} sequences that are target AND decoy '\
                '(immutable peptides?). These will not be used for training.\n'.format(len(self.shitty_decoy_seqs))
            )
        return


    def determine_csv_sorting(self):
        with open(self.csv_path, 'r') as in_file:
            reader = csv.DictReader(in_file)
            self.col_for_sorting, self['bigger_scores_better'] = \
                get_score_colname_and_order(reader.fieldnames)
        if self.col_for_sorting == self._svm_score_name:
            self._svm_score_name = self._svm_score_name + '2'

        print('CSV will be sorted by column {0} (reverse={1}'\
              ')'.format(self.col_for_sorting, self['bigger_scores_better']))

        for feat in self['columns_as_features']:
            if feat in reader.fieldnames and feat != self.col_for_sorting:
                self.used_extra_fields.add(feat)


    def sort_by_rank(self, rowdict):
        score = float(rowdict[self.col_for_sorting])
        spec_title = rowdict['Spectrum Title']
        return (spec_title, score)


    @staticmethod
    def parse_protein_ids(csv_field, sep='<|>'):
        '''
        Turns the unified CSV column "Protein ID"
        into a set of all protein IDs.
        '''
        clean = csv_field.replace('decoy_', '').strip()
        prot_id_set = set(clean.split(sep))
        return prot_id_set


    def count_intra_set_features(self):
        '''
        intra-set features as calculated by Percolator:
        - num_pep:  Number of PSMs for which this is the best scoring peptide.
        - num_prot: Number of times the matched protein matches other PSMs.
        - pep_site: Number of different peptides that match this protein.

        own ideas:
        - pep_charge_states: in how many charge states was the peptide found?
        - seq_mods: in how many mod states was the AA-sequence found?
        - num_spec: Number of times the matched spectrum matches other peptides.
        '''
        print('Counting intra-set features...')
        self.num_pep = defaultdict(int)
        self.num_prot = defaultdict(set)
        self.pep_site = defaultdict(set)
        self.score_list_dict = defaultdict(list)

        self.pep_charge_states = defaultdict(set)
        self.seq_mods = defaultdict(set)
        self.num_spec = defaultdict(set)


        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            previous_spec_title = None
            rows_of_spectrum = []

            for row in sorted(
                reader,
                reverse=self['bigger_scores_better'],
                key=self.sort_by_rank
            ):

                if unify_sequence(row['Sequence']) in self.shitty_decoy_seqs:
                    continue
                current_spec_title = row['Spectrum Title']
                if current_spec_title != previous_spec_title:
                    # the next spectrum started, so let's process the info we
                    # collected for the previous spectrum:
                    score_list = [field_to_bayes_float(r[self.col_for_sorting]) for r in rows_of_spectrum]
                    self.score_list_dict[previous_spec_title] = score_list

                    for rank, line in enumerate(rows_of_spectrum):
                        #print("\t".join([
                            #str(rank), line['Spectrum Title'], line[self.col_for_sorting]
                        #]))
                        uni_sequence = unify_sequence(line['Sequence'])
                        peptide = (uni_sequence, line['Modifications'])

                        # multiple proteins are separated by <|>
                        # ignore start_stop_pre_post part since it depends on the peptide
                        # and not the protein (i.e. _233_243_A_R)
                        proteins = set(line['Protein ID'].replace('decoy_', '').split(';'))

                        #old unify csv format:
                        #proteins = self.parse_protein_ids(
                        #    line['proteinacc_start_stop_pre_post_;']
                        #)
                        if len(proteins) > self.maximum_proteins_per_line:
                            self.maximum_proteins_per_line = len(proteins)

                        if rank == 0:
                            # this is the 'best' peptide for that spectrum
                            self.num_pep[peptide] += 1
                        for protein in proteins:
                            self.num_prot[protein].add(
                                (line['Spectrum Title'], uni_sequence, line['Modifications'])
                            )
                            self.pep_site[protein].add(peptide)

                        self.pep_charge_states[peptide].add(int(row['Charge']))
                        self.seq_mods[uni_sequence].add(row['Modifications'])
                        self.num_spec[line['Spectrum Title']].add(peptide)

                    rows_of_spectrum = []

                rows_of_spectrum.append(row)
                previous_spec_title = current_spec_title


    def row_to_features(self, row):
        '''
        Converts a unified CSV row to a SVM feature matrix (numbers only!)
        '''
        sequence = unify_sequence(row['Sequence'])
        charge = field_to_float( row['Charge'] )
        score = field_to_bayes_float( row[self.col_for_sorting] )
        calc_mz, exp_mz, calc_mass, exp_mass = get_mz_values(row)
        #calc_mz = field_to_float( row['Calc m/z'] )  # calc m/z or uCalc?
        #exp_mz = field_to_float( row['Exp m/z'] )

        pre_aa_field = row['Sequence Pre AA']
        post_aa_field = row['Sequence Post AA']
        all_pre_aas = set(re.split(self.delim_regex, pre_aa_field))
        all_post_aas = set(re.split(self.delim_regex, post_aa_field))

        if any(pre_aa not in self.tryptic_aas for pre_aa in all_pre_aas):
            enzN = 0
        else:
            enzN = 1

        if any(post_aa not in self.tryptic_aas for post_aa in all_post_aas):
            enzC = 0
        else:
            enzC = 1

        n_missed_cleavages = len([aa for aa in sequence[:-1] if aa in ['R', 'K']])  # / len(sequence)

        missed_cleavages = [0] * 6
        try:
            missed_cleavages[n_missed_cleavages] = 1
        except IndexError:  # if a peptide has more than 6 missed cleavages
            missed_cleavages[-1] = 2

        spectrum = row['Spectrum Title'].strip()
        mass = (exp_mz * charge) - (charge - 1) * PROTON
        pep_len = len(sequence)
        #delta_mz = calc_mz - exp_mz
        delta_mass = calc_mass - exp_mass

        peptide = (sequence, row['Modifications'])
        proteins = self.parse_protein_ids(
            row['Protein ID']
        )
        num_pep = self.num_pep[peptide]
        pep_charge_states = len(self.pep_charge_states[peptide])
        seq_mods = len(self.seq_mods[sequence])
        num_spec = len(self.num_spec[row['Spectrum Title']])
        num_prot = sum(
            (len(self.num_prot[protein]) for protein in proteins)
        )
        pep_site = sum(
            (len(self.pep_site[protein]) for protein in proteins)
        )

        user_specified_features = []
        for feat in self.used_extra_fields:
            if feat != self.col_for_sorting:
                try:
                    user_specified_features.append(field_to_float(row[feat]))
                except ValueError:
                    pass

        charges = defaultdict(int)
        for charge_n in sorted(self.pep_charge_states[peptide]):
            charges[charge_n] = 1

        if sequence in self.shitty_decoy_seqs:
            is_shitty = 1
        else:
            is_shitty = 0

        score_list = sorted(
            list(set(self.score_list_dict[spectrum])),
            reverse=self['bigger_scores_better']
        )

        try:
            score_list_scaled = scale_scores(score_list)
            rank = score_list.index(score)
            deltLCn = score_list_scaled[rank] - score_list_scaled[ 1]  # Fractional difference between current and second best XCorr
            deltCn  = score_list_scaled[rank] - score_list_scaled[-1]  # Fractional difference between current and worst XCorr
        except (ValueError, IndexError, AssertionError):
            # NaN values will be replaced by the column mean later
            # NaN values are entered when there is no ranking
            # e.g. when only one peptide was matched to the spectrum.
            rank, deltLCn, deltCn = np.nan, np.nan, np.nan

        features = [
            score,
            rank,
            deltCn,
            deltLCn,
            charge,
            #delta_mz,# / pep_len,
            delta_mass,# / pep_len,
            #abs(delta_mz),# / pep_len,
            abs(delta_mass),# / pep_len,
            n_missed_cleavages / pep_len,
            missed_cleavages[0],
            missed_cleavages[1],
            missed_cleavages[2],
            missed_cleavages[3],
            missed_cleavages[4],
            missed_cleavages[5],
            enzN,
            enzC,
            mass,
            pep_len,
            num_pep,
            num_prot,
            pep_site,  
            is_shitty,
            pep_charge_states,
            num_spec,
            seq_mods,
        ]

        for charge_n in self.observed_charges:
            features.append(charges[charge_n])

        return features + user_specified_features


    def collect_data(self):
        '''
        parses a unified csv file and collects features from each row
        '''
        categories = []
        list_of_feature_lists = []
        feature_sets = set()
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            # collecting some stats for FDR calculation:
            self.PSM_count   = 0
            self.decoy_count = 0

            if self['dump_svm_matrix']:
                self.init_svm_matrix_dump()
                additional_matrix_info = []

            for i, row in enumerate(
                sorted(reader, reverse=self['bigger_scores_better'],
                       key=lambda d: float(d[self.col_for_sorting])
                )):

                features = self.row_to_features(row)

                if tuple(features) in feature_sets:
                    continue
                feature_sets.add(tuple(features))

                category, psm_FDR = self.get_psm_category(row)

                list_of_feature_lists.append(features)
                categories.append(category)

                if self['dump_svm_matrix']:
                    label = -1 if row_is_decoy(row) else 1
                    sequence = '{0}.{1}#{2}.{3}'.format(
                        row['Sequence Pre AA'].strip(),
                        row['Sequence'].strip(),
                        row['Modifications'].strip(),
                        row['Sequence Post AA'].strip(),
                    )
                    additional_matrix_info.append({
                        'psm_id': row['Spectrum Title'].strip(),
                        'label': label,
                        'scannr': row['Spectrum Title'].strip().split('.')[-2],
                        'peptide': sequence,
                        'proteins': self.parse_protein_ids(row['Protein ID']),
                    })

                if i % 1000 == 0:
                    score_val = float(row[self.col_for_sorting])
                    msg = 'Generating feature matrix from input csv '\
                          '(line ~{0}) with score {1} and FDR '\
                          '{2}'.format(i, score_val, psm_FDR)
                    print(msg, end = '\r')


        # All data points are collected in one big matrix, to make standardization possible
        print('\nConverting feature matrix to NumPy array...')
        X_raw = np.array(list_of_feature_lists, dtype=float)

        print('Replacing empty/NaN values with the mean of each column...')
        self.nan_replacer = Imputer()
        self.nan_replacer.fit(X_raw)
        X_raw = self.nan_replacer.transform(X_raw)
        # Standardize input matrix to ease machine learning! Scaled data has zero mean and unit variance
        print('Standardizing input matrix...')
        self.scaler = SCALER.fit(X_raw)
        self.X = self.scaler.transform(X_raw)
        self.categories = np.array(categories)
        print()

        if self['dump_svm_matrix']:
            print('Dumping SVM matrix to', self['dump_svm_matrix'])
            
            for i, matrix_row in enumerate(self.X):
                matrix_row_info = additional_matrix_info[i]
                self.dump_svm_matrix_row(
                    row = list(matrix_row),
                    psm_id=matrix_row_info['psm_id'],
                    label=matrix_row_info['label'],
                    scannr=matrix_row_info['scannr'],
                    peptide=matrix_row_info['peptide'],
                    proteins=matrix_row_info['proteins'],
                )
            
            print('Dumped SVM matrix to', self['dump_svm_matrix'])
        return


    def init_svm_matrix_dump(self):
        from misc import FEATURE_NAMES
        colnames = ['PSMId', 'label', 'scannr'] + FEATURE_NAMES
        colnames += ["charge{0}".format(c) for c in self.observed_charges]
        for extra_field in sorted(self.used_extra_fields):
            colnames += [extra_field]
        colnames += ['peptide']
        for n_proteins in range(self.maximum_proteins_per_line):
            colnames.append('proteinId{0}'.format(n_proteins + 1))
        self.matrix_csv_path = self['dump_svm_matrix']
        print('Dumping raw SVM input matrix to', self.matrix_csv_path)
        with open(self.matrix_csv_path, 'w') as f:
            f.write('\t'.join(colnames) + '\n')
        

    def dump_svm_matrix_row(self, row=None, psm_id=None, label=None, scannr=None, peptide=None, proteins=None):
        full_row = [psm_id, label, scannr] + row + [peptide] + list(proteins)
        with open(self.matrix_csv_path, 'a') as f:
            row_str = '\t'.join(str(x) for x in full_row) + '\n'
            f.write(row_str)


    def get_psm_category(self, row):
        '''
        Determines whether a PSM (csv row) should be used as a negative or
        positive training example.

        returns
            1  - high-scoring target (positive training example)
            0  - not-high-scoring target (not usable for training)
           -1  - decoy (negative training example)
        
        '''
        category = 0  # unknown (mix of true positives and false positives)
        self.PSM_count += 1  # for FDR calculation
        sequence = unify_sequence(row['Sequence'])
        psm_FDR = calc_FDR(self.PSM_count, self.decoy_count)

        if row_is_decoy(row):
            self.decoy_count += 1
            if psm_FDR <= 0.25 and sequence not in self.shitty_decoy_seqs:
                category = -1  # decoy (false positive hits)
                self.counter['negative'] += 1
            else:
                if not self.decoy_train_prob:
                    need_max = self.counter['positive'] * 2
                    have = self.counter['negative']
                    still_there = self.counter['decoy'] - have
                    prob = need_max / still_there
                    if prob < 0.001:
                        prob = 0.001
                    self.decoy_train_prob = prob
                    print()
                    print(self.counter)
                    print('need max:', need_max)
                    print('have:', have)
                    print('still_there:', still_there)
                    print('probability:', self.decoy_train_prob)
                    print()
                if self.decoy_train_prob >= 1.0 or random() <= self.decoy_train_prob:
                    category = -1  # decoy (false positive hits)
                    self.counter['negative'] += 1

                

        else:  # row is target
            if psm_FDR <= self['fdr_cutoff'] and sequence not in self.shitty_decoy_seqs:
                category = 1  # high quality target (almost certainly true positives)
                self.counter['positive'] += 1

        if category == 0:
            self.counter['unknown'] += 1
        return (category, psm_FDR)


    def train(self, training_matrix, training_categories):
        counter = Counter(training_categories)
        msg = 'Training {0} SVM on {1} target PSMs and {2} decoy PSMs'\
        '...'.format(self['kernel'], counter[1], counter[-1])
        print(msg, end = '\r')
        # specify the classification method (rbf and linear SVC seem to work best and are quite fast)
        classifier = svm.SVC(
            C           = self['c'],
            kernel      = self['kernel'],
            probability = False,  # we don't want to get probabilities later on -> faster
            cache_size  = self['mb_ram'],  # available RAM in megabytes
            #decision_function_shape = 'ovr',  # doesn't seem to matter
            #class_weight= 'balanced',  # doesn't seem to matter
        )
        # train the SVC on our set of training data:
        classifier.fit(
            training_matrix,
            training_categories,
        )
        print(msg + ' done!')
        return classifier


    def classify(self, classifier, psm_matrix):
        msg = 'Classifying {0} PSMs...'.format(len(psm_matrix))
        print(msg, end = '\r')
        for i, row in enumerate(psm_matrix):
            # get the distance to the separating SVM hyperplane and use it as a score:
            svm_score = classifier.decision_function(np.array([row]))[0]

            features = tuple(row)
            if features not in self.results:
                self.results[features] = svm_score
            else:
                print(
                    'Warning! This combination of features already has a predicted probability! '\
                    'Previous svm_score: {0:f} - Current svm_score: {1:f}'\
                    ''.format( self.results[tuple(row)], svm_score )
                )
                # take the mean value, no idea how to handle this better, but it never happened so far...
                self.results[features] = (self.results[features] + svm_score) / 2.0
        print(msg + ' done!')
        return


    def add_scores_to_csv(self):
        outfname = os.path.basename(self['output_csv'])
        print('Writing output csv {0} ...'.format(outfname))
        msg = 'Writing output csv {0} (line ~{1})...'

        with open(self['output_csv'], 'w', newline='') as out_csv, open(self.csv_path, 'r') as in_csv:
            reader = csv.DictReader(in_csv)
            writer = csv.DictWriter(out_csv, reader.fieldnames + [self._svm_score_name])
            writer.writeheader()
            for i, row in enumerate(reader):
                if i % 1000 == 0:
                    print(msg.format(outfname, i), end='\r')
                features = self.nan_replacer.transform(
                    np.array([ self.row_to_features(row) ])
                )
                features_scaled = tuple(list(self.scaler.transform(features)[0]))
                SVMScore = self.results[features_scaled]
                row[self._svm_score_name] = SVMScore
                writer.writerow(row)
        print('\n')
        return


    def __str__(self):
        out_str = ['\n\tpyPercolator Options:']
        for option, value in self.items():
            out_str.append(
                '{0:·<25}{1}'.format(option, value)
            )
        return '\n'.join(out_str)



if __name__ == '__main__':
    s = SVMWrapper()

    print(s)  # print parameter/settings overview

    s.determine_csv_sorting()
    s.find_shitty_decoys()
    
    print('\nCounter:')
    print(s.counter)
    print()
    s.count_intra_set_features()
    s.collect_data()

    print('Splitting data in half to avoid training and testing on the same features...')
    skfold = StratifiedKFold(
        s.categories, n_folds = 2, shuffle = True
    )

    # use one half to score the other half, and vice versa:
    for i, (train_index, test_index) in enumerate(skfold):
        current_half = '1st' if i == 0 else '2nd'
        other_half = '2nd' if i == 0 else '1st'
        print('\nUsing high-scoring PSMs and decoys of the {0} half to train...'.format(current_half))
        mask = s.categories[train_index] != 0
        train_categories = s.categories[train_index][mask]
        train_features = s.X[train_index][mask]
        svm_classifier = s.train(
            training_matrix     = train_features,
            training_categories = train_categories,
        )


        print('Using the trained SVM to classify all PSMs of the {0} half'.format(other_half))
        s.classify(
            svm_classifier,
            s.X[test_index],
        )
        if s['kernel'].lower() == 'linear':
            print()  # print SVM coefficients (only works for linear kernel)
            print(svm_classifier.coef_)
            print()

    print('\nCounter:')
    print(s.counter)
    print()
    s.add_scores_to_csv()
