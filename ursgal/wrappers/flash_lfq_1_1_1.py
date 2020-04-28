#!/usr/bin/env python3
import ursgal
import os
import csv
import sys
import shutil
from pprint import pprint
import pickle

from ursgal.ukb import PROTON


class flash_lfq_1_1_1(ursgal.UNode):
    """
    """

    META_INFO = {
        "edit_version": 1.00,
        "name": "FlashLFQ",
        "version": "1.1.1",
        "release_date": "2020-04-22",
        "engine_type": {"quantification_engine": True,},
        "input_extensions": [".mzML"],
        "output_extensions": [".csv"],
        "in_development": False,
        "create_own_folder": True,
        "include_in_git": False,
        "distributable": False,
        "utranslation_style": "flash_lfq_style_1",
        "engine": {
            "linux": {"64bit": {"exe": "CMD.exe",}},
            "darwin": {"64bit": {"exe": "CMD.exe",}},
            "win32": {"64bit": {"exe": "CMD.exe",}},
        },
        "citation": "ADD THE CITATION!!!",
    }

    def rewrite_psm_input(self, unified_csv):
        fieldnames = [
            "File Name",
            "Scan Retention Time",
            "Precursor Charge",
            "Base Sequence",
            "Full Sequence",
            "Peptide Monoisotopic Mass",
            "Protein Accession",
        ]
        out_name = os.path.join(
            self.params["output_dir_path"], "flash_lfq_psm_input.tsv"
        )
        with open(unified_csv) as fin, open(out_name, "wt") as fout:
            reader = csv.DictReader(fin)
            writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            for line in reader:
                # Check Mass differences column!!
                # Check Glycan mass column
                # Check Glycan name column
                # pprint(line)
                # breakpoint()
                if 'X' in line['Sequence']:
                    # not supported
                    continue
                if line["Modifications"] == "":
                    full_seq = line["Sequence"]
                else:
                    # continue
                    # full_seq = self.insert_mods(
                        # line["Sequence"], line["Modifications"]
                    # )
                    full_seq = self.insert_mods(
                        line
                    )
                if line["Retention Time (s)"] == '':
                    # breakpoint()
                    file = line['Spectrum Title'].split('.')[0]
                    unit = self.scan_lookup[file]['unit']
                    rt = self.scan_lookup[file]['scan_2_rt'][int(line['Spectrum ID'])]
                    if unit == 'minute':
                        rt /= 60
                else:
                    rt = line['Retention Time (s)']
                if ';' in line["uCalc Mass"]:
                    mass = float(line["uCalc Mass"].split(';')[0])
                else:
                    mass = float(line["uCalc Mass"])
                if line.get('Mass Difference', '') != '':
                    # breakpoint()
                    print(line['Mass Difference'])
                    mass_diff = float(line['Mass Difference'].split(':')[0].split('(')[0])
                    print(mass_diff)
                    print()
                    mass += mass_diff
                if line.get('Glycan Mass', '') != '':
                    # breakpoint()
                    mass += float(line['Glycan Mass'])
                line_to_write = {
                    "File Name": os.path.splitext(
                        os.path.basename(line["Raw data location"])
                    )[0],
                    "Scan Retention Time": rt,
                    "Precursor Charge": line["Charge"],
                    "Base Sequence": line["Sequence"],
                    "Full Sequence": full_seq,
                    "Peptide Monoisotopic Mass": mass,
                    "Protein Accession": line["Protein ID"],
                }
                writer.writerow(line_to_write)
        return out_name

    # def insert_mods(self, sequence, ursgal_mods):
    def insert_mods(self, line):
        base_seq = line['Sequence']
        sequence = line['Sequence']
        all_mods = [(m.rsplit(":", maxsplit=1)[0], int(m.rsplit(":", maxsplit=1)[1])) for m in line['Modifications'].split(";")]
        if line.get('Mass Difference', '') != '':
            print(line.get('Mass Difference', ''))
            # print()
            tmp_mods = []
            for m in line['Mass Difference'].split(';'):
                split = m.rsplit(':', maxsplit=1)
                # sometimes the mod looks like this -300:3;5
                # sometimes like this -300:3
                if len(split) == 2:
                    m = split[0]
                    if split[1] == '' or split[1] == 'n':
                        p = 0
                    else:
                        p = int(split[1])
                    print(m, p)
                    tmp_mods.append((m, p))
            all_mods += tmp_mods
            # all_mods += [(m.rsplit(":", maxsplit=1)[0], int(m.rsplit(":", maxsplit=1)[1])) for m in line['Mass Difference'].split(";")]
        if line.get('Glycan Mass', '') != '':
            m = line['Glycan Mass']
            p = line['Glycosite']
            all_mods.append((m, int(p)))
        mods_sorted = sorted(
            all_mods,
            key=lambda x: x[1],
            reverse=True,
        )
        # add mods as the following
        # just split a ; and write whole string in []
        # check if acetyl can be anywhere or before or after first AA
        # if plain massshift in mod string, add it explicitly!!
        for m in mods_sorted:
            name, pos = m
            sequence = list(sequence)
            sequence.insert(pos, "[{0}:{1}]".format(name, pos))
            sequence = "".join(sequence)
        return sequence

    def rewrite_as_csv(self, tsv_path):
        base, ext = os.path.splitext(tsv_path)
        csv_path = base + '.csv'
        with open(tsv_path) as fin, open(csv_path, 'wt') as fout:
            reader = csv.DictReader(fin, delimiter='\t')
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(fout, fieldnames=fieldnames)
            writer.writeheader()
            for line in reader:
                # use header translations param to translate headers of output
                writer.writerow(line)
        return csv_path

    def rewrite_as_translated_csv(self, tsv_path):
        header_translations = self.UNODE_UPARAMS['header_translations']['uvalue_style_translation']
        flash_lfq_headers = [
            "File Name",
            "Base Sequence",
            "Full Sequence",
            "Protein Group",
            "Peptide Monoisotopic Mass",
            "Precursor Charge",
            "Theoretical MZ",
            "Peak Apex Mass Error (ppm)",
            "MBR Score",
            "Peak Detection Type",
            "PSMs Mapped",
            "Peak Split Valley RT",
            "Base Sequences Mapped",
            "Full Sequences Mapped",
            "Peak intensity",
            "Peak RT Start",
            "Peak RT Apex",
            "Peak RT End",
            "Peak MZ",
            "Peak Charge",
            "Num Charge States Observed",
            "MS2 Retention Time",
        ]
        translated_headers = []
        for original_header_key in flash_lfq_headers:
            ursgal_header_key = header_translations[original_header_key]
            translated_headers.append(ursgal_header_key)
        base, ext = os.path.splitext(tsv_path)
        csv_path = base + '.csv'
        with open(tsv_path) as fin, open(csv_path, 'wt') as fout:
            reader = csv.DictReader(fin, delimiter='\t')
            fieldnames = translated_headers
            writer = csv.DictWriter(fout, fieldnames=translated_headers)
            writer.writeheader()
            for line in reader:
                out_line_dict = {}
                for column in flash_lfq_headers:
                    translated_col = header_translations[column]
                    out_line_dict[translated_col] = line[column]
                writer.writerow(out_line_dict)
        return csv_path

    def __init__(self, *args, **kwargs):
        super(flash_lfq_1_1_1, self).__init__(*args, **kwargs)

    def preflight(self):
        print("[ -ENGINE- ] Executing quantification ..")
        self.time_point(tag="execution")
        if self.params["input_file"].endswith(".json"):
            mzml_files = []
            for fdict in self.params["input_file_dicts"]:
                mzml_files.append(fdict["full"])
        else:  # single mzML file
            mzml_files = os.path.join(
                self.params["input_dir_path"], self.params["input_file"]
            )
        if isinstance(mzml_files, list):
            self.scan_lookup = pickle.load(open(os.path.join(os.path.dirname(mzml_files[0]), '_ursgal_lookup.pkl'), 'rb'))
        else:
            self.scan_lookup = pickle.load(open(os.path.join(os.path.dirname(mzml_files), '_ursgal_lookup.pkl'), 'rb'))

        # assert all mzml files are in the same folder
        if isinstance(mzml_files, list):
            mzml_dirs = []
            for f in mzml_files:
                mzml_dirs.append(os.path.dirname(f))
            if not len(set(mzml_dirs)) == 1:
                raise Exception("All mzmL files must be in the same directory!")

        if isinstance(mzml_files, str):
            input_file_dir = os.path.dirname(mzml_files)
        elif isinstance(mzml_files, list):
            input_file_dir = os.path.dirname(mzml_files[0])

        # Write ExperimentDesign.tsv
        # TODO move to own method
        experiment_setup = self.params["translations"]["experiment_setup"]
        if os.path.exists(os.path.join(input_file_dir, "ExperimentalDesign.tsv")):
            os.remove(os.path.join(input_file_dir, "ExperimentalDesign.tsv"))
        if len(experiment_setup) > 0:
            with open(
                os.path.join(input_file_dir, "ExperimentalDesign.tsv"), "wt"
            ) as fout:
                fieldnames = ["FileName", "Condition", "Biorep", "Fraction", "Techrep"]
                writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter="\t")
                writer.writeheader()
                for i, line_dict in experiment_setup.items():
                    writer.writerow(line_dict)

        # Convert unified csv to FlashLFQ input
        unified_csv = self.params["translations"]["quantification_evidences"]
        mod_map = {}
        mods = self.map_mods()
        psm_input = self.rewrite_psm_input(unified_csv)

        command_list = []
        if sys.platform in ["win32"]:
            command_list = []
        else:
            command_list = ["mono"]

        command_list.append(self.exe)
        command_list.extend(["--rep", input_file_dir])
        command_list.extend(["--idt", psm_input])
        command_list.extend(["--out", self.params["output_dir_path"]])
        # add all other parameters here
        grouped = self.params['translations']['_grouped_by_translated_key']
        for key in grouped.keys():
            if not key.startswith('--'):
                continue
            val = str(list(grouped[key].values())[0])
            if key == '--ppm':
                print('[ WARNING ] Assymetric precursor window not supported, take 2 times precursor_mass_tolerance_plus')
                val = str(2* int(val))

            # print(f'{key}={val}')
            if val != 'False':
                if val == 'True':
                    command_list.append(key)
                else:
                    command_list.append(key)
                    command_list.append(val)
        # print(command_list)
        self.params["command_list"] = command_list

    def postflight(self):
        output_files_basenames = [
            "QuantifiedPeaks.tsv",
            "QuantifiedPeptides.tsv",
            "QuantifiedProteins.tsv",
            "BayesianAnalysisBla.tsv",
        ]
        # rewrite to csv and rename
        for file in output_files_basenames:
            path = os.path.join(self.params["output_dir_path"], file)
            if os.path.exists(path):
                if file == 'QuantifiedPeaks.tsv':
                    csv_file = self.rewrite_as_translated_csv(path)
                else:
                    csv_file = self.rewrite_as_csv(path)
                suffix, ext = os.path.splitext(os.path.basename(csv_file))
                out_name = os.path.splitext(self.params['output_file'])[0]
                if file == 'QuantifiedPeaks.tsv':
                    # without suffix
                    new_out = '{out_name}{ext}'.format(out_name=out_name, ext='.csv')
                else:
                    new_out = "{out_name}_{suffix}{ext}".format(out_name=out_name, suffix=suffix, ext=ext)
                new_path = os.path.join(self.params["output_dir_path"], new_out)
                os.rename(csv_file, new_path)
