#!/usr/bin/env python
# encoding: utf-8

import sugarpy
import ursgal
import sys
import os
import statistics
import pickle
from collections import namedtuple


def main(
    ident_file=None,
    unimod_glycans_incl_in_search=[],
    use_median_accuracy='all',
    max_tree_length=10,
    monosaccharides=None,
    mzml_file=None,
    scan_rt_lookup=None,
    rt_border_tolerance=1,
    charges=[1, 2],
    output_file=None,
    pyqms_params={},
    min_spec_number=1,
    min_tree_length=1,
    max_trees_per_spec=5,
    min_sugarpy_score=0,
    min_sub_cov=0.0,
    ms_level=1,
    force=False,
):
    '''
    required: ident file, mzml_file, monosaccharides
    '''


    assert ident_file is not None, '''
    [Error] ident_file is required '''
    assert mzml_file is not None, '''
    [Error] mzml_file is required '''
    assert output_file is not None, '''
    [Error] output_file is required '''
    assert monosaccharides is not None, '''
    [Error] No monosaccharide compositions are given '''

    sp_run = sugarpy.run.Run(
        monosaccharides=monosaccharides
    )

    peptide_lookup = sp_run.parse_ident_file(
        ident_file=ident_file,
        unimod_glycans_incl_in_search=unimod_glycans_incl_in_search,
    )
    pep_unimod_list = list(peptide_lookup.keys())
    peps_with_glycans = sp_run.add_glycans2peptide(
        peptide_list=pep_unimod_list,
        max_tree_length=max_tree_length,
        # monosaccharides=monosaccharides,
    )

    if scan_rt_lookup is None or scan_rt_lookup == 'create_new_lookup':
        lookup_dict = sp_run.build_rt_lookup(mzml_file, ms_level)
    else:
        with open(scan_rt_lookup, 'rb') as lookup_pkl:
            lookup_dict = pickle.load(lookup_pkl)
    mzml_basename = os.path.basename(mzml_file).replace('.mzML', '')
    scan2rt = lookup_dict[mzml_basename]['scan_2_rt']

    ppm_offset = 0
    if use_median_accuracy == 'all':
        all_accuracies = []
        for pep in peptide_lookup.keys():
            all_accuracies.extend(peptide_lookup[pep]['accuracy'])
        ppm_offset = statistics.median(all_accuracies)

    if output_file is None:
        output_file = '{0}_sugarpy.csv'.format(
            ident_file.replace('.csv', '')
        )
    output_folder = os.path.dirname(output_file)

    pyqms_results = {}
    for n, peptide_unimod in enumerate(sorted(peps_with_glycans)):
        # if n > 1:
        #     continue
        pkl_name = '-'.join(peptide_unimod.split(';'))
        pkl_name = '_'.join(pkl_name.split(':'))
        rt_min = min(peptide_lookup[peptide_unimod]
                     ['rt']) - rt_border_tolerance
        rt_max = max(peptide_lookup[peptide_unimod]
                     ['rt']) + rt_border_tolerance
        if use_median_accuracy == 'peptide':
            ppm_offset = statistics.median(
                peptide_lookup[peptide_unimod]['accuracy']
            )
        pyqms_params['MACHINE_OFFSET_IN_PPM'] = ppm_offset
        print(
            '[ SugarPy  ] Quantification for peptide ',
            peptide_unimod,
            '#{0} out of {1}'.format(
                n + 1,
                len(peps_with_glycans)
            )
        )
        results_pkl = sp_run.quantify(
            molecule_name_dict=peps_with_glycans[peptide_unimod],
            rt_window=(rt_min, rt_max),
            ms_level=ms_level,
            charges=charges,
            params=pyqms_params,
            pkl_name=os.path.join(
                output_folder,
                '{0}_{1}_pyQms_results.pkl'.format(
                    mzml_basename,
                    pkl_name
                )
            ),
            mzml_file=mzml_file,
            force=force,
            # spectra=[],
        )
        pyqms_results[peptide_unimod] = results_pkl

    validated_results = sp_run.validate_results(
        pyqms_results_dict=pyqms_results,
        min_spec_number=min_spec_number,
        min_tree_length=min_tree_length,
        # monosaccharides=monosaccharides,
    )
    sp_results = sugarpy.results.Results(
        validated_results=validated_results,
        monosaccharides=monosaccharides
    )
    sp_results.write_results2csv(
        output_file=output_file,
        max_trees_per_spec=max_trees_per_spec,
        min_sugarpy_score=min_sugarpy_score,
        min_sub_cov=min_sub_cov,
        peptide_lookup=peptide_lookup,
        # monosaccharides=monosaccharides,
        scan_rt_lookup=scan2rt,
        mzml_basename=mzml_basename,
    )
    output_pkl = output_file.replace('.csv', '.pkl')
    with open(output_pkl, 'wb') as out_pkl:
        pickle.dump(sp_results, out_pkl)
    print('Done.')

if __name__ == '__main__':
    mzml_file = sys.argv[1]
    ident_file = sys.argv[2]
    output_file = ident_file.replace('.csv', '_sugarpy.csv')
    scan_rt_lookup = sys.argv[3]
    if scan_rt_lookup == 'None':
        scan_rt_lookup = None
    force = False
    if len(sys.argv) >= 4:
        if sys.argv[4] == 'True':
            force = True
    main(
        ident_file=ident_file,
        unimod_glycans_incl_in_search=[
            'HexNAc',
            'HexNAc(2)',
        ],
        use_median_accuracy='all',  # 'peptide', False
        max_tree_length=10,
        monosaccharides={
            "dHex": 'C6H10O4',
            # "dHexNAc": 'C8H13NO4',
            "Hex": 'C6H10O5',
            # "HexA": 'C6H8O6',
            "HexNAc": 'C8H13NO5',
            "Me2Hex": 'C8H14O5',
            "MeHex": 'C7H12O5',
            # "NeuAc": 'C11H17NO8',
            "Pent": 'C5H8O4',
            # 'dHexN': 'C6H11O3N',
            # 'HexN': 'C6H11O4N',
            # 'MeHexA': 'C7H10O6',
        },
        mzml_file=mzml_file,
        scan_rt_lookup=scan_rt_lookup,
        force=force,
        rt_border_tolerance=1,
        charges=[1, 2, 3],
        output_file=output_file,
        pyqms_params={},
        min_spec_number=1,
        min_tree_length=1,
        max_trees_per_spec=5,
        min_sugarpy_score=0,
        min_sub_cov=0.5,
        ms_level=1,
    )
