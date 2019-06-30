import csv
import os
import pickle
import ursgal


test_case_list = [
    ('TMT_xtandem_vengeance_pmap.csv', 'xtandem_vengeance'),
    ('TMT_msgfplus_pmap.csv', 'msgfplus_v2018_09_12')
]

params = {
    'modifications': [
        'M,opt,any,Oxidation',
        '*,opt,Prot-N-term,Acetyl',
        'C,fix,any,Carbamidomethyl',
        '*,opt,N-term,TMT6plex',
        'K,fix,any,TMT6plex',
    ],
}
# uc = ursgal.UController(params=params, profile='QExactive+', verbose=False)
# uc.scan_rt_lookup_path = 'tests/data/_ursgal_test_lookup.pkl'
# uc.map_mods()
# unify_csv_main = uc.unodes['unify_csv_1_0_0']['class'].import_engine_as_python_function()


def unify_nterm_test():
    for param_l in test_case_list:
        yield unify_csv, param_l[0], param_l[1]


def unify_csv(file, engine):
    uc = ursgal.UController(params=params, profile='QExactive+', verbose=False)
    uc.scan_rt_lookup_path = 'tests/data/_ursgal_test_lookup.pkl'
    uc.map_mods()
    unify_csv_main = uc.unodes['unify_csv_1_0_0']['class'].import_engine_as_python_function()

    output_csv = os.path.join(
        'tests', 'data',
        os.path.splitext(file)[0] + '_unified.csv'
    )
    input_csv = os.path.join(
        'tests', 'data',
        file
    )
    scan_rt_lookup = pickle.load(
        open(
            os.path.join(
                'tests',
                'data',
                '_ursgal_test_pickle.pkl')
            ,
            'rb'
        )
    )
    unify_csv_main(
        input_file=input_csv,
        output_file=output_csv,
        scan_rt_lookup=scan_rt_lookup,
        params={
            'translations': {
                'decoy_tag': 'decoy_',
                'enzyme': 'KR;C;P',
                'semi_enzyme': False,
                'database': os.path.join('tests', 'data', 'P0ADZ4.fasta'),
                'protein_delimiter': '<|>',
                'psm_merge_delimiter': ';',
                'keep_asp_pro_broken_peps': True,
                'precursor_mass_tolerance_minus': 5,
                'precursor_mass_tolerance_plus': 5,
                'precursor_isotope_range': "0,1",
                'max_missed_cleavages': 2,
                'rounded_mass_decimals': 3,
                'use_pyqms_for_mz_calculation': False,
                'aa_exception_dict': {
                    'J': {
                        'original_aa': ['L', 'I'],
                    },
                    'O': {
                        'original_aa': ['K'],
                        'unimod_name': 'Methylpyrroline',
                    },
                },
            },
            'label': '',
            'mods': uc.params['mods'],
        },
        search_engine=engine,
    )
    reader_produced = [line for line in csv.DictReader(open(output_csv))]
    reader_expected = [line for line in csv.DictReader(open(output_csv+'_expected.csv'))]
    for pos, line in enumerate(reader_produced):
        print('#{pos:0>5} Produced: {mod}'.format(pos=pos, mod=line["Modifications"]))
        print('#{pos:0>5} Expected: {mod}'.format(pos=pos, mod=reader_expected[pos]["Modifications"]))
        assert line['Modifications'] == reader_expected[pos]['Modifications']


if __name__ == '__main__':
    for i, params_l in enumerate(test_case_list):
        unify_csv(params_l[0], params_l[1])
