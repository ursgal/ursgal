#!/usr/bin/env python3.4
# encoding: utf-8
import ursgal
import pprint
import sys
import random
import time
import re


AAs = 'ACDEFGHIKLMNPQRSTVWY'


def generate_random_peptides( min_size = 6, max_size = 11, n = 100000):
    peptides = []
    start = time.time()
    for iteration in range( n ):
        aa_len = random.randrange( min_size, max_size )
        peptide = ''
        for _ in range(aa_len):
            peptide += random.choice( AAs )
        peptides.append( peptide )
    stop = time.time()
    print('\nPeptide generation took {0:.3f}s ..'.format( stop - start ))
    return peptides


def main( fasta_file ):
    '''
    Maps 100.000 peptides using regex or upeptide_master

    Usage:
    ./map_peptides_to_fasta_comparison.py <fasta_file>
    '''
    print()
    ITERATIONS = 10000
    peptides = generate_random_peptides( n = ITERATIONS)
    print('Generate {0}  peptides'.format( len( peptides)))
    print('Generate {0} unique peptides'.format( len( set(peptides))))
    uc = ursgal.UController( verbose = False )

    start = time.time()
    fasta_name = uc.upeptide_mapper.build_lookup_from_file( fasta_file )
    stop = time.time()
    print('Fasta Lookup generation took {0:.3f}s'.format( stop - start ))
    # exit(1)
    start = time.time()
    for peptide in peptides:
        uc.upeptide_mapper.map_peptide(
            peptide = peptide,
            fasta_name = fasta_name
        )
    stop = time.time()
    print(
        'FCache (default) peptide mapping generation took {0:.3f}s'.format( stop - start )
    )

    start = time.time()
    for peptide in peptides:
        uc.upeptide_mapper.map_peptide(
            peptide = peptide,
            fasta_name = fasta_name,
            force_regex = True
        )
    stop = time.time()
    print('Regex peptide mapping generation took {0:.3f}s'.format( stop - start ))
    print(uc.upeptide_mapper.hits)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print( main.__doc__)
    else:
        main( sys.argv[1] )
