#!/usr/bin/env python3.5
# encoding: utf-8

# '''
# SugarPy - discovery-driven analysis of glycan compositions from IS-CID
# of intact glycopeptides.

# Copyright (c) 2016 S. Schulze, J. Kraegenbring, A. Oltmann, C. Fufezan,
# M. Hippler

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# '''

from __future__ import absolute_import
from collections import namedtuple
from collections import defaultdict as ddict
import sugarpy
import ursgal
import sys
import pymzml
from pymzml.plot import Factory
import csv
import os
import plotly
import plotly.graph_objs as go
import re
import numpy as np
import pickle


def main():
    return


def sort_glycan_trees(
    self, scored_glycan_trees=None, tuple_pos=1, sort_by="SugarPy_score"
):
    """
    Sort glycan composition e.g. by the SugarPy_score.

    Returns:
        dict
    """
    sorted_glycans = {}
    for glycan in sorted(scored_glycan_trees.keys(), key=lambda tup: tup[tuple_pos]):
        if scored_glycan_trees[glycan][sort_by] not in sorted_glycans.keys():
            sorted_glycans[scored_glycan_trees[glycan][sort_by]] = []
        sorted_glycans[scored_glycan_trees[glycan][sort_by]].append(glycan)
    return sorted_glycans


def parse_result_file(self, result_file, return_type="plot", min_spec_number=1):
    """
    Parses a SugarPy results .csv file and extracts identified peptides
    together with their glycans and charges.

    Arguments:
        result_file (str): Path to the SugarPy result .csv file.
        return_type (str): 'plot' or 'peak_presence'

    Returns:
        dict: The dict contains all identified peptidoforms (Peptide#Unimod:Pos),
            as keys and a dict with the glycans (keys) and {'charges':set(), 'file_names':set()} (value)
            as values
    """
    print("[ SugarPy  ] Parsing SugarPy result file")

    if return_type == "plot":
        plot_molecule_dict = {}
        with open(result_file, "r") as in_file:
            csv_input = csv.DictReader(in_file)
            for line_dict in csv_input:
                if line_dict["Modifications"] != "":
                    pep = "{0}#{1}".format(
                        line_dict["Sequence"], line_dict["Modifications"]
                    )
                else:
                    pep = line_dict["Sequence"]
                if pep not in plot_molecule_dict.keys():
                    plot_molecule_dict[pep] = {}
                plot_molecule = line_dict["Glycan"]
                charges = line_dict["Charges"].split(";")
                if plot_molecule not in plot_molecule_dict[pep].keys():
                    plot_molecule_dict[pep][plot_molecule] = {
                        "charges": [],
                        "file_names": [],
                        "specs": [],
                    }
                plot_molecule_dict[pep][plot_molecule]["charges"].append(
                    [int(c) for c in charges]
                )
                plot_molecule_dict[pep][plot_molecule]["file_names"].append(
                    line_dict["Raw Data Name"]
                )
                plot_molecule_dict[pep][plot_molecule]["specs"].append(
                    int(line_dict["Spectrum ID"])
                )
        return plot_molecule_dict

    elif return_type == "peak_presence":
        formula_to_rt = ddict(list)
        molecule_name_dict = ddict(set)
        rt_list = []
        # charge_set = set()
        line_dict_list = []
        molecule_spec_count = ddict(set)
        with open(result_file, "r") as in_file:
            csv_input = csv.DictReader(in_file)
            csv_fieldnames = csv_input.fieldnames
            peak_presence_dict = None
            for header in csv_fieldnames:
                if "MS1 Spectrum IDs (without IS-CID)" in header:
                    peak_presence_dict = {}
                    ms1_header = header
                if "MS2 Spectrum IDs (without IS-CID)" in header:
                    peak_presence_dict = {}
                    ms2_header = header
            for line_dict in csv_input:
                spec = line_dict["Spectrum ID"]
                formula = line_dict["Chemical Formula"]
                if peak_presence_dict is not None:
                    if formula not in peak_presence_dict.keys():
                        peak_presence_dict[formula] = {
                            "ms1_peak_specs": set(),
                            "ms2_frag_specs": set(),
                        }
                    for s in line_dict[ms1_header].split(";"):
                        if s != "":
                            peak_presence_dict[formula]["ms1_peak_specs"].add(int(s))
                    for s in line_dict[ms2_header].split(";"):
                        if s != "":
                            peak_presence_dict[formula]["ms2_frag_specs"].add(int(s))
                molecule = "#".join(
                    [
                        line_dict["Sequence"],
                        line_dict["Modifications"],
                        line_dict["Glycan"],
                    ]
                )
                formula_to_rt[formula].append(float(line_dict["Retention Time [min]"]))
                molecule_spec_count[molecule].add(spec)
                if len(molecule_spec_count[molecule]) >= min_spec_number:
                    molecule_name_dict[formula].add(molecule)
                rt_list.append(float(line_dict["Retention Time [min]"]))
                # charges = line_dict['Charges'].split(';')
                # for charge in charges:
                #     charge_set.add(int(charge))
                line_dict_list.append(line_dict)
        if peak_presence_dict is not None:
            for formula in molecule_name_dict.keys():
                peak_presence_dict[formula]["name_list"] = sorted(
                    molecule_name_dict[formula]
                )
        return (
            formula_to_rt,
            molecule_name_dict,
            rt_list,
            line_dict_list,
            csv_fieldnames,
            molecule_spec_count,
            peak_presence_dict,
        )

    else:
        print(
            "[ERROR] Not clear how to parse result file, please specify 'plot' or 'peak_presence'"
        )
        sys.exit(1)


def glycan_to_tuple(self, glycan):
    """
    Converts a glycan (unimod style: Hex(2)HexNAc(5)) into a tuple
    of (monosaccharide, count) pairs
    """
    pattern = re.compile(r"""(?P<monosacch>[A-z0-9]*)(?P<count>\([A-z0-9]*\))""")
    glycan_dict = {}
    for glyc_match in pattern.finditer(glycan):
        monosacch = glyc_match.group("monosacch")
        if monosacch == "End":
            count = glyc_match.group("count").strip("(").strip(")")
            if count == "None":
                count = None
        elif glyc_match.group("count") == "":
            count = 1
        else:
            count = int(glyc_match.group("count").strip("(").strip(")"))
        glycan_dict[monosacch] = count
    sp_tuple = tuple(sorted(glycan_dict.items()))
    return sp_tuple


def check_peak_presence(
    self,
    mzml_file=None,
    sp_result_file=None,
    ms_level=1,
    output_file="",
    pyqms_params=None,
    rt_border_tolerance=None,
    min_spec_number=1,
    charges=[1, 2, 3, 4, 5],
):
    """
    Takes a SugarPy result file as well as an mzML file
    to check in the mzML file for the presence of peaks
    corresponding to identified glycopeptides.
    If any are found, it is also checked if they were
    fragmented at some point of the run.
    """
    print("[ SugarPy  ] Parsing SugarPy result file:", sp_result_file)
    internal_precision = pyqms_params["INTERNAL_PRECISION"]
    ms_precision = pyqms_params["REL_MZ_RANGE"]

    (
        formula_to_rt,
        molecule_name_dict,
        rt_list,
        line_dict_list,
        csv_fieldnames,
        molecule_spec_count,
        peak_presence_dict,
    ) = self.parse_result_file(
        sp_result_file, return_type="peak_presence", min_spec_number=1
    )

    print("[ SugarPy  ] Checking presence of intact glycopeptide elution peaks,")
    print("[ SugarPy  ] and if they have been triggered for fragmentation")
    sp_run = sugarpy.run.Run()
    results_pkl, precursor_to_rt_id, lib = sp_run.quantify(
        molecule_name_dict=molecule_name_dict,
        rt_window=(
            min(rt_list) - rt_border_tolerance,
            max(rt_list) + rt_border_tolerance,
        ),
        ms_level=ms_level,
        charges=charges,  # sorted(charge_set),
        params=pyqms_params,
        pkl_name=mzml_file.replace(".mzML", "_check_peaks.pkl"),
        mzml_file=mzml_file,
        collect_precursor=True,
    )

    precursor_tmz_to_rt_id = {}
    for precursor in precursor_to_rt_id.keys():
        precursor_tmz = int(round(precursor * internal_precision))
        if precursor_tmz not in precursor_tmz_to_rt_id.keys():
            precursor_tmz_to_rt_id[precursor_tmz] = []
        precursor_tmz_to_rt_id[precursor_tmz].extend(precursor_to_rt_id[precursor])
    # sugarpy_tmz_set = set()
    glycopep_tmz_with_error = ddict(list)
    for formula in molecule_name_dict.keys():
        for charge in range(1, 6):
            for n, iso_mz in enumerate(
                lib[formula]["env"][(("N", "0.000"),)][charge]["mz"][:3]
            ):
                # if n == 0:
                #     sugarpy_tmz_set.addint(round(iso_mz * internal_precision))
                for t_mz_with_error in range(
                    int(round((iso_mz - (iso_mz * ms_precision)) * internal_precision)),
                    int(round((iso_mz + (iso_mz * ms_precision)) * internal_precision))
                    + 1,
                ):
                    glycopep_tmz_with_error[t_mz_with_error].append(formula)
    selected_glycopeps = {}
    precursor_tmz_set = set(precursor_tmz_to_rt_id.keys())
    glyco_tmz_error_set = set(glycopep_tmz_with_error.keys())
    for selected_tmz in precursor_tmz_set & glyco_tmz_error_set:
        formula_list = glycopep_tmz_with_error[selected_tmz]
        for formula in formula_list:
            if formula not in selected_glycopeps:
                selected_glycopeps[formula] = []
            rt_id = precursor_tmz_to_rt_id[selected_tmz]
            selected_glycopeps[formula].extend(rt_id)

    formula_to_matchspec = {}
    with open(results_pkl, "rb") as open_pkl:
        results = pickle.load(open_pkl)
        for m_key, results_value in results.items():
            formula = m_key.formula
            trivial_name = results.lookup["formula to trivial name"][formula][0]
            for matched_spectrum in results_value["data"]:
                mscore = matched_spectrum.score
                rt = matched_spectrum.rt
                spec_id = matched_spectrum.spec_id
                if (
                    rt >= min(formula_to_rt[formula]) - rt_border_tolerance
                    and rt <= max(formula_to_rt[formula]) + rt_border_tolerance
                ):
                    if formula not in formula_to_matchspec.keys():
                        formula_to_matchspec[formula] = []
                    formula_to_matchspec[formula].append(str(spec_id))

    ms1_new_fieldname = "{0} MS1 Spectrum IDs (without IS-CID)".format(
        os.path.basename(mzml_file).replace(".mzML", "")
    )
    ms2_new_fieldname = "{0} MS2 Spectrum IDs (without IS-CID)".format(
        os.path.basename(mzml_file).replace(".mzML", "")
    )
    csv_fieldnames.extend(
        [
            "MS1 Peaks Present",
            ms1_new_fieldname,
            "MS1 Selected for Fragmentation",
            ms2_new_fieldname,
        ]
    )
    output_file_name = sp_result_file.replace(".csv", "_peak_presence.csv")
    opened_output_file = open(output_file_name, "w")
    if sys.platform == "win32":
        lineterminator = "\n"
    else:
        lineterminator = "\r\n"
    csv_writer = csv.DictWriter(
        opened_output_file, csv_fieldnames, lineterminator=lineterminator
    )
    csv_writer.writeheader()

    # fragmented_peaks_in_window = {}
    formulas_with_peak = set()
    formulas_fragmented = set()
    for line_dict in line_dict_list:
        formula = line_dict["Chemical Formula"]
        if formula not in formula_to_matchspec.keys():
            line_dict[ms1_new_fieldname] = ""
            line_dict["MS1 Peaks Present"] = "False"
        elif len(formula_to_matchspec[formula]) >= min_spec_number:
            line_dict[ms1_new_fieldname] = ";".join(
                sorted(formula_to_matchspec[formula])
            )
            line_dict["MS1 Peaks Present"] = "True"
            formulas_with_peak.add(formula)
        if formula in selected_glycopeps.keys():
            frag_spec_ids = []
            for rt, spec_id in selected_glycopeps[formula]:
                if (
                    rt >= min(formula_to_rt[formula]) - rt_border_tolerance
                    and rt <= max(formula_to_rt[formula]) + rt_border_tolerance
                ):
                    frag_spec_ids.append(str(spec_id))
                    formulas_fragmented.add(formula)
                    # if formula not in fragmented_peaks_in_window.keys():
                    #     fragmented_peaks_in_window[formula] = []
                    # fragmented_peaks_in_window[formula].append(spec_id)
            line_dict[ms2_new_fieldname] = ";".join(sorted(frag_spec_ids))
            if len(frag_spec_ids) > 0:
                line_dict["MS1 Selected for Fragmentation"] = "True"
            else:
                line_dict["MS1 Selected for Fragmentation"] = "False"
        csv_writer.writerow(line_dict)
    opened_output_file.close()
    print("[ SugarPy  ] Updated SugarPy results file: ", output_file_name)

    sugarpy_formulas = set(molecule_name_dict.keys())

    venn_data = [
        {
            "label": "SugarPy identifications",
            "data": sugarpy_formulas,
        },
        {
            "label": "MS1 Peaks",
            "data": formulas_with_peak,
        },
        {
            "label": "Fragmented for MS2",
            "data": formulas_fragmented,
        },
    ]

    # peak_presence_dict = {}
    # for formula in molecule_name_dict.keys():
    #     peak_presence_dict[formula] = {
    #         'name_list' : sorted(molecule_name_dict[formula]),
    #         'ms1_peak_specs' : [],
    #         'ms2_frag_specs' : [],
    #     }
    #     if formula in fragmented_peaks_in_window.keys():
    #         peak_presence_dict[formula][
    #             'ms2_frag_specs'] = fragmented_peaks_in_window[formula]
    #     if formula in formula_to_matchspec.keys():
    #         peak_presence_dict[formula]['ms1_peak_specs'] = [
    #             int(s) for s in formula_to_matchspec[formula]
    #         ]

    return output_file_name, venn_data


def check_frag_specs(
    self,
    mzml_file=None,
    ursgal_ident_file=None,
    sp_result_file=None,
    # peak_presence_dict=None,
    frag_mass_tolerance=None,
    decoy_glycan="End(HexNAc)Hex(5)HexNAc(3)NeuAc(1)dHex(1)",
    glycans_incl_in_search=[],
    # max_tree_length=10,
    min_oxonium_ions=3,
    min_Y_ions=1,
    output_file=None,
    pyqms_params=None,
):
    internal_precision = pyqms_params["INTERNAL_PRECISION"]
    print("[ SugarPy  ] Checking presence of glycopeptide fragment ions ...")
    if mzml_file.endswith("idx.gz") is False:
        indexed_mzml = mzml_file + ".idx.gz"
        if os.path.exists(indexed_mzml):
            pass
        else:
            from pymzml.utils.utils import index_gzip

            with open(mzml_file) as fin:
                fin.seek(0, 2)
                max_offset_len = fin.tell()
                max_spec_no = pymzml.run.Reader(mzml_file).get_spectrum_count() + 10
            index_gzip(
                mzml_file,
                indexed_mzml,
                max_idx=max_spec_no,
                idx_len=len(str(max_offset_len)),
            )
    else:
        indexed_mzml = mzml_file
    pymzml_run = pymzml.run.Reader(
        indexed_mzml, MSn_Precision=frag_mass_tolerance * 1e-6
    )
    ms2_new_fieldname = "{0} MS2 Spectrum IDs (without IS-CID)".format(
        os.path.basename(mzml_file).replace(".mzML", "")
    )

    sp_run = sugarpy.run.Run()
    # parse Ursgal ident file to create a peptide lookup
    ursgal_peptide_lookup = sp_run.parse_ident_file(
        ident_file=ursgal_ident_file,
        unimod_glycans_incl_in_search=[],
    )

    if sys.platform == "win32":
        lineterminator = "\n"
    else:
        lineterminator = "\r\n"

    if decoy_glycan != "None":
        # For each peptide, check if the corresponding ident spectra contain oxonium and/or Y-ions.
        # Spectra of peptides harboring glycans included in glycans_incl_in_search
        # will be searched for corresponding fragment ions.
        # Other spectra will be searched for fragment ions of a decoy glycan,
        # this provides an idea for how often fragment ions match by chance (potential false positives)
        ursgal_pep_to_frag_ions = {}
        peps_no_glycan = set()
        peps_with_glycan = set()
        mod_pattern = re.compile(r""":(?P<pos>[0-9]*$)""")
        for peptide_unimod in ursgal_peptide_lookup.keys():
            ursgal_pep_to_frag_ions[peptide_unimod] = {}
            all_glycans_from_peptide = []
            non_glycan_unimods = []
            if "#" in peptide_unimod:
                peptide, modifications = peptide_unimod.split("#")
            else:
                peptide = peptide_unimod
                modifications = ""
            mod_list = modifications.split(";")
            for mod in mod_list:
                match = mod_pattern.search(mod)
                if match is None:
                    continue
                mod_name = mod[: match.start()]
                mod_pos = mod[match.start() + 1 :]
                if mod_name in glycans_incl_in_search:
                    all_glycans_from_peptide.append(mod)
                else:
                    non_glycan_unimods.append(mod)
            if len(non_glycan_unimods) == 0:
                pep_without_glycans = peptide
            else:
                pep_without_glycans = "{0}#{1}".format(
                    peptide, ";".join(non_glycan_unimods)
                )
            spec_id_list = ursgal_peptide_lookup[peptide_unimod]["spec_id"]
            if len(all_glycans_from_peptide) == 0:
                assert (
                    pep_without_glycans == peptide_unimod
                ), """
                [ ERROR ] peptide_unimod was changed but list all_glycans_from_peptide is empty
                {0}
                {1}
                """.format(
                    pep_without_glycans, peptide_unimod
                )
                glycan_list = [decoy_glycan]
                peps_no_glycan.add(peptide_unimod)
            else:
                glycan_list = all_glycans_from_peptide
                peps_with_glycan.add(peptide_unimod)
            spec_to_frag_ions = self.calc_and_match_frag_ions(
                pymzml_run=pymzml_run,
                glycan_list=glycan_list,
                peptide_unimod=pep_without_glycans,
                spec_id_list=spec_id_list,
                # max_tree_length=max_tree_length,
                internal_precision=internal_precision,
            )
            for spec_id in spec_to_frag_ions.keys():
                ursgal_pep_to_frag_ions[peptide_unimod][spec_id] = spec_to_frag_ions[
                    spec_id
                ]

        # info about oxonium and Y-ions is added to the Ursgal ident file
        targets_with_frag_ions = set()
        decoys_with_frag_ions = set()
        ursgal_output_file = ursgal_ident_file.replace(".csv", "_glycofrag_ions.csv")

        with open(ursgal_ident_file, "r") as u_in_file:
            csv_input = csv.DictReader(u_in_file)
            csv_fieldnames = csv_input.fieldnames
            csv_fieldnames.extend(
                [
                    "Oxonium Ions",
                    "Glycopeptide Y-ions",
                ]
            )
            with open(ursgal_output_file, "w") as u_out_file:
                csv_writer = csv.DictWriter(
                    u_out_file, csv_fieldnames, lineterminator=lineterminator
                )
                csv_writer.writeheader()
                for line_dict in csv_input:
                    has_oxonium_ions = False
                    has_Y_ions = False
                    if line_dict["Modifications"] == "":
                        peptide_unimod = line_dict["Sequence"]
                    else:
                        peptide_unimod = "{0}#{1}".format(
                            line_dict["Sequence"], line_dict["Modifications"]
                        )
                    spec_id = int(line_dict["Spectrum ID"])
                    # line_dict['Oxonium Ions'] = ''
                    # line_dict['Glycopeptide Y-ions'] = ''
                    if ursgal_pep_to_frag_ions[peptide_unimod] == {}:
                        csv_writer.writerow(line_dict)
                        continue
                    Y_ions = ursgal_pep_to_frag_ions[peptide_unimod][spec_id]["Y_ions"]
                    if len(Y_ions) >= min_Y_ions:
                        line_dict["Glycopeptide Y-ions"] = ";".join(Y_ions)
                        for obligatory in [
                            "HexNAc(1)",
                            "HexNAc(1)-H2O(1)",
                            # 'HexNAc(2)',
                            # 'HexNAc(2)-H2O(1)',
                            # 'HexNAc(2)-H2O(2)'
                        ]:
                            if obligatory in Y_ions:
                                has_Y_ions = True
                    oxonium_ions = ursgal_pep_to_frag_ions[peptide_unimod][spec_id][
                        "oxonium_ions"
                    ]
                    if len(oxonium_ions) >= min_oxonium_ions:
                        line_dict["Oxonium Ions"] = ";".join(oxonium_ions)
                        has_oxonium_ions = True
                    csv_writer.writerow(line_dict)
                    if has_Y_ions and has_oxonium_ions:
                        if peptide_unimod in peps_with_glycan:
                            targets_with_frag_ions.add(peptide_unimod)
                        else:
                            decoys_with_frag_ions.add(peptide_unimod)
                            # print('FP!?:', peptide_unimod, spec_id)
        print("[ SugarPy  ] Updated Ursgal results file: ", ursgal_output_file)

        # Venn diagram for potential false positives is generated in wrapper,
        # passing down values here
        venn_data_false_pos = [
            {
                "label": "Ursgal Peptides",
                "data": set(ursgal_pep_to_frag_ions.keys()),
            },
            {
                "label": "Peptides w/ Decoy Glyco Fragment Ions",
                "data": decoys_with_frag_ions,
            },
            {
                "label": "Peptides w/ Target Glyco Fragment Ions",
                "data": targets_with_frag_ions,
            },
        ]

    (
        formula_to_rt,
        molecule_name_dict,
        rt_list,
        line_dict_list,
        csv_fieldnames,
        molecule_spec_count,
        peak_presence_dict,
    ) = self.parse_result_file(
        sp_result_file,
        return_type="peak_presence",
    )
    if peak_presence_dict is None:
        sugarpy_output_file = None
        venn_data_sp_frag = None
        return (
            ursgal_output_file,
            venn_data_false_pos,
            sugarpy_output_file,
            venn_data_sp_frag,
        )

    # For all glycopeptides, identified by IS-CID, that show MS1 peaks in a run without IS-CID,
    # corresponding fragmentation spectra are checked for oxonium and Y-ions
    sugarpy_formula_to_frag_ions = {}
    for n, formula in enumerate(sorted(peak_presence_dict.keys())):
        print(
            "[ SugarPy  ] Checking formula {0} out of {1}    ".format(
                n, len(peak_presence_dict.keys())
            ),
            end="\r",
        )
        sugarpy_formula_to_frag_ions[formula] = {}
        glycopep_list = peak_presence_dict[formula]["name_list"]
        for glycopep in set(glycopep_list):
            sugarpy_formula_to_frag_ions[formula][glycopep] = {}
            peptide, unimod, glycan = glycopep.split("#")
            peptide_unimod = "{0}#{1}".format(peptide, unimod)
            spec_to_frag_ions = self.calc_and_match_frag_ions(
                pymzml_run=pymzml_run,
                glycan_list=[glycan],
                peptide_unimod=peptide_unimod,
                spec_id_list=sorted(peak_presence_dict[formula]["ms2_frag_specs"]),
                # max_tree_length=max_tree_length,
                internal_precision=internal_precision,
            )
            for spec_id in spec_to_frag_ions.keys():
                sugarpy_formula_to_frag_ions[formula][glycopep][
                    spec_id
                ] = spec_to_frag_ions[spec_id]

    # info about oxonium and Y-ions is added to the sugarpy result file
    all_glycopeps = set()
    all_fragmented_glycopeps = set()
    glycopeps_with_frag_ions = set()
    sugarpy_output_file = sp_result_file.replace(".csv", "_glycofrag_ions.csv")
    with open(sp_result_file, "r") as sp_in_file:
        csv_input = csv.DictReader(sp_in_file)
        csv_fieldnames = csv_input.fieldnames
        y_ion_new_fieldname = "{0} Glycopeptide Y-ions".format(
            os.path.basename(mzml_file).replace(".mzML", "")
        )
        ox_ion_new_fieldname = "{0} Oxonium Ions".format(
            os.path.basename(mzml_file).replace(".mzML", "")
        )
        csv_fieldnames.extend(
            [
                "MS2 Frag Ions Present",
                ox_ion_new_fieldname,
                y_ion_new_fieldname,
            ]
        )
        with open(sugarpy_output_file, "w") as sp_out_file:
            csv_writer = csv.DictWriter(
                sp_out_file, csv_fieldnames, lineterminator=lineterminator
            )
            csv_writer.writeheader()
            for line_dict in csv_input:
                glycopep = "{0}#{1}#{2}".format(
                    line_dict["Sequence"],
                    line_dict["Modifications"],
                    line_dict["Glycan"],
                )
                all_glycopeps.add(glycopep)
                formula = line_dict["Chemical Formula"]
                spec_id_list = line_dict[ms2_new_fieldname].split(";")
                if spec_id_list == [""] or spec_id_list == []:
                    csv_writer.writerow(line_dict)
                    continue
                all_fragmented_glycopeps.add(glycopep)
                Y_ions = []
                oxonium_ions = []
                true_glycopep = False
                for spec_id in spec_id_list:
                    has_oxonium_ions = False
                    has_Y_ions = False
                    spec_id = int(spec_id)
                    sugarpy_Y_ions = sugarpy_formula_to_frag_ions[formula][glycopep][
                        spec_id
                    ]["Y_ions"]
                    if len(sugarpy_Y_ions) >= min_Y_ions:
                        for obligatory in [
                            "HexNAc(1)",
                            "HexNAc(1)-H2O(1)",
                            # 'HexNAc(2)',
                            # 'HexNAc(2)-H2O(1)',
                            # 'HexNAc(2)-H2O(2)'
                        ]:
                            if obligatory in sugarpy_Y_ions:
                                has_Y_ions = True
                    Y_ions.append([";".join(sugarpy_Y_ions)])
                    sugarpy_ox_ions = sugarpy_formula_to_frag_ions[formula][glycopep][
                        spec_id
                    ]["oxonium_ions"]
                    if len(sugarpy_ox_ions) >= min_oxonium_ions:
                        has_oxonium_ions = True
                    oxonium_ions.append([";".join(sugarpy_ox_ions)])
                    if has_Y_ions and has_oxonium_ions:
                        glycopeps_with_frag_ions.add(glycopep)
                        true_glycopep = True

                if true_glycopep:
                    line_dict["MS2 Frag Ions Present"] = True
                else:
                    line_dict["MS2 Frag Ions Present"] = False

                y_ions_string = ""
                for y in Y_ions:
                    y_ions_string += "{0};".format(y)
                line_dict[y_ion_new_fieldname] = y_ions_string.strip(";")
                ox_ions_string = ""
                for o in oxonium_ions:
                    ox_ions_string += "{0};".format(o)
                line_dict[ox_ion_new_fieldname] = ox_ions_string.strip(";")
                csv_writer.writerow(line_dict)

    print("[ SugarPy  ] Updated SugarPy results file: ", sugarpy_output_file)

    venn_data_sp_frag = [
        {
            "label": "SugarPy Glycopeptides",
            "data": all_glycopeps,
        },
        {
            "label": "Fragmented Glycopeptides",
            "data": all_fragmented_glycopeps,
        },
        {
            "label": "Glycopeptides with Glyco Fragment Ions",
            "data": glycopeps_with_frag_ions,
        },
    ]

    if decoy_glycan == "None":
        ursgal_output_file = ursgal_ident_file
        venn_data_false_pos = None

    return (
        ursgal_output_file,
        venn_data_false_pos,
        sugarpy_output_file,
        venn_data_sp_frag,
    )


def calc_and_match_frag_ions(
    self,
    glycan_list=[],
    peptide_unimod=None,
    spec_id_list=[],
    pymzml_run=None,
    # max_tree_length=10,
    internal_precision=None,
):
    """
    Returns:
        dict: {spec_id: {'oxonium_ions' : [], 'Y_ions' : [],}}
    """
    combined_calculated_oxonium_ions = {}
    combined_y_list = []
    for glycan in glycan_list:
        glycan_as_list = []
        end_monosacch = None
        glycan_tuple = self.glycan_to_tuple(glycan)
        for monosacch, amount in glycan_tuple:
            if monosacch == "End":
                if end_monosacch is not None and end_monosacch != amount:
                    print("[ERROR] Multiple different end monosaccharides")
                    sys.exit(1)
                end_monosacch = amount
                continue
            glycan_as_list.extend([monosacch] * amount)
            combined_y_list.extend([monosacch] * amount)
        sp_run = sugarpy.run.Run()
        glycan_combinations = sp_run.build_combinations(
            max_tree_length=len(glycan_as_list),
            monosaccharides=glycan_as_list,
            mode="combinations",
        )
        # import pprint
        # pprint.pprint(glycan)
        calculated_oxonium_ions = self.calc_oxonium_ions(
            glycan_combinations=glycan_combinations,
            internal_precision=internal_precision,
        )
        for k, v in calculated_oxonium_ions.items():
            if k not in combined_calculated_oxonium_ions.keys():
                combined_calculated_oxonium_ions[k] = set()
            combined_calculated_oxonium_ions[k] |= v
    spec_to_frag_ions = {}
    for spec_id in spec_id_list:
        spec_to_frag_ions[spec_id] = {
            "oxonium_ions": [],
            "Y_ions": [],
        }
        spectrum = pymzml_run[spec_id]
        selected_precursors = spectrum.selected_precursors
        if selected_precursors != [] and "charge" in selected_precursors[0]:
            charge = selected_precursors[0]["charge"]
        else:
            print(
                """
                [ Warning ] Charge of precursor could not be determined.
                [ Warning ] Working with charge = 2
            """
            )
            charge = 2
        oxonium_ion_tmz_set = set(combined_calculated_oxonium_ions.keys())
        spec_tmz_set = spectrum.t_mz_set
        matching_tmz = oxonium_ion_tmz_set & spec_tmz_set
        for oxonium_ion_tmz in matching_tmz:
            oxonium_ion_names = combined_calculated_oxonium_ions[oxonium_ion_tmz]
            spec_to_frag_ions[spec_id]["oxonium_ions"].append(
                "|".join(sorted(oxonium_ion_names))
            )
        glycan_combinations = sp_run.build_combinations(
            max_tree_length=len(combined_y_list),
            monosaccharides=combined_y_list,
            mode="combinations",
        )
        calculated_Y_ions = self.calc_Y_ions(
            glycan_combinations=glycan_combinations,
            peptide_unimod=peptide_unimod,
            charge=charge,
            end_monosacch=end_monosacch,
            internal_precision=internal_precision,
        )
        Y_ion_tmz_set = set(calculated_Y_ions.keys())
        matching_tmz = Y_ion_tmz_set & spec_tmz_set
        for Y_ion_tmz in matching_tmz:
            Y_ion_name_list = calculated_Y_ions[Y_ion_tmz]
            spec_to_frag_ions[spec_id]["Y_ions"].append("|".join(Y_ion_name_list))

    return spec_to_frag_ions


def calc_oxonium_ions(self, glycan_combinations=None, internal_precision=None):
    """
    Returns:
        dict: { transformed mz for z=1 : [name1, name2, ...] }
    """
    oxonium_ions = {}
    for length in glycan_combinations.keys():
        for glycan_dict in glycan_combinations[length]:
            name_hill = ""
            for monosacch in sorted(glycan_dict.keys()):
                name_hill += "{0}({1})".format(monosacch, glycan_dict[monosacch])
            cc = ursgal.ChemicalComposition()
            cc.add_glycan(name_hill)
            # cc.add_chemical_formula('H(1)')
            mz = ursgal.ucore.calculate_mz(cc._mass(), 1)
            tmz = int(round(mz * internal_precision))
            if tmz not in oxonium_ions.keys():
                oxonium_ions[tmz] = set()
            oxonium_ions[tmz].add(name_hill)
            if length == 1:
                continue
            for water_loss_count in [1]:  # [1, 2]:
                new_name_hill = name_hill + "-H2O({0})".format(water_loss_count)
                cc.subtract_chemical_formula("H(2)O(1)", factor=water_loss_count)
                mz = ursgal.ucore.calculate_mz(cc._mass(), 1)
                tmz = int(round(mz * internal_precision))
                if tmz not in oxonium_ions.keys():
                    oxonium_ions[tmz] = set()
                oxonium_ions[tmz].add(new_name_hill)
                cc.add_chemical_formula("H(2)O(1)", factor=water_loss_count)

    return oxonium_ions


def calc_Y_ions(
    self,
    glycan_combinations=None,
    peptide_unimod=None,
    charge=2,
    end_monosacch="HexNAx",
    internal_precision=None,
):
    """
    Returns:
        dict: { transformed mz: [name1, name2, ...] }
    """
    Y_ions = {}
    cc = ursgal.ChemicalComposition()
    for length in glycan_combinations.keys():
        for glycan_dict in glycan_combinations[length]:
            cc.use(peptide_unimod)
            if end_monosacch is not None and end_monosacch not in glycan_dict.keys():
                continue
            name_hill = ""
            for monosacch in sorted(glycan_dict.keys()):
                name_hill += "{0}({1})".format(monosacch, glycan_dict[monosacch])
            cc.add_glycan(name_hill)
            for z in range(1, charge + 1):
                mz = ursgal.ucore.calculate_mz(cc._mass(), z)
                tmz = int(round(mz * internal_precision))
                # print(z, peptide_unimod, mz, name_hill)
                if tmz not in Y_ions.keys():
                    Y_ions[tmz] = []
                Y_ions[tmz].append(name_hill)
                for water_loss_count in [1, 2]:
                    new_name_hill = name_hill + "-H2O({0})".format(water_loss_count)
                    cc.subtract_chemical_formula("H(2)O(1)", factor=water_loss_count)
                    mz = ursgal.ucore.calculate_mz(cc._mass(), z)
                    tmz = int(round(mz * internal_precision))
                    if tmz not in Y_ions.keys():
                        Y_ions[tmz] = []
                    Y_ions[tmz].append(new_name_hill)
                    cc.add_chemical_formula("H(2)O(1)", factor=water_loss_count)
    return Y_ions


if __name__ == "__main__":
    print(__doc__)
