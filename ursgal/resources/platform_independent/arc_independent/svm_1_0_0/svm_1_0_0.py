#!/usr/bin/python3.4

'''
    usage:
        svm.py unified_input.csv engine_score_column_name
    i.e. :
        svm.py omssa_2_1_6_unified.csv 'OMSSA:pvalue'

    Writes a new file with added column self._prob_name which is the
    estimated probability of a PSM to be false positive (in %), as estimated
    with a Percolator-like support vector machine.
'''
from pprint import pprint

import numpy as np
import sklearn
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import Imputer
from collections import Counter, defaultdict
from random import random
from pymzml.spec import Spectrum
import csv
import sys
import os
import argparse
#import PeptideFragmentor
#import ursgal
import time
import itertools
import shelve

from misc import get_score_colname_and_order, field_to_float, naive_bayes, unify_sequence, calc_FDR, scale_scores, row_is_decoy, count_ion_partners, field_to_bayes_float, get_mz_values, hash_input_filenames





#IN_PATH = args['input_csv']
#if len(IN_PATH) == 1:
    #MULTI_MODE = False
#else:
    #MULTI_MODE = True
#OUT_PATH = args['output_csv']
#KERNEL = args['kernel']  # percolator uses linear kernel that yields good results at all possible FDR cutoffs.
           ## rbf kernel seems to be better at low FDR cutoffs (around 0.01), but linear is better when using high cutoffs (i.e. 0.3)
#C = args['c']  # this thing might do something important but I have no idea, 1 seems to be good
#self['fdr_cutoff'] = args['self['fdr_cutoff']']  # 0.01 works well (for humanBR omssa/xtandem/msgfplus results at least...)
#self['bigger_scores_better'] = args.get('self['bigger_scores_better']', False)
#self['columns_as_features'] = args['columns_as_features']
#self['mb_ram'] = args['self['mb_ram']']



SCALER = sklearn.preprocessing.RobustScaler()  # RobustScaler() seems to be most robust, duh
PROTON = 1.00727646677


class SVMWrapper(dict):


    def __init__(self):
        self._prob_name = 'SVMProb'
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
        #self._chemical_composition = ursgal.ChemicalComposition()

        if __name__ == '__main__':
            self.parse_options()  # parse command line args and set options
            self.set_input_csv()  # either single csv, or in case of multiple
                              # input files, a merged csv is generated

        self.observed_charges = set()
        self.used_extra_fields = set()
        self.decoy_train_prob = None  # probability to include decoy PSMs as negative training examples
        self.maximum_proteins_per_line = 0

        if self.get('count_frag_ions', False):
            frag_ion_shelve_dir = os.path.dirname(os.path.realpath(__file__))
            frag_ion_shelve_path = os.path.join(
                frag_ion_shelve_dir,
                hash_input_filenames(self['count_frag_ions']) + '.shelve'
            )
            print('Opening frag ion shelve', frag_ion_shelve_path)
            self.frag_ion_shelve = shelve.open(frag_ion_shelve_path, writeback=True)
            #self.frag_ion_shelve = {}
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
            help='Penalty parameter C of the error term')
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
        #parser.add_argument(
        #    '-cf', '--count_frag_ions', type=str, nargs='+', required=False,
        #    help='Compare theoretical and observed fragment ions and derived '\
        #         'features. Requires specification of one of more MGF files.')
        parser.add_argument(
            '-d', '--dump_svm_matrix', type=str, default=False,
            help='Dump SVM matrix in PIN format to the specified path.')

        arg_dict = vars(parser.parse_args())  # convert to dict
        self.update(arg_dict)
        if len(self['input_csv']) == 1:
            self['multi_mode'] = False
        else:
            self['multi_mode'] = True
        try:
            self['gamma'] = float(self['gamma'])
        except ValueError:
            assert self['gamma'] == 'auto', 'Invalid gamma param: '\
                '{0}'.format(self['gamma'])


    def set_input_csv(self):
        '''
        distinguishes one vs. many unified input csv files and either
        sets the single csv as input, or merges all csvs and sets
        the merged csv as input.
        '''
        if self['multi_mode']:
            from merge_unified_csvs import main as merge_unified_csvs
            print('Merging unified CSVs from multiple engines...')

            features_that_define_unique_psms = \
                ['Sequence', 'Modifications', 'Spectrum Title', 'Is decoy']  #'Charge'?

            fname, ext = os.path.splitext(self['output_csv'])
            merged_out_path = fname + '_mergedSVMcsv' + ext

            self.csv_path = merge_unified_csvs(
                empty_value='', input_csvs=self['input_csv'],
                output_csv=merged_out_path, input_sep=',', 
                join_sep=';', join_sep2=';', output_sep=',',
                columns_for_grouping=features_that_define_unique_psms,
                estimate_fdr=True, float_precision=10, fdr_cutoff=0.8
            )
            print('Generated merged unified CSV file at', self.csv_path)
        else:
            self.csv_path = self['input_csv'][0]
            print('Using single input file', self.csv_path)


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
                key=lambda d: naive_bayes(
                    [float(s) for s in d[self.col_for_sorting].split(';')]
                )
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


    def buffer_mgf(self, mgf_path, precision=10e-5):  #10e-6
        self.mgf_precision = precision
        print('Buffering MGF file {0} (precision: {1})'.format(mgf_path, precision))
        with open(mgf_path, 'r') as mgf:
            for line in mgf:
                if line.startswith('TITLE='):
                    peak_list = []
                    #spec_id = int(line.strip().split('.')[-2])
                    spec_id = line.strip().split('=')[-1]
                    #spec_id_2 = int(line.strip().split('.')[-3])
                    #assert spec_id == spec_id_2, 'MGF specID1 != specID2: ' + spec_id + ' & ' + spec_id_2
                elif 'END IONS' in line:
                    #self.mgf_lookup[spec_id] = pymzml.spec.Spectrum(measuredPrecision=precision)
                    #self.mgf_lookup[spec_id].peaks = peak_list
                    self.mgf_lookup[spec_id] = peak_list
                else:
                    try:
                        mz, intensity = [float(val) for val in line.split()]
                    except ValueError:
                        continue
                    peak_list.append(
                        (mz, intensity)
                    )
                    
    

    def predict_ions(self, peptide):
        if peptide in self.pep_to_mz:
            # read peptide from buffer, if previously calculated
            ions_to_mz = self.pep_to_mz[peptide]
        else:
            ions_to_mz = defaultdict(set)
            frags = PeptideFragmentor.the_all_new_pf(
                peptide, cc_factory=self._chemical_composition
            )
            for ion_type_subdict in frags.values():
                for ion_subdict in ion_type_subdict.values():
                    try:
                        ion_letter = ion_subdict['type']
                        ion_pos = str(ion_subdict['pos'])
                        ion_type = ion_letter + ion_pos
                    except KeyError:
                        continue
                    ions_to_mz[ion_type].add(ion_subdict['mz'])
            self.pep_to_mz[peptide] = ions_to_mz
        return ions_to_mz

    '''
    # same as above, but using the old PeptideFragmentor
    # it's faster, but cannot handle UniMod
    def predict_ions(self, peptide):
        if peptide in self.pep_to_mz:
            ions_to_mz = self.pep_to_mz[peptide]
        else:
            ions_to_mz = defaultdict(set)
            frags = PeptideFragmentor.PeptideFragmentator(
                peptide.split("#")[0]
            )[0]
            for ion_name, theoretical_mz in frags.items():
                ion_letter = ion_name[0]
                ions_to_mz[ion_letter].add(theoretical_mz[0])
            self.pep_to_mz[peptide] = ions_to_mz
        return ions_to_mz
    '''

    '''
    def __OLD_match_frag_ions(self, peptide, spec_id):
        theoretical_ions = self.predict_ions(peptide)
        observed_peaks = self.mgf_lookup[spec_id]
        observed_spec = Spectrum(measuredPrecision=self.mgf_precision)
        observed_spec.peaks = observed_peaks

        ion_stats = {'a': [0, 0], 'b': [0, 0], 'y': [0, 0], 'MH': [0, 0]}

        for ion_letter, possible_mzs in theoretical_ions.items():
            for mz in possible_mzs:

                ion_found = bool(observed_spec.hasPeak(mz)) #  using pymzml

                ion_stats[ion_letter][1] += 1
                if ion_found:
                    ion_stats[ion_letter][0] += 1
        return ion_stats
    '''


    def match_frag_ions(self, peptide, spec_id):
        psm_str = '&'.join([peptide, str(spec_id)])  # for shelving
        if psm_str in self.frag_ion_shelve:
            # load frag-ion-match from shelve if it's already there
            matched_ions, max_i = self.frag_ion_shelve[psm_str]
        else:
            # compute frag-ion-match if not found in shelve:
            theoretical_ions = self.predict_ions(peptide)
            observed_peaks = self.mgf_lookup[spec_id]
            observed_spec = Spectrum(measuredPrecision=self.mgf_precision)
            observed_spec.peaks = observed_peaks

            max_i = sum(observed_spec.i)
            matched_ions = {}

            for ion_type, theoretical_mzs in theoretical_ions.items():
                matched_ions[ion_type] = []
                for theo_mz in theoretical_mzs:

                    observed_mz_int = observed_spec.hasPeak(theo_mz)  #  using pymzml
                    if observed_mz_int:  # if the peak was found
                        matched_ions[ion_type].append(observed_mz_int[0][1])

            # dump frag-ion-match to shelve:
            self.frag_ion_shelve[psm_str] = (matched_ions, max_i)
        return matched_ions, max_i

    '''
    def has_peak(self, theoretical_mz, observed_spec_dict):
        intensity = Nonect
        accepted_mz_values_within_error = \
            self.get_surrounding_transformed_mz_set(theoretical_mz)
        for theo_t_mz in accepted_mz_values_within_error:
            if theo_t_mz in observed_spec_dict:
                intensity = observed_spec_dict[theo_t_mz]
                break
        return intensity
    '''

    def determine_csv_sorting(self):
        if self.get('multi_mode', False):
            self['bigger_scores_better'] = False
            self.col_for_sorting = 'estimated_FDR'
        else:
            with open(self.csv_path, 'r') as in_file:
                reader = csv.DictReader(in_file)
                self.col_for_sorting, self['bigger_scores_better'] = \
                    get_score_colname_and_order(reader.fieldnames)
            if self.col_for_sorting == self._prob_name:
                self._prob_name = self._prob_name + '2'

        print('CSV will be sorted by column {0} (reverse={1}'\
              ')'.format(self.col_for_sorting, self['bigger_scores_better']))

        for feat in self['columns_as_features']:
            if feat in reader.fieldnames and feat != self.col_for_sorting:
                self.used_extra_fields.add(feat)


    def sort_by_rank(self, rowdict):
        score = naive_bayes(
            [float(s) for s in rowdict[self.col_for_sorting].split(';')]
        )
        spec_title = rowdict['Spectrum Title']
        return (spec_title, score)


    ''' possibly not required with the new unified CSV format
    @staticmethod
    def parse_protein_ids(acc):
        # Turns the unified CSV column "Protein ID" into
        # the protein accession.
        acc_clean = acc.replace('decoy_', '').strip()
        #if '<|>' in acc:
        sep = '<|>'
        #else:
            #sep = ';'  # backwards compatability
        accessions = acc_clean.split(sep)
        # remove the _start_stop_pre_post; because it's not part of the proteinID:
        protein_IDs = set()
        for a in accessions:
            pid = []
            for e in a.split('_'):
                if len(e.strip()) <=1:
                    continue
                try:
                    __ = float(e)
                except ValueError:
                    pid.append(e)
            protein_IDs.add(''.join(pid))
        protein_IDs.discard('')
        assert len(protein_IDs) >= 1, 'Could not determine protein IDs: {0}'.format(acc)
        return protein_IDs
    '''


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
                        score = field_to_bayes_float(line[self.col_for_sorting])
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
        mods = row['Modifications']
        sequence = unify_sequence(row['Sequence'])
        charge = field_to_float( row['Charge'] )
        score = field_to_bayes_float( row[self.col_for_sorting] )
        calc_mz, exp_mz, calc_mass, exp_mass = get_mz_values(row)
        #calc_mz = field_to_float( row['Calc m/z'] )  # calc m/z or uCalc?
        #exp_mz = field_to_float( row['Exp m/z'] )

        proteinacc = row['proteinacc_start_stop_pre_post_;'].split('_')
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

        n_missed_cleavages = len([aa for aa in sequence[:-1] if aa in ['R', 'K']])# / len(sequence)

        missed_cleavages = [0] * 6
        try:
            missed_cleavages[n_missed_cleavages] = 1
        except IndexError:  # if a peptide has more than 10 missed cleavages
            missed_cleavages[-1] = 2

        spectrum = row['Spectrum Title'].strip()
        mass = (exp_mz * charge) - (charge - 1) * PROTON
        pep_len = len(sequence)
        delta_mz = calc_mz - exp_mz
        delta_mass = calc_mass - exp_mass

        peptide = (sequence, row['Modifications'])
        psm = (peptide, spectrum)
        proteins = self.parse_protein_ids(
            row['proteinacc_start_stop_pre_post_;']
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
        #print('num_prot: {0}, pep_site: {1}, #prot: {2}'.format(
                #num_prot, pep_site, len(proteins)
            #)
        #)

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

        ion_features = []
        if self['count_frag_ions']:
            # time estimation:
            if not hasattr(self, 'start_time'):
                self.start_time = time.time()
                elapsed_time = 'N/A'
                psms_per_sec = 0
            else:
                elapsed_time = time.time() - self.start_time
                psms_per_sec = self.counter['parsed PSMs'] / elapsed_time
            self.counter['parsed PSMs'] += 1

            matched_ions, max_i = self.match_frag_ions(
                peptide='#'.join(peptide),
                spec_id=spectrum,
            )
            # sum up all the matched ion intensities:
            explained_i = sum(itertools.chain(*list(matched_ions.values())))
            i_ratio = explained_i / max_i
            ion_features.append(i_ratio)

            ion_features.append(
                count_ion_partners(matched_ions, pep_len) / pep_len
            )

            ion_dict = {}
            for ion_letter in ('a', 'b', 'y', 'M', 'all'):
                ion_dict[ion_letter] = {
                    'count': 0,
                    'total': 0,
                }

            for ion_type, intensities in matched_ions.items():
                ion_letter = ion_type[0]
                ion_dict[ion_letter]['total'] += 1
                ion_dict['all']['total'] += 1
                if intensities:
                    ion_dict[ion_letter]['count'] += 1
                    ion_dict['all']['count'] += 1

            for ion_letter in ('a', 'b', 'y', 'M', 'all'):
                try:
                    ion_dict[ion_letter]['ratio'] = \
                        ion_dict[ion_letter]['count'] / ion_dict[ion_letter]['total']
                except ZeroDivisionError:
                    ion_dict[ion_letter]['ratio'] = np.nan

                #ion_features.append(ion_dict[ion_letter]['count'])
                ion_features.append(ion_dict[ion_letter]['ratio'])

            #if self.counter['parsed PSMs'] % 1000 == 0:
                #ion_stat_str = '''PSM {psm_n} of {psm_total} ({psm_per_s:.3f} per second):

#Explained intensity: {i_ratio:.3f}% ({i_x:.3f} of {i_t:.3f})
#Matched ions:
    #a-ions:  {d[a][ratio]:.3f} ({d[a][count]: >3} of {d[a][total]: >3})
    #b-ions:  {d[b][ratio]:.3f} ({d[b][count]: >3} of {d[b][total]: >3})
    #y-ions:  {d[y][ratio]:.3f} ({d[y][count]: >3} of {d[y][total]: >3})
    #MH-ions: {d[M][ratio]:.3f} ({d[M][count]: >3} of {d[M][total]: >3})
#all ions:    {d[all][ratio]:.3f} ({d[all][count]: >3} of {d[all][total]: >3})
                #'''.format(
                    #i_ratio=i_ratio, i_t=max_i, i_x=explained_i,
                    #d=ion_dict, psm_n=self.counter['parsed PSMs'],
                    #psm_total=self.counter['target'] + self.counter['decoy'],
                    #psm_per_s=psms_per_sec
                #)
                #print(ion_stat_str)

        return features + ion_features + user_specified_features


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
                       key=lambda d: naive_bayes(
                           [float(s) for s in d[self.col_for_sorting].split(';')]
                ))):

                features = self.row_to_features(row)

                if tuple(features) in feature_sets:
                    continue
                feature_sets.add(tuple(features))

                category, psm_FDR = self.get_psm_category(row)

                list_of_feature_lists.append(features)
                categories.append(category)

                if self['dump_svm_matrix']:
                    label = -1 if row_is_decoy(row) else 1
                    splitted = row['proteinacc_start_stop_pre_post_;'].strip().split('_')
                    pre_aa = splitted[-2]
                    post_aa = splitted[-1]
                    sequence = '{0}.{1}#{2}.{3}'.format(
                        pre_aa,
                        row['Sequence'].strip(),
                        row['Modifications'].strip(),
                        post_aa,
                    )
                    additional_matrix_info.append({
                        'psm_id': row['Spectrum Title'].strip(),
                        'label': label,
                        'scannr': row['Spectrum Title'].strip().split('.')[-2],
                        'peptide': sequence,
                        'proteins': self.parse_protein_ids(row['proteinacc_start_stop_pre_post_;']),
                    })

                if i % 1000 == 0:
                    score_val = naive_bayes(
                        [float(s) for s in row[self.col_for_sorting].split(';')]
                    )
                    msg = 'Generating feature matrix from input csv '\
                          '(line ~{0}) with score {1} and FDR '\
                          '{2}'.format(i, score_val, psm_FDR)
                    #msg = 'Generating feature matrix from input csv (line ~{0})...'.format(i)
                    print(msg, end = '\r')
                    #print(msg)


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
        if self['count_frag_ions']:
            colnames += ["i_ratio", "a_ratio", "b_ratio", "y_ratio", "MH_ratio"]
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
            probability = True,  # we want to get probabilities later on
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


    def classify(self, classifier, psm_matrix, psm_categories):
        msg = 'Classifying {0} PSMs...'.format(len(psm_matrix))
        print(msg, end = '\r')
        for i, row in enumerate(psm_matrix):
            prob = classifier.predict_proba(np.array([row]))[0][0]*100  # multiply by 100 to get longer floats?

            category = psm_categories[i]

            features = tuple(row)
            if features not in self.results:
                self.results[features] = prob
            else:
                print(
                    'Warning! This combination of features already has a predicted probability! '\
                    'Previous prob: {0:f} - Current prob: {1:f}'\
                    ''.format( self.results[tuple(row)], prob )
                )
                # take the mean value, no idea how to handle this better, but it happens super rarely anyways...
                self.results[features] = (self.results[features] + prob)/2.0
        print(msg + ' done!')
        return


    def add_scores_to_csv(self):
        msg = 'Writing output csv {0} (line ~{1})...'

        with open(self['output_csv'], 'w', newline='') as out_csv, open(self.csv_path, 'r') as in_csv:
            reader = csv.DictReader(in_csv)
            writer = csv.DictWriter(out_csv, reader.fieldnames + [self._prob_name])
            writer.writeheader()
            for i, row in enumerate(reader):
                if i % 1000 == 0:
                    print(msg.format(os.path.basename(self['output_csv']), i), end='\r')
                features = self.nan_replacer.transform( np.array([ self.row_to_features(row) ]) )
                features_scaled = tuple(list(self.scaler.transform(features)[0]))
                SVMProb = self.results[features_scaled]
                #if SVMProb >= 0.05:  # filtering output csv
                    #continue
                row[self._prob_name] = SVMProb
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

    #MGF_PATH = '/media/plan-f/mzML/Lukas_Kremer/pypercolator_testing/humanBR/120813OTc1_NQL-AU-0314-LFQ-LCM-SG-02_025.mgf'
    #MGF_PATH = '/media/plan-f/mzML/Lukas_Kremer/pypercolator_testing/technical_rep1/qExactive00189.mgf'

    s = SVMWrapper()

    print(s)  # print parameter/settings overview

    if s.get('count_frag_ions', False):
        for mgf_path in s['count_frag_ions']:
            s.buffer_mgf(mgf_path)

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
            s.categories[test_index]
        )
        if s['kernel'].lower() == 'linear':
            print()
            print(svm_classifier.coef_)
            print()

    print('\nCounter:')
    print(s.counter)
    print()
    s.add_scores_to_csv()
