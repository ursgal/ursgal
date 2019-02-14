#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import csv
from collections import defaultdict as ddict
import os
import glob
import math

params = {
    'database': os.path.join(
        os.pardir,
        'example_data',
        'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
    ),
    'csv_filter_rules': [
        ['Is decoy', 'equals', 'false'],
        ['PEP', 'lte', 0.01],
    ],
}
# We specify all search engines and validation engines that we want
# to use in a list (version numbers might differ on windows or mac):
search_engines = [
    'omssa',
    'xtandem_piledriver',
    'msgfplus_v9979',
    # 'myrimatch_2_1_138',
    # 'msamanda_1_0_0_5243',
]

validation_engines = [
    'percolator_2_08',
    'qvality',
]

# The different levels with different modifications
# for the cascade are defined
cascade = {
    '0': [
        'C,fix,any,Carbamidomethyl'
    ],
    '1': [
        'C,fix,any,Carbamidomethyl',
        'N,opt,any,Deamidated',
        'Q,opt,any,Deamidated'
    ],
    '2': [
        'C,fix,any,Carbamidomethyl',
        '*,opt,Prot-N-term,Acetyl'
    ],
    '3': [
        'C,fix,any,Carbamidomethyl',
        'M,opt,any,Oxidation'
    ],
    '4': [
        'C,fix,any,Carbamidomethyl',
        'E,opt,any,Methyl',
        'K,opt,any,Methyl',
        'R,opt,any,Methyl'
    ],
    '5': [
        'C,fix,any,Carbamidomethyl',
        'S,opt,any,Phospho',
        'T,opt,any,Phospho'
    ],
}

mass_spectrometer = 'LTQ XL low res'

get_params = {
    'ftp_url': 'ftp.peptideatlas.org',
    'ftp_login': 'PASS00269',
    'ftp_password': 'FI4645a',
    'ftp_include_ext': [
        'JB_FASP_pH8_2-3_28122012.mzML',
        'JB_FASP_pH8_2-4_28122012.mzML',
        'JB_FASP_pH8_3-1_28122012.mzML',
        'JB_FASP_pH8_4-1_28122012.mzML',
    ],
    'ftp_output_folder': os.path.join(
        os.pardir,
        'example_data',
        'cascade_search'
    ),
    'http_url': 'https://www.sas.upenn.edu/~sschulze/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
    'http_output_folder': os.path.join(
        os.pardir,
        'example_data'
    )
}


def get_files():
    uc = ursgal.UController(
        params=get_params
    )
    if os.path.exists(params['database']) is False:
        uc.fetch_file(
            engine='get_http_files_1_0_0'
        )

    if os.path.exists(get_params['ftp_output_folder']) is False:
        os.makedirs(get_params['ftp_output_folder'])
    uc.fetch_file(
        engine='get_ftp_files_1_0_0'
    )

    spec_files = []
    for mzML_file in glob.glob(
        os.path.join(
            get_params['ftp_output_folder'],
            '*.mzML'
        )
    ):
        spec_files.append(mzML_file)

    return spec_files


def search(validation_engine):
    '''
    Executes a cascade search on four example files from the 
    data from Barth et al.

    usage:
        ./cascade_search_example.py

    Searches for peptides using a cascade search approach similar to Kertesz-Farkas et al.
    for which spectra were first searched for unmodified peptides, followed by consecutive searches
    for the following modifications: 
    oxidation of M,
    deamidation of N/Q,
    methylation of E/K/R,
    N-terminal acetylation,
    phosphorylation of S/T.
    After each step, spectra with a PSM below 1 % PEP were removed. 
    '''
    # Initializing the uPLANIT UController class with
    # our specified modifications and mass spectrometer
    uc = ursgal.UController(
        profile=mass_spectrometer,  # 'LTQ XL low res' profile!
        params=params
    )
    # complete workflow for every level of the cascade:
    # every spectrum file is searched with every search engine,
    # results are validated seperately,
    # validated results are merged and filtered for targets and PEP <= 0.01.

    def workflow(spec_file, prefix=None, validation_engine=None, filter_before_validation=False, force=False):
        validated_results = []

        # Convert mzML to MGF outside the loop, so this step is not repeated in
        # the loop
        mgf_spec_file = uc.convert(
            input_file=spec_file,
            engine='mzml2mgf_1_0_0'
        )
        for search_engine in search_engines:
            uc.params['prefix'] = prefix
            unified_search_results = uc.search(
                input_file=mgf_spec_file,
                engine=search_engine,
                force=force,
            )
            uc.params['prefix'] = ''

            if filter_before_validation == True:
                uc.params['csv_filter_rules'] = [
                    ['Modifications', 'contains', '{0}'.format(
                        cascade[level][1].split(',')[3])]
                ]
                filtered_search_results = uc.execute_misc_engine(
                    input_file=unified_search_results,
                    engine='filter_csv_1_0_0'
                )
            else:
                filtered_search_results = unified_search_results
            validated_search_results = uc.validate(
                input_file=filtered_search_results,
                engine=validation_engine,
                force=force,
            )
            validated_results.append(validated_search_results)

        validated_results_from_all_engines = uc.execute_misc_engine(
            input_file=sorted(validated_results),
            engine='merge_csvs_1_0_0',
            force=force,
        )
        uc.params['csv_filter_rules'] = [
            ['Is decoy', 'equals', 'false'],
            ['PEP', 'lte', 0.01],
        ]
        filtered_validated_results = uc.execute_misc_engine(
            input_file=validated_results_from_all_engines,
            engine='filter_csv_1_0_0'
        )
        return filtered_validated_results

    result_files = []
    for spec_file in spec_files:
        spectra_with_PSM = set()
        for level in sorted(cascade.keys()):
            uc.params['modifications'] = cascade[level]
            if level == '0':
                results = workflow(
                    spec_file,
                    validation_engine=validation_engine,
                    prefix='cascade-lvl-{0}'.format(level)
                )
            else:
                uc.params['scan_exclusion_list'] = list(spectra_with_PSM)
                results = workflow(
                    spec_file,
                    validation_engine=validation_engine,
                    filter_before_validation=True,
                    force=True,
                    prefix='cascade-lvl-{0}'.format(level)
                )
            result_files.append(results)
            #  spectrum IDs for PSMs are written into an exclusion list for the next level of the cascade search,
            #  these spectra will b excluded during mzml2mgf conversion
            with open(results) as in_file:
                csv_input = csv.DictReader(in_file)
                for line_dict in csv_input:
                    spectra_with_PSM.add(line_dict['Spectrum ID'])
            print(
                'Number of spectra that will be removed for the next cacade level: {0}'.format(
                    len(spectra_with_PSM)
                )
            )

    results_all_files = uc.execute_misc_engine(
        input_file=sorted(result_files),
        engine='merge_csvs_1_0_0',
    )
    return results_all_files


def analyze(collector):
    '''
    Simle analysis script for the cascade search,
    counting the number of identified peptides (combination of peptide sequence and modifications)
    and PSMs (additionally include the spectrum ID)
    '''

    mod_list = [
        'Oxidation',
        'Deamidated',
        'Methyl',
        'Acetyl',
        'Phospho'
    ]
    fieldnames = [
        'approach',
        'count_type',
        'validation_engine',
        'unmodified',
        'multimodified'
    ] + mod_list + ['total']

    csv_writer = csv.DictWriter(open('cascade_results.csv', 'w'), fieldnames)
    csv_writer.writeheader()
    uc = ursgal.UController()
    uc.params['validation_score_field'] = 'PEP'
    uc.params['bigger_scores_better'] = False

    # Count the number of identified peptides and PSMs for the different modifications
    # Spectra with multiple PSMs are sanitized, i.e. only the PSM with best PEP score is counted
    # and only if the best hit has a PEP that is at least two orders of
    # magnitude smaller than the others
    for validation_engine, result_file in collector.items():
        counter_dict = {
            'psm': ddict(set),
            'pep': ddict(set)
        }
        grouped_psms = uc._group_psms(
            result_file, validation_score_field='PEP', bigger_scores_better=False)
        for spec_title, grouped_psm_list in grouped_psms.items():
            best_score, best_line_dict = grouped_psm_list[0]
            if len(grouped_psm_list) > 1:
                second_best_score, second_best_line_dict = grouped_psm_list[1]
                best_peptide_and_mod = best_line_dict[
                    'Sequence'] + best_line_dict['Modifications']
                second_best_peptide_and_mod = second_best_line_dict[
                    'Sequence'] + second_best_line_dict['Modifications']

                if best_peptide_and_mod == second_best_peptide_and_mod:
                    line_dict = best_line_dict
                elif best_line_dict['Sequence'] == second_best_line_dict['Sequence']:
                    if best_score == second_best_score:
                        line_dict = best_line_dict
                    else:
                        if (-1 * math.log10(best_score)) - (-1 * math.log10(second_best_score)) >= 2:
                            line_dict = best_line_dict
                        else:
                            continue
                else:
                    if (-1 * math.log10(best_score)) - (-1 * math.log10(second_best_score)) >= 2:
                        line_dict = best_line_dict
                    else:
                        continue
            else:
                line_dict = best_line_dict

            count = 0
            for mod in mod_list:
                if mod in line_dict['Modifications']:
                    count += 1
            key_2_add = ''
            if count == 0:
                key_2_add = 'unmodified'
            elif count >= 2:
                key_2_add = 'multimodified'
            elif count == 1:
                for mod in mod_list:
                    if mod in line_dict['Modifications']:
                        key_2_add = mod
                        break
            # for peptide identification comparison
            counter_dict['pep'][key_2_add].add(
                line_dict['Sequence'] + line_dict['Modifications']
            )
            # for PSM comparison
            counter_dict['psm'][key_2_add].add(
                line_dict['Spectrum Title'] +
                line_dict['Sequence'] + line_dict['Modifications']
            )
        for counter_key, count_dict in counter_dict.items():
            dict_2_write = {
                'approach': 'cascade',
                'count_type': counter_key,
                'validation_engine': validation_engine
            }
            total_number = 0
            for key, obj_set in count_dict.items():
                dict_2_write[key] = len(obj_set)
                total_number += len(obj_set)
            dict_2_write['total'] = total_number
            csv_writer.writerow(dict_2_write)
    return

if __name__ == '__main__':
    spec_files = get_files()
    collector = {}
    for validation_engine in validation_engines:
        results_all_files = search(validation_engine)
        print('>>> ', 'final results for {0}'.format(
            validation_engine), ' were written into:')
        print('>>> ', results_all_files)
        collector[validation_engine] = results_all_files
    analyze(collector)
    print('>>> ', 'number of identified peptides and PSMs were written into:')
    print('>>> ', 'cascade_results.csv')
