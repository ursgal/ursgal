#!/usr/bin/env python3.4
import ursgal
import os
from collections import defaultdict as ddict
import csv
import itertools
import sys
from .pipi_1_4_5 import pipi_1_4_5 as pipi

class pipi_1_4_6( pipi ):
    """
    Unode for PIPI: PTM-Invariant Peptide Identification
    For furhter information see: http://bioinformatics.ust.hk/pipi.html

    Note:
        Please download and extract PIPI manually from 
        http://bioinformatics.ust.hk/pipi.html

    Reference:
    Yu, F., Li, N., Yu, W. (2016) PIPI: PTM-Invariant Peptide Identification 
    Using Coding Method. J Prot Res 15(12)
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'PIPI',
        'version': '1.4.6',
        'release_date': '2018-08-23',
        'utranslation_style': 'pipi_style_1',
        'input_extensions': ['.mgf', '.mzML', '.mzXML'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'engine': {
            'platform_independent': {
                'arc_independent': {
                    'exe': 'PIPI-1.4.6.jar',
                    'url': 'http://bioinformatics.ust.hk/pipi.html',
                    'zip_md5': '',
                    'additional_exe': [],
                },
            },
        },
        'citation':
        'Yu, F., Li, N., Yu, W. (2016) PIPI: PTM-Invariant '
            'Peptide Identification Using Coding Method. '
            'J Prot Res 15(12)'
    }

    def __init__(self, *args, **kwargs):
        super(pipi_1_4_5, self).__init__(*args, **kwargs)
        pass


    def write_params_file(self):
        with open(self.param_file_name, 'w') as io:
            print('''# 1.4.6
# First line is the parameter file version. Don't change it.
thread_num = {thread_num}
percolator_path = ursgal/resources/darwin/64bit/percolator_2_08/percolator_2_08

# Database
db = {db}
database_type = Others # Different types have different fasta header patterns. Available values: UniProt, SwissProt, TAIR, ITAG, RefSeq, Others
missed_cleavage = {missed_cleavage}
min_peptide_length = {min_peptide_length}
max_peptide_length = {max_peptide_length}
add_decoy = {add_decoy} # 0 = don't generate and search decoy sequences automatically; 1 = generate and search decoy sequences
add_contaminant = {add_contaminant} # 0 = don't add contaminant proteins automatically; 1 = add contaminant proteins

# Spectrum
ms_level = {ms_level}

# Tolerance
ms1_tolerance_unit = {ms1_tolerance_unit}
ms1_tolerance = {ms1_tolerance}
ms2_tolerance = {ms2_tolerance}
mz_bin_offset = {mz_bin_offset}
min_clear_mz = {min_clear_mz}
max_clear_mz = {max_clear_mz}

# Modification related
min_ptm_mass = {min_ptm_mass}
max_ptm_mass = {max_ptm_mass}

# Isotopic labelling strategy
15N = {15N} # 1: 15N. 0: 14N.

# considered modifications in generating tags
# specify additional mass and amino acid. DO NOT change the last character.
# maximum number is 10
# empty entries must start with 0.0
mod01 = {mod01}
mod02 = {mod02}
mod03 = {mod03}
mod04 = {mod04}
mod05 = {mod05}
mod06 = {mod06}
mod07 = {mod07}
mod08 = {mod08}
mod09 = {mod09}
mod10 = {mod10}

# considered peptide/protein N/C-terminal modifications in generating tags
# empty ones must with value 0.0
# the maximum number for each terminal is 9
Nterm = {pepNterm}
Cterm = {pepCterm}

# Fix modification
G = {G}
A = {A}
S = {S}
P = {P}
V = {V}
T = {T}
C = {C}
I = {I}
L = {L}
N = {N}
D = {D}
Q = {Q}
K = {K}
E = {E}
M = {M}
H = {H}
F = {F}
R = {R}
Y = {Y}
W = {W}
O = {O}
U = {U}
n = {n}
c = {c}

# Enzyme digestion specificities
# enzyme name    is cut from C-term      cleavage site   protection site
{enzyme}

# Do not change the following
output_percolator_input = 1
'''.format(
                **self.params_to_write),
                file=io
            )
        return
