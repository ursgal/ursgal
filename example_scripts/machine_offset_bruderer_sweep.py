#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import glob
import csv
import os
from collections import defaultdict as ddict
import sys
import re


MQ_OFFSET_TO_FILENAME = [
    (4.71,  'B_D140314_SGSDSsample2_R01_MSG_T0.mzML'),
    (4.98,  'B_D140314_SGSDSsample6_R01_MSG_T0.mzML'),
    (4.9,   'B_D140314_SGSDSsample1_R01_MSG_T0.mzML'),
    (5.41,  'B_D140314_SGSDSsample4_R01_MSG_T0.mzML'),
    (5.78,  'B_D140314_SGSDSsample5_R01_MSG_T0.mzML'),
    (6.01,  'B_D140314_SGSDSsample8_R01_MSG_T0.mzML'),
    (6.22,  'B_D140314_SGSDSsample7_R01_MSG_T0.mzML'),
    (6.83,  'B_D140314_SGSDSsample3_R01_MSG_T0.mzML'),
    (7.61,  'B_D140314_SGSDSsample4_R02_MSG_T0.mzML'),
    (7.59,  'B_D140314_SGSDSsample8_R02_MSG_T0.mzML'),
    (7.93,  'B_D140314_SGSDSsample6_R02_MSG_T0.mzML'),
    (7.91,  'B_D140314_SGSDSsample1_R02_MSG_T0.mzML'),
    (8.23,  'B_D140314_SGSDSsample3_R02_MSG_T0.mzML'),
    (8.33,  'B_D140314_SGSDSsample7_R02_MSG_T0.mzML'),
    (9.2,   'B_D140314_SGSDSsample5_R02_MSG_T0.mzML'),
    (9.4,   'B_D140314_SGSDSsample2_R02_MSG_T0.mzML'),
    (9.79,  'B_D140314_SGSDSsample1_R03_MSG_T0.mzML'),
    (10.01, 'B_D140314_SGSDSsample3_R03_MSG_T0.mzML'),
    (10.03, 'B_D140314_SGSDSsample7_R03_MSG_T0.mzML'),
    (10.58, 'B_D140314_SGSDSsample2_R03_MSG_T0.mzML'),
    (11.1,  'B_D140314_SGSDSsample4_R03_MSG_T0.mzML'),
    (11.21, 'B_D140314_SGSDSsample5_R03_MSG_T0.mzML'),
    (11.45, 'B_D140314_SGSDSsample6_R03_MSG_T0.mzML'),
    (12.19, 'B_D140314_SGSDSsample8_R03_MSG_T0.mzML'),
]

GENERAL_PARAMS = {
    'database': os.path.join(
        os.pardir,
        'example_data',
        'hs_201303_qs_sip_target_decoy.fasta'
    ),
    'modifications': [
        'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
    ],
    'scan_skip_modulo_step': 10,
    'http_url': 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/misc/hs_201303_qs_sip_target_decoy.fasta',
    'http_output_folder': os.path.join(
        os.pardir,
        'example_data'
    )
}


def search(input_folder=None):
    '''
    Does the parameter sweep on every tenth MS2 spectrum of the data from
    Bruderer et al. (2015) und X!Tandem Sledgehammer.

    Note:

        Please download the .RAW data for the DDA dataset from peptideatlas.org
        (PASS00589, password: WF6554orn) and convert to mzML.
        Then the script can be executed with the folder with the mzML files as
        the first argument.

    Warning:

        This script (if the sweep ranges are not changed) will perform 10080
        searches which will produce approximately 100 GB output (inclusive mzML
        files)

    usage:

        ./machine_offset_bruderer_sweep.py <folder_with_bruderer_data>

    Sweeps over:

        * machine_offset_in_ppm from -20 to +20 ppm offset
        * precursor mass tolerance from 1 to 5 ppm
        * fragment mass tolerance from -2.5 to 20 ppm

    The search can be very time consuming (depending on your machine/cluster),
    therefor the analyze step can be performed separately by calling analyze()
    instead of search() when one has already performed the searches and wants
    to analyze the results.
    '''

    file_2_target_offset = {}
    for MQ_offset, file_name in MQ_OFFSET_TO_FILENAME:
        file_2_target_offset[file_name] = {'offsets': []}
        for n in range(-20, 20, 2):
            file_2_target_offset[file_name]['offsets'].append(n)

    engine_list = ['xtandem_sledgehammer']

    frag_ion_tolerance_list = [2.5, 5, 10, 20]

    precursor_ion_tolerance_list = [1, 2, 3, 4, 5]

    R = ursgal.UController(
        profile='QExactive+',
        params=GENERAL_PARAMS
    )

    if os.path.exists(R.params['database']) is False:
        R.fetch_file(
            engine='get_http_files_1_0_0'
        )

    prefix_format_string = '_pit_{1}_fit_{2}'
    for mzML_path in glob.glob(os.path.join(input_folder, '*.mzML')):

        mzML_basename = os.path.basename(mzML_path)
        if mzML_basename not in file_2_target_offset.keys():
            continue
        for ppm_offset in file_2_target_offset[mzML_basename]['offsets']:
            R.params['machine_offset_in_ppm'] = ppm_offset
            R.params['prefix'] = 'ppm_offset_{0}'.format(
                int(ppm_offset)
            )
            mgf_file = R.convert(
                input_file=mzML_path,
                engine='mzml2mgf_1_0_0'
            )
            for engine in engine_list:
                for precursor_ion_tolerane in precursor_ion_tolerance_list:
                    for frag_ion_tolerance in frag_ion_tolerance_list:

                        new_prefix = prefix_format_string.format(
                            precursor_ion_tolerane,
                            frag_ion_tolerance
                        )
                        R.params[
                            'precursor_mass_tolerance_minus'] = precursor_ion_tolerane
                        R.params[
                            'precursor_mass_tolerance_plus'] = precursor_ion_tolerane
                        R.params['frag_mass_tolerance'] = frag_ion_tolerance
                        R.params['prefix'] = new_prefix

                        unified_search_result_file = R.search(
                            input_file=mzML_path,
                            engine=engine,
                            force=False,
                        )

    return


def analyze(folder):
    '''

    Parses the result files form search and write a result .csv file which
    contains the data to plot figure 2.

    '''

    R = ursgal.UController(
        profile='QExactive+',
        params=GENERAL_PARAMS
    )
    csv_collector = {}
    ve = 'qvality_2_02'

    sample_regex_pattern = 'sample\d_R0\d'

    sample_2_x_pos_and_mq_offset = {}

    sample_offset_combos = []

    all_tested_offsets = [str(n) for n in range(-20, 21, 2)]

    for pos, (mq_ppm_off, mzML_file) in enumerate(MQ_OFFSET_TO_FILENAME):
        _sample = re.search(sample_regex_pattern, mzML_file).group()
        sample_2_x_pos_and_mq_offset[_sample] = (pos, mq_ppm_off)
        for theo_offset in all_tested_offsets:
            sample_offset_combos.append((_sample, theo_offset))

    for csv_path in glob.glob(os.path.join('{0}'.format(folder), '*', '*_unified.csv')):
        dirname = os.path.dirname(csv_path)
        sample = re.search(sample_regex_pattern, csv_path).group()
        splitted_basename = os.path.basename(csv_path).split('_')
        offset = splitted_basename[2]
        precursor_ion_tolerance = splitted_basename[4]
        frag_ion_tolerance = splitted_basename[6]
        prefix = '_'.join(splitted_basename[:7])

        R.params['machine_offset_in_ppm'] = offset
        R.params['precursor_mass_tolerance_minus'] = precursor_ion_tolerance
        R.params['precursor_mass_tolerance_plus'] = precursor_ion_tolerance
        R.params['frag_mass_tolerance'] = frag_ion_tolerance
        R.params['prefix'] = prefix

        validated_path = csv_path.replace(
            '_unified.csv',
            '_{0}_validated.csv'.format(ve)
        )
        if os.path.exists(validated_path):
            csv_path = validated_path
        else:
            try:
                csv_path = R.validate(
                    input_file=csv_path,
                    engine=ve
                )
            except:
                continue

        pit_fit = (precursor_ion_tolerance, frag_ion_tolerance)

        if pit_fit not in csv_collector.keys():
            csv_collector[pit_fit] = ddict(set)

        csv_key = (sample, offset)

        print('Reading file: {0}'.format(csv_path))
        for line_dict in csv.DictReader(open(csv_path, 'r')):
            if line_dict['Is decoy'] == 'true':
                continue
            if float(line_dict['PEP']) <= 0.01:
                csv_collector[pit_fit][csv_key].add(
                    '{0}{1}'.format(
                        line_dict['Sequence'],
                        line_dict['Modifications']
                    )
                )

    fieldnames = [
        'Sample',
        'pos',
        'MQ_offset',
        'tested_ppm_offset',
        'peptide_count'
    ]

    outfile_name_format_string = 'bruderer_data_ppm_sweep_precursor_mass_tolerance_{0}_fragment_mass_tolerance_{1}.csv'

    for pit_fit in csv_collector.keys():
        with open(outfile_name_format_string.format(*pit_fit), 'w') as io:
            csv_writer = csv.DictWriter(io, fieldnames)
            csv_writer.writeheader()

            # write missing values
            for sample_offset in sample_offset_combos:
                sample, ppm_offset = sample_offset
                if sample_offset not in csv_collector[pit_fit].keys():
                    dict_2_write = {
                        'Sample': sample,
                        'pos': sample_2_x_pos_and_mq_offset[sample][0],
                        'MQ_offset': '',
                        'tested_ppm_offset': ppm_offset,
                        'peptide_count': 0,
                    }
                    csv_writer.writerow(dict_2_write)

            for (sample, ppm_offset), peptide_set in csv_collector[pit_fit].items():
                dict_2_write = {
                    'Sample': sample,
                    'pos': sample_2_x_pos_and_mq_offset[sample][0],
                    'MQ_offset': sample_2_x_pos_and_mq_offset[sample][1] * -1,
                    'tested_ppm_offset': ppm_offset,
                    'peptide_count': len(peptide_set),
                }
                csv_writer.writerow(dict_2_write)
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(search.__doc__)
        sys.exit(1)
    search(sys.argv[1])
    analyze(sys.argv[1])
