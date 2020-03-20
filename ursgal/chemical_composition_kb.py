#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
The knowledge base holds all constants required for chemical composistion
in ursgal.

ISOTOPIC_DISTRIBUTIONS correspond to Berglund M. & Wieser M.E.
Isotopic compositions of the elements 2009 (IUPAC Technical Report)
Pure Appl. Chem., 2011, Vol. 83, No. 2, pp. 397-410
http://dx.doi.org/10.1351/PAC-REP-10-06-02
Published online 2011-01-14
http://www.ciaaw.org/pubs/TICE2009.pdf


"""
#
# ursgal
#
# Copyright (C) 2010-2011 J. Barth, A. Niehues and C. Fufezan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

isotopic_distributions = {
    # Isotopic masses verified using
    # http://ciaaw.org/atomic-masses.htm
    # Wang, M., Audi, G., Wapstra, A. H., Kondev, F. G., MacCormick, M.,
    # Xu, X. and Pfeiffer, B. (2012)
    # The Ame2012 atomic mass evaluation. Chinese Phys. C 36, 1603–2014
    'H': [(1.0078250322, 0.999885), (2.0141017781, 0.000115)],
    'C': [(12.0000,       0.9893), (13.003354835, 0.0107)],
    'N': [(14.003074004,  0.99636), (15.000108899, 0.00364)],
    'O': [(15.994914620,  0.99757), (16.999131757, 0.00038),
          (17.999159613,  0.00205)],
    'Si': [(27.976926535,  0.92223), (28.976494665, 0.04685),
           (29.97377001,  0.03092)],
    'P': [(30.973761998,  1.00)],
    'S': [(31.972071174,  0.9499), (32.971458910, 0.0075),
          (33.9678670,  0.0425), (35.967081, 0.0001)],
    'Na': [(22.98976928,  1.00)],
    'Cl': [(34.9688527,  0.7576), (36.9659026, 0.2424)],
    'Br': [(78.918338,  0.5069), (80.916290, 0.4931)],
    'Se': [(73.9224759,  0.0089), (75.9192137, 0.0937),
           (76.9199142,  0.0763), (77.917309, 0.2377),
           (79.916522,  0.4961), (81.916700, 0.0873)]
}

aa_compositions = {
    'A': 'C3H5NO',
    'C': 'C3H5NOS',
    'D': 'C4H5NO3',
    'E': 'C5H7NO3',
    'F': 'C9H9NO',
    'G': 'C2H3NO',
    'H': 'C6H7N3O',
    'I': 'C6H11NO',
    'K': 'C6H12N2O',
    'L': 'C6H11NO',
    'M': 'C5H9NOS',
    'N': 'C4H6N2O2',
    'P': 'C5H7NO',
    'Q': 'C5H8N2O2',
    'R': 'C6H12N4O',
    'S': 'C3H5NO2',
    'T': 'C4H7NO2',
    'V': 'C5H9NO',
    'W': 'C11H10N2O',
    'Y': 'C9H9NO2',
    'U': 'C3H5NOSe'  # Selenocystein
}

monosaccharide_compositions = {
    "dHex"      : 'C6H10O4',
    "dHexNAc"   : 'C8H13NO4',
    "Hex"       : 'C6H10O5',
    "HexA"      : 'C6H8O6',
    "HexNAc"    : 'C8H13NO5',
    "Me2Hex"    : 'C8H14O5',
    "MeHex"     : 'C7H12O5',
    "MedHex"    : 'C7H12O4',
    "NeuAc"     : 'C11H17NO8',
    "Pent"      : 'C5H8O4',
    'dHexN'     : 'C6H11O3N',
    'HexN'      : 'C6H11O4N',
    'MeHexA'    : 'C7H10O6',
    'NOHCNFmPse': 'C14H22O8N2',
    'dHexNSpep' : 'C13H23O8N3S',
    'Hep'       : 'C7H12O6',
}

aa_names = {
    'A': 'alanine',
    'C': 'cysteine',
    'D': 'aspartic_acid',
    'E': 'glutamic_acid',
    'F': 'phenylalanine',
    'G': 'glycine',
    'H': 'histidine',
    'I': 'isoleucine',
    'K': 'lysine',
    'L': 'leucine',
    'M': 'methionine',
    'N': 'asparagine',
    'P': 'proline',
    'Q': 'glutamine',
    'R': 'arginine',
    'S': 'serine',
    'T': 'threonine',
    'V': 'valine',
    'W': 'tryptophan',
    'Y': 'tyrosine',
    'U': 'selenocystein'  # Selenocystein
}
