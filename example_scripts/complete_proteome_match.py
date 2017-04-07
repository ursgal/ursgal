#!/usr/bin/env python3.4
# encoding: utf-8


import ursgal
import glob
import os.path
import sys
import time

def main(fasta_database, class_version):
    '''

    Example script to demonstrate speed and memory efficiency of the new 
    upeptide_mapper.
    
    Specify fasta_database and class_version as input.

    usage:
        ./complete_proteome_match.py <fasta_database> <class_version>
    
    Class versions
        * UPeptideMapper_v2
        * UPeptideMapper_v3
        * UPeptideMapper_v4

    '''

    input_params = {
        'database' : sys.argv[1],
    }

    uc = ursgal.UController(
        params = input_params
    )

    print('Parsing fasta and digesting sequences')
    peptides = set()
    digest_start = time.time()
    for fastaID, sequence in ursgal.ucore.parseFasta( open( input_params['database'], 'r' ) ):
        tryptic_peptides = ursgal.ucore.digest(
            sequence,
            ('KR', 'C'),
            # no_missed_cleavages = True
        )
        for p in tryptic_peptides:
            if 6 <= len(p) <= 40:  
                peptides.add( p )
    print(
        'Parsing fasta and digesting sequences took {0} seconds'.format(
            time.time() - digest_start
        )
    )

    upapa_class = uc.unodes['upeptide_mapper_1_0_0']['class'].import_engine_as_python_function(
        class_version
    )

    print('Buffering fasta and mapping {0} peptides'.format(len(peptides)))
    map_start = time.time()  
    peptide_mapper = upapa_class(
        fasta_database = input_params['database']
    )
    if class_version == 'UPeptideMapper_v4':
        args = [
            list(peptides)
        ]
    else:
        args = [
            list(peptides),
            os.path.basename(fasta_database)
        ]
    p2p_mappings = peptide_mapper.map_peptides(*args)
    print(
        'Buffering fasta and mapping {0} peptides took {1} seconds'.format(
            len(peptides),
            time.time() - map_start
        )
    )
    if len(p2p_mappings.keys()) == len(peptides):
        print('All peptides have been mapped!')
    else:
        print('WARNING: Not all peptide have been mapped')

if __name__ == "__main__":

    main(sys.argv[1], sys.argv[2])