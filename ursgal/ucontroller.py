#!/usr/bin/env python
import sys
import os
import glob
import platform
import ursgal
import importlib
import pickle
import pprint
import json
import inspect
import tempfile
import zipfile
import stat
import shutil
from collections import Counter
import pkg_resources


class UController(ursgal.UNode):
    '''
    ursgal main class

    Keyword Arguments:
        params (dict): params that are used for all further analyses,
            overriding default values from ursgal/uparams.py
        profile (str): Profiles key for faster parameter selection. This
            idea is adapted from MS-GF+ and translated to all search engines.

            Currently available profiles are:

                * 'QExactive+'
                * 'LTQ XL high res'
                * 'LTQ XL low res'

    Example::

        >>> us = ursgal.UController(
        ...    profile = 'LTQ XL low res',
        ...    params = { 'database': 'BSA.fasta' }
        ...)

    '''

    META_INFO = {
        'engine_type'            : {
            'controller'        : True,
        },
        'engine_url' : {
            'internal' : True,
        },
        'utranslation_style'        : 'ucontroller_style_1',
        'citation' : 'Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. & Fufezan, C. Ursgal, universal Python module combining common bottom-up proteomics tools for large-scale analysis. J. Proteome res. acs.jproteome.5b00860 (2015). doi:10.1021/acs.jproteome.5b00860'
    }

    def __init__( self, *args, **kwargs):
        # kwargs['engine_path'] = ursgal.__file__
        super(UController, self).__init__(*args, **kwargs)
        self.exe                  = ''
        self.profiles             = ursgal.PROFILES
        self.platform             = sys.platform
        self.architecture         = platform.architecture()
        self.unodes               = {}
        self.scan_rt_lookup       = {}  # will be set on self.set_target()
        self.scan_rt_lookup_path  = {}  # will be set on self.set_target()
        self.force                = kwargs.get('force', False)
        self.user_defined_params  = {}
        self.params               = ParamsDict()
        self.init_kwargs          = {}
        self._run_after_meta_init = True
        self.verbose              = True

        # self.update_user_params   = False

        # Second init is initialized after the Meta_class has returned the
        # object ... otherwise we can not access the info injected by the
        # meta class (Meta_UNode)

    def _after_init_meta_callback(self, *args, **kwargs):
        self.time_point( tag = 'init' )
        self.verbose = kwargs.get('verbose', True)
        if self.verbose:
            self.print_header(
                'UController initialized',
                tag='init',
                newline=False
            )
            ursgal_string = 'Ursgal v{0}  -  '\
                'https://github.com/ursgal/ursgal'.format(ursgal.__version__)
            print('         -\-{0: ^58}-/-\n'.format(ursgal_string))
        self.params = ParamsDict()
        self.init_kwargs = kwargs
        self.reset_controller()

        self.unodes = self._collect_all_unode_wrappers()
        # self.unodes = self.collect_all_unodes_from_kb()
        self.determine_availability_of_unodes()
        # if pymzml generation 2 is used we reset the default converter version
        if self.verbose:
            self.show_unode_overview()

    def _collect_all_unode_wrappers( self ):
        '''
        The ucontroller function to collect all unode wrappers

        Iterates over all files in the engine folder and checks

        Returns:
            dict: Dictionary of unodes
        '''
        unodes = {
            '__by_meta_type' : {},  # groups e.g. all search engines
            '__engine_type' : {}    # groups e.g. all XTandem
        }
        wrappers_path_glob = os.path.join(
            ursgal.base_dir, 'wrappers', '*.py'
        )
        for wrapper_file in glob.glob( wrappers_path_glob ):
            filename = os.path.basename( wrapper_file )
            if filename.startswith('__'):
                continue
            if wrapper_file.startswith('.'):
                continue
            wrapper_module_name = filename.replace('.py', '')

            wrapper_module = importlib.__import__(
                "ursgal.wrappers.{0}".format( wrapper_module_name ),
                fromlist = [ wrapper_module_name ]
            )
            assert hasattr(wrapper_module, wrapper_module_name ), '''
            wrappers/{0}.py contains no class named {0}
            '''.format( wrapper_module_name )


            wrapper_class = getattr(wrapper_module, wrapper_module_name)
        #     try:
        #         initialized_wrapper_class = wrapper_class(
        #             engine_path = engine_exe_path
        #         )
        #     except TypeError:
        #         print('''

        # Do you have *args and **kwargs in your Class ?

        # E.g.:

        # class msblender_09_2015( ursgal.UNode ):
        #     def __init__( self,  *args, **kwargs ):

        #         ''')

            '''NOTE: This has to be assert in the final version '''

            # assert hasattr(wrapper_class, 'META_INFO' ), '''
            # wrappers/{0}.py contains class attribute META_INFO
            # '''.format( wrapper_module_name )

            if hasattr(wrapper_class, 'META_INFO' ):
                wrapper_meta_info = getattr(wrapper_class, 'META_INFO')
            else:
                wrapper_meta_info = {}
            engine            = wrapper_meta_info.get(
                'engine',
                None
            )
            include_in_git    = wrapper_meta_info.get(
                'include_in_git',
                None
            )
            in_development    = wrapper_meta_info.get(
                'in_development',
                True
            )
            zip_md5           = wrapper_meta_info.get(
                'zip_md5',
                None
            )
            distributable = wrapper_meta_info.get(
                'distributable',
                True
            )

            unodes[ wrapper_module_name ] = {
                'available'         : False,
                'type'              : None,
                'class'             : None,
                'engine'            : engine,
                'include_in_git'    : include_in_git,
                'distributable'     : distributable,
                'META_INFO'         : wrapper_meta_info,
                'in_development'    : in_development,
                'import_status'     : 'n/d',
                '_wrapper_class'    : wrapper_class,
            }
            uses_unode = wrapper_meta_info.get(
                'uses_unode',
                None
            )
            if uses_unode is not None:
                unodes[ wrapper_module_name ]['uses_unode'] = uses_unode

            engine_type = wrapper_meta_info.get('engine_type', {})
            for meta_type, meta_type_bool in engine_type.items():
                if meta_type_bool is True:
                    if meta_type not in unodes['__by_meta_type'].keys():
                        unodes['__by_meta_type'][ meta_type ] = []
                    unodes['__by_meta_type'][ meta_type ].append(
                        wrapper_module_name
                    )
        return unodes

    def reset_controller( self ):

        temp_params = {}
        temp_params.update( self.DEFAULT_PARAMS )

        profile = self.init_kwargs.get('profile', None)
        if profile is not None:
            profile_params = self.set_profile( profile, dev_mode = True )
            temp_params.update( profile_params )

        init_params = self.init_kwargs.get('params', None)
        if init_params is not None:
            for k, v in init_params.items():
                temp_params[ k ] = v

        for k, v in self.params.items():
            temp_params[ k ] = v

        # sanitized_params = self.abs_paths_for_specific_keys( temp_params )
        self.params.clear()
        self.params.update( temp_params )
        return

    def convert_results_to_csv(self, input_file, force=None, output_file_name=None):
        '''
        The ucontroller convert_results_to_csv function

        Note: uses the Java mzidentml library (Reisinger et al., 2012)

        Keyword Arguments:
            input_file (str): The complete path to the input, input file
                currently has to be an identification engine result file
            force (bool): (re)do the analysis if output files already exists
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::

            >>> us=ursgal.UController( profile='LTQ XL high res' )
            >>> us.convert_results_to_csv(
            ...    input_file = 'my_result.xml',
            ...)

        Returns:
            str: Path of the output file

        Notes: internal function, use :meth:`.convert` instead
        '''

        input_suffix = os.path.splitext( input_file )[-1].lower()

        if input_suffix == ".csv":
            self.print_info(
                "No need to convert to csv because input is already a csv!",
                caller = 'cnvrtcsv'
            )
            report = input_file

        else:
            file_json_path = input_file + self.params['json_extension']
            json_content = self.load_json( json_path = file_json_path )
            last_engine = self.get_last_search_engine(
                history = json_content[3]['history'],
            )
            if 'xtandem' in last_engine:
                engine_name = self.params['xtandem_converter_version']
            elif 'msgfplus' in last_engine:
                engine_name = self.params.get(
                    'msgfplus_mzid_converter_version',
                    None
                )
                if engine_name is None:
                    engine_name = self.UNODE_UPARAMS['msgfplus_mzid_converter_version']['uvalue_style_translation'][last_engine]
            else:
                engine_name = self.params['mzidentml_converter_version']

            report = self.execute_unode(
                input_file       = input_file,
                engine           = engine_name,
                force            = force,
                output_file_name = output_file_name
            )
        return report

    def convert_to_mgf_and_update_rt_lookup(self, input_file, force=None, output_file_name=None):
        '''
        Converts the mzML to mgf and updates the scanID to retention time
        lookup. The looukp is needed for the unifying of the .csv files.

        Arguments:
            input_file (str): mzML input file name

        Returns:
            str: name of the output mgf file

        Notes: internal function, use :meth:`.convert` instead

        '''
        engine_name = self.params['mzml2mgf_converter_version']
        self.input_file_sanity_check(
            input_file,
            engine     = engine_name,
            extensions = ["mzml"]
        )
        answer = self.prepare_unode_run(
            input_file,
            output_file = output_file_name,
            engine = engine_name,
            force  = force
        )

        # Making sure the retention-time lookup pickle is there and
        # contains info about the currenz mzML:
        scan_rt_lookup_path = self.io['input']['scan_rt_lookup_path']
        if os.path.exists( scan_rt_lookup_path ) is False:
            answer = 'No RT lookup pickle found. Expected {0}'.format(
                scan_rt_lookup_path
            )
        else:
            scan_rt_lookup = pickle.load(
                open( scan_rt_lookup_path, 'rb' )
            )
            self.scan_rt_lookup.update( scan_rt_lookup )

        if answer is None:
            file_root = self.io['output']['finfo']['file_root']
            if file_root not in scan_rt_lookup.keys():
                answer = '{file_root} has no entry in RT lookup pkl: {0}'.format(
                    scan_rt_lookup_path,
                    **self.io['output']['finfo']
                )

        report = self.run_unode_if_required(
            force, engine_name, answer
        )

        # update RT lookup pickle in case something changed:
        if answer is not None:
            file_root = self.io['output']['finfo']['file_root']
            self.scan_rt_lookup[ file_root ] = report['execution']
            with open( scan_rt_lookup_path, 'wb' ) as rtpkl:
                pickle.dump(
                    self.scan_rt_lookup,
                    rtpkl
                )
        self.scan_rt_lookup_path = scan_rt_lookup_path
        return report['output_file']

    def determine_availability_of_unodes(self):
        '''
        The ucontroller determine_availability_of_unodes function

        Note: internal function

        Checks for engines in ursgal/resources/<platform>/<architecture>
        and expects the executable to be in the corresponding folder.
        '''
        arc_specific_engine_folders = os.path.join(
            ursgal.base_dir,
            'resources',
            self.platform,
            self.architecture[0]
        )
        arc_independent_engine_folders = os.path.join(
            ursgal.base_dir,
            'resources',
            'platform_independent',
            'arc_independent'
        )
        engine_folders = [
            (
                self.platform,
                self.architecture[0],
                arc_specific_engine_folders
            ),
            (
                'platform_independent',
                'arc_independent',
                arc_independent_engine_folders
            )
        ]
        for platform_key, arc_key, engine_folder in engine_folders:

            for engine in sorted( self.unodes.keys() ):
                if engine.startswith('__'):
                    # we skip __by_meta_type and __engine_type dicts ...
                    continue

                # kb_info = self.unodes.get( engine, {} )
                kb_info = self.unodes[ engine ]
                # if len(kb_info.keys()) == 0:
                #     self.print_info('No wrapper found for ')
                #     # No info available
                #     continue

                kb_engine_entry = kb_info.get( 'engine', None )

                if kb_engine_entry is None:
                    # if True: # self.verbose is False:
                    #     self.print_info(
                    #         'Skipped {0}, no engine entry in meta_info'.format(
                    #             engine
                    #         )
                    #     )
                    continue
                if platform_key not in kb_engine_entry.keys():
                    continue
                if arc_key not in kb_engine_entry[ platform_key ].keys():
                    continue

                exe_name = kb_engine_entry[ platform_key ][ arc_key ].get(
                    'exe',
                    None
                )
                if exe_name is None:
                    continue

                engine_folder_path = os.path.join( engine_folder, engine )
                engine_exe_path = os.path.join( engine_folder_path, exe_name )

                self.unodes[ engine ]['resource_folder'] = engine_folder_path

                alternative_exe_folder = kb_info.get(
                    'uses_unode',
                    None
                )
                if os.path.exists( engine_exe_path ) or alternative_exe_folder is not None:
                    _wrapper_class = self.unodes[ engine ]['_wrapper_class']
                    try:
                        self.unodes[ engine ]['class'] = _wrapper_class(
                            engine_path = engine_exe_path
                        )
                    except TypeError:
                        print('''

                Do you have *args and **kwargs in your Class {0} ?
                E.g.:

                class msblender_09_2015( ursgal.UNode ):
                    def __init__( self,  *args, **kwargs ):

                            '''.format(engine))
                        self.unodes[ engine ]['import_status'] = 'Class syntax error?'
                        self.unodes[ engine ]['available'] = False
                        continue

                    if self.unodes[ engine ]['class'].dependencies_ok is False:
                        self.unodes[ engine ]['import_status'] = 'dependencies failed'
                        self.unodes[ engine ]['available'] = False
                    else:
                        self.unodes[ engine ]['import_status'] = 'available'
                        self.unodes[ engine ]['available'] = True

                else:
                    self.unodes[ engine ]['import_status'] = 'cant find exe'
                    self.unodes[ engine ]['available'] = False
                    in_development = self.unodes[ engine ]['META_INFO']['in_development']
                    if not in_development:
                        if self.verbose:
                            print(
                                '[ WARNiNG! ] Engine {0} is not available in {1}'.format(
                                    engine,
                                    engine_folder_path
                                )
                            )
        return

    def engine_sanity_check( self, short_engine):
        '''
        The ucontroller engine_sanity_check function

        Takes input and name and tries to guess the full engine name,
        e.g. including the version number. omssa as inpout will yield
        omssa_2_1_9 if there is only one omssa engine installed, i.e.
        the mapping (<stored_fulle_engine_name>.startswith( <input> )
        has to be unique and defined.

        Additionally, sanity check also validates if engine is available
        on the system.

        Note: internal function, since assertion error is called.

        Arguments:
            short_engine (str): engine short name or tag

        calls `self.guess_engine_name()`

        Returns:
            str: Full name of the engine or None.
        '''
        matches = self.guess_engine_name( short_engine )
        assert len(matches) > 0, '''
      The engine name "{0}" you have specified was not found.
      Make sure that you spelled it correctly!
        '''.format( short_engine )
        assert len(matches) == 1, '''
      The engine name "{0}" you have specified is not explicit.
      Multiple hits found: {1}.
        '''.format( short_engine, ", ".join(matches) )
        full_engine_name = matches[0]
        assert self.unodes[full_engine_name].get('available', False) is True or \
            self.unodes[full_engine_name].get('in_development', False) is True, '''
      Requested engine {0} was mapped on {1}, which is not available
      on your system.
        '''.format( short_engine, full_engine_name )

        return full_engine_name

    def fetch_file( self, engine=None ):
        '''
        The UController fetch_file function

        Downloads files (FTP or HTTP).

        Keyword Arguments:
            engine (str): Available options are 'get_http_files_1_0_0' and
                'get_ftp_files_1_0_0'

        Example::

            >>> params = {
            ...     'ftp_url'       : 'ftp.peptideatlas.org',
            ...     'ftp_login'         : 'PASS00269',
            ...     'ftp_password'      : 'FI4645a',
            ...     'ftp_include_ext'   : [
            ...         'JB_FASP_pH8_2-3_28122012.mzML',
            ...     ],
            ...     'ftp_output_folder' : '/home/Desktop/,
            ... }
            >>> uc = ursgal.UController(
            ...     params = params
            ... )
            >>> uc.fetch_file(
            ...     engine     = 'get_ftp_files_1_0_0'
            ... )

        Returns:
            str: Path of the downloaded file
        '''
        assert engine is not None, '''Please specify a download engine
        Engines: get_http_files_1_0_0 or get_ftp_files_1_0_0

        '''
        answer = self.execute_unode(
            input_file = None,
            engine     = engine,
        )
        # remove the temporary input file!
        try:
            if self.params['prefix'] is not None:
                tmp_file_name = '{0}_{1}'.format(
                    self.params['prefix'],
                    self.io['input']['finfo']['json']
                )
            else:
                tmp_file_name = self.io['input']['finfo']['json']
            path_2_remove = os.path.join(
                self.io['input']['finfo']['dir'],
                tmp_file_name
            )
            os.remove(
                path_2_remove
            )
        except:
            self.print_info(
                'Automatic removal of tmp file {0} failed'.format(
                    path_2_remove
                ),
                caller = 'Info'
            )
            self.print_info(
                'Please check folder and clean up manually: {0}'.format(
                    self.io['input']['finfo']['dir']
                ),
                caller = 'Info'
            )
        return answer

    def generate_target_decoy(self, input_files=None, engine=None, force=False, output_file_name=None):
        '''
        [ WARNING ] This function is not supported anymore!
                    Please use :meth:`.execute_misc_engine` instead

        The ucontroller function for target_decoy database generation.

        Keyword Arguments:
            input_files (list): List with complete paths to one or more
                fasta databases.
            engine (str): name of the database generator which should be run,
                can also be a short version if this name is unambigous
            force (bool): (re)do the analysis if ouput files already exists
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::

            >>> my_databases = ['homo_sapiensA.fasta', 'homo_sapiensB.fasta']
            >>> uc = ursgal.UController()
            >>> new_target_decoy_db = uc.generate_target_decoy(
            ...    input_files      = my_databases,
            ...    engine           = 'generate_target_decoy_1_0_0',
            ...    output_file_name = 'my_homo_sapiens_target_decoy_db.fasta'
            ...)

        The returned database can then be set as the new database
        for searches.

        Example::

            >>> uc.params['database'] = new_target_decoy_db

        Returns:
            str: Name/path of the output file
        '''
        self.print_old_function_warning(
            'generate_target_decoy',
            'execute_misc_engine'
        )
        if engine is None:
            engine = 'generate_target_decoy_1_0_0'
        return self.execute_unode(
            input_file       = input_files,
            engine           = engine,
            force            = force,
            output_file_name = output_file_name
        )

    def guess_engine_name(self, short_engine):
        '''
        The ucontroller function for guessing the right engine name from a
        short name. For example 'omssa' is translated into omssa_2_1_9 which
        is the only available version of omssa in ursgal. If you use an
        ambigous name or if a engine has multiple version, it is required to
        name the engine unambigously. Instead of myrimatch use
        myrimatch_2_1_138.

        Arguments:
            short_engine (str): engine short name or tag


        Iterates over `self.unodes.keys()` and checks if:

            * the keys start with the short_engine
            * that the match is unique

        Notes: internal function

        Returns:
            str: Full name of engine or `None` if short_engine has
                multiple hits
        '''
        matches = []
        for engine in self.unodes.keys():
            if engine.lower().startswith( short_engine.lower() ):
                matches.append( engine )

        return matches

    def merge_csvs(self, input_files, force=None, output_file_name=None, merge_duplicates=False ):
        '''
        The ucontroller merge_csvs function

        Merges unified .csv files generated by the same search engine into
        a single .csv file. This is needed if you want to validate search
        results from the same identification engine on multiple mzML files.
        For example if multiple fraction of the original sample for LS-MS/MS
        analysis were measured and represent a sample/analysis entity.

        Keyword Arguments:
            input_files (list): A list containing the complete paths to two or
                more input files. Input files have to be .csv files.
            force (bool): (re)do the analysis if output file already exists
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.


        Example::

            >>> us = ursgal.UController()
            >>> xtandem_results = [
            ...     'BSA_1_xtandem_sledgehammer_unified.csv',
            ...     'BSA_2_xtandem_sledgehammer_unified.csv',
            ...     'BSA_3_xtandem_sledgehammer_unified.csv'
            ... ]
            >>> us.merge_csvs( input_files = xtandem_results )

        Returns:
            str: Path of the output file
        '''
        one_file_str  = isinstance(input_files, str)
        one_file_list = isinstance(input_files, list) and len(input_files) == 1
        if one_file_str or one_file_list:
            # only a single file was specified, nothing to merge
            # -> return the unchanged input file
            self.print_info(
                'merge_csvs() received only one input file, '
                'continuing without merging',
                caller = "WARNING"
            )
            if one_file_list:
                output_file = input_files[0]
            elif one_file_str:
                output_file = input_files
        else:
            # multiple files were specified (expected!), merge them:
            engine_name = 'merge_csvs_1_0_0'
            self.input_file_sanity_check(
                input_files,
                engine=engine_name,
                multi=True
            )
            answer = self.prepare_unode_run(
                input_files,
                output_file = output_file_name,
                engine = engine_name,
                force  = force
            )

            search_engines_of_merged_files = []
            for d in self.io['output']['params']['input_file_dicts']:
                search_engines_of_merged_files.append( d["last_engine"] )

            report = self.run_unode_if_required(
                force, engine_name, answer,
                history_addon = {
                    'search_engines_of_merged_files' : search_engines_of_merged_files
                },
                merge_duplicates=merge_duplicates,
            )
            output_file = report['output_file']
        return output_file

    def combine_search_results(self, input_files, engine=None, force=None, output_file_name=None ):
        '''
        The ucontroller combine_search_results function
        combines search result .csv files that were generated by
        different search engines.

        Keyword Arguments:
            input_files (list): A list containing the complete paths to
                two or more input files. Input files have to be unified result
                .csv files that were produced by different engines.
            engine (str): The name of the desired search result combiner.
                 Can also be a shortened version if it is unambigous.
            force (bool): (Re)do the analysis, even if output file already
                exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::

            >>> uc=ursgal.UController()
            >>> unified_merged_results = [
            ...    'BSA_xtandem_piledriver_unified_merged.csv',
            ...    'BSA_msgfplus_unified_merged.csv',
            ...    'BSA_omssa_unified_merged.csv'
            ...]
            >>> uc.combine_search_results(
            ...    input_files = unified_merged_results,
            ...    engine      = 'combine_FDR_0_1'
            ...)

        Note:
            If you have multiple result files from the same engine, you can
            merge them with :meth:`.merge_csvs`.

        Returns:
            str: Path of the output file
        '''
        engine_name = self.engine_sanity_check( engine )
        self.input_file_sanity_check(
            input_files,
            engine=engine_name,
            multi=True
        )

        answer = self.prepare_unode_run(
            input_files,
            output_file = output_file_name,
            engine = engine_name,
            force  = force
        )

        # making sure that all input files are from different engines:
        input_file_dicts = self.io['output']['params']['input_file_dicts']
        input_file_search_engines = {
            ifd["last_engine"] for ifd in input_file_dicts
        }

        assert len(input_file_search_engines) == len(input_files), '''
      All combine_search_results() input files must be search results from
      *different* search engines.
      You specified {0} input files
      ({1})
      but they are only from {2} different engine(s).
      If you want to analyze multiple files from the same engine, please
      merge them beforehand using merge_csvs().'''.format(
            len(input_files),
            input_files,
            len(input_file_search_engines)
        )

        report = self.run_unode_if_required(
            force, engine_name, answer
        )
        return report['output_file']

    def convert(self, input_file, engine=None, force=None, output_file_name=None, guess_engine=False ):
        '''
        The UController convert function converts the given input_file
        into another format as defined by the specified engine.

        Keyword Arguments:
            input_file (str): The complete path to the input file.
            engine (str): The name of the desired converter engine.
                 Can also be a shortened version if it is unambigous.
            force (bool): (Re)do the analysis, even if output file already
                exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.
            guess_engine (bool): The converter engine is guessed based on
                the input file. This works so far for mzml2mgf conversion and
                conversion of search_engine result files to csv.

        Example::

            >>> uc=ursgal.UController()
            >>> unified_merged_results = 'BSA_msgfplus_unified_merged.csv',
            >>> uc.convert_file(
            ...    input_file = unified_merged_results,
            ...    engine     = 'csv2ssl_1_0_0'
            ...)

        Returns:
            str: Path of the output file
        '''

        if guess_engine is True:
            if input_file.upper().endswith('.MZML'):
                outfile = self.convert_to_mgf_and_update_rt_lookup(
                    input_file       = input_file,
                    force            = force,
                    output_file_name = output_file_name
                )
            else:
                file_json_path = input_file + self.params['json_extension']
                last_engine_type = None

                assert os.path.exists( file_json_path ), '''
                Cannot guess a suitable engine, since no json for
                the input file was found.
                {0}
                '''.format(input_file)

                json_content = self.load_json(
                        json_path = file_json_path
                    )
                last_engine_type = self.get_last_engine_type(
                        history = json_content[3]['history'],
                    )

                if 'search_engine' in last_engine_type:

                    outfile = self.convert_results_to_csv(
                        input_file       = input_file,
                        force            = force,
                        output_file_name = output_file_name
                    )
                else:
                    print('Cannot guess a suitable engine, please specify it.')
                    sys.exit(1)

        elif len(self.guess_engine_name(engine)) == 1 and\
                self.guess_engine_name(engine)[0] in ['mzml2mgf_1_0_0','mzml2mgf_2_0_0']:
            outfile = self.convert_to_mgf_and_update_rt_lookup(
                input_file       = input_file,
                force            = force,
                output_file_name = output_file_name
            )
        else:
            outfile = self.execute_unode(
                input_file       = input_file,
                engine           = engine,
                force            = force,
                output_file_name = output_file_name
            )

        return outfile

    def execute_misc_engine(self, input_file, engine=None, force=None, output_file_name=None, merge_duplicates=False ):
        '''
        The UController execute_misc_engine function

        This function can be used to execute any misc engine by
        only giving the input_file and engine name.

        Keyword Arguments:
            input_file (str): The complete path to the input, a unified
                (and possibly merged) search result .csv.
            engine (str): the name of the validation engine which should be
                run, can also be a short version if this name is unambigous
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.
            merge_duplicates (bool): If True, the produced output file will
                be checked for duplicated PSMs, which will be merged into a single line.
                Caution, the original output file will be overwritten!

        Note:
            Input files to :meth:`.validate` must be in unified csv format (i.e.
            output files of :meth:`.search` or :meth:`.unify_csv`).

        Example::

            >>> my_databases = ['homo_sapiensA.fasta', 'homo_sapiensB.fasta']
            >>> uc = ursgal.UController()
            >>> new_target_decoy_db = uc.execute_misc_engine(
            ...    input_files      = my_databases,
            ...    engine           = 'generate_target_decoy_1_0_0',
            ...    output_file_name = 'my_homo_sapiens_target_decoy_db.fasta'
            ...)

        Returns:
            str: Path of the output file
        '''
        engine_name = self.engine_sanity_check(engine)
        if 'merge_csvs' in engine_name:
            outfile = self.merge_csvs(
                input_file,
                force = force,
                output_file_name = output_file_name,
                merge_duplicates = merge_duplicates
            )

        else:
            outfile = self.execute_unode(
                input_file       = input_file,
                engine           = engine,
                force            = force,
                output_file_name = output_file_name,
                merge_duplicates = merge_duplicates,
            )

        return outfile

    def set_file_info_dict( self, in_file ):
        '''Splits ext and path and so on '''
        finfo = {}
        full_path = os.path.abspath( in_file )
        finfo['file'] = os.path.basename( full_path )
        finfo['dir']  = os.path.dirname( full_path )
        finfo['full'] = os.path.join( finfo['dir'], finfo['file'] )

        if finfo['file'].upper().endswith('.GZ'):
            finfo['is_compressed'] = True
            finfo['file_root'], finfo['file_extention'] = os.path.splitext(
                finfo['file'][:-3]
            )
        else:
            finfo['is_compressed'] = False
            finfo['file_root'], finfo['file_extention'] = os.path.splitext(
                finfo['file']
            )
        finfo['json'] = finfo['file'] + self.params['json_extension']
        if os.path.exists( os.path.join( finfo['dir'], finfo['json'] )):
            finfo['json_exists'] = True
        else:
            finfo['json_exists'] = False
        return finfo

    def prepare_unode_run( self, input_file, engine=None, force=None, output_file=None ):
        # resetting controller
        # and updating self.io['input']['params'] to reflect
        # merged params and json if available ..
        self.reset_controller()
        # if force is not None:   # overwriting default force value with
            # self.force = force  # user-specified settings

        engine_name = self.engine_sanity_check( engine )
        # isn't this executed b4?
        self.print_info(
            "Preparing unode run for engine {0} on file(s) {1}".format(
                engine_name,
                input_file
            ),
            caller = 'prprun'
        )

        # If the UNode received multiple input files,
        # a helper file is generated (contains input filenames and their MD5s)
        # the helper file acts as the new input file. A basic json is dumped
        # for the helper file, too.
        if isinstance( input_file, list ):
            self.input_file_dicts = self.generate_multi_file_dicts(input_file)
            # the helper file now acts as the input file:
            input_file       = self.generate_multi_helper_file( input_file )
            self.dump_multi_json( input_file, self.input_file_dicts )

        self.set_ios(
            input_file,
            engine = engine_name,
            userdefined_output_fname = output_file
        )

        # set basic io finfo and takes care of json load into proper io
        answer = self.eval_if_run_needs_to_be_executed(
            engine = engine_name,
            force  = force,
        )

        # if re-run is scheduled, delete output file from previous run
        # if there is one (it might cause trouble...)
        if answer is not None:
            if os.path.isfile(self.io['output']['finfo']['full']):
                os.remove( self.io['output']['finfo']['full'] )

        # At this point we know if we need to rerun and
        # thus we can move params and stats on
        if answer is not None:
            self.io['output']['stats' ] = self.io['input']['stats' ]
            self.io['output']['params'] = self.io['input']['params']
            if hasattr(self, 'input_file_dicts'):
                self.io['input']['params']['input_file_dicts'] = self.input_file_dicts
        return answer

    def generate_multi_dir_and_basename( self, input_files ):
        self.input_file_sanity_check( input_files, multi=True )

        common_fname_w_ext = "_".join(
            self.determine_common_head_tail_part_of_names( input_files )
        )
        common_fname, __ = os.path.splitext( common_fname_w_ext )
        common_dir = self.determine_common_top_level_folder(
            [os.path.abspath(path) for path in input_files]
        )
        return common_dir, common_fname.strip("_")

    def generate_multi_helper_file( self, input_files ):
        '''
        for UNodes that take multiple input files.
        generates a temporary single input helper file,
        which acts as the input file so that all the
        routines (set_io, write history) work normally
        with multiple files.
        '''
        directory, basename = self.generate_multi_dir_and_basename( input_files )
        extension           = self.params['helper_extension']

        '''
        # TODO: confirm that this code block is not needed anymore:
        prefix = self.params['prefix']
        if prefix != "" and prefix != None:
            prefix_bools = set()
            for ifd in self.input_file_dicts:
                prefix_bools.add( ifd['file'].startswith(prefix) )
            if len(prefix_bools) > 1 or prefix_bools == {True}:
                prefix = None
                self.params["prefix"] = None

        if prefix != "" and prefix != None:
            basename = prefix + "_" + basename
        '''

        multi_helper_fname = os.path.join( directory, basename + extension )

        input_file_dicts = []

        with open( multi_helper_fname, 'w') as helper_file:
            for input_file in sorted( input_files ):
                input_file_md5  = self.calc_md5( input_file )
                input_file_base = os.path.basename( input_file )
                row = ",".join( [input_file_base, input_file_md5] ) + "\n"
                helper_file.write( row )

        return multi_helper_fname

    def dump_multi_json( self, fpath, fdicts ):
        '''
        For UNodes that take multiple input files.
        Generates a json for the multi-input helper file.
        This json allows ursgal to check whether input
        changed or not, to determine if a node has to be
        re-run or not.
        '''

        # a file-info dict containing information about all the
        # input files (i.e. 'file_extention': [".csv", ".csv"] )
        multi_info  = self.merge_fdicts( *fdicts )

        # file-info dict containing information about the multi-helper file
        helper_info = self.set_file_info_dict( fpath )

        # get the md5 of the multi-helper file
        helper_info[ 'md5' ] = self.calc_md5( fpath )

        json_file = fpath + self.params['json_extension']
        j_content = [
            multi_info,
            helper_info,
            self.params.copy(),  # params
            self.stats.copy(),   # stats
        ]

        keys_to_delete = self.params.get(
            'del_from_params_before_json_dump',
            []
        )
        for key in keys_to_delete:
            if key in j_content[2].keys():
                del j_content[2][ key ]

        for param_key in list(j_content[2].keys()):
            if param_key.startswith('_'):
                del j_content[2][ param_key ]

        # j_content[3]['history'][-1]['ursgal_version'] = ursgal.__version__

        # dumping a history for multiple files would be tricky,
        # so let's not attempt it for now...
        with open( json_file , 'w') as file_object:
            json.dump(
                j_content,
                file_object,
                sort_keys = True,
                indent = 2
            )

    def merge_fdicts( self, *fdicts):  # , join=False ):
        '''

        '''
        merged_fdict = {}
        keys = set()
        for fdict in fdicts:
            for key in fdict.keys():
                keys.add( key )

        for key in sorted(keys):
            merged_fdict[ key ] = []
            for fdict in fdicts:
                if key in fdict:
                    merged_fdict[ key ].append( fdict[ key ] )
            # if join:
            #     merged_fdict[ key ] = ",".join(
            #         [str(x) for x in merged_fdict[ key ] ]
            #     )
        return merged_fdict

    def generate_multi_file_dicts( self, input_files ):
        '''
        generates a file_dict for access in the UNode classes.
        in the UNode classes, a file_dict can be found for each input file
        under self.params["input_file_dicts"].
        also adds some "quick-access" entries to the file_dicts.
        these file dicts contain the input/output file dicts for that file,
        as well as quick-access information (i.e. "last_engine")
        '''
        list_of_file_dicts = []
        for input_file in input_files:
            file_json_path = input_file + self.params['json_extension']

            last_engine = None
            last_engine_colname = None

            # if the file has a json, we can retrieve its file information from it:
            if os.path.exists( file_json_path ):

                json_content = self.load_json(
                    json_path = file_json_path
                )
                if len(json_content) > 3 and 'history' in json_content[3]:
                    last_engine = self.get_last_search_engine(
                            history = json_content[3]['history'],
                            multiple_engines = True,
                        )
                    if last_engine is not None and type(last_engine) != list:
                        # last_engine_meta_node = self.meta_unodes[ last_engine ]

                        last_engine_colname = \
                            self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][last_engine]
                        # old translation style:
                        # last_engine_colname = \
                        #     last_engine_meta_node.DEFAULT_PARAMS['validation_score_field'].split(":")[0]


                # write all the information we just collected to a dict for that file:
                file_dict = {}

                # old method: load finfo from json no matter what
                # file_dict.update( json_content[1] )
                # new method: regenerate finfo from file path (allows moving files around),
                # but load history etc from json
                file_dict.update(
                    self.set_file_info_dict( input_file )
                )
                file_dict['last_engine'] = last_engine
                file_dict['last_engine_colname'] = last_engine_colname

            else:
            # if the file has no json yet, we generate only the file path dict...
            # in that case, we have no auxiliary information like "last_search_engine"
                file_dict = self.set_file_info_dict( input_file )

            list_of_file_dicts.append( file_dict )
        return list_of_file_dicts

    def set_ios(self, input_file, engine=None, userdefined_output_fname=None ):
        self.io = {
            'input'  : {
                'finfo'   : None,
                'params'  : None,
                'stats'   : None,
                'i_finfo' : None,
                'o_finfo' : None,
            },
            'output' : {
                'finfo'   : None,
                'params'  : None,
                'stats'   : None,
                'i_finfo' : None,
                'o_finfo' : None,
            },
        }
        #
        # -\- Setting up self.io['input'] -/-
        #
        self.print_info(
            msg    = 'Setting self.io["input"]',
            caller = 'set_ios'
        )
        self.io['input']['finfo'] = self.set_file_info_dict(input_file)
        self.take_care_of_params_and_stats(io_mode = 'input')
        # setting status ...
        self.io['input']['stats']['run_status'] = 'scheduled'
        # setting default if no json was loaded ...

        if self.io['input']['finfo']['json_exists'] is False:
            # user defined params are already updated in self.params
            # during _after_init_meta_callback
            self.io['input']['params'] = self.params.copy()
        else:
            # update controller params that have been changed since json dump
            # NOTE: They are not updated!
            number_of_diffs_between_json_and_params = 0
            for u_param, u_value in self.params.items():
                if u_param not in self.io['input']['params'] or \
                        self.io['input']['params'][ u_param ] != u_value:
                    #
                    number_of_diffs_between_json_and_params += 1
                    self.print_info(
                        'Mismatch of param {0}: UController: {1}; i_json: {2}'.format(
                            u_param,
                            u_value,
                            self.io['input']['params'].get(u_param, '[no_entry]')
                        ),
                        caller = 'set_ios'
                    )
                    self.io['input']['params'][ u_param ] = u_value
            # check if params from previous run are identical with default
            for i_json_param, i_json_value in self.io['input']['params'].items():
                if i_json_param in self.params.keys():
                    continue
                if i_json_param not in self.meta_unodes[ engine ].PARAMS_TRIGGERING_RERUN:
                    continue
                default_value = self.meta_unodes[engine].UNODE_UPARAMS[i_json_param]['default_value']
                if i_json_value != default_value:
                    number_of_diffs_between_json_and_params += 1
                    self.print_info(
                        'Mismatch of param {0}: UController: {1}; i_json: {2}'.format(
                            i_json_param,
                            default_value,
                            i_json_value
                        )
                    )
                    self.io['input']['params'][i_json_param] = default_value
            if number_of_diffs_between_json_and_params > 0:
                self.print_info(
                    'Updated {0} params in self.io["input"]["params"]'.format(
                        number_of_diffs_between_json_and_params
                    ),
                    caller = 'set_ios'
                )
            # lets propagate md5 information into input finfo
            # for json dump.. evals are always done on loaded
            # i_finfo and o_finfo

        if self.io['input']['finfo']['json_exists']:
            self.io['input']['finfo']['md5'] = self.io['input']['o_finfo']['md5']
        # setting pickle path ...
        pickle_path = self.io['input'].get(
            'scan_rt_lookup_path',
            None
        )
        if pickle_path is None:
            self.io['input']['scan_rt_lookup_path'] = os.path.join(
                self.io['input']['finfo']['dir'],
                self.io['input']['params']['rt_pickle_name'],
            )
            self.scan_rt_lookup = {}
        #
        # -\- Setting up self.io['output'] -/-
        #
        if userdefined_output_fname is None:
            # (default behaviour:) auto-generate output filename
            output_file = self.build_name_from_history_or_regen(
                engine = engine,
            )
        else:
            # if user specified a filename, make sure it's not completely crazy
            sanitized_fname = self.sanitize_userdefined_output_filename(
                userdefined_output_fname, engine
            )
            output_file = os.path.join(
                self.io['input']['finfo']['dir'],
                sanitized_fname
            )

        self.io['output']['finfo'] = self.set_file_info_dict( output_file )
        self.take_care_of_params_and_stats( io_mode = 'output')
        # pprint.pprint( self.io )
        # exit(1)
        return

    def sanitize_userdefined_output_filename(self, user_fname, engine ):
        '''
        If the user defined a node output file name, we remove all path info from it
        (not supported) and throw a warning; possibly add a prefix; possibly add the
        correct file extension (if user didn't already include it)
        '''
        if os.sep in user_fname:
            self.print_info(
                ('You cannot assign a full path to output_file_name! '
                'The path is automatically determined by ursgal.'),
                caller='WARNING'
            )
        ok_extension = self.decide_output_extension(engine)
        prefix = self.params['prefix']
        user_fname = os.path.basename( user_fname )
        if ok_extension is None or user_fname.endswith( ok_extension ):
            out_fname = user_fname
        else:
            out_fname = user_fname + ok_extension
        if prefix not in [None,''] and not user_fname.startswith(prefix):
            out_fname = '_'.join( [prefix, out_fname] )
        self.print_info(
            "You defined {0}'s output file name as: {1}".format(
                engine, out_fname
            ),
            caller = 'Info'
        )
        return out_fname

    def take_care_of_params_and_stats(self, io_mode=None):
        if io_mode is None:
            io_mode = 'input'
        if self.io[ io_mode ]['finfo']['json_exists']:
            j_content = self.load_json(
                finfo = self.io[ io_mode ]['finfo']
            )
            i_finfo, o_finfo, params, stats = j_content
            self.io[ io_mode ]['params' ] = params
            self.io[ io_mode ][ 'stats' ] = stats
            self.io[ io_mode ]['i_finfo'] = i_finfo
            self.io[ io_mode ]['o_finfo'] = o_finfo

            #if io_mode == 'input':
            ##io_key = 'i_finfo'
            #elif io_mode == 'output':
                #io_key = 'o_finfo'

            #input_path_from_json = self.io[ io_mode ][ io_key  ]['dir']
            #input_path_from_file = self.io[ 'input' ][ 'finfo' ]['dir']
            ## input paths according to json:
            #debug_print( self.io[ io_mode ]['i_finfo'] )
            ## input paths according to input file:
            #debug_print( self.io[ 'input' ][ 'finfo' ], color="RED")


            # i_info was the file info that was used to start the run that
            #   lead to the json
            # o_info is the file info that was produced after the run that
            #   lead to the json
            # if io_mode == 'input':
            #     compare = i_finfo
            #     # we want to get the information of the output file that was
            #     # produced
            # else:
            #     compare = o_finfo
            #     # we want to get the information that was used as an input
            #     # for this call
            # if 'THIS HAS TO BE CHECKED' == '42':
            #     if self.io['output']['finfo'] is not None:
            #         for io_k, io_v in sorted(o_finfo.items()):
            #             generate_v = self.io['output']['finfo'].get( io_k, None )
            #             if 'exists' in io_k:
            #                 continue
            #             if generate_v is None:
            #                self.io['output']['finfo'][ io_k ] = io_v
            #             else:
            #                 assert generate_v == io_v, '''
            #                 Auto generation and json finfo mismatch
            #                 json {0}:{1} .. auto generated {0}:{2}
            #                 mode: {3}
            #                 json loaded: {4}
            #                 '''.format(
            #                     io_k,
            #                     io_v,
            #                     generate_v,
            #                     io_mode,
            #                     self.io[ io_mode ]['finfo']['json']
            #                 )
            # this is required to format the output file properly using
            # the file history ...
            # self.io['output']['params'] = json_params
            # self.io['output']['stats'] = json_stats
        else:
            self.io[ io_mode ]['params'] = {}
            self.io[ io_mode ]['stats'] = {
                'time_points'    : {},
                'history'        : [],
            }

    def decide_output_extension( self, engine ):
        file_extension = None
        file_extensions = self.meta_unodes[ engine ].META_INFO.get(
            'output_extensions',
            None
        )
        if file_extensions is not None and type(file_extensions) is list:
            if len(file_extensions) >= 1:
                file_extension = str(file_extensions[0])
            else:
                file_extension = ""
        return file_extension

    def build_name_from_history_or_regen( self, engine ):
        file_name_blocks = []

        #if self.io['input']['finfo']['json_exists'] and self.io['input']['stats']['history'] != []:
            #for h_pos, entry in enumerate(self.io['input']['stats']['history']):
                #if h_pos == 0:
                    #file_name_blocks.append(
                        #entry['finfo']['file_root']
                    #)
                #else:
                    #history_engine = entry['engine']
                    #engines_unode = self.meta_unodes[ history_engine ]
                    #engine_wants_name_in_output = engines_unode.META_INFO.get(
                        #'include_engine_in_name',
                        #False
                    #)
                    #if engine_wants_name_in_output:
                        #file_name_blocks.append( history_engine )
        #else:
            #file_name_blocks.append(
                #self.io['input']['finfo']['file_root']
            #)

        # don't build name from history, just take the last file root:
        file_name_blocks.append(
            self.io['input']['finfo']['file_root'].strip('.u')
        )
        # add uNodes name as defined in kb
        # if there is no entry called 'output_suffix', the engine/node
        # name is used instead; if it's None, no suffix is added
        output_suffix = self.meta_unodes[ engine ].META_INFO.get(
            'output_suffix', engine
        )
        if output_suffix is not None:
            file_name_blocks.append( output_suffix )

        # add a user-specified prefix (if specified):
        prefix = self.params['prefix']

        # prepend prefix, but only if it wasnt prepended before
        if prefix != "" and prefix is not None:
            current_file = '_'.join( file_name_blocks )
            if not current_file.startswith( prefix ):
                file_name_blocks.insert( 0, prefix )

        #
        # Final output file name (without directory)
        #
        output_file = '_'.join( file_name_blocks )

        # Add file extension if needed (engine-specific, defined in kb)
        file_extension = self.decide_output_extension(engine)
        if file_extension is None:
            self.print_info(
                'No file extension ("output_extension") defined in '\
                'kb.{0}.META_INFO. Keeping input file extension'.format(
                    self.engine
                ),
                caller = "WARNING"
            )
            file_extension = self.io['input']['finfo']['file_extention']

        output_file += file_extension

        # global_ucontroller_compress_flag = self.params.get('compress_raw_search_results_if_possible', False)
        # compress_engine_output = self.unodes[ engine ]['class'].META_INFO.get( 'compress_raw_search_results', False)
        # if compress_engine_output and global_ucontroller_compress_flag:
        if self.params.get('compress_raw_search_results_if_possible', False):
            if self.UNODE_UPARAMS['compress_raw_search_results_if_possible']['uvalue_style_translation'].get(
                engine, False
            ):
                output_file += '.gz'

        path_building_blocks = [
            self.io['input']['finfo']['dir']
        ]

        # old method...
        #if self.io['input']['params'].get('search_engines_create_folders', False):
            #if self.meta_unodes[ engine ].META_INFO['engine_type'].get('search_engine', False):
                #engine_folder = os.path.join(
                    #self.io['input']['finfo']['dir'],
                    #engine
                #)
                #if os.path.exists( engine_folder ) is False:
                    #os.mkdir(engine_folder, mode=0o777)
                #path_building_blocks.append( engine_folder )

        engine_creates_folder = self.meta_unodes[ engine ].META_INFO.get(
            'create_own_folder', False
        )

        if engine_creates_folder == True and self.params['engines_create_folders'] == True:

            engine_folder = os.path.join(
                self.io['input']['finfo']['dir'],
                engine
            )
            if os.path.exists( engine_folder ) is False:
                os.mkdir(engine_folder, mode=0o777)
            path_building_blocks.append( engine_folder )

        path_building_blocks.append( output_file )
        full_output = os.path.join(
            *path_building_blocks
        )
        self.print_info(
            "Generated engine {0} output file name: {1}".format(
                engine, full_output
            ),
            caller = 'Info'
        )
        return full_output


    def eval_if_run_needs_to_be_executed(self, engine = None, force = None):
        '''
        Returns the reason why self.run needs to be executed
        or None if there is no need
        '''
        reasons = []
        # answer with reason will always switch need_to_run True
        if self.io['output']['finfo']['json_exists'] is False:
            reasons.append(
                'Never executed before. No out_json {0} found.'.format(
                    self.io['output']['finfo']['json']
                )
            )

        if self.io['output']['finfo']['json_exists']:
            # no reason to rerun yet :))
            # o_json exists no force
            i_params = self.io['input']['params']
            o_params = self.io['output']['params']

            for used_param in self.meta_unodes[engine].PARAMS_TRIGGERING_RERUN:
                if used_param in o_params.keys() and used_param in i_params.keys():
                    in_param = i_params[used_param]
                    out_param = o_params[used_param]

                    if type(in_param) is list:
                        in_param = list(sorted(in_param))
                    if type(out_param) is list:
                        out_param = list(sorted(out_param))
                    if out_param != in_param:
                        reasons.append(
                            'Node related parameters (for instance "{0}") '\
                            'have changed compared to the last output '\
                            '...'.format(used_param)
                        )
                        break
                else:
                    default_value = self.meta_unodes[engine].UNODE_UPARAMS[used_param]['default_value']
                    if used_param not in o_params.keys():
                        reasons.append(
                            'parameter "{0}" '\
                            'was not found in previous output params.'\
                            '...'.format(used_param)
                        )
                        break
                    else:
                        if type(default_value) is list:
                            default_value = sorted(default_value)
                        out_param = o_params[used_param]
                        if type(out_param) is list:
                            out_param = sorted(out_param)
                        if out_param != default_value:
                            reasons.append(
                                'A new node related parameter ("{0}") '\
                                'has been added compared to the last output '\
                                '...'.format(used_param)
                            )
                            # print('default:',default_value)
                            # print('used',o_params[used_param])
                            # print(self.meta_unodes[engine].UNODE_UPARAMS[used_param]['default_value'])
                            # exit(1)

                            break

        if self.io['output']['finfo']['json_exists']:
            # o_json exists no force no node related params changed
            o_history = self.io['output']['stats']['history']
            if len(o_history) > 0:
                last_o_history = \
                    self.io['output']['stats']['history'][-1]
                # print( o_history )
                # print( last_o_history )
                # print( 'history overview ')
                if last_o_history['status'] != 'complete':
                    reasons.append('Previous run was not completed, status {status}'.format( **last_o_history ))
        if self.io['output']['finfo']['json_exists'] and self.io['input']['finfo']['json_exists']:
            if self.io['input']['o_finfo']['md5'] != self.io['output']['i_finfo']['md5']:
                reasons.append(
                    'md5 of input file {file} changed - old run: {0} - new run: {1} '.format(
                        self.io['input']['o_finfo']['md5'],
                        self.io['output']['i_finfo']['md5'],
                        **self.io['output']['finfo']
                    )
                )

        if self.force is True:
            # when specifying UController(force=True)
            reasons.append( 'You used (the) force! (via UController)' )
        if force is True:
            # when specifying i.e. search(force=True)
            reasons.append( 'You used (the) force!' )

        if len(reasons) == 0:
            answer = None
        else:
            answer = '\n & '.join( reasons )
        return answer

    def compress_out_if_possible( self, raw_search_results, engine ):
        global_ucontroller_compress_flag = self.params.get('compress_raw_search_results_if_possible', False)
        compress_engine_output = self.unodes[ engine ]['class'].META_INFO.get( 'compress_raw_search_results', False)
        print('''


            {0} & {1} <<< Compress ?


            '''.format( compress_engine_output, global_ucontroller_compress_flag )
        )
        if compress_engine_output and global_ucontroller_compress_flag:
            print('We are compressing now and renaming the shiznit')
            sys.exit(1)

    def search_mgf(self, input_file, engine=None, force=None, output_file_name=None):
        '''
        The UController search_mgf function

        Does the main peptide identification search with the specified
        identification engine.
        This function is called with every mzML and every search which should
        be used. The function uses :meth:`.UNode.run` to execute a single
        search engine. For example to execute X!Tandem via command line.

        Keyword Arguments:
            input_file (str): The complete path to the input, input file has
                to be a .MGF file (but .mzML files can be converted to .MGF
                with Ursgal)
            engine (str): the name of the identification engine which should be
                run, can also be a short version if this name is unambigous.
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::

            >>> uc = ursgal.UController(
            ...    profile ='LTQ XL high res',
            ...    params  = {'database': 'BSA.fasta'}
            ... )
            >>> uc.search_mgf(
            ...    input_file = 'BSA.mgf',
            ...    engine     = 'xtandem_piledriver'
            ... )

        Returns:
            str: Path of the output file

        Note:
            Consider using :meth:`.search` instead. :meth:`.search`
            automatically converts mzML to MGF and produces a unified
            CSV output file.
        '''
        engine_name = self.engine_sanity_check(engine)
        self.input_file_sanity_check(
            input_file,
            engine=engine_name,
            extensions=['.mgf']
        )
        for search_engine_type in [
            'protein_database_search_engine',
            'cross_link_search_engine',
        ]:
            if self.unodes[ engine_name ]['class'].META_INFO.get(
                search_engine_type,
                False
            ) is not False:
            # if 'search_engine' in self.unodes[ engine_name ]['class'].META_INFO.keys():
            #     if self.unodes[ engine_name ]['class'].META_INFO['search_engine'] == True:
                self.input_file_sanity_check(
                    self.params['database'],
                    engine     = engine_name,
                    custom_str = 'FASTA database (uc.params["database"])',
                    extensions = ['fasta', 'fa', 'fast']
                )
                break
        answer = self.prepare_unode_run(
            input_file,
            output_file = output_file_name,
            engine = engine_name,
            force  = force
        )

        # in case we run search_mgf only, uc.scan_rt_lookup_path has not been
        # set thus we do it again ...
        # this wont work if the mgf conversion was done differently and we
        # do not have TRUSTWORTHY information about RT and SCAN_IDs for this
        # file ....
        self.scan_rt_lookup_path = self.io['input']['scan_rt_lookup_path']

        report = self.run_unode_if_required(
            force, engine_name, answer
        )
        return report['output_file']

    def search(self, input_file, engine=None, force=None, output_file_name=None):
        '''
        The ucontroller search function

        Performs a peptide search using the specified search engine and
        mzML file. Produces a CSV file with peptide spectrum matches in
        the unified Ursgal CSV format.
        see: :ref:`List of available engines<available-engines>`

        Keyword Arguments:
            input_file (str): The complete path to the mzML file, or an MGF
                file that was converted from mzML.
            engine (str): The name of the identification engine which should be
                used, can also be a short version if this name is unambigous.
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::
            >>> uc = ursgal.UController(
            ...    profile = 'LTQ XL high res',
            ...    params  = {'database': 'BSA.fasta'}
            ... )
            >>> uc.search(
            ...    input_file = 'BSA.mzML',
            ...    engine     = 'omssa'
            ... )

        Returns:
            str: Path of the output file (unified CSV format)

        Note:
            Some search engines require a lot of RAM (up to 14GB,
            depending on your input files). If you don't have a lot
            of RAM, some engines might crash. Consider using X!Tandem
            or OMSSA in these cases, since they are less demanding.

        Note:
            This function calls five search-related ursgal functions
            in succession, all of which can also be called individually:

                * :meth:`.convert` (mzml to mgf, if required, using the mzml2mgf engine)
                * :meth:`.search_mgf`
                * :meth:`.convert` (raw search results to csv, if required)
                * :meth:`.execute_misc_engine` (peptide_mapper)
                * :meth:`.execute_misc_engine` (unify_csv)
        '''

        # Verify that the specified engine is a valid UNode
        # will be done for each step ...
        # engine_name = self.engine_sanity_check( engine )

        # Verify input file exists and is mzML
        # will be done for each step
        # self.input_file_sanity_check(
        #     input_file,
        #     extensions = ['mzml', 'mzml.gz', 'mgf']
        # )

        # verify database exists and is fasta
        # will be done for seach_mgf
        # if 'search_engine' in self.unodes[ engine_name ]['class'].META_INFO.keys():
        #     if self.unodes[ engine_name ]['class'].META_INFO['search_engine'] is True:
        #         self.input_file_sanity_check(
        #             self.params['database'],
        #             engine     = engine_name,
        #             custom_str = 'FASTA database (uc.params["database"])',
        #             extensions = ['fasta', 'fa', 'fast'],
        #         )

        # 1. Convert mzML(.gz) to MGF format (if it's not already MGF):
        if not input_file.upper().endswith('.MGF'):
            mgf_file = self.convert(
                input_file,
                engine = self.params['mzml2mgf_converter_version'],
                force = force,
            )
        else:
            mgf_file = input_file

        # 2. Feed MGF into search engine of choice:
        raw_search_results = self.search_mgf(
            input_file = mgf_file,
            engine     = engine,
            force      = force,
        )

        # 3. Convert search result to CSV if required (mzidentml-lib):
        csv_search_results = self.convert(
            input_file = raw_search_results,
            engine = None,
            guess_engine = True,
            force      = force,
        )

        #insert peptide mapping here inlcuding the classification as a db engine
        engine_name = self.guess_engine_name( engine )
        engine_type = self.unodes[ engine_name[0] ]['class'].META_INFO['engine_type'].get(
            'protein_database_search_engine',
            False
        )
        if engine_type is not False:
            #if mapper version == 'COmpomics stuff'
            #execute this node and in map peptides, these results are read...
            mapped_csv_search_results = self.execute_misc_engine(
                input_file       = csv_search_results,
                output_file_name = output_file_name,
                engine           = self.params['peptide_mapper_converter_version'],
                force            = force,
            )
        else:
            mapped_csv_search_results = csv_search_results

        # 4. Convert csv to unified ursgal csv format:
        unified_search_results = self.execute_misc_engine(
            input_file       = mapped_csv_search_results,
            output_file_name = output_file_name,
            engine           = self.params['unify_csv_converter_version'],
            force            = force,
            merge_duplicates = True,
        )
        return unified_search_results

    def quantify(self, input_file, engine, force=None, output_file_name=None, multi=False):
        """
        The ucontroller quantify function

        Performs a peptide/protein quantification using the specified quantification engine and
        mzML/ident file file. Produces a CSV file with peptide/protein quants in
        the unified Ursgal CSV format.
        see: :ref:`List of available engines<available-engines>`

        Keyword Arguments:
            input_file (str): The complete path to the mzML file.
            engine (str): The name of the quantification engine which should be
                used, can also be a short version if this name is unambigous.
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::

            >>> uc = ursgal.UController(
            ...    profile = 'LTQ XL high res',
            ...    params  = {'evidence': 'BSA_idents.csv'}
            ... )
            >>> uc.quantify(
            ...    input_file = 'BSA.mzML',
            ...    engine     = 'pyQms_0_0_1'
            ... )

        Returns:
            str: Path of the output file (unified CSV format)
        """

        # Verify that the specified engine is a valid UNode
        engine_name = self.engine_sanity_check( engine )

        self.input_file_sanity_check(
            input_file,
            extensions = ['mzml', 'mzml.gz', 'mzml.igz'],
            multi=multi
        )

        answer = self.prepare_unode_run(
            input_file,
            output_file = output_file_name,
            engine = engine_name,
            force  = force
        )

        # in future unify output

        report = self.run_unode_if_required(
            force, engine_name, answer
        )

        return report['output_file']

    def get_mzml_that_corresponds_to_mgf(self, mgf_path):
        '''
        Checks the history of a MGF file to determine which
        mzML is stems from. Returns the path to that mzML.
        '''
        error_msg = ('\n  Could not find the mzML file that '
                     'corresponds to {0}').format(mgf_path)
        if hasattr(self, 'io'):
            self.io['tmp'] = {}
        else:
            self.io = { 'tmp':{} }
        self.io['tmp']['finfo'] = self.set_file_info_dict( mgf_path )
        self.take_care_of_params_and_stats( io_mode = 'tmp')
        history = self.io['tmp']['stats']['history']
        for entry in history:
            if entry['engine'] == self.params['mzml2mgf_converter_version']:
                corresponding_mzml = os.path.join(
                    entry['finfo']['dir'],
                    entry['finfo']['file']
                )
                break
        else:
            raise Exception( error_msg )
        assert os.path.isfile( corresponding_mzml ), error_msg
        return corresponding_mzml

    def set_profile( self, profile, dev_mode = False ):
        '''
        The ucontroller set_profile function

        Note:
            internal function

        Arguments:
            profile (str): Profile speficied to use for all searches.

        Available profiles:

            * 'QExactive+'
            * 'LTQ XL high res'
            * 'LTQ XL low res'


        Sets self.params according to profile name defined
        in ursgal.kb.profiles

        Example::


            >>>'LTQ XL low res' : {
            ...    # MS 1 orbitrap & MSn iontrap
            ...    'frag_mass_tolerance'       : 0.5,
            ...    'frag_mass_tolerance_unit'  : 'da',
            ...    'instrument'                : 'low_res_LTQ',
            ...    'frag_method'               : 'cid'
            ...}


        Own profiles can easily be defined in profiles.py in ursgal/kb
        according to the need parameters or machine specifications.
        '''
        assert profile in self.profiles.keys(), '''
            {0} is not defined in ursgal.profile.PROFILES
            or has not been updated in self.profiles
            '''.format( profile )
        number_of_updated_params = len(
            ursgal.PROFILES[ profile ]
        )
        self.print_info(
            'Initializing profile {0}'.format( profile ),
            caller= 'profile'
        )
        self.print_info(
            '{0} parameter{1} been updated'.format(
                number_of_updated_params,
                's have' if number_of_updated_params > 1 else ' has'
            ),
            caller = 'profile'
        )

        self.init_kwargs['profile'] = profile
        if dev_mode:
            return ursgal.PROFILES[ profile ]
        else:
            self.params.update( ursgal.PROFILES[ profile ])
        return None

    def show_unode_overview( self ):
        '''
        The ucontroller show_unode_overview function

        Note:
            internal function

        Prints the overview of all available nodes. The overview
        includes the category, name and availability of each
        node. Available nodes are highlighted. Here also the correct
        functionality of the engine avaibility and installation is verified.
        '''
        n = 0
        print()
        for meta_type in sorted(self.unodes['__by_meta_type'].keys()):
            if meta_type == 'in_development':
                continue

            number_of_no_dev_nodes = 0
            for engine in sorted(self.unodes['__by_meta_type'][ meta_type ]):
                if self.unodes[ engine ]['in_development'] is False:
                    number_of_no_dev_nodes += 1

            if number_of_no_dev_nodes == 0:
                continue


            print('\t{BOLD}{0}{ENDC}(s):'.format(
                meta_type.upper(),
                **ursgal.COLORS
            ))
            for engine in sorted(self.unodes['__by_meta_type'][ meta_type ]):

                if self.unodes[ engine ]['in_development']:
                    continue

                node_status = self.unodes[ engine ].get(
                    'import_status',
                    'n/a'
                )
                if meta_type.upper() == "CONTROLLER":
                    node_status = 'available'

                if node_status == 'available':
                    color = ursgal.COLORS['GREEN']
                elif node_status == 'n/a':
                    color = ursgal.COLORS['YELLOW']
                else:
                    color = ursgal.COLORS['RED']
                url_available = ''
                if hasattr( self.unodes[ engine ]['class'], 'META_INFO'):
                    local_META_INFO = self.unodes[ engine ]['class'].META_INFO
                    if 'engine_url' in local_META_INFO.keys():
                        if 'internal' in local_META_INFO['engine_url'].keys():
                            url_available = '\t{GREY} internal {ENDC}'.format(
                                **ursgal.COLORS
                            )
                        else:
                            url_available = '\t{YELLOW} url available {ENDC}'.format(
                                **ursgal.COLORS
                            )

                print('\t{0: >3} : {1:28} [{3} {2: ^25} {ENDC}] {4}'.format(
                    n,
                    engine,
                    node_status,
                    color,
                    url_available,
                    **ursgal.COLORS
                ))
                n += 1
        return

    def run_unode_if_required( self, force, engine_name, answer, merge_duplicates=False, history_addon=None ):
        '''
        The ucontroller run_unode_if_required function

        Note:
            internal function

        Executes a UNode if required. Otherwise prints why the run
        was not required. If the UNode is executed, the corresponding
        json is dumped and the history is updated.

        Keyword Arguments:
            force (bool): (re)do the analysis if output files already
                exists
            engine_name (str): name of the engine to be executed (after
                verifying with engine_sanity_check )
            answer (str or None): The answer of prepare_unode_run().
                Can be None if no re-run is required, or a string
                indicating the reason for re-run
        '''
        # get the name of the caller function for printouts (i.e. "search()" )
        current_frame = inspect.currentframe()
        caller_frame  = inspect.getouterframes(current_frame, 2)
        caller_function_name = caller_frame[1][3]

        # dict with some basic info for easy printing:
        print_d = {
            'file' : self.io['input']['finfo']['file'],
            'function' : caller_function_name,
        }

        if answer is None:
            # no need to re-run the node, output was previously generated
            self.print_info(
                ('Skipping {function}() on file {file} since it was '
                 'previously executed with the same input file(s) and '
                 'parameters.').format( **print_d ),
                caller = 'Info'
            )
            self.print_info(
                'To re-run, use {function}( force=True )'.format( **print_d ),
                caller = 'Info'
                )
            report = {
                'output_file' : os.path.join(
                    self.io['output']['finfo']['dir'],
                    self.io['output']['finfo']['file']
                )
            }
            self.update_output_json()
        else:
            # node has to be run because it was never executed before,
            # or because input file or params changed
            self.print_info(
                '{function}() scheduled on input file {file}'.format(**print_d),
                caller = 'Info'
            )
            self.print_info(
                'Reason for run: {0}'.format( answer ),
                caller = 'Info'
            )

            if history_addon is None:
                history_addon = {}

            self.io['output']['stats']['history'] = self.update_history_status(
                status  = 'launching',
                engine  = engine_name,
                history = self.io['output']['stats']['history'],
                history_addon = history_addon,
            )
            json_path = self.dump_json_and_calc_md5()
            report = self.unodes[ engine_name ]['class'].run(
                json_path = json_path,
            )

            if merge_duplicates:
                psm_defining_colnames = self.params['psm_defining_colnames']
                score_colname = self.UNODE_UPARAMS['validation_score_field'][
                        'uvalue_style_translation'].get(engine_name, None)
                if score_colname:
                    psm_defining_colnames.append(score_colname)

                psm_counter = ursgal.ucore.count_distinct_psms(
                    csv_file_path=report['output_file'],
                    psm_defining_colnames=psm_defining_colnames
                )
                if psm_counter != Counter():
                    if max(psm_counter.values()) > 1:
                        out_file = ursgal.ucore.merge_duplicate_psm_rows(
                            csv_file_path=report['output_file'],
                            psm_counter=psm_counter,
                            joinchar=self.params['psm_merge_delimiter'],
                            psm_defining_colnames=psm_defining_colnames,
                            psm_colnames_to_merge_multiple_values=self.params['psm_colnames_to_merge_multiple_values']
                        )
                        self.print_info(
                            'Result file path: {0}'.format(out_file),
                            caller = 'Info'
                        )

            self.dump_json_and_calc_md5(
                stats = report['stats'],
                params = report['params']
            )

        self.verify_engine_produced_an_output_file(
            report['output_file'],
            engine_name
        )

        return report

    def verify_engine_produced_an_output_file(self, expected_fpath, engine_name):
        '''
        Since not all engines raise an exception when they fail, we
        check if the output file was successfully produced or not
        to throw a proper exception in case the engine crashed.
        '''
        try:
            self.input_file_sanity_check(
                expected_fpath,
                custom_str='Output file generated by {0}'.format(engine_name)
            )
        except AssertionError as ass:
            error_msg = '''
     \n{0} (most likely) crashed!

      The uNode {0} did not produce a valid output file at the expected location:
        {1}
      Inspect the printouts above for possible causes and verify that all input files are valid.
            '''.format( engine_name, expected_fpath )
            raise Exception( error_msg ) from ass
        return


    def unify_csv(self, input_file, force=False, output_file_name=None):
        '''
        [ WARNING ] This function is not supported anymore!
                    Please use :meth:`.execute_misc_engine` instead

        The ucontroller unify_csv function

        Unifies the .csv files which were converted by the mzidentml library.
        The corrections for each engine are listed in the node under
        ursgal/resources/arc_independent/unify_csv_1_0_0

        Keyword Arguments:
            input_file (str): The complete path to the input, input file has
                currently to be a .csv file.
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::

            >>> uc=ursgal.UController(
            ...     profile = 'LTQ XL low res',
            ...     params  = {'database': 'BSA.fasta'}
            ... )
            >>> xtandem_result_xml = uc.search_mgf(
            ...     input_file = 'BSA.mzML',
            ...     engine     = 'xtandem',
            ... )
            >>> xtandem_result_csv = uc.convert_results_to_csv(
            ...     input_file = xtandem_result_xml
            ... )
            >>> unified_csv = uc.unify_csv(
            ...     input_file = xtandem_result_csv
            ... )

        Returns:
            str: Path of the output file
        '''

        # self.input_file_sanity_check( input_file, engine=engine_name, extensions=['.csv'] )

        self.print_old_function_warning(
            'unify_csv',
            'execute_misc_engine'
        )

        return self.execute_unode(
            input_file       = input_file,
            engine           = self.params['unify_csv_converter_version'],
            force            = force,
            output_file_name = output_file_name
        )

    def map_peptides_to_fasta(self, input_file, force=False, output_file_name=None):
        '''
        [ WARNING ] This function is not supported anymore!
                    Please use :meth:`.execute_misc_engine` instead

        The ucontroller function to call the upeptide_mapper node.

        Note:
            Different converter versions can be used (see parameter
            'peptide_mapper_converter_version') as well as different classes
            inside the converter node (see parameter
            'peptide_mapper_class_version' )

        Available converter nodes
            * upeptide_mapper_1_0_0

        Available converter classes of upeptide_mapper_1_0_0
            * UPeptideMapper_v3 (default)
            * UPeptideMapper_v4 (no buffering and enhanced speed to v3)
            * UPeptideMapper_v2

        Keyword Arguments:
            input_file (str): The complete path to the input, input file has
                currently to be a .csv file.
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Returns:
            str: Path of the output file
        '''
        self.print_old_function_warning(
            'map_peptides_to_fasta',
            'execute_misc_engine'
        )

        return self.execute_unode(
            input_file       = input_file,
            engine           = self.params['peptide_mapper_converter_version'],
            force            = force,
            output_file_name = output_file_name
        )

    def filter_csv(self, input_file, force=False, output_file_name=None):
        '''
        [ WARNING ] This function is not supported anymore!
                    Please use :meth:`.execute_misc_engine` instead

        The UController filter_csv function

        Filters .csv files row-wise according to user-defined rules.

        Keyword Arguments:
            input_file (str): The complete path to the input, input file has
                currently to be a .csv file.
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        The filter rules have to be defined in the params. See the engine
        documentation for further information ( :meth:`.filter_csv_1_0_0._execute` ).

        Example:

            >>> # Only columns with these attributes will be retained:
            >>> # a) 'PEP' column value must be lower than or equal to 0.01
            >>> # b) 'Is decoy' column value must equal 'false'
            >>> uc.params['csv_filter_rules'] = [
            ...     ['PEP',      'lte',    0.01   ],
            ...     ['Is decoy', 'equals', 'false']
            ... ]
            >>> uc.filter_csv( 'my_results.csv' )
        '''
        self.print_old_function_warning(
            'filter_csv',
            'execute_misc_engine'
        )
        return self.execute_unode(
            input_file       = input_file,
            engine           = 'filter_csv_1_0_0',
            force            = force,
            output_file_name = output_file_name
        )

    def print_old_function_warning(self, old_funct_name, new_func_name):
        '''
        '''
        print('''
        [ WARNING ] You are using an old UController function:
                    {0}
        [ WARNING ] This funtion is not supported/updated anymore!
        [ WARNING ] Please use the following instead:
                    {1}
        '''.format(
                old_funct_name,
                new_func_name
            )
        )
        return

    def prepare_resources(self, root_zip_target_folder):
        '''

        '''

        zip_file_list = []
        update_kb_list = []
        root_resource_folder = os.path.join(
            ursgal.base_dir,
            'resources',
        )

        missing_md5_format_string = '''
        Please include the following in the knowledge base in META_INFO of {0}:
        'engine' : {{
            '{1}' : {{
                '{2}' : {{
                    'zip_md5' : '{3}'
                }}
            }}
        }}
                '''

        for root_dir, folder_list, file_list in os.walk(root_resource_folder):
            engine = os.path.split(root_dir)[-1]
            if engine in self.unodes.keys():
                # we do not include binaries in the repository
                include_in_git = self.unodes[ engine ].get(
                    'include_in_git',
                    None
                )
                if include_in_git in [ None, True ]:
                    continue
                # or we cannot dictribute it, restrictive licenses etc.
                distributable = self.unodes[ engine ].get(
                    'distributable',
                    True
                )
                if distributable is False:
                    continue

                resource_source_folder = 'ursgal{0}'.format(
                    root_dir.split('ursgal')[-1]
                )

                target_folder_for_zips = os.path.join(
                    root_zip_target_folder,
                    resource_source_folder
                )

                splitted_root_dir = resource_source_folder.split( os.sep )

                current_platform     = splitted_root_dir[ -3 ]
                current_architecture = splitted_root_dir[ -2 ]

                zip_file_name_for_shutil = os.path.join(
                    target_folder_for_zips,
                    '{0}'.format(engine)
                )
                zip_file_name = '{0}.zip'.format(
                    zip_file_name_for_shutil
                )

                md5_file_name = os.path.join(
                    target_folder_for_zips,
                    '{0}.md'.format(engine)
                )
                kb_engine_dict = self.unodes[ engine ].get(
                    'engine',
                    None
                )
                if kb_engine_dict is None:
                    print(
                        'No "engine" entry in kb for engine {0}, Please contact the Ursgal team'.format(
                            engine
                        )
                    )
                    continue
                try:
                    md5_in_kb  = kb_engine_dict[ current_platform ][ current_architecture ]['zip_md5']
                    kb_has_md5 = True
                except:
                    md5_in_kb  = None
                    kb_has_md5 = False
                    # continue

                # md5_in_kb_dict = self.unodes[engine].get(
                #     'zip_md5',
                #     None
                # )
                # kb_has_md5 = False
                # md5_in_kb = None
                # if md5_in_kb_dict is not None:
                #     if current_platform in md5_in_kb_dict.keys():
                #         if current_platform =='arc_independet':
                #             kb_has_md5 = True
                #             md5_in_kb = md5_in_kb_dict[current_platform]
                #         elif current_architecture in md5_in_kb_dict[current_platform].keys():
                #             kb_has_md5 = True
                #             md5_in_kb = md5_in_kb_dict[current_platform][current_architecture]
                #         else:
                #             pass
                #     else:
                #         pass
                        # zip, calc md5 and report md5

                online_folder_has_md5 = False
                online_md_5           = None
                if kb_has_md5:
                    # check online if md5 dile is present!
                    http_get_params = {
                        'http_url': os.path.join(
                            self.params['ursgal_resource_url'],
                            resource_source_folder,
                            '{0}.md'.format(engine)
                        ).replace('\\','/'),
                        'http_output_folder' : root_zip_target_folder,
                    }
                    get_http_main = self.unodes['get_http_files_1_0_0']['class'].import_engine_as_python_function()

                    download_md_5_name =  os.path.join(
                        http_get_params['http_output_folder'],
                        '{0}.md'.format(
                                engine
                            )
                    )
                    get_http_main( **http_get_params )
                    if os.path.exists( download_md_5_name ):
                        online_folder_has_md5 = True
                        online_md_5 = open(
                           download_md_5_name,
                            'r'
                        ).readline().strip()
                        print('Remove tmp file: {0}'.format(download_md_5_name))
                        os.remove( download_md_5_name )
                    else:
                        print(
                            'File {0} is not present in online resource folder'.format(
                                http_get_params['http_url']
                            )
                        )
                        pass

                    if online_folder_has_md5:

                        if online_md_5 == md5_in_kb:
                            print(
                                '''
        md5 in knowledge base is equal to the md5 online for {engine} on platform {current_platform} and architecture {current_architecture}:
        md5 online:             {online_md_5}
        md5 in knowledge base : {md5_in_kb}
        Nothing to do here...
                                '''.format(
                                    online_md_5          = online_md_5,
                                    md5_in_kb            = md5_in_kb,
                                    current_platform     = current_platform,
                                    current_architecture = current_architecture,
                                    engine               = engine
                                )
                            )
                            continue
                    else:
                        # build also zip, but keep the stuff and write md5 check fil for online repo
                        if os.path.exists(target_folder_for_zips) is False:
                            os.makedirs(target_folder_for_zips)
                        shutil.make_archive(
                            zip_file_name_for_shutil,
                            'zip',
                            resource_source_folder
                        )
                        calculated_zip_md5 = self.calc_md5( zip_file_name )
                        if calculated_zip_md5 == md5_in_kb:
                            print(
                                'Correct zip file {0} with md5: {1} is present and can be uploaded now!'.format(
                                    zip_file_name,
                                    calculated_zip_md5
                                )
                            )
                            with open(md5_file_name,'w') as io:
                                print( calculated_zip_md5, file=io)

                            zip_file_list.append(
                                ( zip_file_name, calculated_zip_md5 )
                            )

                        else:
                            print(
                                'md5 in kb found for {0} on platform {1} and architecture {2} differs from your zip file.'.format(
                                    engine,
                                    current_platform,
                                    current_architecture
                                ),
                                'zip file location: {0}'.format(target_folder_for_zips)
                            )
                            os.remove(zip_file_name)
                            message = missing_md5_format_string.format(
                                engine,
                                current_platform,
                                current_architecture,
                                calculated_zip_md5
                            )
                            print( message )
                            update_kb_list.append((engine,message))
                            print('created zip file has been removed, include correct md5 in META_IFO first')
                else:
                    print(
                        'No md5 in kb found for {0} on platform {1} and architecture {2}'.format(
                            engine,
                            current_platform,
                            current_architecture
                        )
                    )
                    if os.path.exists(target_folder_for_zips) is False:
                        os.makedirs(target_folder_for_zips)
                    shutil.make_archive(
                        zip_file_name_for_shutil,
                        'zip',
                        resource_source_folder
                    )
                    calculated_zip_md5 = self.calc_md5( zip_file_name )
                    os.remove(zip_file_name)
                    message = missing_md5_format_string.format(
                        engine,
                        current_platform,
                        current_architecture,
                        calculated_zip_md5
                    )
                    print( message )
                    update_kb_list.append((engine,message))
        return zip_file_list, update_kb_list

    def download_resources(self, resources=None):
        '''
        Function to download all executable from the specified http url

        Keyword Arguments:
            resources (list): list of specific resources that should be
                downloaded. If left to None, all possible resources are
                downloaded.
        '''
        download_zip_files = []
        get_http_main = self.unodes['get_http_files_1_0_0']['class'].import_engine_as_python_function()
        base_http_get_params = {
            'http_url_root': self.params['ursgal_resource_url'],
        }
        if resources is None:
            resources = self.unodes.keys()
        for engine in resources:
            if 'resource_folder' in self.unodes[engine].keys():
                if self.unodes[engine]['available'] is False:
                    include_in_git = self.unodes[engine].get('include_in_git')
                    in_development = self.unodes[engine].get('in_development', False)
                    if include_in_git is True or in_development is True:
                        continue
                    print(
                        'Executable for {0} is not available on your system'.format(
                            engine
                        )
                    )
                    distributable = self.unodes[engine]['META_INFO'].get(
                        'distributable',
                        True
                    )
                    if distributable is False:
                        print(
                            'Engine {0} cannot be downloaded automatically, please download the engine manually and move it to the appropriate folder'.format(
                                engine,
                            )
                        )
                        continue
                    # check for md5 in kb:
                    kb_engine_dict = self.unodes[ engine ].get(
                        'engine',
                        None
                    )
                    if kb_engine_dict is None:
                        print(
                            'No "engine" entry in kb for engine {0}, Please contact the Ursgal team'.format(
                                engine
                            )
                        )
                        continue

                    if 'platform_independent' in kb_engine_dict.keys():
                        current_platform = 'platform_independent'
                    else:
                        current_platform = self.platform

                    if 'arc_independent' in kb_engine_dict[ current_platform ].keys():
                        current_architecture = 'arc_independent'
                    else:
                        current_architecture = self.architecture[0]

                    try:
                        md5_in_kb = kb_engine_dict[ current_platform ][ current_architecture ]['zip_md5']
                    except:
                        print(
                            'No md5 entry for {engine} on {platform}/{architecture}'.format(
                                engine       = engine,
                                platform     = current_platform,
                                architecture = current_architecture
                            )
                        )
                        continue
                    if md5_in_kb is None:
                        print(
                            'No md5 entry in kb for engine {0}, Please contact the Ursgal team'.format(
                                engine
                            )
                        )
                        continue

                    source_folder = 'ursgal{0}'.format(
                        self.unodes[engine]['resource_folder'].split('ursgal')[-1]
                    )

                    #check if resource folder is present
                    if os.path.exists( self.unodes[engine]['resource_folder'] ) is False:
                        os.makedirs( self.unodes[engine]['resource_folder'] )

                    # now check online md presence!
                    tmp_http_get_params = {}
                    tmp_http_get_params['http_url'] = os.path.join(
                        base_http_get_params['http_url_root'],
                        source_folder,
                        # engine,
                        '{0}.md'.format(
                            engine
                        )
                    ).replace('\\','/')
                    tmp_http_get_params[ 'http_output_folder'] = os.path.join(
                        self.unodes[engine]['resource_folder'],
                        # engine
                    )
                    download_md_5_name = os.path.join(
                        tmp_http_get_params[ 'http_output_folder'],
                        '{0}.md'.format(
                            engine
                        )
                    ).replace('\\','/')
                    try:
                        get_http_main( **tmp_http_get_params )
                    except:
                        print(
                            '''
        File {0} is not present in online resource folder.
        Please install the engine manually!
                            '''.format(
                                tmp_http_get_params['http_url']
                            )
                        )
                        continue

                    online_md_5 = open(
                       download_md_5_name,
                        'r'
                    ).readline().strip()
                    print('Remove tmp file: {0}'.format(download_md_5_name))
                    os.remove( download_md_5_name )

                    if md5_in_kb == online_md_5:
                        # download zip
                        zip_file_name = os.path.join(
                            source_folder,
                            # engine,
                            '{0}.zip'.format(engine)
                        )
                        tmp_http_get_params['http_url'] =  os.path.join(
                            self.params['ursgal_resource_url'],
                            zip_file_name
                        ).replace('\\','/')
                        print(
                            'MD5 check successful! The executables will be downloaded from {0}'.format(
                                tmp_http_get_params['http_url']
                                )
                        )
                        try:
                            get_http_main( **tmp_http_get_params )
                        except:
                            print(
                            '''
        File {0} is not present in online resource folder.
        [  INFO   ] Please contact the Ursgal team!
                            '''.format(
                                tmp_http_get_params['http_url']
                            )
                        )
                        # check md5 of zip!!!
                        calculated_zip_md5 = self.calc_md5( zip_file_name )
                        if calculated_zip_md5 != md5_in_kb:
                            print(
                                '''
        [ WARNING ] md5 of downloaded zip file {0} differs from
        [ WARNING ] md5 in knowledge base, exiting now!!!
        [  INFO   ] Please contact the Ursgal team!
                                '''.format(zip_file_name)
                            )
                            os.remove( zip_file_name )
                            continue

                        download_zip_files.append(
                            (
                                engine,
                                zip_file_name
                            )
                        )
                        executables_list = [
                            self.unodes[engine]['engine'][ current_platform ][current_architecture]['exe']
                        ]
                        executables_list += self.unodes[engine]['engine'][ current_platform ][current_architecture].get(
                            'additional_exe',
                            []
                        )
                        with zipfile.ZipFile(zip_file_name, 'r') as io:
                            for name in io.namelist():
                                io.extract(
                                    member = name,
                                    path   = tmp_http_get_params['http_output_folder']
                                )
                                target_file  = os.path.join(
                                    tmp_http_get_params['http_output_folder'],
                                    name
                                )
                                # change engine executable to executable by user
                                # and group
                                if name in executables_list:
                                    current_stat = os.stat(target_file).st_mode
                                    os.chmod(
                                        target_file,
                                        current_stat | stat.S_IXUSR | stat.S_IXGRP
                                    )
                        print('Remove tmp file: {0}'.format(zip_file_name))
                        os.remove( zip_file_name )
                    else:
                        print(
                            '''
        [ WARNING ] md5 of online repository for engine {0} differs from
        [ WARNING ] md5 in knowledge base, exiting now!!!
        [  INFO   ] Please contact the Ursgal team!
                            '''.format(engine)
                        )

                        continue

        return download_zip_files

    def execute_unode(self, input_file, engine=None, force=False, output_file_name=None, dry_run=False, merge_duplicates=False):
        '''
        The UController execute_unode function. Executes arbitrary UNodes, as
        specified by their name.

        Keyword Arguments:
            input_file (str or list of str): The complete path to the input,
                or a list of paths to the input files.
            engine (str): Engine name one wants to execute
            force (bool): (Re)do the analysis if output files already exists
            dry_run (bool): Do not execute; only return the output file name

        Note:
            Can also execute UNodes that are tagged as 'in development' in kb
            (=not shown in UController overview) if their name is specified.
        '''

        if input_file is None:
            tmp_file_name = tempfile.NamedTemporaryFile(prefix='Ursgal_', suffix='.txt').name
            with open (tmp_file_name, 'w') as tmp_io:
                print(
                    '''
>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
>>> love = this
>>> this is love
True
>>> love is True
False
>>> love is False
False
>>> love is not True or False
True
>>> love is love
True
>>>
                ''',
                    file = tmp_io
                )
            tmp_io.close()
                      # pass
            input_file = tmp_file_name
        engine_name = self.engine_sanity_check( engine )
        multi, input_file = self.distinguish_multi_and_single_input( input_file )
        self.input_file_sanity_check( input_file, engine=engine_name, multi=multi )

        answer = self.prepare_unode_run(
            input_file,
            output_file = output_file_name,
            engine = engine_name,
            force  = force
        )
        if dry_run is True:
            answer = None  # do not execute, even if params changed!
        report = self.run_unode_if_required(
            force, engine_name, answer,
            merge_duplicates=merge_duplicates
        )
        return report['output_file']

    def distinguish_multi_and_single_input(self, in_input):
        '''
        Finds out whether the input is a single file or a list of
        files and returns a bool indicating so, as well as the
        input file(s)
        '''
        multi = True
        if isinstance(in_input, str):
            # input is a single file
            multi = False
            out_input = in_input
        elif isinstance(in_input, list):
            if len(in_input) == 1:
                # input is a single file too (but inside a list...)
                multi = False
                out_input = in_input[0]
            else:
                # input is a list of multiple files
                multi = True
                out_input = in_input
        else:
            # this should never be the case, but input_file_sanity_check()
            # will throw a proper exception
            out_input = in_input
        return multi, out_input


    def validate(self, input_file, engine=None, force=None, output_file_name=None ):
        '''
        The UController validate function

        Does statistical post-processing of unified search result .csv files
        with the specified validation engine.

        Depending on the validation method a posterior error probability (PEP)
        and/or a q-value will be available in the final results.

        Keyword Arguments:
            input_file (str): The complete path to the input, a unified
                (and possibly merged) search result .csv.
            engine (str): the name of the validation engine which should be
                run, can also be a short version if this name is unambigous
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Note:
            Input files to :meth:`.validate` must be in unified csv format (i.e.
            output files of :meth:`.search` or :meth:`.unify_csv`).

        Example::

            >>> uc = ursgal.UController(
            ...    profile = 'LTQ XL low res',
            ...    params  = {'database': 'BSA.fasta'}
            ... )
            >>> xtandem_result_csv = uc.search(
            ...    input_file = 'BSA.mzML',
            ...    engine     = 'xtandem_piledriver'
            ... )
            >>> validated_csv = uc.validate(
            ...    input_file = xtandem_result_csv,
            ...    engine     = 'percolator_2_08'
            ... )

        Returns:
            str: Path of the output file
        '''

        return self.execute_unode(
            input_file       = input_file,
            engine           = engine,
            force            = force,
            output_file_name = output_file_name
        )


    def visualize(self, input_files, engine=None, force=None, output_file_name=None, multi=True):
        '''
        The ucontroller function for visualization

        Does graphical visualization of result .csv files.

        Keyword Arguments:
            input_files (list): list with complete paths of .csv files
            engine (str): the name of the visualizer which should be run,
                 can also be a short version if this name is unambigous
            force (bool): (Re)do the analysis, even if output file
                already exists.
            output_file_name (str or None): Desired output file name
                excluding path (optional). If None, output file name will
                be auto-generated.

        Example::

            >>> uc = ursgal.UController( profile='LTQ XL high res' )
            >>> xtandem_result_csv = uc.search(
            ...     input_file = 'BSA.mzML',
            ...     engine     = 'xtandem_piledriver',
            ... )
            >>> omssa_result_csv = uc.search(
            ...     input_file = 'BSA.mzML',
            ...     engine     = 'omssa',
            ... )
            >>> uc.visualize(
            ...     input_files = [xtandem_result_csv, omssa_result_csv],
            ...     engine      = 'venndiagram',
            ... )

        Note:
            For detailed information about the VennDiagram UNode, see
            :meth:`.venndiagram_1_0_0._execute`.

        Returns:
            str: Path of the output file
        '''
        return self.execute_unode(
            input_file       = input_files,
            engine           = engine,
            force            = force,
            output_file_name = output_file_name
        )


    def input_file_sanity_check(self, input_file, engine=None, extensions=None, multi=False, custom_str=None ):
        '''
        The ucontroller input_file_sanity_check function

        Asserts that input files exist, can be read, have the right file type
        and file extension etc. Raises an AssertionError if any criterion is
        violated.

        Keyword Arguments:
            input_file (str or list): input file path to be checked, or a list
                 of input file paths in the case of multi-nodes
            engine (str): the name of the engine, file extension requirements
                 will be looked up in engine/kb (optional)
            extensions (list): a list of permitted file extensions (optional)
            multi (bool): whether the UNode accepts multiple input files or not

        Note:
            Internal Function

        Returns:
            None
        '''

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller_function_name = calframe[1][3]

        if custom_str is None:
            custom_str = \
                'Input to {0}()'.format(caller_function_name)
        else:
            custom_str = \
                'Error in {0}() - '.format(caller_function_name) + custom_str

        # a dictionary for easy string formatting in error messages:
        d = {
            "input_file" : input_file,
            "engine"     : engine,
            "custom_str" : custom_str,
        }

        if multi:
            # verify that input to multi-nodes is a list of 2 or more elements:
            assert isinstance( input_file, list ) and len( input_file ) >= 2, '''
          {custom_str} must be a list of at least two files,
          but you specified:
        \t{input_file}'''.format( **d )

            # verify that input list to multi-nodes only contains strings:
            for f in input_file:
                assert isinstance(f, str), '''
          {custom_str} must contain only strings (file paths),
          but you specified this element:
        \t{f}'''.format( f=f, **d )

            input_file_list = input_file  # it's a list, so we can treat it like that.

        elif not multi:
            # verify that input to single-nodes is a str:
            assert isinstance( input_file, str ), '''
          {custom_str} must be a string (the path to a file),
          but you specified:
        \t{input_file}'''.format( **d )
            input_file_list = [input_file]  # put it into a list, so we can treat both str and list inputs the same (loop over them)

        for in_file in input_file_list:
            d['in_file'] = in_file

            # verify that input file exists:
            assert os.path.isfile( in_file ), '''
          {custom_str} is not a file. Make sure that the file exists, and that
          you typed the path correctly. You specified this path:
        \t{in_file}'''.format( **d )

            # verify that input file is not empty:
            assert os.stat( in_file ).st_size > 0, '''
          {custom_str} is empty. You specified this file:
        \t{in_file}'''.format( **d )

            # verify that current user has file reading permissions:
            assert os.access( in_file, os.R_OK ), '''
          {custom_str} cannot be read. Make sure you have file reading permissions
          on your current user. You specified this file:
        \t{in_file}'''.format( **d )

            # verify that the file ends with one of the extensions specified in UNode.kb, or user-specified:
            all_extensions = set()
            if engine is not None:
                engine_extensions = self.unodes[ engine ]['class'].META_INFO['input_extensions']
                for ext in engine_extensions:
                    all_extensions.add( ext.upper() )
            if extensions is not None:
                for ext in extensions:
                    all_extensions.add( ext.upper() )

            if len(all_extensions) > 0:
                ext_is_allowed = False
                d['ok_extensions'] = " or ".join( all_extensions )
                for ext in all_extensions:
                    if in_file.upper().endswith( ext ):
                        ext_is_allowed = True
                assert ext_is_allowed, '''
          {custom_str} does not have the correct file extension.
          You specified the file
        \t{in_file}
          but only files ending with {ok_extensions} are permitted for engine {0}.
          '''.format(engine, **d )


class ParamsDict(dict):
    '''
    A dict that only accepts known keys, i.e. keys that are listed in uparams.py
    '''
    allowed_params = set(ursgal.uparams.ursgal_params.keys()) | \
        {'mods', 'translations', 'TEST_PARAMS', 'TEST_PARAMS_2nd'}

    def __setitem__(self, key, value):
        if key not in ParamsDict.allowed_params:
            raise ValueError('Unknown UController parameter: "{}". '
                'Please check your spelling, and check '
                'http://ursgal.readthedocs.io/en/latest/parameter.html '
                'for a list of available parameters.'.format(key))
        super().__setitem__(key, value)

    def update(self, dict_to_add):
        params_to_add = set(dict_to_add.keys())
        unknown_params = params_to_add - ParamsDict.allowed_params
        if unknown_params:
            up_str = sorted(['"{}"'.format(s) for s in unknown_params])
            raise ValueError('Unknown UController parameter(s): {}. '
                'Please check your spelling, and check '
                'http://ursgal.readthedocs.io/en/latest/parameter.html '
                'for a list of available parameters.'.format(', '.join(up_str)))
        super().update(dict_to_add)
