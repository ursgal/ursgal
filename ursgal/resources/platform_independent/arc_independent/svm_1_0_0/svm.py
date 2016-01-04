#!/usr/bin/python3.4

'''
    usage:
        svm.py unified_input.csv engine_score_column_name
    i.e. :
        svm.py omssa_2_1_6_unified.csv "OMSSA:pvalue"

    Writes a new file with added column "SVMProb" which is the
    estimated probability of a PSM to be false positive (in %), as estimated
    with a Percolator-like support vector machine.
'''


import numpy as np
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, Imputer
from collections import Counter, defaultdict
import csv
import sys
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '-i', '--input_csv', type=str, help='Input CSV name')
parser.add_argument(
    '-o', '--output_csv', type=str, help='Output CSV name')
parser.add_argument(
    '-k', '--kernel', type=str, default='rbf',
    help='SVM kernel type (i.e. linear or rbf)')
parser.add_argument(
    '-c', type=float, default=1.0, help='Penalty parameter C of the error term')
parser.add_argument(
    '-r', '--mb_ram', type=float, default=3000, help='Available RAM in megabytes, for SVM calculation')
parser.add_argument(
    '-f', '--fdr_cutoff', type=float, default=0.01, 
    help='Target PSMs with a lower FDR will be used as a positive training set')
parser.add_argument(
    '-s', '--sort_by', type=str, help='Score used for sorting (for FDR calculation)')
parser.add_argument(
    '-b', '--bigger_scores_better', action='store_true', help='Flag to define that bigger scores (for sorting) indicate higher quality')
parser.add_argument(
    '-x', '--columns_as_features', type=str, default=','.join([
        'MS-GF:RawScore',
        'MS-GF:DeNovoScore',
        'MS-GF:SpecEValue',
        'MS-GF:EValue',
        'OMSSA:evalue',
        'OMSSA:pvalue',
        'X\!Tandem:expect',
        'X\!Tandem:hyperscore',
    ]),
    help='Columns that should be used as a feature directly (e.g. secondary scores). Will be converted to float')

args = vars(parser.parse_args())  # convert to dict

IN_PATH = args['input_csv']
OUT_PATH = args['output_csv']
SCALER = RobustScaler()  # RobustScaler() seems to be most robust, duh
KERNEL = args['kernel']  # percolator uses linear kernel that yields good results at all possible FDR cutoffs.
           # rbf kernel seems to be better at low FDR cutoffs (around 0.01), but linear is better when using high cutoffs (i.e. 0.3)
C = args['c']  # this thing might do something important but I have no idea, 1 seems to be good
FDR_CUTOFF = args['fdr_cutoff']  # 0.01 works well (for humanBR omssa/xtandem/msgfplus results at least...)
COL_TO_SORT_BY = args['sort_by']  # the name of the column that should be used for sorting
BIGGER_SCORES_BETTER = args.get('bigger_scores_better', False)
ENGINE_SPECIFIC_FEATURES = args['columns_as_features'].split(',')
MB_RAM = args['mb_ram']

PROTON = 1.00727646677


class SVMWrapper():


    def __init__( self, unified_csv_path ):
        self.csv_path = unified_csv_path
        self.stats = {
           -1: [],
            0: [],
            1: [],
        }
        self.results  = {}
        self.shitty_decoy_seqs = set()  # is overwritten by find_shitty_decoys()
        return


    @staticmethod
    def unify_sequence(seq):
        '''
        Some sequences cannot be distinguished by MS (i.e. sequences
        where L is replaced by I and vice versa).
        Such target/decoy pairs are not suitable for training.
        This function applies rules to a sequence that allow identification
        of such target/decoy pairs,
        i.e.
            unify_sequence("EILE") == unify_sequence("ELLE")
            -> True
        '''
        # replace leucin with isoleucin cause they cant be distinguished:
        seq = seq.replace('L', 'I')
        # sort first 2 amino acids:
        if len(seq) >= 2:
            seq = "".join(sorted(seq[:2])) + seq[2:]
        return seq

    def find_shitty_decoys(self):
        target_seqs = set()
        decoy_seqs  = set()
        with open( self.csv_path, "r" ) as f:
            reader = csv.DictReader( f )
            for row in reader:
                if row["Is decoy"].lower() == "true" or "decoy_" in row["proteinacc_start_stop_pre_post_;"]:
                    decoy_seqs.add(self.unify_sequence(row["Sequence"]))
                else:
                    target_seqs.add(self.unify_sequence(row["Sequence"]))
        self.shitty_decoy_seqs = target_seqs.intersection(decoy_seqs)
        if len(self.shitty_decoy_seqs) > 0:
            print(
                "Warning! Found {0} sequences that are target AND decoy "\
                "(immutable peptides?)\n".format(len(self.shitty_decoy_seqs))
            )
        return


    def count_intra_set_features(self):
        '''
        intra-set features as calculated by Percolator:
        - num_pep:  Number of PSMs for which this is the best scoring peptide.
        - num_prot: Number of times the matched protein matches other PSMs.
        - pep_site: Number of different peptides that match this protein.
        '''
        self.num_pep  = defaultdict(int)
        self.num_prot = defaultdict(set)
        self.pep_site = defaultdict(set)
        self.score_list_dict = defaultdict(list)

        with open(self.csv_path, "r") as f:
            reader = csv.DictReader(f)
            previous_spec_title = None
            rows_of_spectrum = []
            for row in sorted(reader, key=lambda d: (d['Spectrum Title'], float(d[COL_TO_SORT_BY]))):
                if self.unify_sequence(row["Sequence"]) in self.shitty_decoy_seqs:
                    continue
                current_spec_title = row["Spectrum Title"]
                if current_spec_title != previous_spec_title:
                    # the next spectrum started, so let's process the info we
                    # collected for the previous spectrum:
                    score_list = [float(r[COL_TO_SORT_BY]) for r in rows_of_spectrum]
                    self.score_list_dict[previous_spec_title] = score_list

                    for rank, line in enumerate(rows_of_spectrum):
                        score = float(line[COL_TO_SORT_BY])
                        proteinacc = line["proteinacc_start_stop_pre_post_;"]
                        peptide = (line["Sequence"], line["Modifications"])
                        protein = proteinacc.replace('decoy_', '').split()[0]

                        if rank == 0:
                            # this is the "best" peptide for that spectrum
                            self.num_pep[peptide] += 1
                        self.num_prot[protein].add(
                            (line["Spectrum Title"], line["Sequence"], line["Modifications"])
                        )
                        self.pep_site[protein].add(peptide)

                    rows_of_spectrum = []

                rows_of_spectrum.append(row)
                previous_spec_title = current_spec_title


    @staticmethod
    def calc_FDR(PSM_count, false_positives):
        '''
        calculate false discovery rate according to FDR Method 2
        (Käll et al. 2008) as explained by Jones et al. 2009
        '''
        true_positives  = PSM_count - (2 * false_positives)
        if true_positives <= 0:  # prevent FDR above 1. Not sure if this is done?
            return 1.0
        FDR = false_positives / ( false_positives + true_positives)
        return FDR


    @staticmethod
    def scale_scores(l):
        # scales a list l to values from -1 to 1
        out_l = []
        assert len(l) > 1
        norm = max(l) - min(l)
        assert norm != 0
        for x in l:
            x_str = (x - min(l)) / norm
            out_l.append( (x_str * 2) -1 )
        return out_l


    def row_to_features(self, row):
        #mods = row["Modifications"]
        sequence = row["Sequence"]
        charge = float( row["Charge"] )
        score = float( row[ COL_TO_SORT_BY ] )
        calc_mz = float( row["Calc m/z"] )
        exp_mz = float( row["Exp m/z"] )

        proteinacc = row["proteinacc_start_stop_pre_post_;"].split("_")
        pre_aa = proteinacc[-2]
        post_aa = proteinacc[-1]
        if pre_aa in ['R', 'K', '-']:
            enzN = 1
        else:
            enzN = 0
        if sequence[-1] in ['R', 'K'] or post_aa == '-':
            enzC = 1
        else:
            enzC = 0

        n_missed_cleavages = len([aa for aa in sequence[:-1] if aa in ["R", "K"]])# / len(sequence)

        missed_cleavages = [0] * 11
        try:
            missed_cleavages[n_missed_cleavages] = 1
        except IndexError:  # if a peptide has more than 10 missed cleavages
            missed_cleavages[-1] = 1

        mass    = ( exp_mz * charge ) - ( charge - 1 ) * PROTON
        pep_len = len( sequence )
        abs_delta_mass = abs( calc_mz - exp_mz )
        delta_mass = calc_mz - exp_mz
        precursor_charge = float(row["Spectrum Title"].split(".")[-1])
        delta_charge = charge - precursor_charge

        peptide = (sequence, row["Modifications"])
        spectrum = row["Spectrum Title"]
        psm = (peptide, spectrum)
        protein = row["proteinacc_start_stop_pre_post_;"].replace('decoy_', '').split()[0]
        num_pep  = self.num_pep[peptide]
        num_prot = len(self.num_prot[protein])
        pep_site = len(self.pep_site[protein])

        engine_specific_features = []
        for feat in ENGINE_SPECIFIC_FEATURES:
            if feat in row and feat != COL_TO_SORT_BY:
                try:
                    engine_specific_features.append(float(row[feat]))
                except ValueError:
                    pass

        charges = [0] * 11
        for charge_n in range(11):
            if charge == charge_n:
                charges[charge_n] = 1

        if self.unify_sequence(sequence) in self.shitty_decoy_seqs:
            is_shitty = 1
        else:
            is_shitty = 0


        score_list = sorted(list(set(self.score_list_dict[spectrum])))

        try:
            score_list_scaled = self.scale_scores(score_list)
            rank = score_list.index(score)
            deltLCn = score_list_scaled[rank] - score_list_scaled[ 1]  # Fractional difference between current and second best XCorr
            deltCn  = score_list_scaled[rank] - score_list_scaled[-1]  # Fractional difference between current and worst XCorr
        except (ValueError, IndexError, AssertionError):
            # NaN values will be replaced by the column mean later
            rank, deltLCn, deltCn = np.nan, np.nan, np.nan


        features = [
            score,
            rank,
            deltCn,
            deltLCn,
            charge,
            #charges[1],
            #charges[2],
            #charges[3],
            #charges[4],
            #charges[5],
            #charges[6],
            #charges[7],
            #charges[8],
            #charges[9],
            #charges[10],
            delta_charge,
            abs_delta_mass,
            delta_mass,
            n_missed_cleavages,
            #missed_cleavages[0],
            #missed_cleavages[1],
            #missed_cleavages[2],
            #missed_cleavages[3],
            #missed_cleavages[4],
            #missed_cleavages[5],
            #missed_cleavages[6],
            #missed_cleavages[7],
            #missed_cleavages[8],
            #missed_cleavages[9],
            #missed_cleavages[10],
            enzN,
            enzC,
            mass,
            pep_len,
            num_pep,
            num_prot,
            pep_site,
            is_shitty,
        ]
        
        return tuple(features + engine_specific_features)


    def collect_data(self):
        '''
        parses a unified csv file and collects features from each row
        '''
        categories = []
        list_of_feature_lists = []
        feature_sets = set()
        with open( self.csv_path, "r" ) as f:
            reader = csv.DictReader( f )
            # collecting some stats for FDR calculation:
            PSM_count   = 0
            decoy_count = 0

            for i, row in enumerate(sorted(reader, key=lambda d: float(d[COL_TO_SORT_BY]), reverse=BIGGER_SCORES_BETTER)):

                if i % 1000 == 0:
                    msg = "Generating feature matrix from input csv (line ~{0})...".format(i)
                    print(msg, end = '\r')

                features = self.row_to_features(row)

                if features in feature_sets:
                    continue
                feature_sets.add(features)

                PSM_count += 1  # for FDR calculation
                # Positive and negative examples will be used for training
                if row["Is decoy"].lower() == "true" or "decoy_" in row["proteinacc_start_stop_pre_post_;"]:
                    if self.unify_sequence(row["Sequence"]) not in self.shitty_decoy_seqs:
                        category = -1  # decoy (false positive hits)
                    else:
                        category = 0
                    decoy_count += 1

                elif row["Is decoy"].lower() == "false":
                    # FDR calculation (for selecting positive training examples)
                    psm_FDR = self.calc_FDR(PSM_count, decoy_count)
                    if psm_FDR <= FDR_CUTOFF and self.unify_sequence(row["Sequence"]) not in self.shitty_decoy_seqs:
                        category = 1  # high quality target (almost certainly true positives)
                    else:
                        category = 0  # unknown (mix of true positives and false positives)
                list_of_feature_lists.append( features )
                categories.append( category )


        # All data points are collected in one big matrix, to make standardization possible
        X_raw = np.array( list_of_feature_lists )
        # Replace NaN values with the mean of each column:
        self.nan_replacer = Imputer()
        self.nan_replacer.fit(X_raw)
        X_raw = self.nan_replacer.transform(X_raw)
        # Standardize input matrix to ease machine learning! Scaled data has zero mean and unit variance
        self.scaler = SCALER.fit(X_raw)
        self.X = self.scaler.transform(X_raw)
        self.categories = np.array( categories )
        print()
        assert len(X_raw) == len({ tuple(row) for row in X_raw }), 'Rows are repeated :('
        return


    def train( self, training_matrix, training_categories ):
        counter = Counter(training_categories)
        msg = "Training {0} SVM on {1} target PSMs and {2} decoy PSMs"\
        "...".format(KERNEL, counter[1], counter[-1])
        print(msg, end = '\r')
        # specify the classification method (rbf and linear SVC seem to work best and are quite fast)
        classifier = svm.SVC(
            C           = C,
            kernel      = KERNEL,
            probability = True,  # we want to get probabilities later on
            cache_size  = MB_RAM,  # available RAM in megabytes
            #decision_function_shape = 'ovr',  # doesn't seem to matter
            #class_weight= "balanced",  # doesn't seem to matter
        )
        # train the SVC on our set of training data:
        classifier.fit(
            training_matrix,
            training_categories,
        )
        print(msg + " done!")
        return classifier


    def classify(self, classifier, psm_matrix, psm_categories):
        msg = "Classifying {0} PSMs...".format(len(psm_matrix))
        print(msg, end = '\r')
        for i, row in enumerate(psm_matrix):
            prob = classifier.predict_proba(np.array([row]))[0][0]*100  # multiply by 100 to get longer floats?

            category = psm_categories[i]
            self.stats[category].append(prob)

            features = tuple(row)
            if features not in self.results:
                self.results[features] = prob
            else:
                print(
                    "Warning! This combination of features already has a predicted probability! "\
                    "Previous prob: {0:f} - Current prob: {1:f}"\
                    "".format( self.results[tuple(row)], prob )
                )
                # take the mean value, no idea how to handle this better, but it happens super rarely anyways...
                self.results[features] = (self.results[features] + prob)/2.0
        print(msg + ' done!')
        return


    def add_scores_to_csv(self, out_path):
        msg = 'Writing output csv {0} (line ~{1})...'

        with open(out_path, 'w', newline='') as out_csv, open(self.csv_path, 'r') as in_csv:
            reader = csv.DictReader(in_csv)
            writer = csv.DictWriter(out_csv, reader.fieldnames + ["SVMProb"])
            writer.writeheader()
            for i, row in enumerate(reader):
                if i % 1000 == 0:
                    print(msg.format(os.path.basename(out_path), i), end='\r')
                features = self.nan_replacer.transform( np.array([ self.row_to_features(row) ]) )
                features_scaled = tuple(list(self.scaler.transform(features)[0]))
                SVMProb = self.results[features_scaled]
                #if SVMProb >= 0.05:
                    #continue
                row["SVMProb"] = SVMProb
                writer.writerow(row)
        print("\n")
        return



if __name__ == "__main__":
    s = SVMWrapper(IN_PATH)

    print('''
        
        using these params:
        
IN_PATH: {0}
OUT_PATH: {1}
KERNEL: {2}
C: {3}
FDR_CUTOFF: {4}
COL_TO_SORT_BY: {5}
BIGGER_SCORES_BETTER: {6}
ENGINE_SPECIFIC_FEATURES: {7}
MB_RAM: {8}

    '''.format(
        IN_PATH, OUT_PATH, KERNEL, C, FDR_CUTOFF, COL_TO_SORT_BY, BIGGER_SCORES_BETTER, ENGINE_SPECIFIC_FEATURES, MB_RAM
        )
    )

    s.find_shitty_decoys()
    s.count_intra_set_features()
    s.collect_data()

    print('Splitting data in half to avoid training and testing on the same features...')
    skfold = StratifiedKFold(
        s.categories, n_folds = 2, shuffle = True
    )

    # use one half to score the other half, and vice versa:
    for i, (train_index, test_index) in enumerate(skfold):
        current_half = "1st" if i == 0 else "2nd"
        other_half = "2nd" if i == 0 else "1st"
        print("\nUsing high-scoring PSMs and decoys of the {0} half to train...".format(current_half))
        mask = s.categories[train_index] != 0
        train_categories = s.categories[train_index][mask]
        train_features = s.X[train_index][mask]
        svm_classifier = s.train(
            training_matrix     = train_features,
            training_categories = train_categories,
        )
        print("Using the trained SVM to classify all PSMs of the {0} half".format(other_half))
        s.classify(
            svm_classifier,
            s.X[test_index],
            s.categories[test_index]
        )
    s.add_scores_to_csv(OUT_PATH)
