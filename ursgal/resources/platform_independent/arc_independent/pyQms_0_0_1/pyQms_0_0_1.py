#!/usr/bin/env python3
# encoding: utf-8
"""
"""
import pyqms
import pymzml

import os
import argparse
import pickle
import peptide_fragmentor


def set_up_argparser():
    """
    """
    arg_parser = argparse.ArgumentParser(
        description='Calculate peptide amounts.'
    )
    # molecules
    arg_parser.add_argument(
        '-m',
        '--molecules',
        help='Molecules to quantify'
             'Can be either a path to an ident file or a list of strings (or None)',
        type=str,
        action='append',
        default=[]
    )
    # mzml_file name
    arg_parser.add_argument(
        '-i',
        '--input_file',
        help='Name of the input mzML file.',
        type=str
    )
    # output name
    arg_parser.add_argument(
        '-o',
        '--output',
        default='protein_amounts.csv',
        help='Name the output file.',
        type=str
    )
    # evidence file
    arg_parser.add_argument(
        '-e',
        '--evidence_files',
        help='evidence files, (e.g. unified and verified search results',
        type=str,
        action='append'
    )
    # rt_border_tolerance
    arg_parser.add_argument(
        '-rt_border',
        # '--retention_time_border_tolerance',
        help='Border tolerance for retention time when quantifying',
        type=float
    )
    # label
    arg_parser.add_argument(
        '-label',
        help='Labeling method, either 14N or 15N',
        type=str
    )
    # label_percentile
    arg_parser.add_argument(
        '-label_percentile',
        help='label percent, e.g. 0.990',
        type=float
    )
    # max charge
    arg_parser.add_argument(
        '-max_charge',
        help='Maximum considered charge',
        type=int
    )
    # min charge
    arg_parser.add_argument(
        '-min_charge',
        help='Minimum considered charge',
        type=int
    )

    arg_parser.add_argument(
        '-fixed_labels',
        help='Path to file in python dict style specifying fixed labels',
        type=str
    )

    return arg_parser


def fragment_evidences(evidence_files, ions, charges):
    """DOC."""
    for ev in evidence_files:
        pass
    pass


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
    fragment_peptide=False,
    fragments_to_match=None,
    params= {}
):
    """DOCSTRING."""
    if not isinstance(mzml_files, list) and isinstance(mzml_files, str):
        mzml_files = [mzml_files]
    print('[ -ENGINE- ] Parse Evidences')

    if fragment_peptide is True:
        # molecules and evidence are build from the input evidence files
        # we need to parse the file, fragment each peptide and write a similiar csv with the fragments as rows
        # evidence_files = fragment_evidences(evidence_files)
        raise Exception('Not supported yet')
    fixed_labels, evidences, molecules = pyqms.adaptors.parse_evidence(
        fixed_labels=fixed_labels,
        evidence_files=evidence_files,
        molecules=molecules,
        evidence_score_field=evidence_score_field
    )
    params = {
        'molecules'        : molecules,
        'charges'          : [
            x for x in range(min_charge, max_charge + 1)
        ],
        'params'           : params,
        'metabolic_labels' : {
            label              : [0.000, label_percentile],
        },
        'trivial_names'    : None,
        'fixed_labels'     : fixed_labels,
        'verbose'          : False,
        'evidences'        : evidences
    }
    print('[ -ENGINE- ] Set up Isotopolugue Library')
    lib = pyqms.IsotopologueLibrary(**params)

    print('[ -ENGINE- ] Matching isotopologues to spectra ..')
    results            = None
    for mzml_file in mzml_files:
        run = pymzml.run.Reader(
            mzml_file,
            obo_version='1.1.0'
        )

        mzml_file_basename = os.path.basename(mzml_file)
        for n, spec in enumerate(run):
            if spec['id'] == 'TIC':
                break
            if n % 500 == 0:
                print(
                    '[ -ENGINE- ] File : {0:^40} : Processing spectrum {1}'.format(
                        mzml_file_basename,
                        n,
                    ),
                    end='\r'
                )
            scan_time = spec['scan time'] #/ 60.0
            # print(scan_time)
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
    evidence_files=[],
    fixed_labels=None,
    molecules=None,
    rt_border_tolerance=1,
    label='N14',
    label_percentile=0.000,
    min_charge=1,
    max_charge=5,
    evidence_score_field='PEP',
    ms_level=1,
    trivial_names={},
    pyQms_params={},
    write_rt_info_file=True
):
    """DOCSTRING."""
    out_pickle = os.path.join(
        pickle_name
    )

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
        params=pyQms_params
    )

    with open(out_pickle, 'wb') as f:
        pickle.dump(results, f)
    if write_rt_info_file is True:
        results.write_rt_info_file(
            output_file=rt_summary_file,
            rt_border_tolerance=float(rt_border_tolerance)
        )
        results.calc_amounts_from_rt_info_file(
            rt_info_file=rt_summary_file,
            rt_border_tolerance=float(rt_border_tolerance)
        )

    return rt_summary_file


if __name__ == '__main__':

    arg_parser = set_up_argparser()

    arguments = arg_parser.parse_args()

    main(
        mzml_file=arguments.input_file,
        output_file=arguments.output,
        pickle_name ='quant_pickle.csv',
        evidence_files=arguments.evidence_files,
        fixed_labels=None,
        molecules=arguments.molecules,
        rt_border_tolerance=arguments.rt_border,
        label='15N',
        label_percentile=arguments.label_percentile,
        min_charge=arguments.min_charge,
        max_charge=arguments.max_charge,
    )

