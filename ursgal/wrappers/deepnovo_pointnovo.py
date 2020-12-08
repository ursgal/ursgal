#!/usr/bin/env python3.4
import ursgal
import os
import csv
import sys


class deepnovo_pointnovo(ursgal.UNode):
    """
    PointNovo UNode
    pytorch re-implementation of DeepNovo
    For further information, see https://github.com/volpato30/PointNovo/

    Reference:
    Tran, N.H.; Zhang, X.; Xin, L.; Shan, B.; Li, M. (2017) De novo peptide sequencing by deep learning. PNAS 114 (31) 

    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'PointNovo',
        'version'            : 'DeepNovo v2',
        'release_date'       : '2019-05-21',
        'engine_type' : {
            'de_novo_search_engine' : True,
        },
        'input_extensions'   : ['.mgf'],
        'output_extensions'  : ['.csv'],
        'in_development'     : False,
        'create_own_folder'  : True,
        'include_in_git'     : False,
        'distributable'      : False,
        'utranslation_style' : 'deepnovo_style_1',
        'engine' : {
            'platform_independent'    : {
                'arc_independent' : {
                    'exe'            : 'main.py',
                    'url'            : 'https://github.com/volpato30/DeepNovoV2',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation' :
        'Tran, N.H.; Zhang, X.; Xin, L.; Shan, B.; Li, M. (2017) '
            'De novo peptide sequencing by deep learning. PNAS 114 (31)'
    }

    def __init__(self, *args, **kwargs):
        super(deepnovo_pointnovo, self).__init__(*args, **kwargs)
        pass

    def preflight(self):
        """
        Create deepnovo_config.py file and format command line via self.params

        Returns:
                dict: self.params
        """

        self.time_point(tag='execution')

        # main = self.import_engine_as_python_function()

        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        self.params['translations']['mgf_new_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '_tmp.mgf'
        )
        self.created_tmp_files.append(
            self.params['translations']['mgf_new_input_file']
        )

        self.params['translations']['feature_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '_features.csv'
        )
        self.created_tmp_files.append(
            self.params['translations']['feature_file']
        )

        self.params['translations']['tmp_output_file_incl_path'] = os.path.join(
            self.params['translations']['mgf_new_input_file'] + '.tsv'
        )
        self.created_tmp_files.append(
            self.params['translations']['tmp_output_file_incl_path']
        )

        self.params['translations']['params_file'] = os.path.join(
            os.path.dirname(self.exe),
            'config.py'
        )
        self.created_tmp_files.append(
            self.params['translations']['params_file'])

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        mgf_org_input_file = open(
            self.params['translations']['mgf_input_file'], 'r', encoding='UTF-8'
        )
        lines = mgf_org_input_file.readlines()
        mgf_org_input_file.close()


        feature_headers = [
            'spec_group_id',
            'm/z',
            'z',
            'rt_mean',
            'seq',
            'scans',
            'profile',
            'feature area',
            'irt',
        ]
        if sys.platform == 'win32':
            lineterminator = '\n'
        else:
            lineterminator = '\r\n'
        self.scan_lookup = {}
        print('rewriting mgf input file to include SEQ')
        with open(
            self.params['translations']['mgf_new_input_file'], 'w', encoding='UTF-8'
        ) as mgf_new_input_file:
            with open(
                self.params['translations']['feature_file'], 'w', encoding='UTF-8'
            ) as feature_in:
                feature_csv = csv.DictWriter(
                    feature_in,
                    fieldnames=feature_headers,
                    lineterminator=lineterminator
                )
                feature_csv.writeheader()
                spec_group = 0
                for n, line in enumerate(lines):
                    line = line.strip()
                    if line.startswith('BEGIN IONS'):
                        spec_group += 1
                        entry = [line]
                        entry_dict = {}
                        feature_dict = {
                            'spec_group_id': spec_group,
                            'seq': '',
                            'profile': '',
                            'feature area': 0,
                            'irt': 0,
                        }
                    elif line.startswith('TITLE='):
                        entry_dict['TITLE'] = line
                    elif line.startswith('SEQ='):
                        entry_dict['SEQ'] = line
                        feature_dict['seq'] = line.split('=')[1]
                    elif line.startswith('PEPMASS='):
                        feature_dict['m/z'] = line.split('=')[1]
                        entry_dict['PEPMASS'] = line
                    elif line.startswith('CHARGE='):
                        feature_dict['z'] = line.split('=')[1].strip('+')
                        entry_dict['CHARGE'] = line
                    elif line.startswith('SCANS='):
                        feature_dict['scans'] = line.split('=')[1]
                        entry_dict['SCANS'] = line
                    elif line.startswith('RTINSECONDS='):
                        feature_dict['rt_mean'] = line.split('=')[1]
                        entry_dict['RTINSECONDS'] = line
                    elif line.startswith('END IONS'):
                        entry.append(line)
                        entry.append('')
                        # if 'SEQ' not in entry_dict:
                        #     entry_dict['SEQ'] = 'SEQ= '
                        scan = entry_dict['SCANS'].split('=')[1]
                        charge = entry_dict['CHARGE'].split('=')[1].strip('+')
                        self.scan_lookup[scan] = charge
                        for n, write_line in enumerate(entry):
                            if n == 1:
                                for header in [
                                    'TITLE',
                                    'PEPMASS',
                                    'CHARGE',
                                    'SCANS',
                                    'RTINSECONDS',
                                    # 'SEQ',
                                ]:
                                    print(
                                        entry_dict[header],
                                        file=mgf_new_input_file
                                    )
                            print(write_line, file=mgf_new_input_file)
                        feature_csv.writerow(feature_dict)
                    else:
                        entry.append(line)

        print(
            '''
            [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
            [ WARNING ] need to be combined for DeepNovo (use of symmetric tolerance window).
            [ WARNING ] The arithmetic mean is used.
            '''
        )

        self.params_to_write = {
            'mgf_new_input_file' : self.params['translations']['mgf_new_input_file'],
            'output_path' : self.params['translations']['tmp_output_file_incl_path'],
            'feature_file': self.params['translations']['feature_file']
        }
        self.params['translations']['precursor_mass_tolerance'] = (float(self.params['precursor_mass_tolerance_plus']) +
                                                                   float(self.params['precursor_mass_tolerance_minus']) ) \
            / 2.0

        if self.params['translations']['precursor_mass_tolerance_unit'] == 'ppm':
            self.params_to_write['precursor_mass_tolerance_da'] = \
                ursgal.ucore.convert_ppm_to_dalton(
                    self.params['translations']['precursor_mass_tolerance'],
                    base_mz=self.params['translations']['base_mz']
            )
            self.params_to_write['precursor_mass_tolerance_ppm'] = \
                self.params['translations']['precursor_mass_tolerance'] 
        elif self.params['translations']['precursor_mass_tolerance_unit'] == 'da':
            self.params_to_write['precursor_mass_tolerance_ppm'] = \
                ursgal.ucore.convert_dalton_to_ppm(
                    self.params['translations']['precursor_mass_tolerance'],
                    base_mz=self.params['translations']['base_mz']
            )
            self.params_to_write['precursor_mass_tolerance_da'] = \
                self.params['translations']['precursor_mass_tolerance']

        if self.params['translations']['frag_mass_tolerance_unit'] == 'ppm':
            self.params_to_write['frag_mass_tolerance_da'] = \
                ursgal.ucore.convert_ppm_to_dalton(
                    self.params['translations']['frag_mass_tolerance'],
                    base_mz=self.params['translations']['base_mz']
            )
        elif self.params['translations']['frag_mass_tolerance_unit'] == 'da':
            self.params_to_write['frag_mass_tolerance_da'] = \
                self.params['translations']['frag_mass_tolerance']

        assert self.params['translations']['deepnovo_mode'] == 'search_denovo', '''
            [ ERROR ] Only search_denovo supported as deepnovo_mmode so far!
            '''
        # self.params_to_write['denovo_mode'] = False
        # self.params_to_write['db_mode'] = False
        # self.params_to_write['hybrid_mode'] = False
        # if self.params['translations']['deepnovo_mode'] == 'search_denovo':
        #     self.params_to_write['denovo_mode'] = True
        # elif self.params['translations']['deepnovo_mode'] == 'search_db':
        #     self.params_to_write['db_mode'] = True
        # elif self.params['translations']['deepnovo_mode'] == 'search_hybrid':
        #     self.params_to_write['hybrid_mode'] = True

        # vocab_reverse = [
        #     'A',
        #     'R',
        #     'N',
        #     'D',
        #     'C',
        #     'E',
        #     'Q',
        #     'G',
        #     'H',
        #     'I',
        #     'L',
        #     'K',
        #     'M',
        #     'F',
        #     'P',
        #     'S',
        #     'T',
        #     'W',
        #     'Y',
        #     'V',
        # ]
        # mass_H = 1.0078
        # mass_N_terminus = 1.0078
        # mass_C_terminus = 17.0027
        # mass_AA = dict([
        #     ('_PAD', 0.0),
        #     ('_GO', mass_N_terminus-mass_H),
        #     ('_EOS', mass_C_terminus+mass_H),
        #     ('A', 71.03711),
        #     ('R', 156.10111),
        #     ('N', 114.04293),
        #     ('D', 115.02694),
        #     ('C', 103.00919),
        #     ('E', 129.04259),
        #     ('Q', 128.05858),
        #     ('G', 57.02146),
        #     ('H', 137.05891),
        #     ('I', 113.08406),
        #     ('L', 113.08406),
        #     ('K', 128.09496),
        #     ('M', 131.04049),
        #     ('F', 147.06841),
        #     ('P', 97.05276),
        #     ('S', 87.03203),
        #     ('T', 101.04768),
        #     ('W', 186.07931),
        #     ('Y', 163.06333),
        #     ('V', 99.06841),
        # ])
        # import pprint
        # pprint.pprint(self.params['translations'])
        # exit()
        # self.params_to_write['feature_file'] = os.path.join(
        #     os.path.dirname(self.exe),
        #     'features.csv'
        # )

        for deepnovo_param in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][deepnovo_param].items():
                if type(deepnovo_param) is tuple:
                    continue
                elif deepnovo_param == 'knapsack_file':
                    if param_value is None or param_value == 'default':
                        knapsack_file = os.path.join(
                            os.path.dirname(self.exe),
                            'fix_C_var_NMQ_knapsack.npy'
                        )
                        self.params_to_write['knapsack_file'] = knapsack_file
                    else:
                        self.params_to_write['knapsack_file'] = param_value
                elif deepnovo_param == 'train_dir':
                    if param_value is None or param_value == 'default':
                        train_dir = os.path.join(
                            os.path.dirname(self.exe),
                            'train'
                        )
                        self.params_to_write['train_dir'] = train_dir
                    else:
                        self.params_to_write['train_dir'] = param_value
                elif deepnovo_param == 'modifications':
                    assert set(param_value) == set(
                        ['M,opt,any,Oxidation',
                         'C,fix,any,Carbamidomethyl',
                         'N,opt,any,Deamidated',
                         'Q,opt,any,Deamidated'
                         ]),'''
                    [ ERROR ] The default model of DeepNovo only supports the following modification list:
                        ['M,opt,any,Oxidation',
                         'C,fix,any,Carbamidomethyl'],
                    [ ERROR ] You specified instead: {0}
                    '''.format(param_value) 
                    #      '''
                    # [ ERROR ] The default model of DeepNovo only supports the following modification list:
                    #     ['M,opt,any,Oxidation',
                    #      'C,fix,any,Carbamidomethyl',
                    #      'N,opt,any,Deamidated',
                    #      'Q,opt,any,Deamidated']
                    # [ ERROR ] You specified instead: {0}
                    # '''.format(param_value)
                #     cc = ursgal.ChemicalComposition()
                #     for mod_dict in self.params['mods']['opt']:
                #         '''
                #         {'_id': 0,
                #           'aa': '*',
                #           'composition': {'C': 2, 'H': 2, 'O': 1},
                #           'id': '1',
                #           'mass': 42.010565,
                #           'name': 'Acetyl',
                #           'org': '*,opt,Prot-N-term,Acetyl',
                #           'pos': 'Prot-N-term',
                #           'unimod': True},
                #         '''
                #         if mod_dict['pos'] != 'any':
                #             print(
                #                 '''
                #   [WARNING] DeepNovo does not support positional arguments for modifications.
                #   [WARNING] The following modification will be used on any position:
                #   [WARNING] {0}
                #             '''.format(mod_dict['org'])
                #             )
                #         if mod_dict['aa'] == '*':
                #             print('''
                #             Not sure how to handle this modification in DeepNovo:
                #             {0}
                #             '''.format(mod_dict['org']))
                #             sys.exit(1)
                #         mod_index = vocab_reverse.index(mod_dict['aa'])
                #         vocab_reverse.insert(mod_index+1, mod_dict['aa']+'mod')
                #         cc.use('{0}#{1}:1'.format(
                #             mod_dict['aa'],
                #             mod_dict['name']
                #         ))
                #         mass_AA[mod_dict['aa']+'mod'] = cc._mass()

                #     for mod_dict in self.params['mods']['fix']:
                #         if mod_dict['pos'] != 'any':
                #             print(
                #                 '''
                #   [WARNING] DeepNovo does not support positional arguments for modifications.
                #   [WARNING] The following modification will be used on any position:
                #   [WARNING] {0}
                #             '''.format(mod_dict['org'])
                #             )
                #         if mod_dict['aa'] == '*':
                #             print('''
                #             Not sure how to handle this modification in DeepNovo:
                #             {0}
                #             '''.format(mod_dict['org']))
                #             sys.exit(1)
                #         mod_index = vocab_reverse.index(mod_dict['aa'])
                #         vocab_reverse[mod_index] = mod_dict['aa']+'mod'
                #         del mass_AA[mod_dict['aa']]
                #         cc.use('{0}#{1}:1'.format(
                #             mod_dict['aa'],
                #             mod_dict['name']
                #         ))
                #         mass_AA[mod_dict['aa']+'mod'] = cc._mass()
                #     self.params_to_write['mass_AA'] = mass_AA
                #     self.params_to_write['vocab_reverse'] = vocab_reverse
                else:
                    self.params_to_write[deepnovo_param] = param_value

        self.write_params_file()

        self.params['command_list'] = [
            sys.executable,
            self.exe,
            '--{0}'.format(self.params['translations']['deepnovo_mode']),
            '--beam_size', str(self.params['translations']['deepnovo_beam_size']),
            '--train_dir', self.params_to_write['train_dir'],
        ]

        return self.params


    def postflight(self):
        '''
        Reformats the DeepNovo output file
        '''
        deepnovo_header = [
            'feature_id',
            'feature_area',
            'predicted_sequence',
            'predicted_score',
            'predicted_position_score',
            'precursor_mz',
            'precursor_charge',
            'protein_access_id',
            'scan_list_middle',
            'scan_list_original',
            'predicted_score_max',
        ]

        mod_lookup = {
            'C(Carbamidomethylation)': ('C', 'Carbamidomethyl'),
            'M(Oxidation)': ('M', 'Oxidation'),
            'N(Deamidation)': ('N', 'Deamidated'),
            'Q(Deamidation)': ('Q', 'Deamidated'),
        }

        translated_headers = []
        header_translations = self.UNODE_UPARAMS[
            'header_translations']['uvalue_style_translation']
        for original_header_key in deepnovo_header:
            if original_header_key not in header_translations.keys():
                ursgal_header_key = original_header_key     
            else:
                ursgal_header_key = header_translations[original_header_key]
            if ursgal_header_key not in translated_headers:
                translated_headers.append(ursgal_header_key)

        translated_headers += [
            'Raw data location',
            'Spectrum Title',
            'Retention Time (s)',
            'Modifications',
        ]

        csv_kwargs = {}
        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'
        csv_writer = csv.DictWriter(
            open(self.params['translations']['output_file_incl_path'], 'w'),
            fieldnames=translated_headers,
            **csv_kwargs
        )

        deepnovo_output = os.path.join(
            self.params['translations']['tmp_output_file_incl_path']
        )
        csv_reader = csv.DictReader(
            open(deepnovo_output, 'r'),
            fieldnames=translated_headers,
            delimiter='\t',
        )

        csv_writer.writeheader()
        for n, line_dict in enumerate(csv_reader):
            if n == 0:
                continue
            line_dict['Raw data location'] = os.path.abspath(
                self.params['translations']['mgf_input_file']
            )
            line_dict['Charge'] = self.scan_lookup[line_dict['Spectrum ID']]

        #     ############################################
        #     # all fixing here has to go into unify csv! #
        #     ############################################

            tmp_seq = ''
            seq_list = line_dict['Sequence'].split(',')
            tmp_mods = []
            for n, aa in enumerate(seq_list):
                if '(' in aa:
                    org_aa, mod = mod_lookup[aa]
                    tmp_mods.append(
                        '{0}:{1}'.format(mod, n+1)
                    )
                    tmp_seq += org_aa
                else:
                    tmp_seq += aa
            line_dict['Sequence'] = tmp_seq
            line_dict['Modifications'] = ';'.join(tmp_mods)
            if line_dict['Sequence'] == '':
                continue
            csv_writer.writerow(line_dict)
        return

    def write_params_file(self):
        with open(self.params['translations']['params_file'], 'w') as io:
            print('''
# DeepNovoV2 is publicly available for non-commercial uses.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import argparse
from itertools import combinations

# ==============================================================================
# FLAGS (options) for this app
# ==============================================================================

parser = argparse.ArgumentParser()
parser.add_argument("--train_dir", type=str, default="train")
parser.add_argument("--beam_size", type=int, default="5")
parser.add_argument("--train", dest="train", action="store_true")
parser.add_argument("--search_denovo", dest="search_denovo", action="store_true")
parser.add_argument("--search_db", dest="search_db", action="store_true")
parser.add_argument("--valid", dest="valid", action="store_true")
parser.add_argument("--test", dest="test", action="store_true")

parser.set_defaults(train=False)
parser.set_defaults(search_denovo=False)
parser.set_defaults(search_db=False)
parser.set_defaults(test=False)
parser.set_defaults(valid=False)

args = parser.parse_args()

FLAGS = args
train_dir = FLAGS.train_dir
use_lstm = {use_lstm}


# ==============================================================================
# GLOBAL VARIABLES for VOCABULARY
# ==============================================================================


# Special vocabulary symbols - we always put them at the start.
_PAD = '_PAD'
_GO = '_GO'
_EOS = '_EOS'
_START_VOCAB = [_PAD, _GO, _EOS]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
assert PAD_ID == 0
vocab_reverse = ['A',
                 'R',
                 'N',
                 'N(Deamidation)',
                 'D',
                 #~ 'C',
                 'C(Carbamidomethylation)',
                 'E',
                 'Q',
                 'Q(Deamidation)',
                 'G',
                 'H',
                 'I',
                 'L',
                 'K',
                 'M',
                 'M(Oxidation)',
                 'F',
                 'P',
                 'S',
                 'T',
                 'W',
                 'Y',
                 'V',
                ]

vocab_reverse = _START_VOCAB + vocab_reverse
print("vocab_reverse ", vocab_reverse)

vocab = dict([(x, y) for (y, x) in enumerate(vocab_reverse)])
print("vocab ", vocab)

vocab_size = len(vocab_reverse)
print("vocab_size ", vocab_size)


# database search parameter
## the PTMs to be included in the database search
fix_mod_dict = dict([("C", "C(Carbamidomethylation)")])
# var_mod_dict = dict([("N", "N(Deamidation)"), ('Q', 'Q(Deamidation)'), ('M', 'M(Oxidation)')])
var_mod_dict = dict([('M', 'M(Oxidation)')])
max_num_mod = 3
db_ppm_tolenrance = 20.
semi_cleavage = False

normalizing_std_n = 150
normalizing_mean_n = 10

inference_value_max_batch_size = 20
num_psm_per_scan_for_percolator = 10
db_fasta_file = "fasta_files/uniprot_sprot_human_with_decoy.fasta"
num_db_searcher_worker = 8
fragment_ion_mz_diff_threshold = 0.02
quick_scorer = "num_matched_ions"


def _fix_transform(aa: str):
    def trans(peptide: list):
        return [x if x != aa else fix_mod_dict[x] for x in peptide]
    return trans


def fix_mod_peptide_transform(peptide: list):
    """
    apply fix modification transform on a peptide
    :param peptide:
    :return:
    """
    for aa in fix_mod_dict.keys():
        trans = _fix_transform(aa)
        peptide = trans(peptide)
    return peptide


def _find_all_ptm(peptide, position_list):
    if len(position_list) == 0:
        return [peptide]
    position = position_list[0]
    aa = peptide[position]
    result = []
    temp = peptide[:]
    temp[position] = var_mod_dict[aa]
    result += _find_all_ptm(temp, position_list[1:])
    return result


def var_mod_peptide_transform(peptide: list):
    """
    apply var modification transform on a peptide, the max number of var mod is max_num_mod
    :param peptide:
    :return:
    """
    position_list = [position for position, aa in enumerate(peptide) if aa in var_mod_dict]
    position_count = len(position_list)
    num_mod = min(position_count, max_num_mod)
    position_combination_list = []
    for x in range(1, num_mod+1):
        position_combination_list += combinations(position_list, x)
    # find all ptm peptides
    ptm_peptide_list = []
    for position_combination in position_combination_list:
        ptm_peptide_list += _find_all_ptm(peptide, position_combination)
    return ptm_peptide_list


# ==============================================================================
# GLOBAL VARIABLES for THEORETICAL MASS
# ==============================================================================


mass_H = 1.0078
mass_H2O = 18.0106
mass_NH3 = 17.0265
mass_N_terminus = 1.0078
mass_C_terminus = 17.0027
mass_CO = 27.9949

mass_AA = dict([
('_PAD', 0.0),
('_GO', mass_N_terminus-mass_H),
('_EOS', mass_C_terminus+mass_H),
('A', 71.03711),
('R', 156.10111),
('N', 114.04293),
('N(Deamidation)', 115.02695),
('D', 115.02694),
('C(Carbamidomethylation)', 160.03065),
('E', 129.04259),
('Q', 128.05858),
('Q(Deamidation)', 129.0426),
('G', 57.02146),
('H', 137.05891),
('I', 113.08406),
('L', 113.08406),
('K', 128.09496),
('M', 131.04049),
('M(Oxidation)', 147.0354),
('F', 147.06841),
('P', 97.05276),
('S', 87.03203),
('T', 101.04768),
('W', 186.07931),
('Y', 163.06333),
('V', 99.06841),
])

mass_ID = [mass_AA[vocab_reverse[x]] for x in range(vocab_size)]
mass_ID_np = np.array(mass_ID, dtype=np.float32)

mass_AA_min = mass_AA["G"] # 57.02146


# ==============================================================================
# GLOBAL VARIABLES for PRECISION, RESOLUTION, temp-Limits of MASS & LEN
# ==============================================================================

MZ_MAX = {MZ_MAX}

MAX_NUM_PEAK = {MAX_NUM_PEAK}

KNAPSACK_AA_RESOLUTION = 10000 # 0.0001 Da
mass_AA_min_round = int(round(mass_AA_min * KNAPSACK_AA_RESOLUTION)) # 57.02146
KNAPSACK_MASS_PRECISION_TOLERANCE = 100 # 0.01 Da
num_position = 0

PRECURSOR_MASS_PRECISION_TOLERANCE = {precursor_mass_tolerance_da}

# ONLY for accuracy evaluation
#~ PRECURSOR_MASS_PRECISION_INPUT_FILTER = 0.01
#~ PRECURSOR_MASS_PRECISION_INPUT_FILTER = 1000
AA_MATCH_PRECISION = {frag_mass_tolerance_da}

# skip (x > MZ_MAX,MAX_LEN)
MAX_LEN = 50 if args.search_denovo else 30
print("MAX_LEN ", MAX_LEN)


# ==============================================================================
# HYPER-PARAMETERS of the NEURAL NETWORKS
# ==============================================================================


num_ion = 12
print("num_ion ", num_ion)

weight_decay = 0.0  # no weight decay lead to better result.
print("weight_decay ", weight_decay)

#~ encoding_cnn_size = 4 * (RESOLUTION//10) # 4 # proportion to RESOLUTION
#~ encoding_cnn_filter = 4
#~ print("encoding_cnn_size ", encoding_cnn_size)
#~ print("encoding_cnn_filter ", encoding_cnn_filter)

embedding_size = 512
print("embedding_size ", embedding_size)

num_lstm_layers = 1
num_units = 64
lstm_hidden_units = 512
print("num_lstm_layers ", num_lstm_layers)
print("num_units ", num_units)

dropout_rate = 0.25

batch_size = 16
num_workers = 6
print("batch_size ", batch_size)

num_epoch = 20

init_lr = 1e-3

steps_per_validation = 300  # 100 # 2 # 4 # 200
print("steps_per_validation ", steps_per_validation)

max_gradient_norm = 5.0
print("max_gradient_norm ", max_gradient_norm)


# ==============================================================================
# DATASETS
# ==============================================================================

data_format = "mgf"
cleavage_rule = "{cleavage_rule}"
num_missed_cleavage = 2
knapsack_file = r"{knapsack_file}"

input_spectrum_file_train = "ABRF_DDA/spectrums.mgf"
input_feature_file_train = "ABRF_DDA/features.csv.identified.train.nodup"
input_spectrum_file_valid = "ABRF_DDA/spectrums.mgf"
input_feature_file_valid = "ABRF_DDA/features.csv.identified.valid.nodup"
input_spectrum_file_test = "data.training/dia.hla.elife.jurkat_oxford/testing_jurkat_oxford.spectrum.mgf"
input_feature_file_test = "data.training/dia.hla.elife.jurkat_oxford/testing_jurkat_oxford.feature.csv"
# denovo files
denovo_input_spectrum_file = r"{mgf_new_input_file}"
denovo_input_feature_file = r"{feature_file}"
denovo_output_file = r"{output_path}"

# db search files
search_db_input_spectrum_file = "Lumos_data/PXD008999/export_0.mgf"
search_db_input_feature_file = "Lumos_data/PXD008999/export_0.csv"
db_output_file = search_db_input_feature_file + '.pin'

# test accuracy
predicted_format = "deepnovo"
target_file = denovo_input_feature_file
predicted_file = denovo_output_file

accuracy_file = predicted_file + ".accuracy"
denovo_only_file = predicted_file + ".denovo_only"
scan2fea_file = predicted_file + ".scan2fea"
multifea_file = predicted_file + ".multifea"
# ==============================================================================
# feature file column format
col_feature_id = "spec_group_id"
col_precursor_mz = "m/z"
col_precursor_charge = "z"
col_rt_mean = "rt_mean"
col_raw_sequence = "seq"
col_scan_list = "scans"
col_feature_area = "feature area"

# predicted file column format
pcol_feature_id = 0
pcol_feature_area = 1
pcol_sequence = 2
pcol_score = 3
pcol_position_score = 4
pcol_precursor_mz = 5
pcol_precursor_charge = 6
pcol_protein_id = 7
pcol_scan_list_middle = 8
pcol_scan_list_original = 9
pcol_score_max = 10

distance_scale_factor = 100.
sinusoid_base = 30000.
spectrum_reso = 10
n_position = int(MZ_MAX) * spectrum_reso

'''.format(
                **self.params_to_write),
                file=io
            )
        return
