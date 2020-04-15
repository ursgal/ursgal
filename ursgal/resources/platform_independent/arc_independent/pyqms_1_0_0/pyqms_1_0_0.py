#!/usr/bin/env python
# encoding: utf-8
"""
"""
import pyqms
import pymzml

import os
import pickle


def generate_result_pickle(
    mzml_files,
    fixed_labels,
    molecules,
    evidence_files,
    min_charge,
    max_charge,
    label,
    ms_level,
    label_percentile,
    evidence_score_field=None,
    mz_score_percentile=0.4,
    trivial_names=None,
    pyqms_params=None,
    verbose=True
):
    """DOCSTRING."""
    if isinstance(mzml_files, str):
        mzml_files = [mzml_files]
    print('[ -ENGINE- ] Parse Evidences')

    fixed_labels, evidences, molecules = pyqms.adaptors.parse_evidence(
        fixed_labels=fixed_labels,
        evidence_files=evidence_files,
        molecules=molecules,
        evidence_score_field=evidence_score_field
    )

    params = {
        'molecules': molecules,
        'charges': [
            x for x in range(min_charge, max_charge + 1)
        ],
        'params': pyqms_params,
        'metabolic_labels': {
            label: label_percentile,
        },
        'trivial_names': trivial_names,
        'fixed_labels': fixed_labels,
        'verbose': verbose,
        'evidences': evidences
    }
    print('[ -ENGINE- ] Set up Isotopolugue Library')
    lib = pyqms.IsotopologueLibrary(**params)

    print('[ -ENGINE- ] Matching isotopologues to spectra ..')
    results = None
    for mzml_file in mzml_files:
        run = pymzml.run.Reader(
            mzml_file,
            obo_version='1.1.0',
            extraAccessions=[('MS:1000016' , ['value','unitName'])]
        )

        mzml_file_basename = os.path.basename(mzml_file)
        for n, spec in enumerate(run):
            if spec['id'] == 'TIC':
                break
            if n % 100 == 0:
                print(
                    '[ -ENGINE- ] File : {0:^40} : '
                    'Processing spectrum {1}'.format(
                        mzml_file_basename,
                        n,
                    ),
                    end='\r'
                )
            scan_time, unit = spec.scan_time

            if unit == 'second':
                scan_time /= 60
            elif unit != 'minute':
                print('''
                    [Warning] The retention time unit is not recognized or not specified.
                    [Warning] It is assumed to be minutes and continues with that.
                ''')

            if spec['ms level'] == ms_level:
                results = lib.match_all(
                    mz_i_list=spec.centroidedPeaks,
                    file_name=mzml_file_basename,
                    spec_id=spec['id'],
                    spec_rt=scan_time,
                    results=results
                )
        print()
    return results


def main(
    mzml_file=None,
    output_file=None,
    pickle_name=None,
    evidence_files=None,
    fixed_labels=None,
    molecules=None,
    rt_border_tolerance=1,
    label='14N',
    label_percentile=0.0,
    min_charge=1,
    max_charge=5,
    evidence_score_field='PEP',
    ms_level=1,
    trivial_names=None,
    pyqms_params=None,
    verbose=True
):
    """DOCSTRING."""

    rt_summary_file = os.path.join(
        output_file
    )

    results = generate_result_pickle(
        mzml_file,
        fixed_labels,
        molecules,
        evidence_files,
        min_charge,
        max_charge,
        label,
        ms_level,
        label_percentile,
        evidence_score_field,
        trivial_names=trivial_names,
        pyqms_params=pyqms_params,
        verbose=True
    )

    with open(pickle_name, 'wb') as f:
        pickle.dump(results, f)

    results.write_rt_info_file(
        output_file=rt_summary_file,
        rt_border_tolerance=float(rt_border_tolerance)
    )
    results.calc_amounts_from_rt_info_file(
        rt_info_file=rt_summary_file,
        rt_border_tolerance=float(rt_border_tolerance)
    )

    return rt_summary_file

