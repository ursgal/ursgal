#!/usr/bin/env python3

# encoding: utf-8

import ursgal
import csv
import os


TESTS = [

    {'peptide': 'STGGAAGMLGGARSQRVVR'},
    {'peptide': 'FTMADGGSIEPQENTSGEAFVEELIR'},
    {'peptide': 'AAGGAIPHHTYAAACIDTEDVEAAAAACR'},
    {'peptide': 'AERTGGEWGVSRDGAGGGSAGGGGR'},
    {'peptide': 'QDAAVTTGTVAAAAAAAAFGGGK'},
    {'peptide': 'AMVAGGVEAGVLADGADERSAVQLGK'},
    {'peptide': 'IEGEFAAVEELDSSAGLLK'},
    {'peptide': 'EGMRPRFTSSVPGEYR'},
    {'peptide': 'AKAGASAADGTAASTNSESAEGRNSAEEK'},
    {'peptide': 'ATSTESDEIALLEK'},
    {'peptide': 'SPATGPATSGGLMSASPGNGAMVR'},
    {'peptide': 'VEEDGEELSLDEESDALAASDFSQAEPR'},
    {'peptide': 'RRGVGGGSGGSCGGGSGGQGGCGGGGAGR'},
    {'peptide': 'AAAAAAPPADETAAAAAALEAVATAAAAPAPEAAPVGR'},
    {'peptide': 'APGAGPGTTLLITDIQSSTALWELLPEDVMAK'},
    {'peptide': 'AVSRANGGGGGGAAAAANTGGAAASTSGGGAAAEGAGAAGEGGEDPAMR'},
    {'peptide': 'SSGGGGSRGAIGTGTGGANKFPQPK'},
    {'peptide': 'GLLLDLADPVIGAAWEPHISDPGLWRFLKPHLK'},
    {'peptide': 'GWLAVQALEPQAERREAPAPGPTAAVSAAAPAAADK'},
    {'peptide': 'FQAAPWTFFLRSPLTDEPVDASMCR'},
    {'peptide': 'VFQRVTVNAVDEWDEEARMHVAER'},
    {'peptide': 'LGALEDADQGFSLLGIGFDEWK'},
    {'peptide': 'CMNPVTDIAGGAEALLPSPTAPPQGSHSEVAR'},
    {'peptide': 'GGSGGGGGGGGGGDGSGGRMVPGSGGSSAQAGQGPGDSLAGAPSASAAGR'},
    {'peptide': 'QTQLEDQAEEEEAEAQAQAEK'},
    {'peptide': 'KAFLEYLAVQQEQLAREGVAELPPEQQEQLMR'},
    {'peptide': 'QLKDIEERSSAVSSGITENEEADLIEIIVISLNK'},
    {'peptide': 'LGSTSAPPSASKHGTPAGGGGSGGGR'},
    {'peptide': 'LGLFFPAGLAHTEPDRSKEPQYAQCGTR'},
    {'peptide': 'VHGAYERYPTFLVQAHYEAGRGAAAEFMGYSGR'},
    {'peptide': 'DLNEIPAAVQIILALELFSAVQDPMHLRDAKVK'},
    {'peptide': 'GSSCSGTYVSGSALDVTHTGTSGQDSSGDVWGSAAEKRSGGR'},
    {'peptide': 'LDFGMPGYLDGAKVAVEMRAGGLQLR'},
    {'peptide': 'SEVAQPVGVEGSPSALLPAGLGSLVAGK'},
    {'peptide': 'AAAAATQAGSRDPAHSLGKAAAAASLAAALLDASLLTTLHVHVPSGR'},
]

R = ursgal.UController(
    profile = 'LTQ XL low res',
    params = {
        'database': 'tests/data/test_Creinhardtii_target_decoy.fasta',
        'modifications':[
            '*,opt,Prot-N-term,Acetyl'    # N-Acteylation[]
        ]
    },
    force=True
)
IS_AVAILABLE = R.unodes['omssa_2_1_9']['available']

if IS_AVAILABLE:
    output_file = R.search(
        input_file = 'tests/data/test_Creinhardtii_QE_pH8.mzML',
        engine     = 'omssa',
        force      = True
    )
else:
    output_file = os.path.join(
        'tests',
        'data',
        'test_shipped_Creinhardtii_QE_pH8_omssa_2_1_9_unified.csv'
    )

peptides_set = set()
for line_dict in csv.DictReader(open(output_file, 'r')):
    peptides_set.add( line_dict['Sequence'] )


def compare_peptide_test():
    for test_id, test_dict in enumerate(TESTS):
        yield compare_peptide, test_dict


def compare_peptide( test_dict ):
    assert test_dict['peptide'] in peptides_set


def number_of_peptides_test():
    test_peptides = set()
    for peptide_dict in TESTS:
        test_peptides.add( peptide_dict['peptide'] )
    assert len(peptides_set) == len(test_peptides)


if __name__ == '__main__':
    print(__doc__)
