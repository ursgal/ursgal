"""Tests for TMT quant node
"""
import os
from io import StringIO
import numpy as np
import pandas as pd
from pyqms.chemical_composition import ChemicalComposition

import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            __file__,
            "..",
            "..",
            "ursgal",
            "resources",
            "platform_independent",
            "arc_independent",
            "TMT_quant_1_0_0",
        )
    ),
)

from TMT_quant_1_0_0 import (
    calculate_P2T,
    calculate_S2I,
    fix_crosstalk_dot,
    fix_crosstalk_linalg_solve,
    get_intensities,
    interpolate_qc,
    correct_S2I,
)

PROTON = 1.007_276_466_583


ISOTOPE_OVERLAP1 = """
Mass-Tag,126,127L,127H
126 ,0.950,0.050,0.000
127L,0.000,0.950,0.050
127H,0.000,0.000,1.000
"""


ISOTOPE_OVERLAP2 = """
Mass-Tag,126,127L,127H
126 ,1.000,0.000,0.000
127L,0.000,0.500,0.500
127H,0.000,0.000,1.000
"""

ISOTOPE_OVERLAP3 = """
Mass-Tag,126,127L,127H
126 ,0.500,0.000,0.500
127L,0.000,1.000,0.000
127H,0.000,0.000,1.000
"""


class Spectrum:
    def __init__(self, peaks=None, noise_level=1):
        self._peaks = peaks
        self._noise_level = noise_level

    def peaks(self, type=None):
        return self._peaks

    def estimated_noise_level(self, mode="median"):
        return self._noise_level


def _correct_S2I(S2I, result):
    channels = np.array([100.0, 200.0, 100.0])
    corrected_intensities = correct_S2I(channels, S2I)
    assert np.allclose(corrected_intensities, result, atol=1e-5)


def test_correct_S2I():
    cases =  [(1, [0.25, 0.5, 0.25]), (0.5, [0.125, 0.25, 0.125]), (0, [0, 0, 0])]
    for c in cases:
        yield _correct_S2I, c[0], c[1]


def _fix_crosstalk_dot(matrix, result):
    """Test crosstalk fix.

    Use precomputed impurities and assert fix sets all values to 100.0
    """
    TMT_channels = np.array([100, 100, 100])
    matrix = StringIO(matrix)
    matrix = pd.read_csv(matrix)
    impurity_matrix = matrix.drop(columns="Mass-Tag").values
    impurity_matrix = impurity_matrix.T
    fixed = fix_crosstalk_dot(TMT_channels, impurity_matrix)
    assert np.allclose(fixed, np.array(result))


def test_fix_crosstalk():
    cases =  [
        (ISOTOPE_OVERLAP1, [95, 100, 105]),
        (ISOTOPE_OVERLAP2, [100, 50, 150]),
        (ISOTOPE_OVERLAP3, [50, 100, 150]),
    ]
    for c in cases:
        yield _fix_crosstalk_dot, c[0], c[1]


def _fix_crosstalk_linalg_solve(matrix, result):
    """Test crosstalk fix.

    Use precomputed impurities and assert fix sets all values to 100.0
    """
    TMT_channels = np.array([100, 100, 100])
    matrix = StringIO(matrix)
    matrix = pd.read_csv(matrix)
    impurity_matrix = matrix.drop(columns="Mass-Tag").values
    impurity_matrix_inversed = np.linalg.inv(impurity_matrix.T)
    fixed = fix_crosstalk_linalg_solve(TMT_channels, impurity_matrix_inversed)
    assert np.allclose(fixed, np.array(result))


def test_fix_crosstalk_linalg_solve():
    cases = [
        (ISOTOPE_OVERLAP1, [95, 100, 105]),
        (ISOTOPE_OVERLAP2, [100, 50, 150]),
        (ISOTOPE_OVERLAP3, [50, 100, 150]),
    ]
    for c in cases:
        yield _fix_crosstalk_linalg_solve, c[0], c[1]


def _compare_crosstalk_solvers(matrix, result):
    TMT_channels = np.array([100, 100, 100])
    matrix = StringIO(matrix)
    matrix = pd.read_csv(matrix)
    matrix = matrix.drop(columns="Mass-Tag").values

    dot_matrix = matrix.T
    linalg_matrix = np.linalg.inv(matrix.T)

    dot_fixed = fix_crosstalk_dot(TMT_channels, dot_matrix)
    linalg_fixed = fix_crosstalk_linalg_solve(TMT_channels, linalg_matrix)

    assert np.allclose(dot_fixed, linalg_fixed)


def test_compare_crosstalk_solvers():
    cases = [
        (ISOTOPE_OVERLAP1, [95, 100, 105]),
        (ISOTOPE_OVERLAP2, [100, 50, 150]),
        (ISOTOPE_OVERLAP3, [50, 100, 150]),
    ]
    for c in cases:
        yield _compare_crosstalk_solvers, c[0], c[1]


def _get_intensities(mz, peaks, unit, tol, expected_result):
    """Test extracting intensities for given masses from peak list.
    
    Args:
        mz (list): mz to extract
        peaks (np.array): peak list
        unit (str): tolerance unit
        tol (float): tolerance
        expected_result (int): number of extracted peaks
    """
    if unit == "da":
        extracted_peaks = get_intensities(
            mz, peaks, tolerance_unit=unit, tolerance_da=tol
        )
    else:
        extracted_peaks = get_intensities(
            mz, peaks, tolerance_unit=unit, tolerance_ppm=tol
        )

    test_result = len(extracted_peaks)
    assert expected_result == test_result


def test_get_intensities():
    cases = [
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "da",
            0.003,
            2,
        ),
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "da",
            0.002,
            2,
        ),
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "da",
            0.0031,
            3,
        ),
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "da",
            0.0,
            0,
        ),
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "ppm",
            20e-5,
            3,
        ),
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "ppm",
            15.87396e-6,
            2,
        ),
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "ppm",
            1e-5,
            0,
        ),
        (
            [126],
            np.array([(126.002, 100), (126.003, 100), (125.998, 100)]),
            "ppm",
            0,
            0,
        ),
    ]
    for c in cases:
        yield _get_intensities, c[0], c[1], c[2], c[3], c[4]


# def _calc_isotope_envelopes(peptides, charges, expected_results):
#     """Test calculation of isotope envelopes.
    
#     Args:
#         peptides (list): list of peptide sequences
#         charges (list): list of charge states
#         expected_results (tuple): tuple with monoisotopic mass
#     """
#     lib = calc_isotope_envelopes(peptides, charges)
#     assert len(lib.keys()) == expected_results[0]
#     peptide_cc = ChemicalComposition(peptides[0]).hill_notation_unimod()
#     assert [peptide_cc] == list(lib.keys())
#     arr = np.array(lib[peptide_cc]["env"][(("N", "0.000"),)][charges[0]]["mz"])
#     assert (abs(arr - expected_results[1]) < expected_results[1] * 5e-6).any()


# def test_calc_isotope_envelopes():
#     cases = [
#         (["ELVISLIVES"], [1], (1, 1100.633 + PROTON)),
#         # test some more cases
#     ]
#     for c in cases:
#         yield _calc_isotope_envelopes, c[0], c[1], c[2]

def _calculate_S2I(ms1_spec, peptide, charge, window, result):
    """Test signal 2 intensity calculation
    
    Args:
        ms1_spec (Spectrum): spectrum class with peaks() and estimated_noise_level methods
        peptide (str): peptide sequence
        charge (int): Description
        window (tuple): lower and upper isolation window border
        result (float): expeted S2I
    """
    # cc_obj = ChemicalComposition()
    # lib = lib = calc_isotope_envelopes([peptide], [charge])
    s2i = calculate_S2I(ms1_spec, peptide, charge, window)
    assert np.isclose(s2i, result)


def test_calcuate_S2I():
    cases = [
        (
            Spectrum(
                peaks=np.array(
                    [
                        (1101.6401678803702, 100),
                        (1102.6431931587235, 400),
                        (1101.8401678803702, 500),
                    ]
                )
            ),
            1100.6328914136 + PROTON,
            1,
            (1100.633 + PROTON - 2, 1100.633 + PROTON + 2),
            0.5,
        ),
        (
            Spectrum(
                peaks=np.array([(1101.6401678803702, 100), (1102.6431931587235, 400)])
            ),
            1100.6328914136 + PROTON,
            1,
            (1100.633 + PROTON - 2, 1100.633 + PROTON + 2),
            1,
        ),
        (
            Spectrum(peaks=np.array([(1101.8401678803702, 500)])),
            1100.6328914136 + PROTON,
            1,
            (1100.633 + PROTON - 2, 1100.633 + PROTON + 2),
            0.0,
        ),
    ]
    for c in cases:
        yield _calculate_S2I, c[0], c[1], c[2], c[3], c[4]


def _calculate_P2T(ms1_spec, peptide, charge, window, result):
    # cc_obj = ChemicalComposition()
    # lib = lib = calc_isotope_envelopes([peptide], [charge])
    p2t = calculate_P2T(ms1_spec, peptide, charge, window)
    assert np.isclose(p2t, result)


def test_calculate_P2T():
    cases = [
        (
            Spectrum(
                peaks=np.array(
                    [
                        (1101.6401678803702, 100),
                        (1102.6431931587235, 400),
                        (1101.8401678803702, 500),
                    ]
                ),
                noise_level=1,
            ),
            1100.6328914136 + PROTON,
            1,
            (1100.633 + PROTON - 2, 1100.633 + PROTON + 2),
            500,
        ),
        (
            Spectrum(
                peaks=np.array(
                    [
                        (1101.6401678803702, 100),
                        (1102.6431931587235, 400),
                        (1101.8401678803702, 500),
                    ]
                ),
                noise_level=2,
            ),
            1100.6328914136 + PROTON,
            1,
            (1100.633 + PROTON - 2, 1100.633 + PROTON + 2),
            250,
        ),
        (
            Spectrum(
                peaks=np.array(
                    [
                        (1101.6401678803702, 100),
                        (1102.6431931587235, 400),
                        (1101.8401678803702, 500),
                    ]
                ),
                noise_level=0.5,
            ),
            1100.6328914136 + PROTON,
            1,
            (1100.633 + PROTON - 2, 1100.633 + PROTON + 2),
            1000,
        ),
        (
            Spectrum(peaks=np.array([(1101.8401678803702, 500)]), noise_level=1),
            1100.6328914136 + PROTON,
            1,
            (1100.633 + PROTON - 2, 1100.633 + PROTON + 2),
            0.0,
        ),
    ]
    for c in cases:
        yield _calculate_P2T, c[0], c[1], c[2], c[3], c[4]


# @pytest.mark.parametrize(
#     "input_data,output",
#     [
#         ((0.5, 0.5, 1, 3, 2), 0.5),  # same S2I always leeds to same output
#         ((100, 100, 1, 5, 2), 100),
#         ((0.25, 0.75, 1, 3, 2), 0.5),  # different S2I, ms2 same distance to e and l
#         ((0.75, 0.25, 1, 3, 2), 0.5),  # and the other way around :)
#         ((-0.75, -0.25, 1, 3, 2), -0.5),  # try negative values
#         ((-0.25, -0.75, 1, 3, 2), -0.5),  # different S2I, ms2 same distance to e and l
#         ((0.25, 0.75, 1, 1e10, 2), 0.25),  # ms2 way closer to early scan
#         ((0.25, 0.75, 1, 1e10, 1e10 - 1), 0.75),  # ms2 way closer to early scan
#     ],
#     ids=[
#         "Same S2I",
#         "Same S2I high value",
#         "Different S2I equidistance",
#         "Different S2I equidistance reverse",
#         "Negative S2I",
#         "Negative S2I reverse",
#         "MS2 close to early scan",
#         "MS2 close to late scan",
#     ],
# )
def _interpolate_qc(input_data, output):
    qc_e, qc_l, RT_e, RT_l, RT_ms2 = input_data
    interpolated_qc = interpolate_qc(qc_e, qc_l, RT_e, RT_l, RT_ms2)
    # assert interpolated_qc == output
    assert np.isclose(interpolated_qc, output)


def test_interpolate_qc():
    cases = [
        ((0.5, 0.5, 1, 3, 2), 0.5),  # same S2I always leeds to same output
        ((100, 100, 1, 5, 2), 100),
        ((0.25, 0.75, 1, 3, 2), 0.5),  # different S2I, ms2 same distance to e and l
        ((0.75, 0.25, 1, 3, 2), 0.5),  # and the other way around :)
        ((-0.75, -0.25, 1, 3, 2), -0.5),  # try negative values
        ((-0.25, -0.75, 1, 3, 2), -0.5),  # different S2I, ms2 same distance to e and l
        ((0.25, 0.75, 1, 1e10, 2), 0.25),  # ms2 way closer to early scan
        ((0.25, 0.75, 1, 1e10, 1e10 - 1), 0.75),  # ms2 way closer to early scan
    ]
    for c in cases:
        yield _interpolate_qc, c[0], c[1]


if __name__ == "__main__":
    pytest.main()
