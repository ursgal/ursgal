#!/usr/bin/env python
import ursgal
import os
import csv
import sys


class deepnovo_0_0_1(ursgal.UNode):
    """
    DeepNovo UNode
    For further information, see https://github.com/nh2tran/DeepNovo

    Note:
        Please download manually from https://github.com/StSchulze/DeepNovo?organization=StSchulze&organization=StSchulze
        or using git clone https://github.com/StSchulze/DeepNovo.git
        and download the model from https://drive.google.com/open?id=0By9IxqHK5MdWalJLSGliWW1RY2c

    Reference:
    Tran, N.H.; Zhang, X.; Xin, L.; Shan, B.; Li, M. (2017) De novo peptide sequencing by deep learning. PNAS 114 (31)

    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'DeepNovo',
        'version'            : '0.0.1',
        'release_date'       : '2017-11-29',
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
                    'exe'            : 'deepnovo_main.py',
                    'url'            : 'https://github.com/nh2tran/DeepNovo',
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
        super(deepnovo_0_0_1, self).__init__(*args, **kwargs)
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

        self.params['translations']['tmp_output_file_incl_path'] = os.path.join(
            self.params['translations']['mgf_new_input_file'] + '.tsv'
        )
        # self.created_tmp_files.append(
        #     self.params['translations']['tmp_output_file_incl_path']
        # )

        self.params['translations']['params_file'] = os.path.join(
            os.path.dirname(self.exe),
            'deepnovo_config.py'
        )
        # self.created_tmp_files.append(
        #     self.params['translations']['params_file'])

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        mgf_org_input_file = open(
            self.params['translations']['mgf_input_file'], 'r', encoding='UTF-8'
        )
        lines = mgf_org_input_file.readlines()
        mgf_org_input_file.close()

        self.scan_lookup = {}
        print('rewriting mgf input file to include SEQ')
        with open(
            self.params['translations']['mgf_new_input_file'], 'w', encoding='UTF-8'
        ) as mgf_new_input_file:
            for n, line in enumerate(lines):
                line = line.strip()
                if line.startswith('BEGIN IONS'):
                    entry = [line]
                    entry_dict = {}
                elif line.startswith('TITLE='):
                    entry_dict['TITLE'] = line
                elif line.startswith('SEQ='):
                    entry_dict['SEQ'] = line
                elif line.startswith('PEPMASS='):
                    entry_dict['PEPMASS'] = line
                elif line.startswith('CHARGE='):
                    entry_dict['CHARGE'] = line
                elif line.startswith('SCANS='):
                    entry_dict['SCANS'] = line
                elif line.startswith('RTINSECONDS='):
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
                else:
                    entry.append(line)
        mgf_new_input_file.close()

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
        for deepnovo_param in self.params['translations']['_grouped_by_translated_key'].keys():
            for ursgal_param_name, param_value in self.params['translations']['_grouped_by_translated_key'][deepnovo_param].items():
                if type(deepnovo_param) is tuple:
                    continue
                elif deepnovo_param == 'knapsack_file':
                    if param_value is None or param_value == 'default':
                        knapsack_file = os.path.join(
                            os.path.dirname(self.exe),
                            'knapsack.npy'
                        )
                    else:
                        knapsack_file = param_value
                    self.params_to_write['knapsack_file'] = knapsack_file
                elif deepnovo_param == 'train_dir':
                    if param_value is None or param_value == 'default':
                        train_dir = os.path.join(
                            os.path.dirname(self.exe),
                            'train.example'
                        )
                    else:
                        train_dir = param_value
                    self.params_to_write['train_dir'] = train_dir
                elif deepnovo_param == 'modifications':
                    assert set(param_value) == set(
                        ['M,opt,any,Oxidation',
                         'C,fix,any,Carbamidomethyl',
                         'N,opt,any,Deamidated',
                         'Q,opt,any,Deamidated']), '''
                    [ ERROR ] The default model of DeepNovo only supports the following modification list:
                        ['M,opt,any,Oxidation',
                         'C,fix,any,Carbamidomethyl',
                         'N,opt,any,Deamidated',
                         'Q,opt,any,Deamidated']
                    [ ERROR ] You specified instead: {0}
                    '''.format(param_value)
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
            '--{0}'.format(self.params['translations']['deepnovo_mode'])
        ]
        print('executing command list')
        print(' '.join(self.params['command_list']))

        return self.params


    def postflight(self):
        '''
        Reformats the DeepNovo output file
        '''
        deepnovo_header = [
            'scan',
            'predicted_sequence',
            'predicted_score',
            'predicted_position_score',
        ]

        mod_lookup = {
            'Cmod': ('C', 'Carbamidomethyl'),
            'Mmod': ('M', 'Oxidation'),
            'Nmod': ('N', 'Deamidated'),
            'Qmod': ('Q', 'Deamidated'),
        }

        translated_headers = []
        header_translations = self.UNODE_UPARAMS[
            'header_translations']['uvalue_style_translation']
        for original_header_key in deepnovo_header:
            ursgal_header_key = header_translations[original_header_key]
            if ursgal_header_key not in translated_headers:
                translated_headers.append(ursgal_header_key)

        translated_headers += [
            'Raw data location',
            'Spectrum Title',
            'Charge',
            'Retention Time (s)',
            'Exp m/z',
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
                if 'mod' in aa:
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
# Copyright 2017 Hieu Tran. All Rights Reserved.
#
# DeepNovo is publicly available for non-commercial uses.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf


# ==============================================================================
# FLAGS (options) for this app
# ==============================================================================


tf.app.flags.DEFINE_string("train_dir", # flag_name
                           r"{train_dir}", # default_value
                           "Training directory.") # docstring

tf.app.flags.DEFINE_integer("direction",
                            {direction},
                            "Set to 0/1/2 for Forward/Backward/Bi-directional.")

tf.app.flags.DEFINE_boolean("use_intensity",
                            {use_intensity},
                            "Set to True to use intensity-model.")

tf.app.flags.DEFINE_boolean("shared",
                            {shared},
                            "Set to True to use shared weights.")

tf.app.flags.DEFINE_boolean("use_lstm",
                            {use_lstm},
                            "Set to True to use lstm-model.")

tf.app.flags.DEFINE_boolean("knapsack_build",
                            {knapsack_build},
                            "Set to True to build knapsack matrix.")

tf.app.flags.DEFINE_boolean("train",
                            False,
                            "Set to True for training.")

tf.app.flags.DEFINE_boolean("test_true_feeding",
                            False,
                            "Set to True for testing.")

tf.app.flags.DEFINE_boolean("decode",
                            False,
                            "Set to True for decoding.")

tf.app.flags.DEFINE_boolean("beam_search",
                            {beam_search},
                            "Set to True for beam search.")

tf.app.flags.DEFINE_integer("beam_size",
                            {beam_size},
                            "Number of optimal paths to search during decoding.")

tf.app.flags.DEFINE_boolean("search_db",
                            False,
                            "Set to True to do a database search.")

tf.app.flags.DEFINE_boolean("search_denovo",
                            False,
                            "Set to True to do a denovo search.")

tf.app.flags.DEFINE_boolean("search_hybrid",
                            False,
                            "Set to True to do a hybrid, db+denovo, search.")

tf.app.flags.DEFINE_boolean("test",
                            False,
                            "Set to True to test the prediction accuracy.")

tf.app.flags.DEFINE_boolean("header_seq",
                            False,
                            "Set to False if peptide sequence is not provided.")

tf.app.flags.DEFINE_boolean("decoy",
                            False,
                            "Set to True to search decoy database.")

FLAGS = tf.app.flags.FLAGS


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

vocab_reverse = ['A',
                 'R',
                 'N',
                 'Nmod',
                 'D',
                 #~ 'C',
                 'Cmod',
                 'E',
                 'Q',
                 'Qmod',
                 'G',
                 'H',
                 'I',
                 'L',
                 'K',
                 'M',
                 'Mmod',
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
           ('Nmod', 115.02695),
           ('D', 115.02694),
           # ('C', 103.00919),
           ('Cmod', 160.03065),
           # ('Cmod', 161.01919),
           ('E', 129.04259),
           ('Q', 128.05858),
           ('Qmod', 129.0426),
           ('G', 57.02146),
           ('H', 137.05891),
           ('I', 113.08406),
           ('L', 113.08406),
           ('K', 128.09496),
           ('M', 131.04049),
           ('Mmod', 147.0354),
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


# if change, need to re-compile cython_speedup
SPECTRUM_RESOLUTION = 10 # bins for 1.0 Da = precision 0.1 Da
#~ SPECTRUM_RESOLUTION = 20 # bins for 1.0 Da = precision 0.05 Da
#~ SPECTRUM_RESOLUTION = 40 # bins for 1.0 Da = precision 0.025 Da
#~ SPECTRUM_RESOLUTION = 50 # bins for 1.0 Da = precision 0.02 Da
#~ SPECTRUM_RESOLUTION = 80 # bins for 1.0 Da = precision 0.0125 Da
print("SPECTRUM_RESOLUTION ", SPECTRUM_RESOLUTION)

# if change, need to re-compile cython_speedup
WINDOW_SIZE = 10 # 10 bins
print("WINDOW_SIZE ", WINDOW_SIZE)

MZ_MAX = 3000.0
MZ_SIZE = int(MZ_MAX * SPECTRUM_RESOLUTION) # 30k

KNAPSACK_AA_RESOLUTION = 10000 # 0.0001 Da
mass_AA_min_round = int(round(mass_AA_min * KNAPSACK_AA_RESOLUTION)) # 57.02146
KNAPSACK_MASS_PRECISION_TOLERANCE = 100 # 0.01 Da
num_position = 0

PRECURSOR_MASS_PRECISION_TOLERANCE = 0.01

# ONLY for accuracy evaluation
#~ PRECURSOR_MASS_PRECISION_INPUT_FILTER = 0.01
PRECURSOR_MASS_PRECISION_INPUT_FILTER = 1000
AA_MATCH_PRECISION = 0.1

# skip (x > MZ_MAX,MAX_LEN)
MAX_LEN = 50 if FLAGS.decode else 30
print("MAX_LEN ", MAX_LEN)

# We use a number of buckets and pad to the closest one for efficiency.
_buckets = [12, 22, 32]
#~ _buckets = [12,22,32,42,52] # for decode
print("_buckets ", _buckets)


# ==============================================================================
# HYPER-PARAMETERS of the NEURAL NETWORKS
# ==============================================================================


num_ion = 8 # 2
print("num_ion ", num_ion)

l2_loss_weight = 0.0 # 0.0
print("l2_loss_weight ", l2_loss_weight)

#~ encoding_cnn_size = 4 * (RESOLUTION//10) # 4 # proportion to RESOLUTION
#~ encoding_cnn_filter = 4
#~ print("encoding_cnn_size ", encoding_cnn_size)
#~ print("encoding_cnn_filter ", encoding_cnn_filter)

embedding_size = 512
print("embedding_size ", embedding_size)

num_layers = 1
num_units = 512
print("num_layers ", num_layers)
print("num_units ", num_units)

keep_conv = 0.75
keep_dense = 0.5
print("keep_conv ", keep_conv)
print("keep_dense ", keep_dense)

batch_size = 128
print("batch_size ", batch_size)

epoch_stop = 20 # 50
print("epoch_stop ", epoch_stop)

train_stack_size = 4500
valid_stack_size = 15000 # 10%
test_stack_size = 4000
buffer_size = {buffer_size}
print("train_stack_size ", train_stack_size)
print("valid_stack_size ", valid_stack_size)
print("test_stack_size ", test_stack_size)
print("buffer_size ", buffer_size)

steps_per_checkpoint = 100 # 20 # 100 # 2 # 4 # 200
random_test_batches = 10
print("steps_per_checkpoint ", steps_per_checkpoint)
print("random_test_batches ", random_test_batches)

max_gradient_norm = 5.0
print("max_gradient_norm ", max_gradient_norm)


# ==============================================================================
# DATASETS
# ==============================================================================

# YEAST-LOW-COON_2013-PEAKS-DB-DUP
data_format = "mgf"
cleavage_rule = "{cleavage_rule}"
num_missed_cleavage = {num_missed_cleavage}
fixed_mod_list = ['C']
var_mod_list = ['N', 'Q', 'M']
precursor_mass_tolerance = {precursor_mass_tolerance_da} # Da
precursor_mass_ppm = {precursor_mass_tolerance_ppm}/1000000 # ppm (20 better) # instead of absolute 0.01 Da
knapsack_file = r"{knapsack_file}"
# training/testing/decoding files
# input_file_train = r"data.training/dia.xchen.nov27/fraction_1.mgf.split.train.dup"
# input_file_valid = r"data.training/dia.xchen.nov27/fraction_1.mgf.split.valid.dup"
# input_file_test = r"C:\\Users\\Admin\\Desktop\\ursgal_dev\\ursgal\\ursgal\\resources\\platform_independent\\arc_independent\\deepnovo_0_0_1\\data.training\\yeast.low.coon_2013\\peaks.db.mgf.test.dup"
decode_test_file = r"{mgf_new_input_file}"
decode_output_file = r"{output_path}"
# denovo files
denovo_input_file = r"{mgf_new_input_file}"
denovo_output_file = r"{output_path}"
# db files
db_fasta_file = r"{db_fasta_file}"
db_input_file = r"{mgf_new_input_file}"
db_output_file = r"{output_path}"
if FLAGS.decoy:
  db_output_file += ".decoy"
# hybrid files
hybrid_input_file = r"{mgf_new_input_file}"
hybrid_denovo_file = hybrid_input_file + ".deepnovo_hybrid_denovo"
hybrid_output_file = r"{output_path}"
# if FLAGS.decoy:
#   hybrid_output_file += ".decoy"
# test accuracy
# predicted_format = "deepnovo"
# target_file = "data.training/dia.xchen.nov27/fraction_1.mgf.split.test.dup.target"
# predicted_file = denovo_output_file
# accuracy_file = predicted_file + ".accuracy"
# ==============================================================================
'''.format(
                **self.params_to_write),
                file=io
            )
        return
