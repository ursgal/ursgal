#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import csv

# TESTS =[
#     {'peptide': 'STGGAAGMLGGARSQRVVR'},
#     {'peptide': 'FTMADGGSIEPQENTSGEAFVEELIR'},
#     {'peptide': 'AAGGAIPHHTYAAACIDTEDVEAAAAACR'},
#     {'peptide': 'AERTGGEWGVSRDGAGGGSAGGGGR'},
#     {'peptide': 'QDAAVTTGTVAAAAAAAAFGGGK'},
#     {'peptide': 'AMVAGGVEAGVLADGADERSAVQLGK'},
#     {'peptide': 'IEGEFAAVEELDSSAGLLK'},
#     {'peptide': 'EGMRPRFTSSVPGEYR'},
#     {'peptide': 'AKAGASAADGTAASTNSESAEGRNSAEEK'},
#     {'peptide': 'ATSTESDEIALLEK'},
#     {'peptide': 'SPATGPATSGGLMSASPGNGAMVR'},
#     {'peptide': 'VEEDGEELSLDEESDALAASDFSQAEPR'},
#     {'peptide': 'RRGVGGGSGGSCGGGSGGQGGCGGGGAGR'},
#     {'peptide': 'AAAAAAPPADETAAAAAALEAVATAAAAPAPEAAPVGR'},
#     {'peptide': 'APGAGPGTTLLITDIQSSTALWELLPEDVMAK'},
#     {'peptide': 'AVSRANGGGGGGAAAAANTGGAAASTSGGGAAAEGAGAAGEGGEDPAMR'},
#     {'peptide': 'SSGGGGSRGAIGTGTGGANKFPQPK'},
#     {'peptide': 'GLLLDLADPVIGAAWEPHISDPGLWRFLKPHLK'},
#     {'peptide': 'GWLAVQALEPQAERREAPAPGPTAAVSAAAPAAADK'},
#     {'peptide': 'FQAAPWTFFLRSPLTDEPVDASMCR'},
#     {'peptide': 'VFQRVTVNAVDEWDEEARMHVAER'},
#     {'peptide': 'LGALEDADQGFSLLGIGFDEWK'},
#     {'peptide': 'CMNPVTDIAGGAEALLPSPTAPPQGSHSEVAR'},
#     {'peptide': 'GGSGGGGGGGGGGDGSGGRMVPGSGGSSAQAGQGPGDSLAGAPSASAAGR'},
#     {'peptide': 'QTQLEDQAEEEEAEAQAQAEK'},
#     {'peptide': 'KAFLEYLAVQQEQLAREGVAELPPEQQEQLMR'},
#     {'peptide': 'QLKDIEERSSAVSSGITENEEADLIEIIVISLNK'},
#     {'peptide': 'LGSTSAPPSASKHGTPAGGGGSGGGR'},
#     {'peptide': 'LGLFFPAGLAHTEPDRSKEPQYAQCGTR'},
#     {'peptide': 'VHGAYERYPTFLVQAHYEAGRGAAAEFMGYSGR'},
#     {'peptide': 'DLNEIPAAVQIILALELFSAVQDPMHLRDAKVK'},
#     {'peptide': 'GSSCSGTYVSGSALDVTHTGTSGQDSSGDVWGSAAEKRSGGR'},
#     {'peptide': 'LDFGMPGYLDGAKVAVEMRAGGLQLR'},
#     {'peptide': 'SEVAQPVGVEGSPSALLPAGLGSLVAGK'},
#     {'peptide': 'AAAAATQAGSRDPAHSLGKAAAAASLAAALLDASLLTTLHVHVPSGR'},
# ]

# R = ursgal.UController(
#     profile = 'LTQ XL low res',
#     params = {
#         'database': 'tests/data/test_Creinhardtii_target_decoy.fasta',
#         'modifications':[
#             '*,opt,Prot-N-term,Acetyl'    # N-Acteylation[]
#         ]
#     },
#     force=True
# )

# mgf_file = R.convert_to_mgf_and_update_rt_lookup(
#     input_file = 'tests/data/test_Creinhardtii_QE_pH8.mzML',
#     force      = True
# )
# raw_results = R.search_mgf(
#     input_file = mgf_file,
#     engine     = 'omssa',
#     force      = True
# )
# converted_results = R.convert_results_to_csv(
#     input_file = raw_results,
#     force      = True,
# )
# output_file = R.unify_csv(
#     input_file = converted_results,
#     force      = True
# )

# peptides_set = set()
# for line_dict in csv.DictReader(open(output_file, 'r')):
#     peptides_set.add( line_dict['Sequence'] )


# def compare_peptide_test():
#     for test_id, test_dict in enumerate(TESTS):
#         yield compare_peptide, test_dict


# def compare_peptide( test_dict ):
#     assert test_dict['peptide'] in peptides_set

# def number_of_peptides_test():
#     test_peptides = set()
#     for peptide_dict in TESTS:
#         test_peptides.add( peptide_dict['peptide'] )
#     assert len(peptides_set) == len(test_peptides)


# if __name__ == '__main__':
#     print(__doc__)
