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

from collections import defaultdict as ddict
from itertools import combinations_with_replacement
from itertools import combinations
import ursgal
import sys
import pymzml
import csv
import os
import re

mod_pattern = re.compile(r"(?P<modname>.*):(?P<pos>[0-9]*)$")
glyco_pattern = re.compile(r"""(?P<monosacch>[A-z0-9]*)(?P<count>\([A-z0-9]*\))""")


def main(
    frag_mass_tolerance=20,
    glycopep_ident_file=None,
    output_file=None,
    mzml_file_list=[],
    internal_precision=10,
    decoy_glycan="",
    min_Y_ions=2,
    min_oxonium_ions=1,
    glycans_incl_in_search=[],
    psm_defining_colnames=[],
):
    (
        glycopep_ident_dict,
        non_glycopep_line_dicts,
        psm2glycopep_lookup,
    ) = parse_result_file(
        glycopep_ident_file,
        glycans_incl_in_search=glycans_incl_in_search,
        psm_defining_colnames=psm_defining_colnames,
    )
    glycopep_to_frag_ions = check_frag_specs(
        mzml_file_list=mzml_file_list,
        glycopep_ident_dict=glycopep_ident_dict,
        frag_mass_tolerance=frag_mass_tolerance,
        decoy_glycan=decoy_glycan,
        min_oxonium_ions=min_oxonium_ions,
        min_Y_ions=min_Y_ions,
        internal_precision=internal_precision,
    )
    write_output_file(
        output_file_name=output_file,
        ursgal_ident_file=glycopep_ident_file,
        glycopep_to_frag_ions=glycopep_to_frag_ions,
        psm2glycopep_lookup=psm2glycopep_lookup,
        non_glycopep_line_dicts=non_glycopep_line_dicts,
        psm_defining_colnames=psm_defining_colnames,
        min_Y_ions=min_Y_ions,
        min_oxonium_ions=min_oxonium_ions,
    )
    return output_file


def parse_result_file(result_file, glycans_incl_in_search=[], psm_defining_colnames=[]):
    """
    Parses an Ursgal results .csv file and extracts identified peptides
    together with their glycans and charges.

    Arguments:
        result_file (str): Path to the Ursgal result .csv file.
        glycans_incl_in_search (list): list of glycans that were included in search as modifications
        psm_defining_colnames (list): header of columns that define the psm

    Returns:
        glycopep_ident_dict (dict): The dict contains all mzml files as keys and as values a dict with
            the identified glycopeptides (Peptide#Unimod:Pos#glycan) (keys) and (spectrum id, charge) (value)
        non_glycopep_line_dicts (list): List of line dicts for all idents that don't correspond to glycopeptides
        psm2glycopep_lookup (dict): psm identifier to glycopep mapper
    """
    print("[ SugarPy  ] Parsing Ursgal result file")

    glycopep_ident_dict = {}
    non_glycopep_line_dicts = ddict(list)
    psm2glycopep_lookup = {}
    with open(result_file, "r") as in_file:
        csv_input = csv.DictReader(in_file)
        for line_dict in csv_input:
            ms_file = line_dict["Spectrum Title"].split(".")[0]
            if ms_file not in glycopep_ident_dict.keys():
                glycopep_ident_dict[ms_file] = ddict(list)
            spec_id = int(line_dict["Spectrum Title"].split(".")[-2])
            charge = int(line_dict["Charge"])
            pep = line_dict["Sequence"]
            glycans = []
            if "Glycan" in line_dict.keys():
                if line_dict["Glycan"] != "":
                    glycans.append(line_dict["Glycan"])
            unimod_list = []
            if line_dict["Modifications"] != "":
                for mod in line_dict["Modifications"].split(";"):
                    match = mod_pattern.search(mod)
                    modname = match.group("modname")
                    pos = match.group("pos")
                    if modname in glycans_incl_in_search:
                        if "(" in modname:
                            glycans.append(modname)
                        else:
                            glycans.append(modname + "(1)")
                    elif ":" in modname:
                        unimod_list.append(mod)
                    else:
                        glycomatch = glyco_pattern.search(modname)
                        if glycomatch is not None:
                            glycans.append(modname)
                        else:
                            unimod_list.append(mod)
            psm = "#".join([line_dict[x] for x in psm_defining_colnames])
            if glycans != []:
                pep_unimod_glycan = "{0}#{1}#{2}".format(
                    pep, ";".join(unimod_list), ";".join(glycans)
                )
                psm2glycopep_lookup[psm] = pep_unimod_glycan
                glycopep_ident_dict[ms_file][pep_unimod_glycan].append((spec_id, charge))
            else:
                non_glycopep_line_dicts[psm].append(line_dict)
    return glycopep_ident_dict, non_glycopep_line_dicts, psm2glycopep_lookup


def write_output_file(
    output_file_name=None,
    ursgal_ident_file=None,
    glycopep_to_frag_ions=None,
    psm2glycopep_lookup=None,
    non_glycopep_line_dicts=None,
    psm_defining_colnames=[],
    min_Y_ions=1,
    min_oxonium_ions=1,
):
    # info about oxonium and Y-ions is added to the Ursgal ident file
    if sys.platform == "win32":
        lineterminator = "\n"
    else:
        lineterminator = "\r\n"
    with open(ursgal_ident_file, "r") as u_in_file:
        csv_input = csv.DictReader(u_in_file)
        csv_fieldnames = csv_input.fieldnames
        csv_fieldnames.extend(
            [
                "MS2 Glycopep Frag Ions Present",
                "Oxonium Ions",
                "Glycopeptide Y-ions",
            ]
        )
        with open(output_file_name, "w") as u_out_file:
            csv_writer = csv.DictWriter(
                u_out_file, csv_fieldnames, lineterminator=lineterminator
            )
            csv_writer.writeheader()
            for line_dict in csv_input:
                has_oxonium_ions = False
                has_Y_ions = False
                psm = "#".join([line_dict[x] for x in psm_defining_colnames])
                if psm in non_glycopep_line_dicts.keys():
                    for ld in non_glycopep_line_dicts[psm]:
                        csv_writer.writerow(ld)
                    continue
                spec_id = int(line_dict["Spectrum ID"])
                ms_file = line_dict["Spectrum Title"].split(".")[0]
                glycopep = psm2glycopep_lookup[psm]

                spec_frag_ions = glycopep_to_frag_ions[ms_file][glycopep][spec_id]
                Y_ions = spec_frag_ions["Y_ions"]
                line_dict["Glycopeptide Y-ions"] = ";".join(Y_ions)
                if len(Y_ions) >= min_Y_ions:
                    has_Y_ions = True
                    # for obligatory in [
                    #     "Hex(1)",
                    #     "Hex(1)-H2O(1)",
                    #     # "HexNAc(1)",
                    #     # "HexNAc(1)-H2O(1)",
                    #     # 'HexNAc(2)',
                    #     # 'HexNAc(2)-H2O(1)',
                    #     # 'HexNAc(2)-H2O(2)'
                    # ]:
                    #     if obligatory in Y_ions:
                    #         has_Y_ions = True
                oxonium_ions = spec_frag_ions["oxonium_ions"]
                line_dict["Oxonium Ions"] = ";".join(oxonium_ions)
                if len(oxonium_ions) >= min_oxonium_ions:
                    has_oxonium_ions = True
                line_dict["MS2 Glycopep Frag Ions Present"] = all(
                    [has_oxonium_ions, has_Y_ions]
                )
                csv_writer.writerow(line_dict)
    print("[ SugarPy  ] Updated results file: ", output_file_name)

    return output_file_name


def check_frag_specs(
    mzml_file_list=None,
    glycopep_ident_dict=None,
    frag_mass_tolerance=None,
    decoy_glycan="End(HexNAc)Hex(5)HexNAc(3)NeuAc(1)dHex(1)",
    min_oxonium_ions=3,
    min_Y_ions=1,
    output_file=None,
    internal_precision=None,
):
    """
    For each glycopeptide, check if the corresponding ident spectra contain oxonium and/or Y-ions.
    """
    print("[ SugarPy  ] Checking presence of glycopeptide fragment ions ...")
    glycopep_to_frag_ions = {}

    # convert mzml files to indexed gzip files, if necessary
    for mzml_file in mzml_file_list:
        basename = os.path.basename(mzml_file)
        if mzml_file.endswith("idx.gz") is False:
            ms_file = basename.replace(".mzML", "")
            if ms_file not in glycopep_ident_dict.keys():
                continue
            indexed_mzml = mzml_file.replace(".mzML", ".idx.gz")
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
            ms_file = basename.replace(".idx.gz", "")
            if ms_file not in glycopep_ident_dict.keys():
                continue
            indexed_mzml = mzml_file
        print("[ SugarPy  ] Working on file: {0}".format(mzml_file))
        pymzml_run = pymzml.run.Reader(
            indexed_mzml, MSn_Precision=frag_mass_tolerance * 1e-6
        )

        glycopep_to_frag_ions[ms_file] = {}
        for n, pep_unimod_glycan in enumerate(glycopep_ident_dict[ms_file].keys()):
            print(
                "[ SugarPy  ] Checking fragment ions for: {0}".format(pep_unimod_glycan)
            )
            print(
                "[ SugarPy  ] Glycopeptide {0} out of {1}".format(
                    n + 1, len(glycopep_ident_dict[ms_file].keys())
                )
            )
            pep, unimod, glycan = pep_unimod_glycan.split("#")
            peptide_unimod = "#".join([pep, unimod])
            glycan_list = glycan.split(";")
            spec_id_charge_list = glycopep_ident_dict[ms_file][pep_unimod_glycan]
            spec_to_frag_ions = calc_and_match_frag_ions(
                pymzml_run=pymzml_run,
                glycan_list=glycan_list,
                peptide_unimod=peptide_unimod,
                spec_id_charge_list=spec_id_charge_list,
                internal_precision=internal_precision,
            )
            glycopep_to_frag_ions[ms_file][pep_unimod_glycan] = {}
            for spec_id in spec_to_frag_ions.keys():
                glycopep_to_frag_ions[ms_file][pep_unimod_glycan][
                    spec_id
                ] = spec_to_frag_ions[spec_id]

    return glycopep_to_frag_ions


def calc_and_match_frag_ions(
    glycan_list=[],
    peptide_unimod=None,
    spec_id_charge_list=[],
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
        glycan_tuple = glycan_to_tuple(glycan)
        for monosacch, amount in glycan_tuple:
            if monosacch == "End":
                if end_monosacch is not None and end_monosacch != amount:
                    print("[ERROR] Multiple different end monosaccharides")
                    sys.exit(1)
                end_monosacch = amount
                continue
            glycan_as_list.extend([monosacch] * amount)
            combined_y_list.extend([monosacch] * amount)
        glycan_combinations = build_combinations(
            max_tree_length=len(glycan_as_list),
            monosaccharides=glycan_as_list,
            mode="combinations",
        )
        # import pprint
        # pprint.pprint(glycan)
        calculated_oxonium_ions = calc_oxonium_ions(
            glycan_combinations=glycan_combinations,
            internal_precision=internal_precision,
        )
        for k, v in calculated_oxonium_ions.items():
            if k not in combined_calculated_oxonium_ions.keys():
                combined_calculated_oxonium_ions[k] = set()
            combined_calculated_oxonium_ions[k] |= v
    spec_to_frag_ions = {}
    for spec_id, charge in spec_id_charge_list:
        spec_to_frag_ions[spec_id] = {
            "oxonium_ions": [],
            "Y_ions": [],
        }
        spectrum = pymzml_run[spec_id]
        oxonium_ion_tmz_set = set(combined_calculated_oxonium_ions.keys())
        spec_tmz_set = spectrum.t_mz_set
        matching_tmz = oxonium_ion_tmz_set & spec_tmz_set
        for oxonium_ion_tmz in matching_tmz:
            oxonium_ion_names = combined_calculated_oxonium_ions[oxonium_ion_tmz]
            spec_to_frag_ions[spec_id]["oxonium_ions"].append(
                "|".join(sorted(oxonium_ion_names))
            )
        glycan_combinations = build_combinations(
            max_tree_length=len(combined_y_list),
            monosaccharides=combined_y_list,
            mode="combinations",
        )
        calculated_Y_ions = calc_Y_ions(
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


def calc_oxonium_ions(glycan_combinations=None, internal_precision=None):
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
                    Y_ions[tmz] = set()
                Y_ions[tmz].add(name_hill)
                if length == 1:
                    nr_water = [1]
                else:
                    nr_water = [1, 2]
                for water_loss_count in nr_water:
                    new_name_hill = name_hill + "-H2O({0})".format(water_loss_count)
                    cc.subtract_chemical_formula("H(2)O(1)", factor=water_loss_count)
                    mz = ursgal.ucore.calculate_mz(cc._mass(), z)
                    tmz = int(round(mz * internal_precision))
                    if tmz not in Y_ions.keys():
                        Y_ions[tmz] = set()
                    Y_ions[tmz].add(new_name_hill)
                    cc.add_chemical_formula("H(2)O(1)", factor=water_loss_count)
    return Y_ions


def glycan_to_tuple(glycan):
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


def build_combinations(
    max_tree_length=None,
    monosaccharides=None,
    mode="replacement",
):
    """
    Builds and returns a dictionary containing chemical compositions
    of all combinations (with replacement, not ordered)
    of a given dict of monosaccharides and a maximal length of the tree.

    Keyword arguments:
        max_tree_length (int): Maximum number of monosaccharides in one combination
        monosaccharides(dict): Dictionary containing name and chemical composition of monosaccharides

    Returns:
        dict: keys: chemical compositions of all combinations (with replacement, not ordered),
            values: combination(s) monosaccharide names corresponding to the chemical composition

    """

    glycan_combinations = {}
    for nr_repeats in range(1, max_tree_length + 1):
        if mode == "combinations":
            glycan_combinations[nr_repeats] = []
            tmp_combinations = set()
            for combo in combinations(monosaccharides, nr_repeats):
                tmp_combinations.add(combo)
            for tmp_combo in tmp_combinations:
                glycan_dict = {}
                for monosacch in set(tmp_combo):
                    count = tmp_combo.count(monosacch)
                    glycan_dict[monosacch] = count
                glycan_combinations[nr_repeats].append(glycan_dict)
        elif mode == "replacement":
            for combo in combinations_with_replacement(monosaccharides, nr_repeats):
                cc = ursgal.ChemicalComposition()
                for monosacch in combo:
                    cc.add_chemical_formula(monosaccharides[monosacch])
                hill_notation = cc.hill_notation_unimod()
                if hill_notation not in glycan_combinations:
                    glycan_combinations[hill_notation] = set()
                glycan_combinations[hill_notation].add(combo)

    return glycan_combinations


if __name__ == "__main__":
    print(__doc__)
