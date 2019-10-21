#!/usr/bin/env python
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main(input_raw_file=None, database=None, enzyme=None):
    '''
    This script executes three steps:
        - convert .raw file using pParse
        - search the resulting .mgf file using pGlyco
        - validate results using pGlycoFDR

    Since pGlyco does not support providing a custom target-decoy database,
    a database including only target sequences must be provided.
    In this database, the N-glycosylation motif N-X-S/T needs to be replaced
    with J-X-S/T, which will be done by the pGlyco wrapper.

    usage:
        ./simple_example_pglyco_workflow.py <input_raw_file> <database> <enzyme>

    '''
    uc = ursgal.UController(
        profile='QExactive+',
        params={
            'database': database,
            'modifications': [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
            ],
            'peptide_mapper_class_version': 'UPeptideMapper_v4',
            'enzyme': enzyme,
            'frag_mass_tolerance'       : 20,
            'frag_mass_tolerance_unit'  : 'ppm',
            'precursor_mass_tolerance_plus' : 5,
            'precursor_mass_tolerance_minus' : 5,
            'aa_exception_dict' : {},
        }
    )

    xtracted_file = uc.convert(
        input_file = input_raw_file,
        engine = 'pparse_2_0',
        # force = True,
    )

    mgf_file = uc.convert(
        input_file = input_raw_file.replace('.raw', '.idx.gz'),
        engine = 'mzml2mgf_2_0_0',
        # force = True,
    )

    search_result = uc.search_mgf(
        input_file = xtracted_file,
        engine = 'pglyco_db_2_2_0',
    )

    # converted_result = uc.convert(
    #     input_file=search_result,
    #     guess_engine = True,
    # )
        
    mapped_results = uc.execute_misc_engine(
        input_file=search_result,
        engine='upeptide_mapper',
    )

    unified_search_results = uc.execute_misc_engine(
        input_file = mapped_results,
        engine='unify_csv'
    )

    validated_file = uc.validate(
        input_file=search_result,
        engine='pglyco_fdr_2_2_0',
    )

    mapped_validated_results = uc.execute_misc_engine(
        input_file=validated_file,
        engine='upeptide_mapper',
    )

    unified_validated_results = uc.execute_misc_engine(
        input_file = mapped_validated_results,
        engine='unify_csv'
    )

    return


if __name__ == '__main__':
    main(input_raw_file=sys.argv[1], database=sys.argv[2],enzyme=sys.argv[3])
