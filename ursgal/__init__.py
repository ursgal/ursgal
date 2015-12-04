#!/usr/bin/env python3.4
# encoding: utf-8
"""

"""
from __future__ import absolute_import
import sys
import os


# We store our version number in a simple text file:
version_path = os.path.join(
    os.path.dirname(__file__),
    'version.txt'
)
with open(version_path, 'r') as version_file:
    ursgal_version = version_file.read().strip()

__version__  = ursgal_version
version_info = tuple(map(int, ursgal_version.split(".")))

if not hasattr(sys, "version_info") or sys.version_info < (3, 4):
    raise RuntimeError("Ursgal requires Python 3.4 or later.")

from .unode import UNode
from .unode import Meta_UNode
from .ucontroller import UController
from .ucore import COLORS

from .chemical_composition import ChemicalComposition as ChemicalComposition
from . import chemical_composition_kb
from .unimod_mapper import UnimodMapper

import ursgal.ucore
from .profiles import PROFILES

GlobalUnimodMapper = UnimodMapper()
base_dir = os.path.dirname( __file__)
