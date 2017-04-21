#!/usr/bin/env python3.4
# encoding: utf-8


import ursgal
import glob
import os.path
import sys
import time

def main( class_version):
    '''

    Example script to demonstrate speed and memory efficiency of the new 
    upeptide_mapper.

    All tryptic peptides (n=1,094,395, 6 < len(peptide) < 40 ) are mapped to the 
    Chlamydomonas reinhardtii (38876 entries) target-decoy database.

    usage:
        ./complete_chlamydomonas_proteome_match.py <class_version>
    
    Class versions
        * UPeptideMapper_v2
        * UPeptideMapper_v3
        * UPeptideMapper_v4

    '''

    input_params = {
        'database' : os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'http_url': 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/misc/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta' ,
        'http_output_folder' : os.path.join(
            os.pardir,
            'example_data',
        )
    }

    uc = ursgal.UController(
        params = input_params
    )

    if os.path.exists(input_params['database']) is False:
        uc.fetch_file(
            engine     = 'get_http_files_1_0_0'
        )
    print('Parsing fasta and digesting sequences')
    peptides = set()
    digest_start = time.time()
    for fastaID, sequence in ursgal.ucore.parseFasta( open( input_params['database'], 'r' ) ):
        tryptic_peptides = ursgal.ucore.digest(
            sequence,
            ('KR', 'C'),
            no_missed_cleavages = True
        )
        for p in tryptic_peptides:
            if 6 <= len(p) <= 40:  
                peptides.add( p )
    print(
        'Parsing fasta and digesting sequences took {0:1.2f} seconds'.format(
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
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ]
    p2p_mappings = peptide_mapper.map_peptides(*args)
    print(
        'Buffering fasta and mapping {0} peptides took {1:1.2f} seconds'.format(
            len(peptides),
            time.time() - map_start
        )
    )
    if len(p2p_mappings.keys()) == len(peptides):
        print('All peptides have been mapped!')
    else:
        print('WARNING: Not all peptide have been mapped')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(main.__doc__)
        exit()
    main(sys.argv[1])