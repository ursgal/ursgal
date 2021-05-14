#!/usr/bin/env python3.4
# encoding: utf-8
import ursgal
import sys
import glob
import os
import shutil


def main(folder=None, target_decoy_database=None):
    ''' 
    Complete example workflow for the identification of intact glycopeptides
    from MS runs employing IS-CID.

    usage:
        ./do_it_all_folder_wide.py <mzML_folder> <target_decoy_database>

    '''
    # define folder with mzML_files as sys.argv[1]
    mzML_files = []
    for mzml in glob.glob(os.path.join('{0}'.format(folder), '*.mzML')):
        mzML_files.append(mzml)

    mass_spectrometer = 'QExactive+'

    # Define search engines for protein database search
    search_engines = [
        'xtandem_vengeance',
        'msgfplus_v2019_07_03',
        'msfragger_2_3',
    ]

    # Define validation engine for protein database search
    validation_engine = 'percolator_3_4_0'

    # Modifications that should be included in the search.
    # Glycan modifications will be added later.
    all_mods = [
        'C,fix,any,Carbamidomethyl',
        'M,opt,any,Oxidation',
        '*,opt,Prot-N-term,Acetyl',
    ]

    # Initializing the Ursgal UController class with
    # our specified modifications and mass spectrometer
    params = {
        'cpus':8,
        'database'      : target_decoy_database,
        'modifications' : all_mods,
        'csv_filter_rules' : [
            ['Is decoy', 'equals', 'false'],
            ['PEP', 'lte', 0.01],
            ['Conflicting uparam', 'contains_not', 'enzyme'],
        ],
        'peptide_mapper_class_version': 'UPeptideMapper_v4',
        'use_pyqms_for_mz_calculation': True,
        '-xmx'     : '16g',
        'upper_mz_limit': 3000,
        'lower_mz_limit': 500,
        'precursor_mass_tolerance_plus': 5,
        'precursor_mass_tolerance_minus': 5,
        'frag_mass_tolerance': 20,
    }

    uc = ursgal.UController(
        profile=mass_spectrometer,
        params=params
    )

    # complete workflow
    result_files_unfilered = []
    glyco_result_files = []
    pot_glyco_result_files = []
    sugarpy_result_files = []
    sugarpy_curated_files = []
    for spec_file in mzML_files:
        mgf_file = uc.convert(
            input_file=spec_file,
            engine='mzml2mgf_2_0_0'
        )
        results_one_file = []
        for search_engine in search_engines:
            # search MS2 specs for peptides with HexNAc and HexNAc(2) modification
            for mod in [
                'N,opt,any,HexNAc',
                'N,opt,any,HexNAc(2)'
            ]:
                uc.params['modifications'].append(mod)
                uc.params['prefix'] = mod.split(',')[3]
                search_result = uc.search_mgf(
                    input_file=mgf_file,
                    engine=search_engine
                )
                uc.params['prefix'] = ''
                converted_result = uc.convert(
                    input_file=search_result,
                    guess_engine=True,
                )
                mapped_results = uc.execute_misc_engine(
                    input_file=converted_result,
                    engine='upeptide_mapper'
                )
                unified_search_results = uc.execute_misc_engine(
                    input_file=mapped_results,
                    engine='unify_csv',
                )
                validated_csv = uc.validate(
                    input_file=unified_search_results,
                    engine=validation_engine,
                )
                filtered_validated_results = uc.execute_misc_engine(
                    input_file=validated_csv,
                    engine='filter_csv',
                )
                results_one_file.append(filtered_validated_results)
                uc.params['modifications'].remove(mod)

        uc.params['prefix'] = '{0}'.format(
            os.path.basename(spec_file).strip('.mzML'))

        all_results_one_file = uc.execute_misc_engine(
            input_file=results_one_file,
            engine='merge_csvs',
        )
        result_files_unfilered.append(all_results_one_file)

        # filter for glycopeptides
        uc.params.update({
            'prefix': 'Glyco_',
            'csv_filter_rules': [
                ['Modifications', 'contains', 'HexNAc'],
                ['Modifications', 'mod_at_glycosite', 'HexNAc'],
            ]
        })
        glyco_file = uc.execute_misc_engine(
            input_file=all_results_one_file,
            engine='filter_csv',
        )
        glyco_result_files.append(glyco_file)

        # sugarpy_run to match glycopeptide fragments in MS1 scans.
        # Modifiy those parameters according your MS specifications
        uc.params.update({
            'prefix': '',
            'mzml_input_file': spec_file,
            'min_number_of_spectra': 2,
            'min_glycan_length': 3,
            'max_glycan_length': 20,
            'min_subtree_coverage': 0.65,
            'min_sugarpy_score': 1,
            'ms_level': 1,
            'rt_border_tolerance': 1,
            'precursor_max_charge': 5,
            'use_median_accuracy': 'peptide',
            'monosaccharide_compositions': {
                "dHex": 'C6H10O4',
                "Hex": 'C6H10O5',
                "HexNAc": 'C8H13NO5',
                "NeuAc": 'C11H17NO8',
                # "dHexNAc": 'C8H13NO4',
                # "HexA": 'C6H8O6',
                # "Me2Hex": 'C8H14O5',
                # "MeHex": 'C7H12O5',
                # "Pent": 'C5H8O4',
                # 'dHexN': 'C6H11O3N',
                # 'HexN': 'C6H11O4N',
                # 'MeHexA': 'C7H10O6',
            },
            'm_score_cutoff': 0.7,
            'mz_score_percentile': 0.7,
            'precursor_mass_tolerance_plus': 10,
            'precursor_mass_tolerance_minus': 10,
            'rel_intensity_range': 0.2,
            'rt_pickle_name': os.path.join(
                os.path.dirname(spec_file),
                '_ursgal_lookup.pkl'
            )
        })
        sugarpy_results = uc.execute_misc_engine(
            input_file=glyco_file,
            engine='sugarpy_run_1_0_0',
        )
        sugarpy_result_files.append(sugarpy_results)

        # sugarpy_plot to plot the results from the sugarpy_run
        # This will plot an elution profile for all identified glycopeptides
        uc.params.update({
            'sugarpy_results_pkl': sugarpy_results.replace('.csv', '.pkl'),
            'sugarpy_results_csv': sugarpy_results,
            'sugarpy_plot_types': [
                'plot_glycan_elution_profile',
            ],
            'plotly_layout': {
                'font' : {
                    'family':'Arial',
                    # 'size': 20,
                    'color' : 'rgb(0, 0, 0)',
                },
                'autosize':True,
                # 'width':1700,
                # 'height':700,
                # 'margin':{
                #     'l':100,
                #     'r':80,
                #     't':100,
                #     'b':60,
                # },
                'xaxis':{
                    'type':'linear',
                    'color':'rgb(0, 0, 0)',
                    'title_font':{
                        'family':'Arial',
                        'size':20,
                        'color':'rgb(0, 0, 0)',
                    },
                    'autorange':True,
                    # 'range':[0,1000.0],
                    'tickmode':'auto',
                    'showexponent':'all',
                    'exponentformat':'B',
                    'ticklen':5,
                    'tickwidth':1,
                    'tickcolor':'rgb(0, 0, 0)',
                    'ticks':'outside',
                    'showline':True,
                    'linecolor':'rgb(0, 0, 0)',
                    'mirror':False,
                    'showgrid':False,
                },
                'yaxis':{
                    'type':'linear',
                    'color':'rgb(0, 0, 0)',
                    'title':'Intensity',
                    'title_font':{
                        'family':'Arial',
                        'size':20,
                        'color':'rgb(0, 0, 0)',
                    },
                    'autorange':True,
                    # 'range':[0.0,100.0],
                    'showexponent':'all',
                    'exponentformat':'B',
                    'ticklen':5,
                    'tickwidth':1,
                    'tickcolor':'rgb(0, 0, 0)',
                    'ticks':'outside',
                    'showline':True,
                    'linecolor':'rgb(0, 0, 0)',
                    'mirror':False,
                    'showgrid':False,
                },
                'legend':{
                    'orientation':'h',
                    'traceorder':'normal',
                },
                'showlegend':True,
                'paper_bgcolor':'rgba(0,0,0,0)',
                'plot_bgcolor':'rgba(0,0,0,0)',
            },
        })
        sugarpy_plots = uc.execute_misc_engine(
            input_file=spec_file,
            engine='sugarpy_plot_1_0_0',
            # force = True,
        )

        # setting uparams back to original
        uc.params.update({
            'prefix': '',
            'ms_level': 2,
            'precursor_max_charge': 5,
            'csv_filter_rules': [
                ['Is decoy', 'equals', 'false'],
                ['PEP', 'lte', 0.01],
            ],
            'precursor_mass_tolerance_plus' : 5,
            'precursor_mass_tolerance_minus': 5,
            'rt_pickle_name': '_ursgal_lookup.pkl',
            'frag_mass_tolerance': 20,
            # 'rt_pickle_name': os.path.join(
            #     os.path.dirname(spec_file),
            #     '_ursgal_lookup.pkl'
            # )
        })

    # combine results from multiple mzML files
    results_all_files_unfiltered = uc.execute_misc_engine(
        input_file=result_files_unfilered,
        engine='merge_csvs',
    )
    glyco_results_all_files = uc.execute_misc_engine(
        input_file=glyco_result_files,
        engine='merge_csvs',
    )
    sugarpy_results_all_files = uc.execute_misc_engine(
        input_file=sugarpy_result_files,
        engine='merge_csvs',
    )

    # Extract the best matches from the raw SugarPy results.
    # This is used for the automatic filtering described in the manuscript.
    uc.params.update({
        'prefix': '',
        'ms_level': 1,
        'min_number_of_spectra': 2,
        'max_trees_per_spec': 1,
        'sugarpy_results_pkl': None,
        'sugarpy_results_csv': sugarpy_results_all_files,
        'sugarpy_plot_types': [
            'extract_best_matches',
        ],
        'rt_pickle_name': 'create_new_lookup',
    })
    sugarpy_extracted = uc.execute_misc_engine(
        # the specific spec file is not important here, 
        # this is just used to localize the scan2rt lookup
        input_file=spec_file,
        engine='sugarpy_plot_1_0_0',
        force = False,
    )

    # Filter extracted results for glycopeptides that were identified
    # in at least two replicates (i.e. two MS files)
    uc.params['csv_filter_rules'] = [
        ['Num Raw Files', 'gte', 2],
    ]

    extracted_filtered = uc.execute_misc_engine(
        input_file=sugarpy_results_all_files.replace('.csv', '_extracted.csv'),
        engine='filter_csv',
    )
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(main.__doc__)
        exit()
    main(
        folder=sys.argv[1],
        target_decoy_database=sys.argv[2],
    )
