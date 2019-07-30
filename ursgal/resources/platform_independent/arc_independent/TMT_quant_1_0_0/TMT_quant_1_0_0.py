#!/usr/bin/env python3
"""Ursgal main resource for TMT quantification.

Takes an mzML as input, removes crosstalk of TMT channels, performs normalization
and computes S2I and P2T
"""
import os
import pickle
import time
from collections import OrderedDict as ODict
from io import StringIO

from scipy import linalg
import numpy as np
import pandas as pd
import pymzml
import pyqms

PROTON = 1.007_276_466_583


# @profile
def fix_crosstalk_linalg_solve(channels, matrix):
    corrected_intensities = linalg.solve(matrix, channels)
    return corrected_intensities


# @profile
def fix_crosstalk_dot(channels, impurity_matrix_inversed, params=None):
    """Correct crosstalk between TMT channels.
    
    Args:
        ms2_spectrum (pymzml.spec.Spectrum): input ms2 spectrum
        params (dict, optional): additional params

    """
    corrected_intensities = impurity_matrix_inversed.dot(channels)
    return corrected_intensities


# @profile
def get_intensities(
    masses, all_peaks, tolerance_unit="da", tolerance_ppm=5e-6, tolerance_da=0.002
):
    """Extract given masses with intensities from spectrum.
    
    Args:
        masses (list): list of masses/mz values to extract from spectrum
        all_peaks (np.ndarray): mz, i array
        tolerance_unit (str, optional): tolerane unit
        tolerance_ppm (float, optional): use tolerance in ppm (relative)
        tolerance_da (float, optional): use tolerance in da (absolute)
    
    """
    signals = {}
    if tolerance_unit.lower() == "ppm":
        tolerance = (all_peaks * tolerance_ppm)[:, 0]
    elif tolerance_unit.lower() == "da":
        tolerance = tolerance_da
    else:
        raise Exception("Dont know unit: {tolerance_unit}. Please use either ppm or da")
    for i, rep_ion in enumerate(masses):
        idx = abs(all_peaks[:, 0] - rep_ion) < tolerance
        peak = all_peaks[idx]
        for p in peak:
            signals[p[0]] = p[1]
    return signals


# @profile
def extract_reporter_signals(ms2_spectrum, reporter_ions, tolerance):
    """Extract signals of given reporter ions.
    
    Args:
        ms2_spectrum (pymzml.spec.Spectrum): input MS2 spectrum
        reporter_ions (dict): dict mapping reporter ion name to mass
        tolerance (TYPE): tolerance in dalton
    
    Returns:
        list: sorted list of reporter intensities
    
    """
    all_peaks = ms2_spectrum.peaks("centroided")
    if not len(all_peaks) == 0:
        sliced_peaks = all_peaks
        signals = np.array([0 for x in range(len(reporter_ions))])
        if len(sliced_peaks) > 0:
            for i, (triv_name, rep_ion_mz) in enumerate(sorted(reporter_ions.items())):
                idx = abs(sliced_peaks[:, 0] - rep_ion_mz) < tolerance
                test = sliced_peaks[idx]
                if len(test) == 1:
                    signals[i] = test[0][1]
                else:
                    signals[i] = 0
        else:
            signals = []
    else:
        signals = []
    return signals


# @profile
def calculate_S2I(
    ms1_spectrum, peptide, charge, isolation_window_borders
):
    """Calculate Signal to Intensity.
    
    For that, the sum of all isotope intensities in the isolation windows is divided by
    the sum of all intensities in the isolation window.
    
    Args:
        ms1_spectrum (pymzml.spec.Spectrum): input_spectrum
        peptide (str): peptide sequence with mods in unimod style
        charge (int): charge of the precursor peptide
        isolation_window_borders (tuple): upper and lower precurso isolation border
    
    """
    lower_border, upper_border = isolation_window_borders
    mz = ms1_spectrum.peaks("centroided")
    all_ions_in_iso_border = mz[lower_border < mz[:, 0]]
    all_ions_in_iso_border = all_ions_in_iso_border[
        upper_border > all_ions_in_iso_border[:, 0]
    ]
    isotope_mz = [peptide, peptide + (PROTON / charge)]
    isotope_int = get_intensities(
        isotope_mz, all_ions_in_iso_border, tolerance_unit="ppm"
    )

    isotope_int_sum = sum(isotope_int.values())
    all_ions_int_sum = sum(all_ions_in_iso_border[:, 1]) + 0.000001
    S2I = isotope_int_sum / all_ions_int_sum
    return S2I


# @profile
def calculate_P2T(
    ms1_spectrum, peptide, charge, isolation_window_borders
):
    """Calculate Precursor to Threshold.
    
    Divide the sum of all isotope intensities in isolation window by the noise level.
    
    Args:
        ms1_spectrum (pymzml.spec.Spectrum): input_spectrum
        peptide (str): peptide sequence with mods in unimod style
        charge (int): charge of the precursor peptide
        isolation_window_borders (tuple): upper and lower precurso isolation border
    
    """
    lower_border, upper_border = isolation_window_borders
    mz = ms1_spectrum.peaks("centroided")
    all_ions_in_iso_border = mz[lower_border < mz[:, 0]]
    all_ions_in_iso_border = all_ions_in_iso_border[
        upper_border > all_ions_in_iso_border[:, 0]
    ]
    isotope_mz = [peptide, peptide + (PROTON / charge)]
    isotope_int = get_intensities(
        isotope_mz, all_ions_in_iso_border, tolerance_unit="ppm"
    )

    isotope_int_sum = sum(isotope_int.values())
    noise_level = ms1_spectrum.estimated_noise_level(mode="median")
    P2T = isotope_int_sum / noise_level
    return P2T


# @profile
def correct_S2I(raw_channels, S2I):
    """Correct Signal 2 Intensity.
    
    To be implemented
    
    Args:
        raw_channels (np.ndarray): array with measured channel intensities
        S2I (float): Signal 2 Intensity
    
    Returns:
        np.ndarray: array with S2I corrected intensities
    
    """
    normalized_channels = raw_channels / (raw_channels.sum() + 1e-5)
    interfering_signal = sum(raw_channels * (1 - S2I))
    interfering_signal_per_reporter = normalized_channels * interfering_signal
    no_inference_channels = raw_channels - interfering_signal_per_reporter
    corrected_channels = (no_inference_channels / (raw_channels.sum() + 1e-5))
    return corrected_channels


# @profile
def interpolate_qc(qc_e, qc_l, RT_e, RT_l, RT_ms2):
    """Calculate time weighted linear combination to extrapolate quality control values.
    
    Args:
        qc_e (float): quality score of early scan
        qc_l (float): quality score of late scan
        RT_e (float): Retention time of early scan
        RT_l (float): Retention time of late scan
        RT_ms2 (float): Retention time of MS2 scan
    
    Returns:
        float: Interpolated QC value
    
    """
    return (RT_ms2 - RT_e) * ((qc_l - qc_e) / (RT_l - RT_e)) + qc_e


# @profile
def main(mzml_file, output_file, param_dict):
    """
    Perform quantification based on mzML input file.
    
    Take an mzML as input, remove coalescence of TMT channels, perform normalization
        and compute S2I and S2N.
    
    Args:
        mzml_file (str): path to input mzml
        output_file (str): path to output csv
        param_dict (dict): dict with all node related parameters
    
    """
    param_dict["reporter_ion_mzs"] = ODict(param_dict["reporter_ion_mzs"])
    trivial_names = param_dict["reporter_ion_mzs"].keys()

    impurity_data = StringIO(param_dict["impurity_matrix"])
    impurity_data = pd.read_csv(impurity_data)

    impurity_matrix = impurity_data.drop(columns="Mass-Tag").values
    impurity_matrix_transposed = impurity_matrix.T
    impurity_matrix_inversed = np.linalg.inv(impurity_matrix_transposed)

    reader = pymzml.run.Reader(mzml_file)
    previous_ms2_idents = []

    all_lines = {}
    all_data  = {}
    tmt_data  = {}
    S2I_data  = {}
    P2T_data  = {}

    for i, spec in enumerate(reader):
        if i % 500 == 0:
            print(f"Process spec {i}", end="\r")
        if spec.ms_level == 1:
            ms1_spec = spec
            if len(previous_ms2_idents) > 0:
                for ident_info in previous_ms2_idents:
                    s2i_spec_data = S2I_data[ident_info["ID"]]
                    p2t_spec_data = P2T_data[ident_info["ID"]]
                    S2I = calculate_S2I(
                        ms1_spec,
                        ident_info["mz"],
                        ident_info["charge"],
                        ident_info["isolation_window_borders"],
                    )
                    s2i_spec_data["S2I_after"] = S2I
                    s2i_spec_data[
                        "RT_after"
                    ] = ms1_spec.scan_time_in_minutes()
                    P2T = calculate_P2T(
                        ms1_spec,
                        ident_info["mz"],
                        ident_info["charge"],
                        ident_info["isolation_window_borders"],
                    )
                    p2t_spec_data["P2T_after"] = P2T
                    p2t_spec_data[
                        "RT_after"
                    ] = ms1_spec.scan_time_in_minutes()
                    interpol_S2I = interpolate_qc(
                        s2i_spec_data["S2I_before"],
                        s2i_spec_data["S2I_after"],
                        s2i_spec_data["RT_before"],
                        s2i_spec_data["RT_after"],
                        s2i_spec_data["RT_MS2"],
                    )
                    interpol_P2T = interpolate_qc(
                        p2t_spec_data["P2T_before"],
                        p2t_spec_data["P2T_after"],
                        p2t_spec_data["RT_before"],
                        p2t_spec_data["RT_after"],
                        p2t_spec_data["RT_MS2"],
                    )
                    s2i_corrected_channels = correct_S2I(
                        tmt_data[ident_info['ID']]['raw'], interpol_S2I
                    )
                    # breakpoint()
                    # Implement normalization over peptides
                    for i, channel in enumerate(tmt_data[ident_info['ID']]['raw']):
                        # breakpoint()
                        nd = {**all_lines[ident_info["ID"]]}
                        nd['Quant Ion'] = list(trivial_names)[i]
                        nd['rel Intensity'] = tmt_data[ident_info['ID']]['normalized'][i]
                        nd['abs Intensity'] = tmt_data[ident_info['ID']]['raw'][i]
                        nd['corr Intensity'] = s2i_corrected_channels[i]
                        nd['P2T'] = interpol_P2T
                        nd['S2I'] = interpol_S2I
                        all_data[ident_info['ID']].append(nd)
                previous_ms2_idents = []
        elif spec.ms_level == 2:
            ms2_spec = spec
            raw_channels = extract_reporter_signals(
                ms2_spec,
                param_dict["reporter_ion_mzs"],
                param_dict["reporter_ion_tolerance"],
            )
            # fixed_channels = fix_crosstalk_dot(raw_channels, impurity_matrix_transposed)
            fixed_channels = fix_crosstalk_linalg_solve(raw_channels, impurity_matrix_inversed)
            if all(fixed_channels == 0):
                continue
            # assert np.allclose(fixed_channels, fixed_channels2), f'{fixed_channels}\n{fixed_channels2}'
            normalized_channels = fixed_channels / fixed_channels.sum()
            if spec.ID not in tmt_data:
                tmt_data[spec.ID] = {'raw': None, 'fixed': None}
            tmt_data[spec.ID]['raw'] = fixed_channels
            tmt_data[spec.ID]['normalized'] = normalized_channels 
            if spec.ID not in all_data:
                all_data[spec.ID] = []

            iso_mz = spec["isolation window target m/z"]
            lower_border = iso_mz - spec["isolation window lower offset"]
            upper_border = iso_mz + spec["isolation window upper offset"]
            charge = spec["charge state"]
            ident_info = {
                'mz': iso_mz,
                "charge": charge,
                "isolation_window_borders": (lower_border, upper_border),
                "RT": ms2_spec.scan_time_in_minutes(),
                "ID": ms2_spec.ID,
            }
            previous_ms2_idents.append(ident_info)
            S2I = calculate_S2I(
                ms1_spec,
                ident_info['mz'],
                ident_info["charge"],
                ident_info["isolation_window_borders"],
            )
            if ms2_spec.ID not in S2I_data:
                S2I_data[ms2_spec.ID] = {
                    "S2I_before": S2I,
                    "S2I_after": None,
                    "RT_before": ms1_spec.scan_time_in_minutes(),
                    "RT_after": None,
                    "RT_MS2": ms2_spec.scan_time_in_minutes(),
                }
            P2T = calculate_P2T(
                ms1_spec,
                ident_info["mz"],
                ident_info["charge"],
                ident_info["isolation_window_borders"],
            )
            if ms2_spec.ID not in P2T_data:
                P2T_data[ms2_spec.ID] = {
                    "P2T_before": P2T,
                    "P2T_after": None,
                    "RT_before": ms1_spec.scan_time_in_minutes(),
                    "RT_after": None,
                    "RT_MS2": ms2_spec.scan_time_in_minutes(),
                }
            line = ODict(
                {
                    "Spectrum ID": ms2_spec.ID,
                    "Charge": charge,
                    "RT": ms2_spec.scan_time_in_minutes(),
                    "Quant Ion": list(trivial_names),
                    "rel Intensity": normalized_channels,
                    "abs Intensity": fixed_channels,
                    "S2I": None,
                    "P2T": None,
                }
            )
            all_lines[ms2_spec.ID] = line
    flat = [item for list in all_data.values() for item in list]
    final_df = pd.DataFrame(flat)
    float_cols = {
        'rel Intensity': 5,
        'abs Intensity': 5,
        'RT': 3,
        'S2I': 5,
        'P2T': 5,
    }
    final_df = final_df.round(float_cols)
    # sometimes there are -0 and 0, making it hard to compare files using hashes
    final_df['rel Intensity'] += 0.0
    final_df['abs Intensity'] += 0.0
    final_df.to_csv(output_file, index=False)

# @profile
def process_previous_idents(scan_numbers, ms1_spec, data_collections):
    for scan in scan_numbers:
        line = data_collections[scan]
        line['RT After'] = ms1_spec.scan_time_in_minutes()
        S2I = calculate_S2I(
            ms1_spec,
            line['Iso mz'],
            line['charge'],
            (
                line['lower isolation window border'],
                line['upper isolation window border'],
            ),
        )
        P2T = calculate_P2T(
            ms1_spec,
            line['Iso mz'],
            line['charge'],
            (
                line['lower isolation window border'],
                line['upper isolation window border'],
            ),
        )

        line['S2I After'] = S2I
        line['P2T After'] = P2T

        interpol_S2I = interpolate_qc(
            line['S2I Before'],
            line['S2I After'],
            line["RT Before"],
            line["RT After"],
            line["Retention time (minutes)"],
        )
        interpol_P2T = interpolate_qc(
            line['P2T Before'],
            line['P2T After'],
            line["RT Before"],
            line["RT After"],
            line["Retention time (minutes)"],
        )

        line['S2I interpolated'] = interpol_S2I
        line['P2T interpolated'] = interpol_P2T


# @profile
def normalize_row(row):
    tmt_cols = [key for key in row.keys() if key.startswith('1')]
    normalized = row[tmt_cols] / row[tmt_cols].sum()
    return normalized

# @profile
def correct_S2I_row(row):
    """Correct Signal 2 Intensity.
    
    Args:
        row (pandas.core.series.Series): row from a pandas dataframe
        
    Returns:
        np.ndarray: row with S2I corrected channels.
    
    """
    S2I = row['S2I interpolated']
    tmt_cols = [col for col in row.keys() if col.startswith('1')]
    raw_channels = row[tmt_cols]
    normalized_channels = raw_channels / (raw_channels.sum() + 1e-5)
    interfering_signal = sum(raw_channels * (1 - S2I))
    interfering_signal_per_reporter = normalized_channels * interfering_signal
    no_inference_channels = raw_channels - interfering_signal_per_reporter
    corrected_channels = (no_inference_channels / (raw_channels.sum() + 1e-5))
    return corrected_channels

# @profile
def main2(mzml_file, output_file, param_dict):
    param_dict["reporter_ion_mzs"] = ODict(param_dict["reporter_ion_mzs"])
    trivial_names = list(param_dict["reporter_ion_mzs"].keys())

    impurity_data = StringIO(param_dict["impurity_matrix"])
    impurity_data = pd.read_csv(impurity_data)

    impurity_matrix = impurity_data.drop(columns="Mass-Tag").values
    impurity_matrix_transposed = impurity_matrix.T
    impurity_matrix_inversed = np.linalg.inv(impurity_matrix_transposed)

    reader = pymzml.run.Reader(mzml_file)
    previous_ms2_idents = []

    data_colletions = {}
    EMPTY = 0

    for i, spec in enumerate(reader):
        if i % 500 == 0:
            print(f"Process spec {i}", end="\r")
        if spec.ms_level == 1:
            ms1_spec = spec
            if len(previous_ms2_idents) > 0:
                process_previous_idents(previous_ms2_idents, ms1_spec, data_colletions)
            previous_ms2_idents = []
        elif spec.ms_level == 2:
            ms2_spec = spec
            raw_channels = extract_reporter_signals(
                ms2_spec,
                param_dict["reporter_ion_mzs"],
                param_dict["reporter_ion_tolerance"],
                # param_dict["reporter_ion_tolerance_unit"],
            )
            fixed_channels = fix_crosstalk_dot(raw_channels, impurity_matrix_transposed)
            # fixed_channels = fix_crosstalk_linalg_solve(raw_channels, impurity_matrix_inversed)
            if all(fixed_channels == 0):
                EMPTY += 1
                continue
            if spec.ID not in data_colletions:
                data_colletions[spec.ID] = {}
            iso_mz = spec["isolation window target m/z"]
            lower_border = iso_mz - spec["isolation window lower offset"]
            upper_border = iso_mz + spec["isolation window upper offset"]
            charge = int(spec["charge state"])

            for i, name in enumerate(trivial_names):
                data_colletions[spec.ID][name] = fixed_channels[i]

            S2I = calculate_S2I(
                ms1_spec,
                iso_mz,
                charge,
                (lower_border, upper_border),
            )
            P2T = calculate_P2T(
                ms1_spec,
                iso_mz,
                charge,
                (lower_border, upper_border),
            )

            data_colletions[spec.ID]['charge'] = charge
            data_colletions[spec.ID]['Iso mz'] = iso_mz
            data_colletions[spec.ID]['lower isolation window border'] = lower_border
            data_colletions[spec.ID]['upper isolation window border'] = upper_border
            data_colletions[spec.ID]['Retention time (minutes)'] = ms2_spec.scan_time_in_minutes()
            data_colletions[spec.ID]['Spectrum ID'] = spec.ID
            data_colletions[spec.ID]['S2I Before'] = S2I
            data_colletions[spec.ID]['P2T Before'] = P2T
            data_colletions[spec.ID]['RT Before'] = ms1_spec.scan_time_in_minutes()

            previous_ms2_idents.append(spec.ID)

    print(f'Skipped {EMPTY} specs.')
    flat = [line for line in data_colletions.values()]
    dataframe = pd.DataFrame(flat)
    tmt_cols = [col for col in dataframe.columns if col.startswith('1')]
    not_tmt_cols = [col for col in dataframe.columns if not col.startswith('1')]
    
    # normalize over peptides
    all_intensities = dataframe[tmt_cols].aggregate('sum')
    medians = dataframe[tmt_cols].aggregate('median')
    dataframe[tmt_cols] = dataframe[tmt_cols] / all_intensities

    # normalize over channels
    # normalize channels
    # dataframe[tmt_cols] = dataframe.apply(normalize, axis=1)

    # correct S2I
    dataframe[tmt_cols] = dataframe.apply(correct_S2I_row, axis=1)
    dataframe[tmt_cols] = dataframe.apply(normalize_row, axis=1)

    # melto to longformat
    dataframe = \
        dataframe.melt(
            id_vars=not_tmt_cols,
            var_name="Quant Ion",
            value_name="Intensity"
        )
    dataframe.to_csv(output_file, index=False)
