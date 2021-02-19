#!/usr/bin/env python
# encoding: utf-8

import sugarpy
import ursgal
import sys
import os
import pickle

# from collections import namedtuple


def main(
    mzml_file=None,
    validated_results_pkl=None,
    plot_types=["plot_glycan_elution_profile"],
    plot_peak_types=[
        "matched",
        "unmatched",
        "labels",
    ],
    remove_subtrees=[],
    plot_molecule_dict=None,
    peak_colors={
        "matched": (0, 200, 0),
        "unmatched": (200, 0, 0),
        "labels": (0, 0, 200),
        "raw": (100, 100, 100),
    },
    ms_level=1,
    output_file=None,
    min_sugarpy_score=0,
    min_sub_cov=0.0,
    min_spec_number=1,
    charges=[1, 2, 3, 4, 5],
    x_axis_type="retention_time",
    score_type="top_scores",
    title=None,
    result_file=None,
    include_subtrees="no_subtrees",
    monosaccharides=None,
    scan_rt_lookup=None,
    pyqms_params=None,
    plotly_layout=None,
    rt_border_tolerance=None,
    ursgal_ident_file=None,
    frag_mass_tolerance=None,
    unimod_glycans_incl_in_search=[],
    max_tree_length=10,
    decoy_glycan="End(HexNAc)Hex(3)HexNAc(2)MeHex(2)Pent(1)dHex(1)",
    min_oxonium_ions=3,
    min_Y_ions=1,
    max_trees_per_spec=1,
    venndiagram_function=None,
):
    """"""

    assert (
        result_file is not None or plot_molecule_dict is not None
    ), """
    [ Error ] not clear what to plot,
    [ Error ] specify result_file or plot_molecule_dict """
    assert (
        output_file is not None
    ), """
    [ Error ] output_file is required """

    ms_precision = pyqms_params["REL_MZ_RANGE"]

    if plot_types == []:
        print(
            """
            Please specify the plot_types.
            Available plot_types are:
                plot_molecule_elution_profile,
                plot_glycan_elution_profile,
                plot_annotated_spectra,
                check_peak_presence,
                check_frag_specs
        """
        )

    validated_results = None
    for pt in plot_types:
        if pt not in [
            "check_peak_presence",
            "check_frag_specs",
            "extract_best_matches",
        ]:
            assert (
                validated_results_pkl is not None
            ), """
            [ Error ] validated_results_pkl is required """
            with open(validated_results_pkl, "rb") as results_pkl:
                validated_results = pickle.load(results_pkl)
            break

    if mzml_file is not None:
        if scan_rt_lookup is None or scan_rt_lookup == "create_new_lookup":
            sp_run = sugarpy.run.Run()
            lookup_dict = sp_run.build_rt_lookup(mzml_file, ms_level)
        else:
            with open(scan_rt_lookup, "rb") as lookup_pkl:
                lookup_dict = pickle.load(lookup_pkl)
        if mzml_file.endswith(".idx.gz"):
            mzml_basename = os.path.basename(mzml_file).replace(".idx.gz", "")
        else:
            mzml_basename = os.path.basename(mzml_file).replace(".mzML", "")
        scan2rt = lookup_dict[mzml_basename]["scan_2_rt"]
    else:
        scan2rt = None

    sp_results = sugarpy.results.Results(
        monosaccharides=monosaccharides,
        scan_rt_lookup=scan2rt,
        validated_results=validated_results,
    )

    created_files = []
    if result_file is not None and plot_types != ["check_peak_presence"]:
        assert (
            plot_molecule_dict is None or plot_molecule_dict == {}
        ), """
        [ Error ] Please use either plot_molecule_dict or result_file
        [ Error ] to specify which molecules to plot, not both!
        """
        plot_molecule_dict = sp_results.parse_result_file(result_file)

    if "write_new_result_csv" in plot_types:
        sp_run = sugarpy.run.Run()
        peptide_lookup = sp_run.parse_ident_file(
            ident_file=ursgal_ident_file,
            unimod_glycans_incl_in_search=unimod_glycans_incl_in_search,
        )
        written_file = sp_results.write_results2csv(
            output_file=validated_results_pkl.replace(".pkl", ".csv"),
            max_trees_per_spec=max_trees_per_spec,
            min_sugarpy_score=min_sugarpy_score,
            min_sub_cov=min_sub_cov,
            peptide_lookup=peptide_lookup,
            monosaccharides=monosaccharides,
            scan_rt_lookup=scan2rt,
            mzml_basename=mzml_basename,
        )
        created_files.append(written_file)

    if "plot_molecule_elution_profile" in plot_types:
        tmp_out_file = output_file.replace(".txt", "_molecule_profile.html")
        written_file = sp_results.plot_molecule_elution_profile(
            plot_molecule_dict=plot_molecule_dict,
            output_file=tmp_out_file,
            include_subtrees=include_subtrees,
            x_axis_type=x_axis_type,
            title=title,
            plotly_layout=plotly_layout,
        )
        created_files.append(written_file)

    if "plot_glycan_elution_profile" in plot_types:
        tmp_out_file = output_file.replace(".txt", "_glycan_profile.html")
        written_file = sp_results.plot_glycan_elution_profile(
            peptide_list=sorted(plot_molecule_dict.keys()),
            min_sugarpy_score=min_sugarpy_score,
            min_sub_cov=min_sub_cov,
            x_axis_type=x_axis_type,
            score_type=score_type,
            output_file=tmp_out_file,
            title=title,
            plotly_layout=plotly_layout,
        )
        created_files.append(written_file)

    if "plot_annotated_spectra" in plot_types:
        written_files = sp_results.plot_annotated_spectra(
            mzml_file=mzml_file,
            plot_peak_types=plot_peak_types,
            remove_subtrees=remove_subtrees,
            plot_molecule_dict=plot_molecule_dict,
            peak_colors=peak_colors,
            ms_level=ms_level,
            output_folder=os.path.dirname(output_file),
            ms_precision=ms_precision,
            plotly_layout=plotly_layout,
        )
        created_files.extend(written_files)

    if "check_peak_presence" in plot_types:
        out_file_csv, venn_data = sp_results.check_peak_presence(
            mzml_file=mzml_file,
            sp_result_file=result_file,
            ms_level=ms_level,
            output_file=output_file,
            pyqms_params=pyqms_params,
            rt_border_tolerance=rt_border_tolerance,
            min_spec_number=min_spec_number,
            charges=charges,
        )

        venn_output_file = output_file.replace(".txt", "_peak_presence_venn_diagram.svg")
        venn_results = venndiagram_function(data=venn_data, output_file=venn_output_file)

        created_files.extend(
            [
                out_file_csv,
                venn_output_file,
            ]
        )

    # if 'check_peak_presence_and_frag_specs' in plot_types:
    #     out_file_csv, venn_data, peak_presence_dict = sp_results.check_peak_presence(
    #         mzml_file=mzml_file,
    #         sp_result_file=result_file,
    #         ms_level=ms_level,
    #         output_file=output_file,
    #         pyqms_params=pyqms_params,
    #         rt_border_tolerance=rt_border_tolerance,
    #         min_spec_number=min_spec_number,
    #         charges=charges,
    #     )

    #     venn_output_file1=output_file.replace('.txt', '_peak_presence_venn_diagram.svg')
    #     venn_results1 = venndiagram_function(
    #         data=venn_data,
    #         out_file=venn_output_file
    #     )

    if "check_frag_specs" in plot_types:
        (
            ursgal_output_file,
            venn_data1,
            sugarpy_output_file,
            venn_data2,
        ) = sp_results.check_frag_specs(
            mzml_file=mzml_file,
            ursgal_ident_file=ursgal_ident_file,
            sp_result_file=result_file,
            frag_mass_tolerance=frag_mass_tolerance,
            decoy_glycan=decoy_glycan,  #'End(HexNAc)Hex(3)HexNAc(2)MeHex(2)Pent(1)dHex(1)',
            glycans_incl_in_search=unimod_glycans_incl_in_search,
            # max_tree_length=max_tree_length,
            output_file=output_file,
            min_oxonium_ions=min_oxonium_ions,
            min_Y_ions=min_Y_ions,
            pyqms_params=pyqms_params,
        )
        venn_out_names = [
            output_file.replace(".txt", "_general_glyco_frag_ions.svg"),
            output_file.replace(".txt", "_sugarpy_glyco_frag_ions.svg"),
        ]

        created_files.extend(
            [
                ursgal_output_file,
            ]
        )

        for n, venn_data in enumerate([venn_data1, venn_data2]):
            if venn_data is None:
                continue
            venn_results2 = venndiagram_function(
                data=venn_data, output_file=venn_out_names[n]
            )
            if n == 1:
                created_files.extend(
                    [
                        sugarpy_output_file,
                        venn_out_names[1],
                    ]
                )
            else:
                created_files.append(venn_out_names[0])

    if "extract_best_matches" in plot_types:
        extracted_file = sp_results.extract_best_matches(
            sp_result_file=result_file,
            output_file=output_file,
            max_trees_per_spec=max_trees_per_spec,
            min_spec_number=min_spec_number,
        )
        created_files.append(extracted_file)

    # output_file = output_file.replace('.html', '.txt')
    with open(output_file, "w") as out_file:
        for f in created_files:
            print(f, file=out_file)

    print("Done.")
    return output_file


if __name__ == "__main__":
    mzml_file = sys.argv[1]
    validated_results_pkl = sys.argv[2]
    result_file = sys.argv[3]
    output_file = result_file.replace(".csv", ".html")
    main(
        mzml_file=mzml_file,
        validated_results_pkl=validated_results_pkl,
        result_file=result_file,
        output_file=output_file,
        monosaccharides={
            "dHex": "C6H10O4",
            # "dHexNAc": 'C8H13NO4',
            "Hex": "C6H10O5",
            # "HexA": 'C6H8O6',
            "HexNAc": "C8H13NO5",
            "Me2Hex": "C8H14O5",
            "MeHex": "C7H12O5",
            # "NeuAc": 'C11H17NO8',
            "Pent": "C5H8O4",
            # 'dHexN': 'C6H11O3N',
            # 'HexN': 'C6H11O4N',
            # 'MeHexA': 'C7H10O6',
        },
    )
