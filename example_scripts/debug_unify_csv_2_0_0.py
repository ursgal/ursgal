#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys
import shutil
from collections import defaultdict as ddict
import csv


def main():
    '''

    '''
    uc = ursgal.UController(
        profile='LTQ XL low res',
        params={
            'database': os.path.join(
                os.pardir,
                'example_data',
                'BSA.fasta'
            ),
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl',    # N-Acteylation
            ],
            # use all header mames here? Mega Venn set key :)
            'visualization_column_names' : [
                'Spectrum ID',
                # 'Spectrum Title',
                'Sequence',
                'Exp m/z',
                'Modifications',
                'Charge',
                'Calc m/z',
                'Protein ID',
                'Sequence Start',
                'Sequence Stop',
                'Sequence Pre AA',
                'Sequence Post AA',
                # 'uCalc m/z',
                # 'Accuracy (ppm)',
                # 'Mass Difference',
                'Complies search criteria',
                'Conflicting uparam',
                'Is decoy',
                'Retention Time (s)',
                # 'Raw data location'
            ],
            'msgfplus_mzid_converter_version' : 'msgfplus_C_mzid2csv_v2017_07_04'
        }
    )

    engine_list = [
        'omssa', # verified so far
        'xtandem_alanine',
        'msgfplus_v2018_01_30',
        # 'msfragger'
    ]

    mzML_file = os.path.join(
        os.pardir,
        'example_data',
        'debug_unify_csv_2_0_0',
        'BSA1.mzML'
    )
    if os.path.exists(mzML_file) is False:
        uc.params['http_url'] = 'http://sourceforge.net/p/open-ms/code/HEAD/tree/OpenMS/share/OpenMS/examples/BSA/BSA1.mzML?format=raw'
        uc.params['http_output_folder'] = os.path.dirname(mzML_file)
        uc.fetch_file(
            engine='get_http_files_1_0_0',
        )
        try:
            shutil.move(
                '{0}?format=raw'.format(mzML_file),
                mzML_file
            )
        except:
            shutil.move(
                '{0}format=raw'.format(mzML_file),
                mzML_file
            )

    duplicated_mzML_file =  mzML_file.replace(
        '.mzML',
        '_copy.mzML'
    )
    if os.path.exists(duplicated_mzML_file) is False:
        shutil.copy(mzML_file, duplicated_mzML_file)

    unify_csv_engine_and_mzML_list = [
        ('unify_csv_2_0_0', duplicated_mzML_file ),
        ('unify_csv_1_0_0', mzML_file),
    ]
    uc.params['visualization_label_positions'] = {}
    for pos, (ue, mzML) in enumerate(unify_csv_engine_and_mzML_list):
        uc.params['visualization_label_positions'][str(pos)] = ue

    verification_results = ddict(dict)

    for engine in engine_list:
        verification_results[engine] = ddict(int)
        unified_file_list = []
        results = ddict(dict)
        for unify_csv_converter_version, mzML_target in unify_csv_engine_and_mzML_list :
            uc.params['unify_csv_converter_version'] = unify_csv_converter_version
            unified_search_result_file = uc.search(
                input_file=mzML_target,
                engine=engine,
                force=True
            )
            unified_file_list.append(
                unified_search_result_file
            )

            for line_dict in csv.DictReader(open(unified_search_result_file,'r')):
                key = '{Spectrum ID}||{Sequence}||{Modifications}||{Charge}'.format(
                    **line_dict
                )
                results[unify_csv_converter_version][ key ] = line_dict

        if len(unified_file_list) == 2 :
            uc.visualize(
                input_files=unified_file_list,
                engine='venndiagram',
                force=True
            )

        # compare result files
        # order should be the same
        assert len(results['unify_csv_1_0_0']) == len(results['unify_csv_2_0_0'])
        for key, line_dict_v1 in results['unify_csv_1_0_0'].items():
            line_dict_v2 = results['unify_csv_2_0_0'][key]

            for k, v in line_dict_v1.items():
                if k not in uc.params['visualization_column_names']:
                    continue
                if v == line_dict_v2[k]:
                    verification_results[engine]['values identical'] += 1
                else:
                    print(
                        '''
                        key {0} values not consistent
                        unify_csv_1_0_0 : {1}
                        unify_csv_2_0_0 : {2}
                        '''.format(
                            k,
                            v,
                            line_dict_v2[k]
                        )
                    )
                    verification_results[engine]['values conflicting'] += 1
                    # exit()
                verification_results[engine]['values tested'] += 1
    print()
    print('Verification summary')
    for engine, report_dict in verification_results.items():
        print(
            'Engine: {0}'.format(
                engine
            )
        )
        for k, v in sorted(report_dict.items()):
            print(
                '\t{0}: {1}'.format(
                    k,
                    v
                )
            )
        print()
    return


if __name__ == '__main__':
    main()
