#!/usr/bin/env python
'''
collection of misc. functions and data that is imported into svm.py
'''
import numpy as np
import functools
import operator
import hashlib
import os


COLUMNS_TO_BE_REMOVED_FROM_MERGED_CSV = set([
    'Start',
    'Stop',
    'gi',
    'NIST score',
    'PSM_ID',
    'Pass Threshold',
    'Raw data location',
    'number of matched peaks',
    'number of unmatched peaks',
    'rank',
    'Rank',
    'Accession',
    'Filename',
])


FEATURE_NAMES = [
    "score",
    "rank",
    "deltCn",
    "deltLCn",
    "charge",
    "delta_mass",
    "abs_delta_mass",
    "n_missed_cleavages",
    "missed_cleavages[0]",
    "missed_cleavages[1]",
    "missed_cleavages[2]",
    "missed_cleavages[3]",
    "missed_cleavages[4]",
    "missed_cleavages[5]",
    "enzN",
    "enzC",
    "mass",
    "pep_len",
    "num_pep",
    "num_prot",
    "pep_site",  
    "is_shitty",
    "pep_charge_states",
    "num_spec",
    "seq_mods",
    #"i_ratio",
    #"a_ratio",
    #"b_ratio",
    #"y_ratio",
    #"MH_ratio",
    #"OMSSA:evalue",
]


def naive_bayes(prob_list):
    '''
    Combines independent probabilities a, b, c
    like this:

                            a*b*c
    combined_prob = -------------------------
                    a*b*c + (1-a)*(1-b)*(1-c)

    For a straightforward explanation, see
    http://www.paulgraham.com/naivebayes.html
    '''
    # multiplying all probabilities: a*b*c
    multiplied_probs = \
        functools.reduce(operator.mul, prob_list, 1)
    # multiplying the opposite of all probabilities: (1-a)*(1-b)*(1-c)
    multiplied_opposite_probs = \
        functools.reduce(operator.mul, (1-p for p in prob_list), 1)
    return multiplied_probs / (multiplied_probs + multiplied_opposite_probs)


def field_to_float(field):
    '''
    Converts the value of a field to float.
    If the field contains multiple separated floats,
    the mean is returned instead. If the field is empty,
    numpy.NaN is returned.
    '''
    try:
        result = float(field)
    except ValueError:
        if field == '':
            result = np.NaN
        elif ';' in field:
            values = [float(v) for v in field.split(';')]
            result = sum(values) / len(values)
        else:
            raise Exception(
                'Field value {0} cannot be converted to float.'.format(field)
            )
    return float(result)


def field_to_bayes_float(field):
    '''
    Converts the value of a field to float.
    If the field contains multiple separated floats,
    the naive Bayes combined value is returned instead.
    If the field is empty, numpy.NaN is returned.
    '''
    try:
        result = float(field)
    except ValueError:
        if field == '':
            result = np.NaN
        elif ';' in field:
            values = [float(v) for v in field.split(';')]
            result = naive_bayes(values)
        else:
            raise Exception(
                'Field value {0} cannot be converted to float.'.format(field)
            )
    return float(result)


def get_score_colname_and_order(colnames):
    '''
    Searches CSV headers for known score columns.
    '''
    known_scores = [
        # score_colname, bigger_scores_better
        ('estimated_FDR', False),
        ('SVMProb', False),
        ('OMSSA:pvalue', False),
        ('X\!Tandem:expect', False),
        ('MS-GF:SpecEValue', False),
        ('MyriMatch:MVH', True),
        ('Amanda:Score', True),
    ]
    for score, bsb in known_scores:
        if score in colnames:
            score_colname = score
            bigger_scores_better = bsb
            break
    else:
        raise Exception('Could not find a valid score field '\
            'for FDR estimation in file', input_csv)
    return score_colname, bigger_scores_better


def calc_FDR(PSM_count, false_positives):
    '''
    calculate false discovery rate according to FDR Method 2
    (Käll et al. 2007) as explained by Jones et al. 2009
    '''
    true_positives  = PSM_count - (2 * false_positives)
    if true_positives <= 0:  # prevent FDR above 1. Not sure if this is done?
        return 1.0
    FDR = false_positives / (false_positives + true_positives)
    return FDR


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


def unify_sequence(seq):
    '''
    Some sequences cannot be distinguished by MS (i.e. sequences
    where L is replaced by I and vice versa).
    Such target/decoy pairs are not suitable for training.
    This function applies rules to a sequence that allow identification 
    of such target/decoy pairs,
    i.e.
        unify_sequence('EILE') == unify_sequence('ELLE')
        -> True
    '''
    # replace leucin with isoleucin cause they cant be distinguished:
    seq = seq.replace('L', 'I')
    # sort first 2 amino acids:
    if len(seq) >= 2:
        seq = ''.join(sorted(seq[:2])) + seq[2:]
    return seq


def row_is_decoy(row):
    if row['Is decoy'].lower() == 'true':
        is_decoy = True
    elif row['Is decoy'].lower() == 'false':
        is_decoy = False
    else:
        raise Exception('Could not determine whether PSM is decoy or not.')
    if 'decoy_' in row.get('proteinacc_start_stop_pre_post_;', ''):
        is_decoy = True
    return is_decoy


def get_mz_values(row):
    calc_mz = field_to_float(row['Calc m/z'])
    exp_mz = field_to_float(row['Exp m/z'])
    ucalc_mz = field_to_float(row['uCalc m/z'])
    charge = field_to_float(row['Charge'])
    if int(round(exp_mz/ucalc_mz, 0)) == charge:
        # OMSSA returns masses instead of m/z values for some reason
        # dividing by charge to correct this
        calc_mass = calc_mz
        exp_mass = exp_mz
        calc_mz /= charge
        exp_mz /= charge
    else:  # no correction required, just computing the masses
        calc_mass = calc_mz * charge
        exp_mass = exp_mz * charge
    return calc_mz, exp_mz, calc_mass, exp_mass


def count_ion_partners(ion_d, pep_len, print_it=False):
    score = 0
    if print_it:
        print('\n ion partners:')
    for i in range(pep_len-2):
        y_ion = 'y' + str(i+1)
        a_ion = 'a' + str(pep_len-i-1)
        b_ion = 'b' + str(pep_len-i-1)

        ions = (y_ion, a_ion, b_ion)
        row_score = sum( int(bool(ion_d[i])) for i in ions ) ** 2
        score += row_score

        if print_it:
            print(int(bool(ion_d[y_ion])), int(bool(ion_d[a_ion])), int(bool(ion_d[b_ion])), ' - ', y_ion, a_ion, b_ion, row_score)
    return score


def hash_input_filenames(fname_list):
    fnames = ''.join([os.path.basename(f) for f in fname_list]).encode()
    hash_object = hashlib.md5(fnames)
    return hash_object.hexdigest()


if __name__ == '__main__':
    print('only for importing :)')
