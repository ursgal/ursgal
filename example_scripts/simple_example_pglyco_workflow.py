#!/usr/bin/env python3.4
# encoding: utf-8

import ursgal
import os
import sys
import shutil


def main(input_raw_file=None, database=None, enzyme=None):
    '''
    This script executes four steps:
        - generate a target decoy database with J-X-S/T replacing N-X-S/T
        - convert .raw file using pParse
        - search the resulting .mgf file using pGlyco
        - validate results using pGlycoFDR

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
            'decoy_generation_mode' : 'shuffle_peptide',
            'convert_aa_in_motif'   : 'J,N[^P][ST],0',
            'aa_exception_dict' : {},
        }
    )

    fasta_database_list = [
        database,
        os.path.join(
            os.path.dirname(database),
            'crap.fasta',
        )
    ]

    new_target_decoy_db_name = uc.generate_target_decoy(
        input_files       = fasta_database_list,
        output_file_name = '{0}_cRAP_target_decoy_{1}_N2J.fasta'.format(database.strip('.fasta'), enzyme),
    )
    print('Generated target decoy database: {0}'.format(new_target_decoy_db_name))
    uc.params['database'] = new_target_decoy_db_name

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
        engine = 'pglyco_2_2_0',
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
