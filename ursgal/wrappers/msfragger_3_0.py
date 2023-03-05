#!/usr/bin/env python3.4
import ursgal
import os
import pprint
from collections import defaultdict as ddict
import csv
import sys


class msfragger_3_0(ursgal.UNode):
    """
    MSFragger unode

    Note:
        Please download and install MSFragger manually from
        http://www.nesvilab.org/software.html

    Reference:
    Kong, A. T., Leprevost, F. V, Avtonomov, D. M., Mellacheruvu, D., and Nesvizhskii, A. I. (2017)
    MSFragger: ultrafast and comprehensive peptide identification in mass spectrometry–based
    proteomics. Nature Methods 14

    Note:
        Addition of user amino acids not implemented yet. Only mzML search
        possible at the moment. The mgf file can still be passed to the node,
        but the mzML has to be in the same folder as the mgf.

    Warning:
        Still in testing phase!
        Metabolic labeling based 15N search may still be errorprone. Use with
        care!

    """

    META_INFO = {
        "edit_version": 1.00,
        "name": "MSFragger",
        "version": "3.0",
        "release_date": "2019-06-05",
        "utranslation_style": "msfragger_style_3",
        "input_extensions": [".mgf", ".mzML", ".mzXML"],
        "output_extensions": [".csv"],
        "create_own_folder": True,
        "in_development": False,
        "include_in_git": False,
        "distributable": False,
        "engine_type": {
            "protein_database_search_engine": True,
        },
        "engine": {
            "platform_independent": {
                "arc_independent": {
                    "exe": "MSFragger-3.0.jar",
                    "url": "http://www.nesvilab.org/software.html",
                    "zip_md5": "",
                    "additional_exe": [],
                },
            },
        },
        "citation": "Polasky, D.A.; Yu, F.; Teo, G.C.; Nesvizhskii A.I. (2020)."
        "Fast and Comprehensive N- and O-glycoproteomics analysis with MSFragger-Glyco"
        "bioRxiv 2020.05.18.102665; doi: https://doi.org/10.1101/2020.05.18.102665 ",
    }

    def __init__(self, *args, **kwargs):
        super(msfragger_3_0, self).__init__(*args, **kwargs)
        pass

    def write_params_file(self):
        with open(self.param_file_name, "w") as io:
            for msfragger_param_name, param_value in sorted(
                self.params_to_write.items()
            ):
                print("{0} = {1}".format(msfragger_param_name, param_value), file=io)

        return

    def preflight(self):
        """
        Formatting the command line and writing the param input file via
        self.params

        Returns:
                dict: self.params
        """
        self.input_file = os.path.join(
            self.params["input_dir_path"], self.params["input_file"]
        )

        self.param_file_name = os.path.join(
            self.params["output_dir_path"],
            "{0}_msfragger.params".format(self.input_file),
        )
        self.created_tmp_files.append(self.param_file_name)
        # further prepare and translate params

        # pprint.pprint(self.params['translations']['_grouped_by_translated_key'])
        # pprint.pprint(self.params)
        # exit()
        self.params_to_write = {
            "output_file_extension": "tsv",  # tsv or pepXML we fix it...
            "output_format": "tsv",  # pepXML or tsv
            "digest_mass_range": "{0} {1}".format(
                self.params["translations"]["_grouped_by_translated_key"][
                    "precursor_min_mass"
                ]["precursor_min_mass"],
                self.params["translations"]["_grouped_by_translated_key"][
                    "precursor_max_mass"
                ]["precursor_max_mass"],
            ),
        }

        write_exclusion_list = [
            "precursor_min_mass",
            "precursor_max_mass",
            "precursor_min_charge",
            "precursor_max_charge",
            "label",
            "-Xmx",
            "header_translations",
            "validation_score_field",
        ]

        additional_15N_modifications = []
        if (
            self.params["translations"]["_grouped_by_translated_key"]["label"]["label"]
            == "15N"
        ):
            self.print_info(
                "Search with label=15N may still be errorprone. Evaluate with care!",
                caller="WARNING",
            )
            for aminoacid, N15_Diff in ursgal.ukb.DICT_15N_DIFF.items():
                existing = False
                for mod_dict in self.params["mods"]["fix"]:
                    if aminoacid == mod_dict["aa"]:
                        mod_dict["mass"] += N15_Diff
                        mod_dict["name"] += "_15N_{0}".format(aminoacid)
                        existing = True
                if existing == True:
                    continue
                else:
                    mod_key = "add_{0}_{1}".format(
                        aminoacid, ursgal.chemical_composition_kb.aa_names[aminoacid]
                    )
                    self.params_to_write[mod_key] = N15_Diff

        self.mass_shift_lookup = {}
        self.mass_glycan_lookup = {}
        for msfragger_param_name in self.params["translations"][
            "_grouped_by_translated_key"
        ].keys():
            for ursgal_param_name, param_value in self.params["translations"][
                "_grouped_by_translated_key"
            ][msfragger_param_name].items():
                if msfragger_param_name in write_exclusion_list:
                    continue
                elif msfragger_param_name == "enzyme":
                    """
                    search_enzyme_name = Trypsin
                    search_enzyme_cutafter = KR
                    search_enzyme_butnotafter = P
                    """
                    aa_site, term, inhibitor = param_value.split(";")
                    self.params_to_write["search_enzyme_name"] = self.params["enzyme"]
                    self.params_to_write["search_enzyme_cutafter"] = aa_site
                    self.params_to_write["search_enzyme_butnotafter"] = inhibitor
                elif msfragger_param_name == "num_enzyme_termini":
                    # num_enzyme_termini = 2 # 2 for enzymatic, 1 for
                    # semi-enzymatic, 0 for nonspecific digestion

                    if (
                        self.params["translations"]["_grouped_by_translated_key"][
                            "enzyme"
                        ]["enzyme"]
                        == "nonspecific"
                    ):
                        self.params_to_write[msfragger_param_name] = 0
                    else:
                        self.params_to_write[msfragger_param_name] = param_value
                elif msfragger_param_name == "clear_mz_range":
                    min_mz, max_mz = param_value
                    self.params_to_write[msfragger_param_name] = "{0} {1}".format(
                        min_mz, max_mz
                    )
                elif msfragger_param_name == "remove_precursor_range":
                    min_mz, max_mz = param_value
                    self.params_to_write[msfragger_param_name] = "{0},{1}".format(
                        min_mz, max_mz
                    )
                elif msfragger_param_name == "delta_mass_exclude_ranges":
                    min_mz, max_mz = param_value
                    self.params_to_write[msfragger_param_name] = "({0},{1})".format(
                        min_mz, max_mz
                    )
                elif msfragger_param_name == "precursor_mass_lower":
                    self.params_to_write[msfragger_param_name] = -1 * param_value
                elif msfragger_param_name == "modifications":
                    """
                    #maximum of 7 mods - amino acid codes, * for any amino acid, [ and ] specifies protein termini, n and c specifies peptide termini
                    variable_mod_01 = 15.9949 M
                    variable_mod_02 = 42.0106 [*
                    #variable_mod_03 = 79.96633 STY
                    #variable_mod_03 = -17.0265 nQnC
                    #variable_mod_04 = -18.0106 nE
                    """
                    # print(self.params['translations']['_grouped_by_translated_key'][msfragger_param_name])
                    # pprint.pprint(self.params[ 'mods' ])
                    # exit()
                    mass_to_mod_aa = ddict(list)
                    for mod_dict in self.params["mods"]["opt"]:
                        """
                        {'_id': 0,
                          'aa': '*',
                          'composition': {'C': 2, 'H': 2, 'O': 1},
                          'id': '1',
                          'mass': 42.010565,
                          'name': 'Acetyl',
                          'org': '*,opt,Prot-N-term,Acetyl',
                          'pos': 'Prot-N-term',
                          'unimod': True},
                        """
                        aa_to_append = mod_dict["aa"]
                        pos_modifier = None
                        if mod_dict["pos"] == "Prot-N-term":
                            pos_modifier = "["
                        elif mod_dict["pos"] == "Prot-C-term":
                            pos_modifier = "]"
                        elif mod_dict["pos"] == "N-term":
                            pos_modifier = "n"
                        elif mod_dict["pos"] == "C-term":
                            pos_modifier = "c"
                        elif mod_dict["pos"] == "any":
                            pass
                        else:
                            print(
                                """
                            Unknown positional argument for given modification:
                            {0}
                            MSFragger cannot deal with this, please use one of the follwing:
                            any, Prot-N-term, Prot-C-term, N-term, C-term
                            """.format(
                                    mod_dict["org"]
                                )
                            )
                            sys.exit(1)
                        if pos_modifier is not None:
                            aa_to_append = "{0}{1}".format(pos_modifier, aa_to_append)
                        mass_to_mod_aa[mod_dict["mass"]].append(aa_to_append)
                    for pos, (mass, aa_list) in enumerate(mass_to_mod_aa.items()):
                        self.params_to_write[
                            "variable_mod_0{0}".format(pos + 1)
                        ] = "{0} {1}".format(mass, "".join(aa_list))
                    for mod_dict in self.params["mods"]["fix"]:
                        """
                        add_C_cysteine = 57.021464             # added to C - avg. 103.1429, mono. 103.00918
                        """
                        if mod_dict["pos"] == "Prot-N-term":
                            mod_key = "add_Nterm_protein"
                        elif mod_dict["pos"] == "Prot-C-term":
                            mod_key = "add_Cterm_protein"
                        elif mod_dict["pos"] == "N-term":
                            mod_key = "add_Nterm_peptide"
                        elif mod_dict["pos"] == "C-term":
                            mod_key = "add_Cterm_peptide"
                        else:
                            mod_key = "add_{0}_{1}".format(
                                mod_dict["aa"],
                                ursgal.chemical_composition_kb.aa_names[mod_dict["aa"]],
                            )
                        self.params_to_write[mod_key] = mod_dict["mass"]

                elif msfragger_param_name == "override_charge":
                    self.params_to_write[msfragger_param_name] = param_value
                    if param_value == 1:
                        self.params_to_write["precursor_charge"] = "{0} {1}".format(
                            self.params["translations"]["_grouped_by_translated_key"][
                                "precursor_min_charge"
                            ]["precursor_min_charge"],
                            self.params["translations"]["_grouped_by_translated_key"][
                                "precursor_max_charge"
                            ]["precursor_max_charge"],
                        )
                elif msfragger_param_name == "fragment_ion_series":
                    ion_list = []
                    for ion in param_value:
                        if ion not in [
                            "a",
                            "b",
                            "c",
                            "y~",
                            "x",
                            "y",
                            "z",
                            "b~",
                            "y-18",
                            "b-18",
                            "Y",
                        ]:
                            print(
                                """
                                [ WARNING ] MSFragger does not allow the following ion:
                                {0}
                                This ion will be skipped, i.e. not included in the search.
                            """.format(
                                    ion
                                )
                            )
                            continue
                        ion_list.append(ion)
                    self.params_to_write[msfragger_param_name] = ",".join(ion_list)
                elif msfragger_param_name in [
                    "mass_offsets",
                    "Y_type_masses",
                ]:
                    cc = ursgal.ChemicalComposition()
                    umama = ursgal.UnimodMapper()
                    masses = []
                    for m in param_value["masses"]:
                        masses.append(str(m))
                    for m in param_value["glycans"]:
                        cc.clear()
                        cc.add_glycan(m)
                        mass = cc._mass()
                        masses.append(str(mass))
                        # for tm in self.transform_mass_add_error(mass):
                        tm = round(mass * 1e5)
                        if tm not in self.mass_glycan_lookup.keys():
                            self.mass_glycan_lookup[tm] = set()
                        self.mass_glycan_lookup[tm].add(m)
                    for m in param_value["chemical_formulas"]:
                        cc.clear()
                        cc.add_chemical_formula(m)
                        mass = cc._mass()
                        masses.append(str(mass))
                        # for tm in self.transform_mass_add_error(mass):
                        tm = round(mass * 1e5)
                        if tm not in self.mass_shift_lookup.keys():
                            self.mass_shift_lookup[tm] = set()
                        self.mass_shift_lookup[tm].add(m)
                    for m in param_value["unimods"]:
                        unimod_mass = umama.name2mass(m)
                        masses.append(str(unimod_mass))
                        # for tm in self.transform_mass_add_error(unimod_mass):
                        tm = round(mass * 1e5)
                        if tm not in self.mass_shift_lookup.keys():
                            self.mass_shift_lookup[tm] = set()
                        self.mass_shift_lookup[tm].add(m)
                    self.params_to_write[msfragger_param_name] = "/".join(masses)
                elif msfragger_param_name == "diagnostic_fragments":
                    cc = ursgal.ChemicalComposition()
                    umama = ursgal.UnimodMapper()
                    masses = []
                    for m in param_value["masses"]:
                        masses.append(m)
                    for m in param_value["glycans"]:
                        cc.clear()
                        cc.add_glycan(m)
                        masses.append(cc._mass())
                    for m in param_value["chemical_formulas"]:
                        cc.clear()
                        cc.add_chemical_formula(m)
                        masses.append(cc._mass())
                    for m in param_value["unimods"]:
                        unimod_mass = umama.name2mass(m)
                        masses.append(unimod_mass)
                    mzs = []
                    for mass in masses:
                        mzs.append(str(ursgal.ucore.calculate_mz(mass, 1)))
                    self.params_to_write[msfragger_param_name] = "/".join(mzs)
                else:
                    self.params_to_write[msfragger_param_name] = param_value

        self.write_params_file()

        if (
            self.input_file.lower().endswith(".mzml")
            or self.input_file.lower().endswith(".mzml.gz")
            or self.input_file.lower().endswith(".mgf")
        ):
            self.params["translations"]["mzml_input_file"] = self.input_file
        # elif self.input_file.lower().endswith('.mgf'):
        #     self.params['translations']['mzml_input_file'] = \
        #         self.meta_unodes['ucontroller'].get_mzml_that_corresponds_to_mgf( self.input_file )
        #     self.print_info(
        #         'MSFragger can only read Proteowizard MGF input files,'
        #         'the corresponding mzML file {0} will be used instead.'.format(
        #             os.path.abspath(self.params['translations']['mzml_input_file'])
        #         ),
        #         caller = "INFO"
        #     )
        else:
            raise Exception(
                "MSFragger input spectrum file must be in mzML or MGF format!"
            )

        self.params["command_list"] = [
            "java",
            "-Xmx{0}".format(
                self.params["translations"]["_grouped_by_translated_key"]["-Xmx"]["-xmx"]
            ),
            "-jar",
            self.exe,
            self.param_file_name,
            self.params["translations"]["mzml_input_file"],
        ]

        self.params["translations"]["output_file_incl_path"] = os.path.join(
            self.params["output_dir_path"], self.params["output_file"]
        )
        return self.params

    def transform_mass_add_error(self, mass):
        if self.params["translations"]["precursor_mass_tolerance_unit"] != "ppm":
            lower_mass = (
                mass
                - self.params["translations"]["precursor_mass_tolerance_minus"]
                * mass
                / 1e6
            )
            upper_mass = (
                mass
                + self.params["translations"]["precursor_mass_tolerance_plus"]
                * mass
                / 1e6
            )
        elif self.params["translations"]["precursor_mass_tolerance_unit"] != "Da":
            lower_mass = (
                mass - self.params["translations"]["precursor_mass_tolerance_minus"]
            )
            upper_mass = (
                mass + self.params["translations"]["precursor_mass_tolerance_plus"]
            )
        else:
            print(
                "[ERROR] mass tolerance unit {0} not supported".format(
                    self.params["translations"]["precursor_mass_tolerance_unit"]
                )
            )
            sys.exit(1)
        transformed_mass_range = []
        for m in range(round(lower_mass * 1e5), round(((upper_mass * 1e5) + 1))):
            transformed_mass_range.append(m)
        return transformed_mass_range

    def postflight(self):
        """
        Reads MSFragger tsv output and write final csv output file.

        Adds:
            * Raw data location, since this can not be added later
            * Converts masses in Da to m/z (could be done in unify_csv)


        """
        ms_fragger_header = [
            "scannum",
            "precursor_neutral_mass",
            "retention_time",
            "charge",
            "hit_rank",
            "peptide",
            "peptide_prev_aa",
            "peptide_next_aa",
            "protein",
            "num_matched_ions",
            "tot_num_ions",
            "calc_neutral_pep_mass",
            "massdiff",
            "num_tol_term",
            "num_missed_cleavages",
            "modification_info",
            "hyperscore",
            "nextscore",
            "expectscore",
            "best_locs",
            "score_without_delta_mass",
            "best_score_with_delta_mass",
            "second_best_score_with_delta_mass",
            "delta_score",
        ]

        translated_headers = []
        header_translations = self.UNODE_UPARAMS["header_translations"][
            "uvalue_style_translation"
        ]
        for original_header_key in ms_fragger_header:
            ursgal_header_key = header_translations[original_header_key]
            translated_headers.append(ursgal_header_key)

        translated_headers += [
            "Spectrum Title",
            "Raw data location",
            "Exp m/z",
            "Calc m/z",
        ]
        if self.params["translations"]["msfragger_labile_mode"] in [
            "labile",
            "nglycan",
        ]:
            translated_headers += ["Mass Difference Annotations", "Glycan"]

        msfragger_output_tsv = os.path.join(
            self.params["input_dir_path"], self.params["file_root"] + ".tsv"
        )
        self.created_tmp_files.append(msfragger_output_tsv)

        if os.path.exists(msfragger_output_tsv) is False:
            msfragger_output_tsv = os.path.join(
                self.params["input_dir_path"],
                self.params["file_root"][len(self.params["prefix"]) + 1 :] + ".tsv",
            )
            if os.path.exists(msfragger_output_tsv) is False:
                msfragger_output_tsv = os.path.join(
                    self.params["input_dir_path"],
                    "_".join(self.params["file_root"].split("_")[1:]) + ".tsv",
                )
                if os.path.exists(msfragger_output_tsv) is False:
                    print(
                        "[ERROR]: MSFragger could not find the correct output tsv file"
                    )

        csv_out_fobject = open(self.params["translations"]["output_file_incl_path"], "w")
        csv_writer = csv.DictWriter(csv_out_fobject, fieldnames=translated_headers)
        csv_writer.writeheader()

        with open(msfragger_output_tsv) as temp_tsv:
            csv_reader = csv.DictReader(
                temp_tsv, fieldnames=translated_headers, delimiter="\t"
            )
            next(csv_reader, None)
            for line_dict in csv_reader:
                line_dict["Raw data location"] = os.path.abspath(
                    self.params["translations"]["mzml_input_file"]
                )

                ############################################
                # all fixing here has to go into unify csv! #
                ############################################

                # 'Precursor neutral mass (Da)' : '',
                # 'Neutral mass of peptide' : 'Calc m/z',# (including any variable modifications) (Da)
                line_dict["Exp m/z"] = ursgal.ucore.calculate_mz(
                    float(line_dict["MSFragger:Precursor neutral mass (Da)"]),
                    float(line_dict["Charge"]),
                )
                line_dict["Calc m/z"] = ursgal.ucore.calculate_mz(
                    float(line_dict["MSFragger:Neutral mass of peptide"]),
                    float(line_dict["Charge"]),
                )
                if self.params["translations"]["msfragger_labile_mode"] in [
                    "labile",
                    "nglycan",
                ]:
                    annotated = False
                    n = 0
                    mass_diff = float(line_dict["Mass Difference"])
                    matching_glycans = []
                    matching_annotations = []
                    for t_mass_diff in self.transform_mass_add_error(mass_diff):
                        # t_mass_diff = round(float(line_dict['Mass Difference']) * 1e5)
                        if t_mass_diff in self.mass_glycan_lookup.keys():
                            matching_glycans.extend(
                                sorted(self.mass_glycan_lookup[t_mass_diff])
                            )
                            annotated = True
                        elif t_mass_diff in self.mass_shift_lookup.keys():
                            matching_annotations.extend(
                                sorted(self.mass_shift_lookup[t_mass_diff])
                            )
                            annotated = True
                    while annotated is False:
                        n += 1
                        mass_diff = mass_diff - ursgal.ukb.PROTON
                        if n == 4:
                            break
                        for t_mass_diff in self.transform_mass_add_error(mass_diff):
                            if t_mass_diff in self.mass_glycan_lookup.keys():
                                matching_glycans.extend(
                                    sorted(self.mass_glycan_lookup[t_mass_diff])
                                )
                                annotated = True
                            elif t_mass_diff in self.mass_shift_lookup.keys():
                                matching_annotations.extend(
                                    sorted(self.mass_shift_lookup[t_mass_diff])
                                )
                                annotated = True
                    line_dict["Glycan"] = ";".join(matching_glycans)
                    line_dict["Mass Difference Annotations"] = ";".join(
                        matching_annotations
                    )
                csv_writer.writerow(line_dict)

        csv_out_fobject.close()
        # if msfragger_output_tsv.endswith('.tsv'):
        #     os.remove(msfragger_output_tsv)
        return
