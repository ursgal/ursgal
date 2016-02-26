#!/usr/bin/env python3
import multiprocessing
# from collections import OrderedDict
META_INFO = {
    'engine_type'            : {
        'controller'        : True,
        'converter'         : False,
        'validation_engine' : False,
        'search_engine'     : False,
        'meta_engine'       : False,
    },
    'engine_url' : {
        'internal' : True,
    },
    'citation' : '<><>'
}

DEFAULT_PARAMS = {
    # general -
    'force'                             : False,
    'cpus'                              : multiprocessing.cpu_count() - 1,
    # do not use up all the power...
    'output_suffix'                     : '',
    'del_from_params_before_json_dump'  : ['grouped_psms'],
    'rt_pickle_name'                    : '_ursgal_lookup.pkl',
    'json_extension'                    : '.u.json',
    'helper_extension'                  : '.u_helper',
    'remove_temporary_files'            : True,
    # 'remove_config_files'               : False,
    'mzidentml_converter_version'       : 'mzidentml_lib_1_6_10',
    'mzml2mgf_converter_version'        : 'mzml2mgf_1_0_0',
    'unify_csv_converter_version'       : 'unify_csv_1_0_0',
    'filter_csv_converter_version'      : 'filter_csv_1_0_0',
    'show_unodes_in_development'        : False,
    'search_engines_create_folders'     : True,
    'compress_raw_search_results_if_possible' : True,
    # -----------------------------------------------------
    'log_enabled'                                           : False,
    # will redirect sys.stdout to the logfile, default name : ursgal.log
    'log_file_name'                                         : None,
    # this can be used to specify a different log file path

    # - xtandem
    'raw_ident_csv_suffix'             : '.csv', #this is the conversion result after csv conversion but before adding of rt
    'ident_csv_suffix'                 : 'idents.csv', #this is final with retention times
    'validated_ident_csv_suffix'       : 'validated.csv',
    'multi_engine_csv_suffix'          : 'summary.csv',
    'maximum_pep_for_ident_csv'        : 0.1,
    'output_file_type'                 : None,
    'input_file_type'                  : None,

    # java
    'java_-Xmx'                        : '13312m',

    # mgf conversion
    'number_of_mz_decimals'            : 5,
    'number_of_i_decimals'             : 5,
    'machine_offset_in_ppm'            : None,
    'scan_exclusion_list'              : None,
    'scan_skip_modulo_step'            : None,


    'compress_output'                  : False,
    'compress_after_post_flight'       : False,
    'compress_ext_exculsion'           : ['.csv'],

    # __ Protein __
    'modifications'                     : [
        # 'C,fix,any,Carbamidomethyl',        # Carbamidomethylation
        'M,opt,any,Oxidation',                # Met oxidation
        '*,opt,Prot-N-term,Acetyl',           # N-terminal N-Acteylation
        # '*,opt,Prot-N-term,Gln->pyro-Glu',  # N-terminal cyclation of Gln
        # '*,opt,Prot-N-term,Glu->pyro-Glu',  # N-terminal cyclation of Glu
        # 'N,opt,any,Deamidated',             # Deamidation of N
        # 'Q,opt,any,Deamidated',             # Deamidation of Q
    ],
    'cleavage_cterm_mass_change'        : '+17.00305',
    'cleavage_nterm_mass_change'        : '+1.00794',
    'semi_enzyme'                       : False,    # [ True, False ]
    'enzyme'                            : 'trypsin',
        #  'argc'                  # '[R]|{{P}}',
        #  'aspn'                  # '[X]|[D]',
        #  'chymotrypsin'          # '[FMWY]|{{P}}',
        #  'chymotrypsin_p'        # '[FMWY]|[X]',
        #  'clostripain'           # '[R]|[X]',
        #  'cnbr'                  # '[M]|{{P}}',
        #  'elastase'              # '[AGILV]|{{P}}',
        #  'formicacid'            # '[D]|{{P}}',
        #  'gluc'                  # '[DE]|{{P}}',
        #  'gluc_bicarb'           # '[E]|{{P}}',
        #  'iodosobenzoate'        # '[W]|[X]',
        #  'lysc'                  # '[K]|{{P}}',
        #  'lysc_p'                # '[K]|[X]',
        #  'lysn'                  # '[X]|[K]',
        #  'lysn_promisc'          # '[X]|[AKRS]',
        #  'nonspecific'           # '[X]|[X]',
        #  'pepsina'               # '[FL]|[X]',
        #  'protein_endopeptidase' # '[P]|[X]',
        #  'staph_protease'        # '[E]|[X]',
        #  'tca'                   # '[FMWY]|{{P}},[KR]|{{P}},[X]|[D]',
        #  'trypsin'               # '[KR]|{{P}}',
        #  'trypsin_p'             # '[RK]|[X]',
        #  'trypsin/cnbr'          # '[KR]|{{P}},[M]|{{P}}',
        #  'trypsin/gluc'          # '[DEKR]|{{P}}',
    'maximum_missed_cleavages'          : 2,
    'max_pep_length'                    : 40,
    'min_pep_length'                    : 6,
    'label'                             : '14N',
    'stp_bias'                          : False,
    'database'                          : None,  # used to be '/media/plan-f/Shared/databases/Chlamydomonas_reinhardtii/v5.5/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta',
    'decoy_tag'                         : 'decoy_',
    'compensate_small_fasta'            : False,
    # __ Scoring __
    'score_a_ions'                      : False,
    'score_b_ions'                      : True,
    'score_c_ions'                      : False,
    'score_x_ions'                      : False,
    'score_y_ions'                      : True,
    'score_z_ions'                      : False,
    'score_-h2o_ions'                   : False,
    'score_-nh3_ions'                   : False,
    'score_imm_ions'                    : False,
    'score_int_ions'                    : False,
    'score_z+1_ions'                    : False,
    'score_z+2_ions'                    : False,

    # __ Spectrum __
    'spec_dynamic_range'                : 10000,  # default is 100 .. ui ui ui
    'base_mz'                           : 1000,
    'precursor_mass_type'               : 'monoisotopic',
    'precursor_mass_tolerance_unit'     : 'ppm',
    'precursor_mass_tolerance_minus'    : 5,
    'precursor_mass_tolerance_plus'     : 5,
    'precursor_isotope_range'           : '0,1',
    'precursor_min_mass'                : 400,
    'precursor_min_charge'              : 1,
    'precursor_max_charge'              : 5,
    'precursor_ppm_offset'              : None,

    'frag_mass_type'                    : 'monoisotopic',
    'frag_mass_tolerance_unit'          : 'ppm',
    'frag_mass_tolerance'               : 20,
    'frag_min_mz'                       : '150',
    'frag_method'                       : 'hcd',
    'mininimal_required_observed_peaks' : '5',
    'mininimal_required_matched_peaks'  : '4',
    'num_match_spec'                    : 10,
    'neutral_loss_enabled'              : False,
    'neutral_loss_mass'                 : '0',
    'neutral_loss_window'               : '0',
    'maximal_accounted_observed_peaks'  : '50',
    'batch_size'                        : '100000',
    'noise_suppression_enabled'         : False,
    'use_refine'                        : False,

    # generate_taret_decoy
    'decoy_generation_mode'             : 'shuffle_peptide',
    'prefix'                            : None,

    # filter_csv
    'csv_filter_rules'                  : None,
    'write_unfiltered_results'          : False,

}


