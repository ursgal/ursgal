#!/usr/bin/env python3.4
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main(database=None,ms_file=None):
    '''
    Example workflow for the open modification search engine TagGraph

    The MS file is first searched with two de novo engines,
    results of those searches are merged and used for the TagGraph search.

    usage:
        ./example_taggraph_workflow.py <mzML_file> <database.fasta>

    '''
    uc = ursgal.UController(
        profile='QExactive+',
        params={
            'database': database,
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                'N,opt,any,Deamidated',
                'Q,opt,any,Deamidated',
            ],
            'peptide_mapper_class_version': 'UPeptideMapper_v3',
            '-xmx': '8000m',
            'csv_filter_rules' : [
                ['Is decoy', 'equals', 'false'],
                ['PEP','lte', 0.01],
                ['Conflicting uparam', 'contains_not', 'enzyme'],
            ],
            'enzyme': 'trypsin',
            'pymzml_spec_id_attribute': {'ID': None},
            'frag_mass_tolerance'       : 20,
            'frag_mass_tolerance_unit'  : 'ppm',
            'precursor_mass_tolerance_plus' : 5,
            'precursor_mass_tolerance_minus' : 5,
            "deepnovo_knapsack_file": "/mnt/Gits/Science/Ursgal/Ursgal/ursgal_feature2/ursgal/resources/platform_independent/arc_independent/deepnovo_pointnovo/knapsack.py",
            "deepnovo_use_lstm": False,
        }
    )

    denovo_list = [
        'deepnovo_pointnovo',
        'novor_1_05',
    ]

    unified_file_list = []
    for engine in denovo_list:
        unified_search_result = uc.search(
            input_file = ms_file,
            engine = engine,
        )

        unified_file_list.append(unified_search_result)

    merged_files = uc.execute_misc_engine(
        input_file=unified_file_list,
        engine='merge_csv',
        merge_duplicates=False,
    )
    uc.params.update({
            'visualization_column_names': ['Modifications', 'Sequence'],
            'visualization_label_positions':{
                '0': 'deepnovo',
                '1': 'novor',
            }
        })
    uc.visualize(
        input_files    = unified_file_list,
        engine         = 'venndiagram_1_1_0',
    )

    uc.params['de_novo_results'] = [merged_files]
    taggraph_search_result = uc.execute_misc_engine(
        input_file = [ms_file],
        engine = 'tag_graph_1_8_0',
    )

    # uc.params['de_novo_results'] = merged_files
    # taggraph_search_result = uc.search(
    #     input_file =[ ms_file],
    #     engine = 'tag_graph_1_8_0',
    # )
    return


if __name__ == '__main__':
    main(ms_file=sys.argv[1], database=sys.argv[2])
