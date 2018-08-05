import unify_csv_2_0_0
import os
import pickle


mods = {'fix': [{'_id': 1, 'aa': 'C', 'mass': 57.021464, 'pos': 'any', 'name': 'Carbamidomethyl', 'composition': {'H': 3, 'C': 2, 'N': 1, 'O': 1}, 'org': 'C,fix,any,Carbamidomethyl', 'id': '4', 'unimod': True}], 'opt': [{'_id': 0, 'aa': '*', 'mass': 42.010565, 'pos': 'Prot-N-term', 'name': 'Acetyl', 'composition': {'H': 2, 'C': 2, 'O': 1}, 'org': '*,opt,Prot-N-term,Acetyl', 'id': '1', 'unimod': True}, {'_id': 2, 'aa': 'K', 'mass': 6.013809, 'pos': 'any', 'name': 'Label:13C(5)15N(1)', 'composition': {'C': -5, '13C': 5, 'N': -1, '15N': 1}, 'org': 'K,opt,any,Label:13C(5)15N(1)', 'id': '268', 'unimod': True}, {'_id': 3, 'aa': 'K', 'mass': 8.014199, 'pos': 'any', 'name': 'Label:13C(6)15N(2)', 'composition': {'C': -6, '13C': 6, 'N': -2, '15N': 2}, 'org': 'K,opt,any,Label:13C(6)15N(2)', 'id': '259', 'unimod': True}, {'_id': 4, 'aa': 'M', 'mass': 15.994915, 'pos': 'any', 'name': 'Oxidation', 'composition': {'O': 1}, 'org': 'M,opt,any,Oxidation', 'id': '35', 'unimod': True}]}

input_csv = os.path.join(
    'tests',
    'data',
    'omssa_2_1_9',
    'test_BSA1_omssa_2_1_9.csv'
)
output_csv = os.path.join(
    'tests',
    'data',
    'omssa_2_1_9',
    'test_BSA1_omssa_2_1_9_unified.csv'
)
scan_rt_lookup = pickle.load(
    open(
        os.path.join(
            'tests',
            'data',
            '_test_ursgal_lookup.pkl'
        )
        ,
        'rb'
    )
)

unify_csv_2_0_0.main(
    input_file     = input_csv,
    output_file    = output_csv,
    scan_rt_lookup = scan_rt_lookup,
    params = {
        'translations' : {
            'decoy_tag': 'decoy_',
            'enzyme' : 'KR;C;P',
            'semi_enzyme' : False,
            'database': os.path.join( 'tests', 'data', 'BSA.fasta'),
            'protein_delimiter' : '<|>',
            'psm_merge_delimiter' : ';',
            'keep_asp_pro_broken_peps':True,
            'precursor_mass_tolerance_minus': 5,
            'precursor_mass_tolerance_plus' : 5,
            'precursor_isotope_range' : "0,1",
            'max_missed_cleavages' : 2,
            'rounded_mass_decimals' : 3,
        },
        'label' : '',
        'mods' : mods
    },
    search_engine  = 'omssa_2_1_9',
)


