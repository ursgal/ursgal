#!/usr/bin/env python3
import os

from nose.tools import raises

import ursgal
from ursgal.exceptions import UrsgalError, EmptylCsvUrsgaError

database = os.path.join("tests", "data", "BSA.fasta")
test_file = os.path.join("tests", "data", "empty_search_results.csv")
R = ursgal.UController(params={"database": database})
print("set up stuff")


@raises(EmptylCsvUrsgaError)
def empty_file_raises_EmptyUrsgalCsvError_in_peptide_mapper_v4_test():
    R = ursgal.UController(
        params={
            "database": database,
            "peptide_mapper_class_version": "UPeptideMapper_v4",
        }
    )
    R.map_peptides_to_fasta(test_file, force=True)


@raises(UrsgalError)
def empty_file_raises_UrsgalError_in_peptide_mapper_v4_test():
    R = ursgal.UController(
        params={
            "database": database,
            "peptide_mapper_class_version": "UPeptideMapper_v4",
        }
    )
    R.map_peptides_to_fasta(test_file, force=True)


@raises(EmptylCsvUrsgaError)
def empty_file_raises_EmptyUrsgalCsvError_in_peptide_mapper_v3_test():
    R = ursgal.UController(
        params={
            "database": database,
            "peptide_mapper_class_version": "UPeptideMapper_v3",
        }
    )
    R.map_peptides_to_fasta(test_file, force=True)


@raises(UrsgalError)
def empty_file_raises_UrsgalError_in_peptide_mapper_v3_test():
    R = ursgal.UController(
        params={
            "database": database,
            "peptide_mapper_class_version": "UPeptideMapper_v3",
        }
    )
    R.map_peptides_to_fasta(test_file, force=True)


@raises(EmptylCsvUrsgaError)
def empty_file_raises_EmptyUrsgalCsvError_in_peptide_mapper_v2_test():
    R = ursgal.UController(
        params={
            "database": database,
            "peptide_mapper_class_version": "UPeptideMapper_v2",
        }
    )
    R.map_peptides_to_fasta(test_file, force=True)


@raises(UrsgalError)
def empty_file_raises_UrsgalError_in_peptide_mapper_v2_test():
    R = ursgal.UController(
        params={
            "database": database,
            "peptide_mapper_class_version": "UPeptideMapper_v2",
        }
    )
    R.map_peptides_to_fasta(test_file, force=True)
