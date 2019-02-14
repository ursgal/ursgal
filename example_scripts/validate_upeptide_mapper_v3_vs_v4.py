#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import glob
import os.path
import sys
import time
import copy


def main():
    '''

    Example script to compare UPeptideMapper v3 vs v4 results.


    usage:
        ./validate_upeptide_mapper_v3_vs_v4.py

    '''

    input_params = {
        'database': os.path.join(
            os.pardir,
            'example_data',
            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
        ),
        'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
        'http_output_folder': os.path.join(
            os.pardir,
            'example_data',
        )
    }

    uc = ursgal.UController(
        params=input_params
    )

    if os.path.exists(input_params['database']) is False:
        uc.fetch_file(
            engine='get_http_files_1_0_0'
        )
    print('Parsing fasta and digesting sequences')
    peptides = set()
    max_number_peptides = 1000000000
    digest_start = time.time()
    for fastaID, sequence in ursgal.ucore.parse_fasta(open(input_params['database'], 'r')):
        tryptic_peptides = ursgal.ucore.digest(
            sequence,
            ('KR', 'C'),
            no_missed_cleavages=True
        )
        for p in tryptic_peptides:
            if 6 <= len(p) <= 40:
                if len(peptides) > max_number_peptides:
                    break
                peptides.add(p)
    print(
        'Parsing fasta and digesting sequences took {0:1.2f} seconds'.format(
            time.time() - digest_start
        )
    )

    # print(peptides)
    upapa_class = uc.unodes['upeptide_mapper_1_0_0']['class'].import_engine_as_python_function(
        'UPeptideMapper_v3'
    )
    print('Buffering fasta and mapping {0} peptides with v3'.format(
        len(peptides)))
    peptide_mapper = upapa_class(input_params['database'])
    fasta_lookup_name = peptide_mapper.fasta_name
    args = [
        list(peptides),
        fasta_lookup_name
    ]
    start_time = time.time()
    v3_p2p_mappings = peptide_mapper.map_peptides(*args)
    print('UPeptideMapper v3 mapper took {0}s'.format(
        time.time() - start_time))
    print('Done')
    v3_p2p_mappings = copy.deepcopy(v3_p2p_mappings)

    upapa_class = uc.unodes['upeptide_mapper_1_0_0']['class'].import_engine_as_python_function(
        'UPeptideMapper_v4'
    )
    print('Buffering fasta and mapping {0} peptides with v4'.format(
        len(peptides)))
    peptide_mapper = upapa_class(input_params['database'])
    args = [
        list(peptides),
    ]
    start_time = time.time()
    v4_p2p_mappings = peptide_mapper.map_peptides(*args)
    print('UPeptideMapper v4 mapper took {0}s'.format(
        time.time() - start_time))
    print('Done')

    assert len(v3_p2p_mappings.keys()) == len(v4_p2p_mappings.keys())
    assert list(sorted(v3_p2p_mappings.keys())) == list(
        sorted(v4_p2p_mappings.keys()))
    compare_keys = [
        'start',
        'end',
        'pre',
        'post',
        'id',
    ]
    num_peps = len(v3_p2p_mappings.keys())
    for ppos, peptide in enumerate(list(sorted(v3_p2p_mappings.keys()))):
        v3_maps = sorted([(d['id'], d['start'], d)
                          for d in v3_p2p_mappings[peptide]])
        v4_maps = sorted([(d['id'], d['start'], d)
                          for d in v4_p2p_mappings[peptide]])
        print(
            'Comparing peptide #{0}/{1}'.format(ppos, num_peps),
            end='\r'
        )
        assert len(v3_maps) == len(v4_maps)

        for pos, (v3_id, v3_start, v3_map_dict) in enumerate(v3_maps):
            v4_id, v4_start, v4_map_dict = v4_maps[pos]
            for key in compare_keys:
                assert v3_map_dict[key] == v4_map_dict[key]


if __name__ == "__main__":
    main()
