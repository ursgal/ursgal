#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys


def main():
    '''
    Simple crosslink search using Kojak and an example file from Barth et al. 
    2014, please note that this is only testing if Kojak works.
    The sample represents no crosslink data in particular, but Kojak is used to
    map possible disulfide bonds.

    Parameters have not been optimized yet, please use this script as a template
    to use Kojak. Please note the different approach for executing Percolator.

    Note:

        Please note that Kojak has to installed manually at the resources folder
        under engine-folder (kojak_1_5_3). 
        Additinally Percolator (2.08) has to be symlinked or copied to
        engine-folder 'kojak_percolator_2_08'. 

    Usage:
        ./simple_srosslink_search.py <path_2_chlamydomonas_reinhardtii_database>

    Note:

        The peptide -.GHYLNATAGTC[-34.00]EEMMK.- from Rubisco large subunit is 
        detected with a predicted disulfide bond site at this position.
        This site is reported to have a disulfide bond in the Uniprot database.
        The modification (C +32, C -34) was set according to  'Tsai PL, Chen SF,
        Huang SY (2013) Mass spectrometry-based strategies for protein disulfide 
        bond identification. Rev Anal Chem 32: 257–268'
        Please use the reference C. reinhardtii (TaxId 3055 ) proteome from
        Unipot.

    '''

    params = {
        'database': sys.argv[1],
        'ftp_url': 'ftp.peptideatlas.org',
        'ftp_login': 'PASS00269',
        'ftp_password': 'FI4645a',
        'ftp_include_ext': [
            'JB_FASP_pH8_2-3_28122012.mzML',
        ],
        'ftp_output_folder': os.path.join(
            os.pardir,
            'example_data',
            'simple_crosslink_search'
        ),
        'cross_link_definition': ['C C -2 test_if_kojak_runs'],
        'mono_link_definition': ['C 32', 'C -34'],
        'modifications': [
            'M,opt,any,Oxidation',        # Met oxidation
        ],
        'precursor_min_mass': 500,
        'precursor_max_mass': 8000,
        'precursor_mass_tolerance_plus': 15,
        'precursor_mass_tolerance_minus': 15,
        'max_accounted_observed_peaks': 0,  # i.e. all
        'max_num_mods': 2
    }

    if os.path.exists(params['ftp_output_folder']) is False:
        os.mkdir(params['ftp_output_folder'])

    uc = ursgal.UController(
        profile='LTQ XL low res',
        params=params
    )
    mzML_file = os.path.join(
        params['ftp_output_folder'],
        params['ftp_include_ext'][0]
    )
    if os.path.exists(mzML_file) is False:
        uc.fetch_file(
            engine='get_ftp_files_1_0_0'
        )

    td_database_name = params['database'].replace(
        '.fasta', '_target_decoy.fasta')
    if os.path.exists(td_database_name) is False:
        uc.execute_misc_engine(
            input_files=[params['database']],
            engine='generate_target_decoy_1_0_0',
            output_file_name=td_database_name,
        )
    uc.params['database'] = td_database_name

    engine = 'kojak_1_5_3'

    mgf_file = uc.convert(
        input_file=mzML_file,
        engine='mzml2mgf',
    )
    raw_result = uc.search_mgf(
        input_file=mgf_file,
        engine=engine,
        force=False,
    )
    for extension in uc.unodes[engine]['META_INFO']['all_extensions']:
        if 'perc' not in extension:
            continue
        file_to_validate = raw_result.replace(
            uc.unodes[engine]['META_INFO']['output_extension'],
            extension
        )
        try:
            uc.validate(
                file_to_validate,
                'kojak_percolator_2_08'
            )
        except:
            pass

    return


if __name__ == '__main__':
    main()
