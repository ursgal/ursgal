#!/usr/bin/env python3.4
import os
import pickle
import sys

import ursgal


class TMT_quant_1_0_0(ursgal.UNode):
    """TMT_quant_0_0_1 UNode

    Takes an mzML as input, removes coalescence of TMT channels, performs normalization
    and computes S2I and P2T.
    """

    META_INFO = {
        "edit_version": 1.00,
        "name": "TMT quant",
        "version": "0.0.1",
        "release_date": None,
        "engine_type": {"quantification_engine": True},
        "input_extensions": [".mzML", ".mzML.gz"],
        "output_extensions": [".csv"],
        "create_own_folder": True,
        # 'output_suffix'      : '',
        "include_in_git": True,
        "in_development": True,
        "distributable": True,
        "utranslation_style": "TMT_quant_style_1",
        "engine": {
            "platform_independent": {"arc_independent": {"exe": "TMT_quant_0_0_1.py"}}
        },
        "citation": "",
    }

    def __init__(self, *args, **kwargs):
        super(TMT_quant_1_0_0, self).__init__(*args, **kwargs)

    def _execute(self):
        main = self.import_engine_as_python_function("main")
        mzml_file = os.path.join(
            self.params["input_dir_path"], self.params["input_file"]
        )
        out = os.path.join(self.params["output_dir_path"], self.params["output_file"])
        main(mzml_file, out, self.params["translations"])
