#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import pprint
import sys
import random
import time
import re


AAs = 'ACDEFGHIKLMNPQRSTVWY'


def generate_random_peptides(min_size=6, max_size=11, n=100000):
    peptides = []
    start = time.time()
    for iteration in range(n):
        aa_len = random.randrange(min_size, max_size)
        peptide = ''
        for _ in range(aa_len):
            peptide += random.choice(AAs)
        peptides.append(peptide)
    stop = time.time()
    print('\nPeptide generation took {0:.3f}s ..'.format(stop - start))
    return peptides


def main(fasta_file, mapper_class_version):
    '''
    Maps 100.000 peptides using regex or upeptide_master

    Usage:
    ./map_peptides_to_fasta_comparison.py <fasta_file> <class_name>

    Class name can be
        * 'UPeptideMapper_v4'
        * 'UPeptideMapper_v3'
        * 'UPeptideMapper_v2'

    '''
    print()
    ITERATIONS = 100000
    peptides = generate_random_peptides(n=ITERATIONS)
    print(
        'Generate {0}  peptides'.format(
            len(peptides)
        )
    )
    print(
        'Generate {0} unique peptides'.format(
            len(set(peptides))
        )
    )
    uc = ursgal.UController(verbose=False)

    start = time.time()
    upapa_class = uc.unodes['upeptide_mapper_1_0_0']['class'].import_engine_as_python_function(
        mapper_class_version
    )
    if mapper_class_version == 'UPeptideMapper_v3':
        upeptide_mapper = upapa_class(fasta_file)
        fasta_name = upeptide_mapper.fasta_name
        args = [
            list(peptides),
            fasta_name
        ]
    elif mapper_class_version == 'UPeptideMapper_v4':
        upeptide_mapper = upapa_class(fasta_file)
        args = [
            list(peptides)
        ]
    else:
        upeptide_mapper = upapa_class(word_len=6)
        fasta_name = upeptide_mapper.build_lookup_from_file(fasta_file)
        args = [
            list(peptides),
            fasta_name
        ]

    stop = time.time()
    print(
        'With class {0} fasta Lookup generation took {1:.3f}s'.format(
            mapper_class_version,
            stop - start
        )
    )

    # exit(1)
    start = time.time()
    # for peptide in peptides:
    upeptide_mapper.map_peptides(*args)
    stop = time.time()
    print(
        'With class {0} peptide mapping took {1:.3f}s'.format(
            mapper_class_version,
            stop - start
        )
    )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(main.__doc__)
    else:
        main(sys.argv[1], sys.argv[2])
