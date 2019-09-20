#!/usr/bin/env python
# encoding: utf-8
"""

"""
from __future__ import absolute_import
import sys
import os

import ursgal.uparams
# this is for unorthodox queries of the params.
# please use the unode functions or UParamsMapper
# to access params since they are translated,
# grouped and so on ...

from .umapmaster import UParamMapper
# from .umapmaster import UPeptideMapper

from .unode import Meta_UNode
from .unode import UNode

from .ucontroller import UController
from .ucore import COLORS

from .chemical_composition import ChemicalComposition as ChemicalComposition
from . import chemical_composition_kb
from .unimod_mapper import UnimodMapper

import ursgal.ucore
from .profiles import PROFILES

import ursgal.ukb

GlobalUnimodMapper = UnimodMapper()
base_dir = os.path.dirname( __file__)


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
