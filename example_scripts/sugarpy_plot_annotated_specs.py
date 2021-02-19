#!/usr/bin/env python3.4
# encoding: utf-8
import ursgal
import sys
import glob
import os
import shutil


def main(spec_file=None, sugarpy_results=None, sugarpy_results_pkl=None):
    """
    This script can be used to plot any spectrum from SugarPy results.
    It woll plot all spectra listed in the input file (sugarpy_results),
    therefore it is recommended to provide a csv file with only a few,
    representative spectra for each glycopeptide.
    Besides the mzml file corresponding to the glycopeptide identifications,
    the sugarpy results csv file as well as the corresponding pkl file is required.

    Usage:
        ./sugarpy_plot_annotated_specs.py <mzml.idx.gz> <sugarpy_results.csv> <sugarpy_results_pkl>
    """

    # initialize the UController
    uc = ursgal.UController()

    # sugarpy_plot to plot he results from the sugarpy_run
    uc.params.update(
        {
            "prefix": "Annotated_specs",
            "sugarpy_results_pkl": sugarpy_results_pkl,
            "sugarpy_results_csv": sugarpy_results,
            "sugarpy_plot_types": [
                "plot_annotated_spectra",
            ],
            "sugarpy_plot_peak_types": [
                "matched",
                "unmatched",
                "labels",
            ],
            # 'sugarpy_include_subtrees': 'individual_subtrees'
            "rt_pickle_name": os.path.join(
                os.path.dirname(spec_file), "_ursgal_lookup.pkl"
            ),
            "ms_level": 1,
            "plotly_layout": {
                "font": {
                    "family": "Arial",
                    "size": 26,
                    "color": "rgb(0, 0, 0)",
                },
                # 'autosize':True,
                "width": 1750,
                "height": 820,
                "margin": {
                    "l": 120,
                    "r": 50,
                    "t": 50,
                    "b": 170,
                },
                "xaxis": {
                    "type": "linear",
                    "color": "rgb(0, 0, 0)",
                    "title": "m/z",
                    "title_font": {
                        "family": "Arial",
                        "size": 26,
                        "color": "rgb(0, 0, 0)",
                    },
                    "autorange": True,
                    # 'range':[1000,1550.0],
                    "tickmode": "auto",
                    "showticklabels": True,
                    "tickfont": {
                        "family": "Arial",
                        "size": 22,
                        "color": "rgb(0, 0, 0)",
                    },
                    "showexponent": "all",
                    "exponentformat": "B",
                    "ticklen": 5,
                    "tickwidth": 1,
                    "tickcolor": "rgb(0, 0, 0)",
                    "ticks": "outside",
                    "showline": True,
                    "linecolor": "rgb(0, 0, 0)",
                    "showgrid": False,
                    "dtick": 100,
                },
                "yaxis": {
                    "type": "linear",
                    "color": "rgb(0, 0, 0)",
                    "title": "Intensity",
                    "title_font": {
                        "family": "Arial",
                        "size": 26,
                        "color": "rgb(0, 0, 0)",
                    },
                    "autorange": True,
                    # 'range':[0.0,25.0],
                    "showticklabels": True,
                    "tickfont": {
                        "family": "Arial",
                        "size": 22,
                        "color": "rgb(0, 0, 0)",
                    },
                    "tickangle": 0,
                    "showexponent": "all",
                    "exponentformat": "B",
                    "ticklen": 5,
                    "tickwidth": 1,
                    "tickcolor": "rgb(0, 0, 0)",
                    "ticks": "outside",
                    "showline": True,
                    "linecolor": "rgb(0, 0, 0)",
                    "showgrid": False,
                    "zeroline": False,
                },
                # 'legend':{
                #     'font':{
                #         'family':'Arial',
                #         'size':10,
                #         'color':'rgb(0, 0, 0)',
                #     },
                #     'orientation':'v',
                #     'traceorder':'normal',
                # },
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
            },
        }
    )

    sugarpy_plots = uc.execute_misc_engine(
        input_file=spec_file,
        engine="sugarpy_plot_1_0_0",
        force=True,
    )


if __name__ == "__main__":
    main(
        spec_file=sys.argv[1],
        sugarpy_results=sys.argv[2],
    )
