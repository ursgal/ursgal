#!/usr/bin/env python3
import ursgal
from ursgal.chemical_composition import ChemicalComposition
import os
import csv
import sys
import shutil
from pprint import pprint
import pickle
import statistics

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
        "in_development": True,
        "create_own_folder": True,
        "include_in_git": False,
        "distributable": False,
        "utranslation_style": "flash_lfq_style_1",
        "engine": {
            "platform_independent": {"arc_independent": {"exe": "CMD.exe",}},
        },
        "citation": "Millikin RJ, Solntsev SK, Shortreed MR, Smith LM. Ultrafast Peptide Label-Free Quantification with FlashLFQ. J Proteome Res. 2018;17(1):386-391. doi:10.1021/acs.jproteome.7b00608",
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
        self.spec_sequence_dict = {}
        with open(unified_csv) as fin:
            reader = csv.DictReader(fin)
            # total_length = sum(1 for row in reader)
            for i, line in enumerate(reader):
                if i % 500 == 0:
                    print('Rewrite line {0}'.format(i), end='\r')
                if 'X' in line['Sequence']:
                    # X in sequence not supported
                    continue
                file = line['Spectrum Title'].split('.')[0]
                if file not in self.all_filenames:
                    continue
                full_seq_name, full_mass = self.get_full_seq_and_mass(line)
                if line["Retention Time (s)"] == '':
                    # # sanitize rt
                    unit = self.scan_lookup[file]['unit']
                    rt = self.scan_lookup[file]['scan_2_rt'][int(line['Spectrum ID'])]
                    if unit != 'minute':
                        rt /= 60
                else:
                    rt = float(line['Retention Time (s)'])
                    rt /= 60
                line_to_write = {
                    "File Name": file,
                    "Scan Retention Time": rt,
                    "Precursor Charge": line["Charge"],
                    "Base Sequence": line["Sequence"],
                    "Full Sequence": full_seq_name,
                    "Peptide Monoisotopic Mass": full_mass,
                    "Protein Accession": line["Protein ID"]#+'|###|'+full_seq,
                }

                spec_seq_id = '{0}#{1}'.format(line['Spectrum Title'], line['Sequence'])
                if spec_seq_id not in self.spec_sequence_dict.keys():
                    self.spec_sequence_dict[spec_seq_id] = {
                        'masses' : [],
                        'names' : [],
                        'line_dicts' : [],
                    }
                self.spec_sequence_dict[spec_seq_id]['masses'].append(full_mass)
                self.spec_sequence_dict[spec_seq_id]['names'].append(full_seq_name)
                self.spec_sequence_dict[spec_seq_id]['line_dicts'].append(line_to_write)

        with open(out_name, "wt") as fout:
            writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            for spec_sequence in self.spec_sequence_dict.keys():
                if len(set(self.spec_sequence_dict[spec_sequence]['masses'])) == 1:
                    monoisotopic_mass = self.spec_sequence_dict[spec_sequence]['masses'][0]
                    full_seq = '|||'.join(sorted(set(self.spec_sequence_dict[spec_sequence]['names'])))
                else:
                    monoisotopic_mass = statistics.mean(
                        self.spec_sequence_dict[spec_sequence]['masses']
                    )
                    full_seq = '|||'.join(sorted(set(self.spec_sequence_dict[spec_sequence]['names'])))
                seq = full_seq.split('#')[0]
                seq_mod = '{0}[{1}]'.format(seq, full_seq)
                for line_dict in self.spec_sequence_dict[spec_sequence]['line_dicts']:
                    line_dict["Full Sequence"] = seq_mod
                    line_dict["Peptide Monoisotopic Mass"] = monoisotopic_mass
                    line_dict["Protein Accession"] #+= '|###|{0}'.format(full_seq)
                    writer.writerow(line_dict)
        return out_name

    def get_full_seq_and_mass(self, full_line_dict):
        sequence = full_line_dict['Sequence']
        modifications = full_line_dict['Modifications']
        mass_diff = full_line_dict['Mass Difference']
        glycan_mass = full_line_dict.get('Glycan Mass', '')

        seq_mod = '{0}#{1}'.format(sequence, modifications)
        self.cc.use(seq_mod)
        seq_mod_mass = self.cc._mass()

        if mass_diff.strip() == '':
            mass_diff_mass = 0
            mass_diff_name = ''
        elif mass_diff.endswith(':n'):
            mass_diff_mass = 0
            mass_diff_name = ''
        else:
            mass_diff_mass = float(mass_diff.rsplit(':', maxsplit=1)[0].split('(')[0])
            mass_diff_name = mass_diff

        if glycan_mass.strip() == '':
            glycan_name = ''
            glycan_mass = 0
        else:
            glycan_mass = float(glycan_mass)
            glycan_name = full_line_dict['Glycan']

        full_seq = '{0}#{1}#{2}'.format(seq_mod, mass_diff_name, glycan_name)
        full_mass = round(seq_mod_mass + mass_diff_mass + glycan_mass, 5)

        return full_seq, full_mass

    def rewrite_as_csv(self, tsv_path):
        base, ext = os.path.splitext(tsv_path)
        csv_path = base + '.csv'
        with open(tsv_path) as fin, open(csv_path, 'wt') as fout:
            reader = csv.DictReader(fin, delimiter='\t')
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(fout, fieldnames=fieldnames)
            writer.writeheader()
            for line in reader:
                # only header translation for quantifiedPeaks
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
        lines_to_write = []
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
                lines_to_write.append(out_line_dict)
            for line in lines_to_write:
                writer.writerow(line)
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
        self.all_filenames = set()
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
                    self.all_filenames.add(line_dict['FileName'])
                    writer.writerow(line_dict)

        # Convert unified csv to FlashLFQ input
        unified_csv = self.params["translations"]["quantification_evidences"]
        self.cc = ChemicalComposition()
        psm_input = self.rewrite_psm_input(unified_csv)

        command_list = []
        if sys.platform in ["win32"]:
            command_list = []
        else:
            command_list = ["mono"]

        # TODO?
        # move all files in dir but not in input files to tmp folder
        # and move back to original folder in postflight
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
        print(' '.join(command_list))
        self.params["command_list"] = command_list

    def postflight(self):
        output_files_basenames = [
            "QuantifiedPeaks.tsv",
            "QuantifiedPeptides.tsv",
            "QuantifiedProteins.tsv",
            "BayesianFoldChangeAnalysis.tsv",
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
                    new_out = '{out_name}{ext}'.format(out_name=out_name, ext='.csv')
                else:
                    new_out = "{out_name}_{suffix}{ext}".format(out_name=out_name, suffix=suffix, ext=ext)
                new_path = os.path.join(self.params["output_dir_path"], new_out)
                os.rename(csv_file, new_path)
