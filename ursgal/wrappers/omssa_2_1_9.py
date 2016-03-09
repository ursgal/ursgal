#!/usr/bin/env python3.4
import ursgal
import pprint
import xml.etree.ElementTree
import os
import platform
import sys
import subprocess
import csv

class omssa_2_1_9( ursgal.UNode ):
    """
    omssa_2_1_9 UNode

    Parameter options at http://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/asn_spec/omssa.asn.html

    2.1.9 parameters at http://proteomicsresource.washington.edu/protocols06/omssa.php

    Reference:
    Geer LY, Markey SP, Kowalak JA, Wagner L, Xu M, Maynard DM, Yang X, Shi W, Bryant SH (2004) Open Mass Spectrometry Search Algorithm.

    """
    META_INFO = {
        'engine_type'            : {
            'controller'        : False,
            'converter'         : False,
            'validation_engine' : False,
            'search_engine'     : True,
            'meta_engine'       : False
        },
        'citation'              : 'Geer LY, Markey SP, Kowalak JA, '\
            'Wagner L, Xu M, Maynard DM, Yang X, Shi W, Bryant SH (2004) '\
            'Open Mass Spectrometry Search Algorithm.',
        'input_types'           : ['.mgf'],
        'output_extension'      : '.csv',
        'create_own_folder'     : True,
        'in_development'        : False,

        'include_in_git'        : False,
        'utranslation_style'    : 'omssa_style_1',
        ### Below are the download information ###
        'engine': {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'omssacl',
                    'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.macos.tar.gz',
                    'zip_md5'        : '9cb92a98c4d96c34cc925b9336cbaec7',
                    'additional_exe' : ['makeblastdb'],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'omssacl',
                    'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.linux.tar.gz',
                    'zip_md5'        : '921e01df9cd2a99d21e9a336b5b862c1',
                    'additional_exe' : ['makeblastdb'],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'omssacl.exe',
                    'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.win32.exe',
                    'zip_md5'        : 'b9d9a8aec3cfe77c48ce0f5752aba8f9',
                    'additional_exe' : ['makeblastdb'],
                },
                '32bit' : {
                    'exe'            : 'omssacl.exe',
                    'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.win32.exe',
                    'zip_md5'        : 'a05a5cdd45fd8abcfc75b1236f8a2390',
                    'additional_exe' : ['makeblastdb'],
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        super(omssa_2_1_9, self).__init__(*args, **kwargs)
        self.omssa_mod_Mapper = None

    def _load_omssa_xml(self):
        ''' Parsing through omssa mods to map omssa mods on unimods '''
        self.omssa_mod_Mapper = {}
        def _create_empty_tmp():
            tmp = {
                'aa_targets' : [],
            }
            return tmp
        tmp = _create_empty_tmp()
        xml_path = os.path.dirname( self.exe )

        xml_names = ['mods.xml', 'usermods.xml']
        for xml_name in xml_names:
            omssa_xml = os.path.join(
                xml_path,
                xml_name
            )
            self.print_info(
                'Parsing omssa xml ({0})'.format(
                     omssa_xml
                ),
                caller='__ini__'
            )
            for event, element in xml.etree.ElementTree.iterparse( omssa_xml ):
                if element.tag.endswith('MSModSpec_residues_E'):
                    tmp['aa_targets'].append( element.text )

                elif element.tag.endswith('MSMod'):
                    tmp['omssa_id'] = element.text
                    # tmp['MSMod'] = element.text # OMSSA ID!
                elif element.tag.endswith('MSModSpec_psi-ms'):
                    tmp['unimod_name'] = element.text
                elif element.tag.endswith('MSModSpec_unimod'):
                    tmp['unimod_id'] = element.text
                    # tmp['MSModSpec_psi-ms'] = element.text # UNIMOD Name
                elif element.tag.endswith('MSModSpec_name'):
                    tmp['omssa_name'] = element.text
                    additional = []
                    if 'protein' in tmp['omssa_name']:
                        additional.append( 'Prot' )
                    if 'n-term' in tmp['omssa_name']:
                        additional.append('N-term')
                    elif 'c-term' in  tmp['omssa_name']:
                        additional.append('C-term')
                    if len(additional) > 0:
                        tmp['aa_targets'].append( '-'.join( additional ))

                elif element.tag.endswith('MSModSpec'):
                    lookup_field = 'unimod_id'
                    try:
                        l_value = tmp[ lookup_field ]
                    except:
                        self.print_info(
                            'Skipping entry {0} (no unimod! map)'.format( tmp ),
                            caller='WARNING!'
                        )
                        tmp['aa_targets'] = []
                        continue

                    if l_value not in \
                            self.omssa_mod_Mapper.keys():
                        self.omssa_mod_Mapper[ l_value ] = {}
                    self.omssa_mod_Mapper[ l_value ][ tmp[ 'omssa_id' ] ] = {
                        'aa_targets' : tmp[ 'aa_targets' ],
                        'omssa_name' : tmp[ 'omssa_name' ]
                    }

                    tmp = _create_empty_tmp()
        return

    def preflight( self ):
        '''
        Formatting the command line via self.params

        unimod Modifications are translated to OMSSA modifications

        Returns:
                self.params(dict)
        '''
        if self.omssa_mod_Mapper is None:
            self._load_omssa_xml()

        # building command_list !
        translations = self.params['_TRANSLATIONS_GROUPED_BY_TRANSLATED_KEY']
        blastdb_suffixes = [ '.phr', '.pin', '.psq' ]
        blastdb_present = True
        for blastdb_suffix in blastdb_suffixes:
            blast_file = self.params['database'] + blastdb_suffix
            if os.path.exists( blast_file ) is False:
                blastdb_present = False
                break

        if blastdb_present is False:
            self.print_info('Executing makeblastdb...')
            proc = subprocess.Popen(
                [
                    os.path.join(
                        os.path.dirname( self.exe ),
                        'makeblastdb'
                    ),
                    '-in', self.params['database'],
                    '-dbtype', 'prot',
                    '-input_type', 'fasta',
                ],
                stdout=subprocess.PIPE,
            )
            for line in proc.stdout:
                print(line.strip().decode('utf'))
        #
        if self.params['label'] == '15N':
            self.params['omssa_label'] = '2'
        else:
            self.params['omssa_label'] = '0'

        # Modifications
        # ------------------------

        for param_key in ['fixed_mods', 'opt_mods']:
            mod_type = param_key[:3]
            modifications = ''
            self.params[ param_key ] = ''
            for mod in self.params[ 'mods' ][ mod_type ]:
                unimod_id_does_not_exist = False
                aa_can_not_be_mapped = True
                if mod[ 'id' ] not in self.omssa_mod_Mapper.keys():
                    unimod_id_does_not_exist = True
                else:
                    if mod['aa'] == '*':
                        search_target = [ mod[ 'pos' ], ]
                    else:
                        search_target = [ mod['aa'], ]
                    for omssa_id in self.omssa_mod_Mapper[ mod[ 'id' ] ].keys():
                        if search_target == self.omssa_mod_Mapper[ mod[ 'id' ] ][ omssa_id ]['aa_targets']:
                            modifications += '{0},'.format( omssa_id )
                            aa_can_not_be_mapped = False
                            omssa_name = self.omssa_mod_Mapper[ mod[ 'id' ] ][ omssa_id ]['omssa_name']
                            self.lookups[ omssa_name ] = {
                                'name'       : mod[ 'name' ],
                                'aa_targets' : self.omssa_mod_Mapper[ mod[ 'id' ] ][ omssa_id ]['aa_targets'],
                                'omssa_id'   : omssa_id,
                                'id'         : mod['id']
                            }
                if unimod_id_does_not_exist or aa_can_not_be_mapped:
                    self.print_info( '''
    The combination of modification name and aminoacid is not supported by
    OMSSA. Continuing without modification: {0}
                    '''.format(mod),
                    caller='WARNING'
                    )
                    continue

            self.params[ param_key ] = modifications.strip(',')


        # semi-enyzmatic cleavage --> translation into omssa enzyme number
        if self.params['semi_enzyme'] is True:
            if translations['-e']['enzyme'] == '0':
                translations['-e']['enzyme'] = '16'
            elif translations['-e']['enzyme'] == '3':
                translations['-e']['enzyme'] = '23'
            elif translations['-e']['enzyme'] == '13':
                translations['-e']['enzyme'] = '24'

        # define the ions to search
        self.params['omssa_ions_to_search'] = []
        for ion in ['a', 'b', 'c', 'x', 'y', 'z']:
            ion_2_add = translations['-i'].get('score_{0}_ions'.format(ion), '')
            if ion_2_add != '':
                self.params['omssa_ions_to_search'].append( ion_2_add )
        self.params['omssa_ions_to_search'] = ','.join(
            self.params['omssa_ions_to_search']
        )

        if self.params['frag_mass_tolerance_unit'] == 'ppm':
            self.params['frag_mass_tolerance'] = \
                ursgal.ucore.convert_ppm_to_dalton(
                    self.params['frag_mass_tolerance'],
                    base_mz=self.params['base_mz']
                )

        # 5ppm precursor error

        self.params['omssa_precursor_error'] = (
            float(self.params['precursor_mass_tolerance_plus']) + \
            float(self.params['precursor_mass_tolerance_minus']) \
        ) / 2.0

        self.params['tmp_output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '_tmp'
        )
        self.created_tmp_files.append( self.params['tmp_output_file_incl_path'] )

        self.params['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        import pprint
        pprint.pprint( self.params )
        pprint.pprint(  self.params['_TRANSLATIONS_GROUPED_BY_TRANSLATED_KEY'] )
        pprint.pprint( translations )
        print( self.params['omssa_ions_to_search'] )
        exit(1)
        exit('break it <<<<')
        # print( translations = self.params['_TRANSLATIONS_GROUPED_BY_TRANSLATED_KEY'] )
        # exit(1)
        self.params['command_list'] = [
            # ---------------------------------------------------------------------
            # general
            self.exe,  # path 2 omssa executable
            # ---------------------------------------------------------------------
            # changeable params:
            # --- INPUT: ---
            '-d', '{database}'.format(**self.params),
            # path 2 database, has to be processed by formatdb from
            # BLAST package

            # -- OUTPUT: ---
            '{omssa_output_type}'.format(**self.params), '{tmp_output_file_incl_path}'.format(**self.params), # -oc for csv, -ox for omx
            '-w',
            # include search spetra and self.params in results,
            # is required for mzid conversion, if omx is used, but omx files
            # are huge ...
            '{num_match_spec_key}'.format(**self.params),
            '{num_match_spec}'.format(**self.params),

            '{num_hits_retain_spec_key}'.format(**self.params), '{num_hits_retain_spec}'.format(**self.params),
            # was 30 before, smaller output files?
            # maximum number of hits retained per precursor charge state per
            # spectrum during the search

            # --- MODS: ---
            '-mv', '{opt_mods}'.format(**self.params),
            # mods, oxidation of M
            '-mf', '{fixed_mods}'.format(**self.params),
            # carbamidomethylation, index 3

            # precursor:
            '-tem', '{omssa_label}'.format(**self.params),
            # variable, precursor ion search type
            # (0 = mono, 1 = avg, 2 = N15, 3 = exact, 4 = multiisotope)
            '-te', '{omssa_precursor_error}'.format(**self.params),
            # precursor ion m/z tolerance in Da (or ppm if -teppm flag set)

            # '-teppm',
            # search precursor masses in units of ppm - this set above!
            '{precursor_min_charge_key}'.format(**self.params), '{precursor_min_charge}'.format(**self.params),
            # minimum precursor charge to search when not 1+
            '{precursor_max_charge_key}'.format(**self.params), '{precursor_max_charge}'.format(**self.params),
            # maximum precursor charge max 5

            # PRODUCT
            '-tom', '{omssa_label}'.format(**self.params),
            # product ion search type, 14N or 15N
            '{frag_mass_tolerance_key}'.format(**self.params), '{frag_mass_tolerance}'.format(**self.params),
            # 20 ppm, QExactive, product ion tolerance

            # --- IONS ---
            '-i', '{omssa_ions_to_search}'.format(**self.params),
            # ids of ions to search (comma delimited, no spaces) b and y ions

            # --- ENZYME ---
            '{enzyme_key}'.format(**self.params), '{enzyme}'.format(**self.params),
            # enzyme is trypsin-p
            '{maximum_missed_cleavages_key}'.format(**self.params), '{maximum_missed_cleavages}'.format(**self.params),
            #  missed cleavages
            '{min_pep_length_key}'.format(**self.params), '{min_pep_length}'.format(**self.params),
            # minimum size of peptides for no-enzyme and semi-tryptic searches
            '{max_pep_length_key}'.format(**self.params), '{max_pep_length}'.format(**self.params),
            # sGUI has 30,maximum size of peptides for no-enzyme and
            # semi-tryptic searches (0=none)

            # --- COMPUTATIONAL AND SPEED ---
            '{cpu_key}'.format(**self.params), '{cpus}'.format(**self.params),
            # number of horses

            # --- SPECTRUM ---
            '{mininimal_required_observed_peaks_key}'.format(**self.params), '{mininimal_required_observed_peaks}'.format(**self.params),
            # the minimum number of m/z values a spectrum must have to be
            # searched

            # --- SCORING ---
            '{mininimal_required_matched_peaks_key}'.format(**self.params), '{mininimal_required_matched_peaks}'.format(**self.params),
            # the minimum number of m/z matches a sequence library peptide must
            # have for the hit to the peptide to be recorded

            # ---------------------------------------------------------------------
            # the following parameters are not changeable, e.g. default
            # protein/taxon
            '-x', '{x}'.format(**self.params),  # default, all taxids, we dont want to change this

            # ions
            '{search_c_terminal_ions_key}'.format(**self.params), '{search_c_terminal_ions}'.format(**self.params),   # search c terminal ions?, same as sGUI default, 0=yes, 1=no
            '{search_for_b1_ions_key}'.format(**self.params), '{search_for_b1_ions}'.format(**self.params),   # should first forward (b1) product ions be in search (1=no)
            '{max_num_of_ions_per_series_to_search_key}', '{max_num_of_ions_per_series_to_search}'.format(**self.params),  # max number of ions in each series being searched (0=all)

            # precursor
            '-z1', '{z1}'.format(**self.params),  # default, fraction of peaks below precursor used to determine if spectrum is charge 1
            '-zcc', '{zcc}'.format(**self.params),  # how should precursor charges be determined?, use a range
            '-tez', '{tez}'.format(**self.params),  # defautl is 0 (disabled), charge dependency of precursor mass tolerance (0 = none, 1 = linear)
            '-pc', '{pc}'.format(**self.params),  # minimum number of precursors that match a spectrum
            '-ti', '{precursor_isotope_range}'.format(**self.params),  # anticipate carbon isotope parent ion assignment errors

            # product
            '-zoh', '{zoh}'.format(**self.params),  # maximum product charge to search, default is 2, sGUI:2
            '-zt', '{zt}'.format(**self.params),  # default,minimum precursor charge to start considering multiply charged products

            # charge
            '-zc', '{zc}'.format(**self.params),  # should charge plus one be determined algorithmically? (1=yes)

            # scoring
            '-scorr', '{scorr}'.format(**self.params),  # turn off correlation correction to score (1=off, 0=use correlation)
            '-scorp', '{scorp}'.format(**self.params),  # sam as sGUI, probability of consecutive ion (used in correlation correction)
            '-he', '{he}'.format(**self.params),  # the maximum evalue allowed in the hit list, cant find in search GUI

            # spectrum
            '-ht', '{ht}'.format(**self.params),  # number of m/z values corresponding to the most intense peaks that must include one match to the theoretical peptide
            '-cl', '{cl}'.format(**self.params),  # low intensity cutoff as a fraction of max peak,
            '-cp', '{cp}'.format(**self.params),  # eliminate charge reduced precursors in spectra (0=no, 1=yes)


            # window
            '-h2', '{h2}'.format(**self.params),  # number of peaks allowed in double charge window
            '-h1', '{h1}'.format(**self.params),  # number of peaks allowed in single charge window (0 = number of ion species)
            '-w1', '{w1}'.format(**self.params),  # default is 27, also in sGUI, single charge window in Da
            '-w2', '{w2}'.format(**self.params),  # double charge window in Da, default

            # mass
            '-ta', '{ta}'.format(**self.params),  # default value, cant find in sGUI self.params, automatic mass tolerance adjustment fraction
            '-tex', '{tex}'.format(**self.params),  # threshold in Da above which the mass of neutron should be added in exact   mass search
            '-mm', '{mm}'.format(**self.params),  # the maximum number of mass ladders to generate per database peptide

            # '-ni', #verbose info print
        ]

        # input
        self.params['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        assert os.path.exists( self.params['mgf_input_file']  ), '''
        OMSSA requires .mgf input (which should have been generated
        automatically ...)
        '''
        self.params['command_list'].append( '-fm')
        self.params['command_list'].append( self.params['mgf_input_file'] )

        if self.params['precursor_mass_tolerance_unit'] == 'ppm':
            self.params['command_list'].append('-teppm')
        else:
            pass #without this flag dalton is used

    def postflight( self ):
        '''
        Will correct the OMSSA headers and add the column retention time to the
        csv file
        '''
        # exit()
        cached_omssa_output = []
        result_file = open( self.params['tmp_output_file_incl_path'], 'r')
        csv_dict_reader_object = csv.DictReader(
            row for row in result_file if not row.startswith('#')
        )
        headers = csv_dict_reader_object.fieldnames
        translated_headers = []
        for header in headers:
            translated_headers.append(
                self.USEARCH_PARAM_VALUE_TRANSLATIONS.get(header, header)
            )
        translated_headers += [
            'Is decoy',
            'Retention Time (s)',
            # 'Raw data location'
        ]
        print('[ PARSING  ] Loading unformatted OMSSA results ...')
        for line_dict in csv_dict_reader_object:
            cached_omssa_output.append( line_dict )
        result_file.close()

        #
        result_file = open( self.params['output_file_incl_path'], 'w')
        csv_dict_writer_object = csv.DictWriter(
            result_file,
            fieldnames = translated_headers
        )
        csv_dict_writer_object.writeheader()
        #
        # self.parse_fasta()
        already_seen_protein_scan_start_stop_combos = set()
        database = self.params['database']
        for m in cached_omssa_output:
            tmp = {}
            for header in headers:
                translated_header = self.USEARCH_PARAM_VALUE_TRANSLATIONS.get(
                    header,
                    header
                )
                tmp[ translated_header ] = m[ header ]
            tmp['Sequence'] = tmp['Sequence'].upper()

            returned_peptide_regex_list = self.peptide_regex(
                self.params['database'],
                tmp['proteinacc_start_stop_pre_post_;'],
                tmp['Sequence']
            )

            translated_mods = []
            if tmp['Modifications'] != '':
                splitted_Modifications = tmp['Modifications'].split(',')
                for mod in splitted_Modifications:
                    omssa_name, position = mod.split(':')
                    omssa_name  = omssa_name.strip()
                    position    = position.strip()
                    unimod_name = self.lookups[ omssa_name ]['name']
                    if position.strip() == '1':
                        # print( self.lookups[ omssa_name ] )
                        for target in self.lookups[ omssa_name ]['aa_targets']:
                            if 'N-TERM' in target.upper():
                                position = '0'
                    translated_mods.append(
                        '{0}:{1}'.format(
                            unimod_name,
                            position
                        )
                    )

            tmp['Modifications'] = ';'.join( translated_mods )

            for protein in returned_peptide_regex_list:
                for pep_regex in protein:
                    start, stop, pre_aa, post_aa, returned_protein_id = pep_regex
                    protein_scan_start_stop = (
                        returned_protein_id,
                        tmp['Spectrum Title'],
                        start,
                        stop
                    )
                    if protein_scan_start_stop in already_seen_protein_scan_start_stop_combos:
                        continue
                    else:
                        already_seen_protein_scan_start_stop_combos.add(protein_scan_start_stop)


                    tmp['Start'] = start
                    tmp['Stop'] = stop

                    tmp['proteinacc_start_stop_pre_post_;'] = '{0}_{1}_{2}_{3}_{4}'.format(
                        tmp['proteinacc_start_stop_pre_post_;'],
                        start,
                        stop,
                        pre_aa,
                        post_aa
                    )



                    if self.params['decoy_tag'] in tmp['proteinacc_start_stop_pre_post_;']:
                        tmp['Is decoy'] = 'true'
                    else:
                        tmp['Is decoy'] = 'false'
                    csv_dict_writer_object.writerow( tmp )
        return


