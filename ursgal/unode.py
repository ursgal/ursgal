#!/usr/bin/python
import json
import os
import ursgal
import importlib
import time
from collections import defaultdict as ddict
import csv
import operator
import sys
import hashlib
from functools import partial
import subprocess
import re
import pprint
import gzip
import copy
from ursgal import ukb


class Meta_UNode(type):
    """Metaclass for our UNode

    additional attributes
    .exe
    .translations
    .default_params
    are read and set.
    """
    XX_meta_collected_nodes = {}

    _collected_initialized_unodes = {}

    _uparam_mapper = ursgal.UParamMapper()
    # _upeptide_mapper = ursgal.UPeptideMapper()

    def __new__(cls, cls_name, cls_bases, cls_dict ):
        new_class = super(
            Meta_UNode,
            cls
        ).__new__(
            cls,
            cls_name,
            cls_bases,
            cls_dict
        )
        return new_class

    def __init__( cls, cls_name, cls_bases, cls_dict ):
        super(Meta_UNode, cls).__init__( cls_name, cls_bases, cls_dict )

    def __call__(cls, *args, **kwargs):
        initd_klass = super(Meta_UNode, cls).__call__( cls, *args, **kwargs )

        engine_path = kwargs.get('engine_path', None)
        if engine_path is None:
            # This happens only when we call our Controller
            engine = 'ucontroller'
            kwargs['engine_path'] = __file__
        else:
            all_parts = os.path.abspath( kwargs['engine_path'] ).split(os.sep)
            engine = all_parts[ -2 ]

        initd_klass.DEFAULT_PARAMS = {}
        initd_klass.UNODE_UPARAMS = {}
        initd_klass.UNODE_UPARAMS_GROUPED_BY_TAG = ddict(list)
        # initd_klass.TRANSLATIONS_GROUPED_BY_TRANSLATED_KEY = {}
        initd_klass.PARAMS_TRIGGERING_RERUN = set()
        for mDict in Meta_UNode._uparam_mapper.mapping_dicts( engine ):
            for tag in mDict['utag']:
                initd_klass.UNODE_UPARAMS_GROUPED_BY_TAG[ tag ].append(
                    mDict['ukey']
                )

            initd_klass.DEFAULT_PARAMS[ mDict['ukey'] ] = \
                mDict['default_value_translated']

            initd_klass.UNODE_UPARAMS[ mDict['ukey'] ] = mDict

            if mDict['triggers_rerun']:
                initd_klass.PARAMS_TRIGGERING_RERUN.add( mDict['ukey'] )

        translation_style = initd_klass.META_INFO.get(
            'utranslation_style',
            None
        )
        if translation_style is not None:
            Meta_UNode._uparam_mapper.lookup[ 'style_2_engine' ][ translation_style ].add(
                engine
            )

        alternative_exe_folder = initd_klass.META_INFO.get(
            'uses_unode',
            None
        )
        if alternative_exe_folder is not None:
            kwargs['engine_path'] = kwargs['engine_path'].replace(
                engine,
                alternative_exe_folder
            )
        initd_klass.exe = kwargs['engine_path']

        obligatory_methods = [
            'preflight',
            'postflight',
        ]

        for method in obligatory_methods:
            engine_method  = getattr( initd_klass, method, None)
            assert callable(engine_method), '''
            {0} class requires {1} method to be defined
            '''.format( engine, method )
        initd_klass.engine = engine

        Meta_UNode._collected_initialized_unodes[ engine ] = initd_klass
        initd_klass.meta_unodes = Meta_UNode._collected_initialized_unodes
        initd_klass.uparam_mapper = Meta_UNode._uparam_mapper
        # initd_klass.upeptide_mapper = Meta_UNode._upeptide_mapper

        if hasattr( initd_klass, '_run_after_meta_init'):
            initd_klass._after_init_meta_callback( *args, **kwargs )

        return initd_klass


class UNode(object, metaclass=Meta_UNode):
    '''
    ursgal class
    '''
    def __init__(self, *args, **kwargs):
        # assert 'engine_path' in kwargs.keys(), \
        #     'Require engine_path as key/value input'
        # # try:
        #     self.exe   = kwargs['engine_path']
        # except:
        #     print(kwargs)
        #     print(self.engine)
        #     exit(1)
        self.params = {
            # 'executable_path' : self.exe,
            'file_info': {}
        }

        self.stats               = self._regenerate_default_stats()
        # This can be updated during __init__
        self.created_tmp_files   = []
        self.lookups             = {}
        self.user_defined_params = {}
        self.force               = False
        self.preflight_answer    = None
        self.execute_answer      = None
        self.postflight_answer   = None
        self.dependencies_ok     = True
        #self.loaded_json = False  # not used?

    def _regenerate_default_stats( self ):
        stats = {
            'time_points'    : {},
            'processed_files': {},
            'history'        : [],
            'startup'        : [],
            'status'         : 'idle'
        }
        return stats

    def abs_paths_for_specific_keys( self, params, param_keys = None):
        '''
        Absolute paths for specific keys from the params dict are determined

        Returns:
            dict: params with paths in abspath version
        '''
        if param_keys is None:
            if 'database' in params:
                param_keys = ['database']
            else:
                return params
        for san_key in param_keys:
            params[ san_key ] = os.path.abspath( params[ san_key ])
        return params

    def calc_md5( self, input_file):
        '''
        Calculated MD5 for input_file

        Args:

            input_file (str): Path to file

        Returns:

            str: MD5 of input file


        Thanks Raymond :)
        http://stackoverflow.com/questions/7829499/using-hashlib-to-compute-md5-digest-of-a-file-in-python-3
        '''
        self.print_info(
            'Calculating md5 for {0} ....'.format(
                os.path.basename(input_file),
                # tag = 'md5'
            ),
            caller='md5'
        )
        with open(input_file, mode='rb') as f:
            d = hashlib.md5()
            for buf in iter(partial(f.read, 1024), b''):
                d.update(buf)
        return d.hexdigest()

    # def check_if_all_default_params_are_in_params(self):
    #     for default_param_key, default_param_value in self.DEFAULT_PARAMS.items():
    #         if default_param_key not in self.params.keys():
    #             self.params[ default_param_key ] = default_param_value
    #     return

    def determine_common_top_level_folder( self, input_files=None ):
        '''
        The unode function determines for a list of input
        files a common top level folder they all belong to

        Keyword Arguments:
            input_files (list): list with input files

        Returns:
            str: The common top level folder
        '''
        paths = []
        for input_file in input_files:
            filepath, file_name = os.path.split(
                input_file
            )
            #print( filepath , input_file , os.path.abspath(filepath))
            splitted_path = filepath.split(
                os.sep
            )
            paths.append( ( len(splitted_path), splitted_path ) )
        paths.sort( reverse=True )
        common_top_level_folder = [
            os.path.abspath(os.sep)
        ]
        for pos in range( paths[0][0] ):
            folder_set = set()
            for number_of_path_elements, path in paths:
                if number_of_path_elements <= pos:
                    folder_set.add( None )
                else:
                    folder_set.add( path[ pos ] )
            if len( folder_set ) != 1:
                break
            else:
                common_top_level_folder.append( path[ pos ] )
        common_top_level_folder.append( '' )
        return os.path.join( *common_top_level_folder )


    def determine_common_name( self, input_files, mode=None):
        '''
        The unode function determines for a list of input
        files a basic common name

        Keyword Arguments:
            mode: head or tail for first or last part of the filename, respectively

        Arguments:
            input_files (list): list with input file names

        Returns:
            str: common file name
        '''
        if mode is None:
            mode = 'head'
        assert mode in ['head', 'tail'], '''
        Can only determine common part of a name from head or tail ...
        '''
        names = []
        for input_file in input_files:
            inf_basename = os.path.basename( input_file )
            if mode == 'head':
                inf_basename = inf_basename
            else:
                inf_basename = inf_basename[::-1]

            names.append( ( len(inf_basename), inf_basename ) )
        names.sort( reverse=True )
        longest_name_length = names[0][0]
        common_name = ''
        for pos in range( longest_name_length ):
            char_set = set()
            for name_length, name in names:
                if name_length <= pos:
                    char_set.add( None )
                else:
                    char_set.add( name[ pos ] )
            if len( char_set ) != 1:
                # print('Breaking ...')
                break
            else:
                common_name += char_set.pop()
            # print( pos , name[ pos ], len(common_name), len(char_set), common_name )
        return common_name

    def determine_common_head_tail_part_of_names( self, input_files=None):
        common_head = self.determine_common_name(
            input_files,
            mode='head'
        )
        common_tail = self.determine_common_name(
            input_files,
            mode='tail'
        )
        return common_head, common_tail[::-1]

    def update_output_json(self):
        '''
        Updates self.io['output']['params'] with self.io['input']['params']

        Although re-run might not be triggered, we need to update
        the output_json.
        '''
        number_of_params_changed = 0
        for i_param, i_value in self.io['input']['params'].items():
            if i_param not in self.io['output']['params'] or \
                    self.io['output']['params'][ i_param ] != i_value:
                number_of_params_changed += 1
                self.io['output']['params'][ i_param ] = i_value

        self.io['output']['finfo']['md5'] = self.io['output']['o_finfo']['md5']
        # self.io['output']['stats'] = self.io['output']['o_finfo']['stats']
        # print('{0} params changed'.format( number_of_params_changed ))
        # print('''

        #     Input

        # ''')
        # pprint.pprint( self.io['input'] )
        # print('''

        #     Output

        # ''')
        # pprint.pprint( self.io['output'] )
        # input('>>>>> Read you jsons! <<<<<<')
        self.dump_json_and_calc_md5( calc_md5 = False)
        return

    def dump_json_and_calc_md5(self, stats=None, params=None, calc_md5=True ):
        '''
        Dumps json with params and stats and calcs md5 for output

        Deletes all entries that are defined in
        params['del_from_params_before_json_dump']
        or keys that start with '_'
        '''
        self.print_info(
            'Preparing json dump',
            caller = 'dmpjson'
        )
        if stats is None:
            stats = self.io['output']['stats'].copy()
        if params is None:
            params = self.io['output']['params'].copy()
        json_file = os.path.join(
            self.io['output']['finfo']['dir'],
            self.io['output']['finfo']['json']
        )
        output_file = os.path.join(
            self.io['output']['finfo']['dir'],
            self.io['output']['finfo']['file']
        )
        # pprint.pprint( self.io['output'])
        # exit(1)
        if os.path.exists( output_file ) and calc_md5:
            self.io['output']['finfo']['md5'] = self.calc_md5(
                output_file
            )
            # print('''

            #     md5:{0}

            #     '''.format( self.io['output']['finfo']['md5']  ))
        j_content = [
            self.io['input']['finfo'].copy(),
            self.io['output']['finfo'].copy(),
            params,
            stats,
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

            elif isinstance(j_content[2][ param_key ], dict):
                for sub_param_key in list(j_content[2][ param_key ].keys()):
                    if sub_param_key.startswith('_'):
                        del j_content[2][ param_key ][sub_param_key]

        with open( json_file , 'w') as file_object:
            json.dump(
                j_content,
                file_object,
                sort_keys = True,
                indent = 2
            )
        self.print_info(
            'Json dumped. Path: {0}'.format(
                json_file
            ),
            caller='dmpjson'
        )
        return json_file


    def _execute(self):
        '''
        The _execute unode function

        Executes the unode executable via shell.

        Note: internal function
            Unodes that do not require execution via shell
            redefine the _execute() function in their engine
            class.

        Returns:
            None
        '''
        self.print_info('Executing command list ...', caller='eXecution')
        assert 'command_list' in self.params.keys(), '''
  No command_list was found in self.params. Convention is to define
  the command list during preflight in the uNode Engine class code or,
  alternatively, redefine uNode._execute() in the engine class altogether
        '''
        self.time_point(tag = 'execution')
        execute_answer = []
        proc = None

        if len(self.params['command_list']) != 0:
            mswindows = ( sys.platform == "win32" )
            if mswindows is True:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                proc = subprocess.Popen(
                    self.params['command_list'],
                    stdout = subprocess.PIPE,
                    shell = False,
                    startupinfo=startupinfo,
                )
            else:
                proc = subprocess.Popen(
                    self.params['command_list'],
                    stdout = subprocess.PIPE,
                    # shell = True
                )
        else:
            print('Command list is empty, nothing to do here...')
            print('_execute failed ....', self.params['command_list'])
            execute_answer.append( 'Command list is empty' )
            self.execute_return_code = 500

        if proc is not None:
            for line in proc.stdout:
                line_decoded = line.strip().decode('utf')
                print( line_decoded )
                execute_answer.append( line_decoded )

            # catching the executable's exit code to detect crashes:
            proc.communicate()[0]
            self.execute_return_code = proc.returncode
            assert self.execute_return_code in [0, None], '''
  \n{0} crashed!

  The executable
    {1}
  terminated with Error code {2} .
  Inspect the printouts above for possible causes and verify that all input files are valid.
            '''.format( self.engine, os.path.relpath(self.exe), self.execute_return_code)

        self.print_execution_time(tag='execution')
        return execute_answer


    def generate_fasta_database_lookup( self, database ):
        if database not in self.lookups['fasta_dbs'].keys():
            self.lookups['fasta_dbs'][ database ] = {}
            lookup_hook = self.lookups['fasta_dbs'][ database ]
            self.print_info(
                'Fasta_db {0}'.format( database ),
                caller ='Caching'
            )
            current_id = None
            for line in open( database ):
                if line[:1] == '>':
                    if line.strip() in lookup_hook.keys():
                        print('[ WARNING ] Fasta database contains duplicates !')
                    current_id = line[1:].strip()
                    lookup_hook[ current_id ] = ''
                else:
                    lookup_hook[ current_id ] += line.strip()
            self.print_info(
                'Done!',
                caller ='Caching'
            )

    def flatten_list(self, multi_list=[]):
        '''
        The unode get_last_engine function

        Reduces a multidimensional list of lists to a flat list including all elements
        '''
        if multi_list == []:
            return multi_list
        if isinstance(multi_list[0], list):
            return self.flatten_list(multi_list[0]) + self.flatten_list(multi_list[1:])
        return multi_list[:1] + self.flatten_list(multi_list[1:])

    def get_last_engine(self, history=None, engine_types=None, multiple_engines=False):
        '''
        The unode get_last_engine function

        Note: returns None if the specified engine type was not used yet.

        Keyword Arguments:
            history (list): A list of path unodes, timestamps and parameters
                that were used. This function can be used on the history loaded
                from a file .json, to find out which search engine was used on
                that file.
                If not specified, this information is taken from the unode class
                itself, and not a specific file.
            engine_types (list): the engine type(s) for which the last used engine
                should be identified
            multiple_engines (bool): if muliple engines have been used, this can be
                set to True. Then reports a list of used engines.

        Examples:
            >>> fpaths = self.generate_basic_file_info( "14N_xtandem.csv" )
            >>> file_info, __    = self.load_json( fpaths=fpaths, mode='input')
            >>> last_engine      = self.get_last_engine(
                    history      = file_info["history"],
                    engine_types = ["protein_database_search_engine"]
                )
            >>> print( last_engine )
            "xtandem_sledgehammer"

        Returns:
            str: The name of the last engine that was used.
        '''
        last_engine = None
        if engine_types is None:
            engine_types = [
                'converter',
                'cross_link_search_engine',
                'de_novo_search_engine',
                'fetcher',
                'misc_engine',
                'meta_engine',
                'protein_database_search_engine',
                'spectral_library_search_engine',
                'validation_engine',
                'visualizer',
            ]
        if not history:
            history = self.stats["history"]
        else:
            for history_event in history[::-1]:
                if history_event['engine'] == 'merge_csvs_1_0_0':
                    merged_engines = set()
                    for element in self.flatten_list(history_event['history_addon']['search_engines_of_merged_files']):
                        merged_engines.add(element)
                    if len( merged_engines ) == 1:
                        last_engine = list(merged_engines)[0]
                    elif multiple_engines == True:
                        last_engine = list(merged_engines)

                    else:
                        assert last_engine != None, '''
                        last_engine cannot be determined, since multiple engines have been used.
                        If you want to return all used engines, set multiple_engines=True
                        {0}
                        '''.format( ", ".join(merged_engines) )
                    break

                meta = history_event.get("META_INFO", {})
                meta_engine_type_info = meta.get("engine_type", {})
                for engine_type in engine_types:
                    if meta_engine_type_info.get( engine_type, False ):
                        last_engine = history_event["engine"]
                        break

        return last_engine

    def get_last_engine_type(self, history=None):
        '''
        The unode get_last_engine_type function

        Keyword Arguments:
            history (list): A list of path unodes, timestamps and parameters
                that were used. This function can be used on the history loaded
                from a file .json, to find out which search engine was used on
                that file.
                If not specified, this information is taken from the unode class
                itself, and not a specific file.

        Examples:
            >>> fpaths = self.generate_basic_file_info( "14N_xtandem.csv" )
            >>> file_info, __    = self.load_json( fpaths=fpaths, mode='input')
            >>> last_engine_type = self.get_last_engine_type(
                    history      = file_info["history"],
                )
            >>> print( last_engine_type )
            "protein_database_search_engine"

        Returns:
            str: The type of the last engine that was used.
            Returns None if the engine_type cannot be specified or if no engine
            was previously executed on this file.
        '''

        last_engine_type = None
        if not history:
            history = self.stats["history"]
        history_event = history[-1]
        meta = history_event.get("META_INFO", {})
        meta_engine_type_info = meta.get("engine_type", {})

        for engine_type in meta_engine_type_info.keys():
            if meta_engine_type_info.get( engine_type, False ):
                last_engine_type = engine_type
                break

        return last_engine_type

    def get_last_search_engine(self, history=None, multiple_engines=False ):
        '''
        The unode get_last_search_engine function

        Note: returns None if no search engine was not used yet.

        Keyword Arguments:
            history (list): A list of path unodes, timestamps and parameters
                that were used. This function can be used on the history loaded
                from a file .json, to find out which search engine was used on
                that file.
                If not specified, this information is taken from the unode class
                itself, and not a specific file.
            multiple_engines (bool): if muliple engines have been used, this can be
                set to True. Then reports a list of used engines.

        Examples:
            >>> fpaths = self.generate_basic_file_info( "14N_xtandem.csv" )
            >>> file_info, __ = self.load_json( fpaths=fpaths, mode='input')
            >>> last_engine   = self.get_last_search_engine(
                    history   = file_info["history"]
                )
            >>> print( last_engine )
            "xtandem_sledgehammer"

        Returns:
            str: The name of the last search engine that was
            used. Returns None if no search engine was used yet.
        '''
        last_search_engine = None
        last_search_engine = self.get_last_engine(
            history=history,
            engine_types=[
                'cross_link_search_engine',
                'de_novo_search_engine',
                'protein_database_search_engine',
                'spectral_library_search_engine',
            ],
            multiple_engines=multiple_engines,
        )
        return last_search_engine

    def _group_psms(self, input_file, validation_score_field=None, bigger_scores_better=None):
        '''
        Reads an input csv and returns a defaultdict with the spectrum title
        mapping to a sorted list of tuples containing each
        a) score (from validation_score_field) and
        b) the whole line dict

        Keyword Arguments:
            validation_score_field (str): fieldname of the column that should be used as validation score
                for sorting of PSMs. If None, get_last_search_engine is used to get the validation_score_field
                defined for the last used search engine.
            bigger_scores_better (bool): defines if in the validation score are increasing (True) or decreasing
                (False) with their quality. If None, get_last_search_engine is used to get  bigger_scores_better
                defined for the last used search engine.
        '''
        print('[ GROUPING ] Parsing {0}'.format( input_file ))

        if bigger_scores_better is None or validation_score_field is None:
            last_engine = self.get_last_search_engine(
                history=self.stats['history']
            )
            assert last_engine, 'Can\'t convert results from no specified search engine.'
            assert 'multiple engines:' not in last_engine, 'Can\'t convert merged results from multiple different engines.'
            if bigger_scores_better is not None or validation_score_field is not None:
                print('''
[ WARNING ] Only "validation_score_field" or "bigger_scores_better" was defined
[ WARNING ] in UController.params. Determining both (!)
[ WARNING ] automatcally based on the last engine: {},
                '''.format(last_engine))
            if last_engine is None or type(last_engine) == list:
                print('''
                    Could not determine last_search_engine from input file.
                    Got {0}
                    Please specify parameters validation_score_field and bigger_scores_better
                '''.format(last_engine))
                sys.exit(1)
            else:
                bigger_scores_better = self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][last_engine]
                validation_score_field = self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][last_engine]

        tmp = ddict(list)
        grouped_psms = ddict(list)

        opened_file = open( input_file, 'r')
        csv_dict_reader_object = csv.DictReader(
            row for row in opened_file if not row.startswith('#')
        )
        n = 0

        for n, line_dict in enumerate(csv_dict_reader_object):
            assert validation_score_field in line_dict.keys(), \
                '''defined validation_score_field {0} is not found,
                please check/add it to uparams.py['validation_score_field']'''.format(validation_score_field)

            tmp[ line_dict[ 'Spectrum Title' ] ].append(
                (
                    float(
                        line_dict[ validation_score_field ]
                    ),
                    line_dict
                )
            )

        for spectrum_title in tmp.keys():
            already_seen = set()

            for score, line_dict in sorted( tmp[ spectrum_title ],
                    key     = operator.itemgetter(0),
                    reverse = bigger_scores_better
                ):
                _identifier = '_'.join( sorted( line_dict.values() ))
                if _identifier in already_seen:
                    continue
                already_seen.add( _identifier )
                grouped_psms[ spectrum_title ].append( ( score, line_dict ) )

        print(
            "[ GROUPING ] Grouped {0} PSMs into {1} unique spectrum titles".format(
                n,
                len( grouped_psms.keys())
            )
        )
        return grouped_psms

    def import_engine_as_python_function( self, function_name = None ):
        '''
        The unode import_engine_as_python_function function

        Imports the main function from a unodes "executable". For unodes
        that are written completely in python and can be executed by
        importing them instead of using the command line.

        Examples:
            >>> us = ursgal.UController()
            >>> cFDR_unode = us.unodes["combine_FDR_0_1"]["class"]
            >>> cFDR_main  = cFDR_unode.import_engine_as_python_function()
            >>> cFDR_main(
                input_file_list = ["1.csv", "2.csv"],
                directory       = "/tmp/",
            )

        Returns:
            function: The function called "main" that
            is specified in the engines python script.

        Note:
            Assertion exception if the executable is not a python
            script, or has no main function.
        '''
        assert os.path.exists( self.exe ), '''
        Engine needs to be python source file in order to import its main
        function!
        '''
        module_dir_name = os.path.dirname( self.exe )
        sys.path.insert( 1, module_dir_name )
        imported_module = importlib.import_module( self.engine )
        if function_name is None:
            function_name = 'main'
        assert hasattr(imported_module, function_name), '''
        Can not import main() function from engine
        {0}
        '''.format( self.exe )
        main_function = getattr( imported_module, function_name)
        return main_function

    def load_json( self, finfo=None, json_path=None):
        j_content = None
        if json_path is None:
            json_path = os.path.join( finfo['dir'], finfo['json'] )
        if os.path.exists( json_path ):
            j_content = json.load( open( json_path, 'r' ) )

        self.compare_json_and_local_ursgal_version(
            history = j_content[3]['history'],
            json_path = json_path
        )
        return j_content

    def compare_json_and_local_ursgal_version(self, history, json_path):
        ''' Print a warning if the history is a from a different version number '''
        json_version = None
        if len(history) > 0 and 'ursgal_version' in history[-1]:
            json_version = history[-1]['ursgal_version']
        if json_version != None and json_version != ursgal.__version__:
            self.print_info(
                ("JSON {0} stems from another Ursgal version!"
                    ).format(os.path.relpath(json_path)), caller="/\\")
            self.print_info(
                ("JSON version: {0} - Local version: {1}"
                    ).format(json_version, ursgal.__version__),
                caller="WARNING!")
            self.print_info(
                "Proceed at your own risk, or use (the) force to re-run the whole analysis!",
                caller="/____\\")
        return

    def map_mods(self):
        '''Maps modifications defined in params["modification"] using unimod.

       Examples:

            >>> [
            ...    "M,opt,any,Oxidation",        # Met oxidation
            ...    "C,fix,any,Carbamidomethyl",  # Carbamidomethylation
            ...    "*,opt,Prot-N-term,Acetyl"    # N-Acteylation
            ... ]

        '''
        self.params[ 'mods' ] = {
            'fix' : [],
            'opt' : []
        }
        for ursgal_index, mod in enumerate(
                sorted( self.params[ 'modifications' ] )):
            mod_params  = mod.split( ',' )
            if len(mod_params) >=6 or len(mod_params) <=3:
                print('''
    [ WARNING ] For modifications, please use the ursgal_style:
    [ WARNING ] 'amino_acid,opt/fix,position,Unimod PSI-MS Name'
    [ WARNING ] or
    [ WARNING ] 'amino_acid,opt/fix,position,name,chemical_composition'
    [ WARNING ] Continue without modification {0} '''.format( mod )
                )
                print(mod_params)
                continue
            aa          = mod_params[ 0 ].strip()
            mod_option  = mod_params[ 1 ].strip()
            pos         = mod_params[ 2 ].strip()
            unimod = False
            unimod_id = None

            if len(mod_params) == 4:
                try:
                    unimod_id = int(mod_params[ 3 ].strip())
                    unimod_name   = ursgal.GlobalUnimodMapper.id2name( unimod_id )
                    mass = ursgal.GlobalUnimodMapper.id2mass( unimod_id )
                    composition = ursgal.GlobalUnimodMapper.id2composition( unimod_id )
                    if unimod_name is None:
                        print('''
    [ WARNING ] '{1}' is not a Unimod modification
    [ WARNING ] please change it to a valid Unimod Accession # or PSI-MS Unimod Name
    [ WARNING ] or add the chemical composition hill notation (including 1)
    [ WARNING ] e.g.: H-1N1O2
    [ WARNING ] ursgal_style: 'amino_acid,opt/fix,position,name,chemical_composition'
    [ WARNING ] Continue without modification {0} '''.format(
                            mod,
                            unimod_id
                        ))
                        continue
                    unimod = True
                    name = unimod_name
                except:
                    unimod_name = mod_params[ 3 ].strip()
                    unimod_id   = ursgal.GlobalUnimodMapper.name2id( unimod_name )
                    mass = ursgal.GlobalUnimodMapper.name2mass( unimod_name )
                    composition = ursgal.GlobalUnimodMapper.name2composition( unimod_name )
                    if unimod_id is None:
                        print('''
    [ WARNING ] '{1}' is not a Unimod modification
    [ WARNING ] please change it to a valid PSI-MS Unimod Name or Unimod Accession #
    [ WARNING ] or add the chemical composition hill notation (including 1)
    [ WARNING ] e.g.: H-1N1O2
    [ WARNING ] ursgal_style: 'amino_acid,opt/fix,position,name,chemical_composition'
    [ WARNING ] Continue without modification {0} '''.format(
                            mod,
                            unimod_name
                        ))
                        continue
                    unimod = True
                    name = unimod_name

            elif len(mod_params) == 5:
                name = mod_params[ 3 ].strip()
                chemical_formula = mod_params[ 4 ].strip()
                chemical_composition = ursgal.ChemicalComposition()
                chemical_composition.add_chemical_formula( chemical_formula )
                composition = chemical_composition
                composition_unimod_style = chemical_composition.hill_notation_unimod()
                unimod_name_list = ursgal.GlobalUnimodMapper.composition2name_list( composition_unimod_style )
                unimod_id_list = ursgal.GlobalUnimodMapper.composition2id_list( composition_unimod_style )
                mass = ursgal.GlobalUnimodMapper.composition2mass( composition_unimod_style )
                for i, unimod_name in enumerate(unimod_name_list):
                    if unimod_name == name:
                        unimod_id = unimod_id_list[ i ]
                        unimod = True
                        break
                if unimod == False and unimod_name_list != []:
                    print(    '''
    [ WARNING ] '{0}' is not a Unimod modification
    [ WARNING ] but the chemical composition you specified is included in Unimod.
    [ WARNING ] Please use one of the Unimod names:
    [ WARNING ] {1}
    [ WARNING ] Continue without modification {2} '''.format(
                            name,
                            unimod_name_list,
                            mod
                    ))
                    continue
                if unimod == False and unimod_name_list == []:
                    print (    '''
    [ WARNING ] '{0}' is not a Unimod modification
    [ WARNING ] trying to continue with the chemical composition you specified
    [ WARNING ] This is not working with OMSSA so far'''.format(
                            mod,
                    ))
                    mass = chemical_composition._mass()
                    # write new userdefined modifications Xml in unimod style

            mod_dict = {
                '_id'   : ursgal_index,
                'aa'    : aa,
                'mass'  : mass,
                'pos'   : pos,
                'name'  : name,
                'composition' : composition,
                'org'   : mod,
                'id'    : unimod_id,
                'unimod': unimod,
            }
            if mod_dict['unimod'] == False:
                ursgal.GlobalUnimodMapper.writeXML( mod_dict )

            self.params[ 'mods' ][ mod_option ].append( mod_dict )
        return self.params[ 'mods' ]

    def peptide_regex(self, database, protein_id, peptide):
        '''
        Note:
            This function is not longer used at the moment.

        The unode peptide_regex function

        Args:
            database (str): Name of the used fasta database
            protein_id (str): protein ID of the processed protein
            peptide (str): peptide which should be mapped on the protein ID's
                sequence

        This function takes a peptide sequence and maps it to its according
        proteins sequence, returning the start and stop position in the sequence
        as well as the amino acid before and after the peptide sequence in the
        full protein sequence. If the peptide sequence contains known amino acid
        substitutions like U (Selenocystein) or J (Leucin or Isoleucin) this
        amino acid is replaced by a regex wildcard '.' in order to be matchable
        on the fasta database (this is defined in kb.unify_csv_1_0_0.py).
        This is especially needed if the original sequence contains a 'X' and
        the search engine guesses/determines the amino acid at this position.

        If the protein ID is ambigous, the peptide is matched against all
        protein candidates and the positions, pre- and post aminoacids in the
        matching sequence as well as the full protein ID as named in the fasta
        database is returned. This is especially needed for MS Amanda results
        where protein IDs are returned truncated and become ambigous for some
        databases.

        If the peptide occurs several times in the protein, all occurences are
        returned.

        The function uses a buffer to perform the regex only once for
        (peptide, protein, database) tuples. All fasta sequences are also
        buffered in `self.lookups['fasta_dbs']` with the name of the database as
        key and then all protein IDs and sequnces as key, value pairs.

        Pre and post amino acids are required for e.g. percolator input files.

        Note:

            The regex and peptide to protein ID mapping may take a while, if a
            large file has to be processed.

        Returns:
            list: list of tuples
            [( peptide_start, peptide_stop, aa_before_peptide, aa_after_peptide, protein_id )]


        '''
        if 'fasta_dbs' not in self.lookups.keys():
            self.lookups['fasta_dbs'] = {}
        if database not in self.lookups['fasta_dbs'].keys():
            self.generate_fasta_database_lookup( database )
        # print(self.lookups)
        # unify_csv_converter_version = self.params['unify_csv_converter_version']
        peptide_for_regex = peptide
        # corrected_peptide = peptide
        for aa_exception, aa_exception_info in self.meta_unodes[ 'unify_csv_1_0_0' ].DEFAULT_PARAMS['aa_exception_dict'].items():
            #regex will match any character in place of unknown aminoc acid...
            peptide_for_regex = peptide_for_regex.replace(
                aa_exception,
                '.'
            )
        ids_matched = []
        if protein_id not in self.lookups['fasta_dbs'][ database ].keys():
            #ms amanda short name problem
            for long_protein_id in self.lookups['fasta_dbs'][ database ].keys():
                if long_protein_id.startswith( protein_id ):
                    sequence_to_check = self.lookups['fasta_dbs'][ database ][long_protein_id]
                    match = re.search( peptide_for_regex, sequence_to_check )
                    if match is not None:
                        ids_matched.append( long_protein_id )
        else:
            ids_matched = [ protein_id ]
        return_buffer_keys = []
        for protein_id in ids_matched:
            full_sequence = self.lookups['fasta_dbs'][ database ][ protein_id ]
            buffer_key = ( database, peptide_for_regex, protein_id )
            if 'peptide_pos_buffer' not in self.lookups.keys():
                self.lookups['peptide_pos_buffer'] = {}
            if buffer_key not in self.lookups['peptide_pos_buffer'].keys():
                match_found = False
                for match in re.finditer( peptide_for_regex, full_sequence ):
                    match_found = True
                    start = match.start()
                    stop = start + len(peptide)

                    if start == 0:
                        pre_aa = '-'
                    else:
                        pre_aa = full_sequence[ start - 1 ]

                    if stop == len(full_sequence):
                        post_aa = '-'
                    else:
                        post_aa = full_sequence[ stop ]
                    pos_aa_protein = (
                        start + 1,
                        stop,
                        pre_aa,
                        post_aa,
                        protein_id
                        )
                    if buffer_key in self.lookups['peptide_pos_buffer']:
                        self.lookups['peptide_pos_buffer'][buffer_key].append(pos_aa_protein)
                    else:
                        self.lookups['peptide_pos_buffer'][buffer_key] = [pos_aa_protein]
                if match_found == False:
                    self.lookups['peptide_pos_buffer'][buffer_key] = [(
                        None,
                        None,
                        None,
                        None,
                        protein_id
                        )]
            # print(self.lookups['peptide_pos_buffer'].keys())
            if self.lookups['peptide_pos_buffer'][buffer_key][0] is None:
                self.print_info(
                    'Peptide {0} cant be found in database {1}, peptide for regex: {2}'.format(
                        peptide,
                        self.params['database'],
                        peptide_for_regex,
                    ),
                    caller='Warning'
                )

            return_buffer_keys.append( self.lookups['peptide_pos_buffer'][buffer_key] )
        return return_buffer_keys

    def _preflight(self):

        if 'citation' in self.META_INFO:
            self.print_info( caller='Citation', msg='')
            self.print_info( caller='Please', msg='')
            self.print_info(
                self.META_INFO["citation"],
                caller='cite:'
            )
            self.print_info( caller='-----', msg='')
            self.print_info( caller='Citation', msg='')

        self.print_info(
            'Executing preflight sequence ...',
            caller='PREFLGHT'
        )
        self.time_point(tag = 'preflight')
        preflight_answer = self.preflight()
        self.print_execution_time(tag='preflight')
        return preflight_answer

    def preflight(self):
        '''This can be/is overwritten by the engine uNode class'''
        return

    def _postflight(self):
        self.print_info(
            'Executing postflight sequence ...',
            caller = 'POSTFLGHT'
        )
        self.time_point(tag = 'postflight')
        postflight_answer = self.postflight()
        self.print_execution_time(tag='postflight')
        return postflight_answer

    def postflight(self):
        '''This can be/is overwritten by the engine uNode class'''
        return

    def print_execution_time( self, tag=None ):

        lap = self.time_point(tag = tag, diff=True, stop=True)
        # print('>>>', tag )
        # print('>>>', self.stats['time_points'])
        # print('>>>>', lap )
        # print('>>>>', self.time_point(tag = 'execution'))
        if lap > 3600:
            unit = 'hours'
            lap /= 3600
        elif lap > 60:
            unit = 'minutes'
            lap /= 60
        else:
            unit = 'seconds'
        msg = 'Execution time {0:.3f} {1}'.format(
            lap,
            unit
        )
        self.print_info( msg, caller=tag )

    @classmethod
    def print_info( cls, msg, caller=None ):
        if caller is None:
            if hasattr(cls, 'engine'):
                caller = cls.engine
            else:
                caller = ''
        if len(caller) > 7:
            caller = caller[:8]

        print(
            '[ {0: ^08s} ] {1}'.format(
                caller,
                msg
            )
        )

    def print_header( self, header, tag=None, newline=True):
        if tag is not None:
            time_stamp = '({0})'.format(
                self.time_point(
                    tag         = tag,
                    diff        = False,
                    format_time = True,
                    stop        = False
                )
            )
        else:
            time_stamp = ''
        print('''
        -\-     {0} {1}     -/-'''.format(
            header,
            time_stamp
        ))
        if newline:
            print()

    def initialize_run(self ):
        self.created_tmp_files = []
        self.io = {
            'input'  : {
                'finfo'  : None,
                'params' : None,
                'stats'  : None
            },
            'output' : {
                'finfo'  : None,
                'params' : None,
                'stats'  : None
            },
        }
        self.preflight_return_code = 0
        self.execute_return_code = 0
        self.postflight_return_code = 0
        self.stats = {}

    def generate_empty_report( self ):
        empty_report = {
            'preflight' : None,
            'execution' : None,
            'postflight': None,
            'stats' : None,
            'addon' : None,
        }
        return empty_report

    def update_params_with_io_data(self):
        '''
        Generates a flat structure in params combining
        io.['input']['finfo'] &
        io.['output']['finfo']
        '''
        i_finfo = self.io['input']['finfo']
        self.params['input_dir_path'] = i_finfo['dir']
        self.params['input_file'] = i_finfo['file']
        self.params['file_root'] = i_finfo['file_root']
        self.params['input_is_compressed'] = i_finfo['is_compressed']

        o_finfo = self.io['output']['finfo']
        self.params['output_dir_path'] = o_finfo['dir']
        self.params['output_file'] = o_finfo['file']

    def fix_md5_and_file_in_json(self, ifile=None, json_path=None):
        '''
        Fixes supplementary output json
        '''
        self.print_info(
            'Preparing json fix',
            caller = 'fix_md5'
        )
        if ifile is None:
            ifile = json_path.replace('.u.json', '')
            if os.path.exists(ifile) is False:
                raise IOError('file corresponding to {0} does not exists'.format(json_path))
        elif json_path is None:
            json_path = ifile+'.u.json'
            if os.path.exists(json_path) is False:
                raise IOError('json ({0}) corresponding to {1} does not exists'.format(json_path, ifile))
        i_finfo, o_finfo, params, stats = self.load_json(json_path=json_path)

        file_root, file_extention = os.path.splitext(os.path.basename(ifile))
        new_o_finfo = {
            'dir': os.path.dirname(ifile),
            'file': os.path.basename(ifile),
            'file_root': file_root,
            'file_extention': file_extention,
            'full': ifile,
            'is_compressed': False,
             'json': os.path.basename(json_path),
             'json_exists': True,
             'md5' : self.calc_md5(ifile)
        }

        j_content = [
            i_finfo,
            new_o_finfo,
            params,
            stats,
        ]
        with open(json_path , 'w') as file_object:
            json.dump(
                j_content,
                file_object,
                sort_keys = True,
                indent = 2
            )
        self.print_info(
            'New json dumped {0}'.format(os.path.basename(json_path)),
            caller = 'fix_md5'
        )


    def run(self, json_path=None ):
        '''
        The general run function.

        Runs engine/uNode child with given params on defined input_file.
        This function is automatically called by all ucontroller functions
        that take an input file and produce a single output file (i.e.
        ucontroller.search() and ucontroller.validate() )


        Keyword Arguments:
            json_path (str): path to input file json, dumped by a controller
            # input_file (str): path to the input file
            # fpaths (dict): dictionary containing file path information.
            # If None, this is generated using unode.generate_basic_file_info( file )
            # force (bool): (re)do the analysis if ouput files already exists

        Returns:
            dict: Report of the run.

        Note:

            Internal function. This function executes the preflight, postflight
            and _execute functions, if defined in the engine python script.

        '''
        self.initialize_run()
        i_finfo, o_finfo, params, stats = self.load_json( json_path=json_path )
        self.params = params
        self.stats = stats
        self.io['input']['finfo'] = i_finfo
        self.io['output']['finfo'] = o_finfo
        self.update_params_with_io_data()
        report = self.generate_empty_report()

        tag = '{0}@{1}'.format(
            self.engine,
            self.io['input']['finfo']['full'],
        )
        self.time_point( tag = tag )
        self.print_header(
            '{0} run initialized with {1}'.format(
                self.engine,
                self.io['input']['finfo']['file']
            ),
            tag=tag
        )
        if self.io['output']['finfo']['is_compressed']:

            self.params['output_file'] = self.params['output_file'].replace('.gz', '')

            self.print_info(
                'Will compress output {output_file} on the fly ... renamed temporarily params["output_file"]'
            .format(
                **self.params
                ),
                caller = 'run'
            )

        # DEFAULT PARAMS ARE INCLUDED HERE :)
        # self.params = self.DEFAULT_PARAMS.copy()

        # self.check_if_all_default_params_are_in_params()

        # self.time_point(tag = 'run')
        self.stats['history'] = self.update_history_status(
            history = self.stats['history']
        )
        self.print_info(
            'Preparing engine',
            caller = 'run'
        )

        # We use translated in the first json dump
        # so we can check which parameters are used during
        # run time or which one lead to a crash

        # self.original_params = copy.deepcopy( self.params )


        # We use original params for second and final dump
        #
        # if 'command_list' in self.original_params:
        #     del self.original_params['command_list']

        if 'translations' in self.params:
            del self.params['translations']

        untranslated_params, translated_params = \
            self.collect_and_translate_params( self.params )
        self.params.update( untranslated_params )
        self.params['translations'] = translated_params

        is_search_engine = False
        for engine_type in ukb.ENGINE_TYPES.keys():
            if 'search_engine' in engine_type:
                is_search_engine = self.META_INFO['engine_type'].get(
                    engine_type,
                    False
                )
            if is_search_engine is True:
                break
        # is_search_engine = self.META_INFO['engine_type'].get(
        #     'search_engine',
        #     False
        # )
        # is_denovo_engine = self.META_INFO['engine_type'].get(
        #     'denovo_engine',
        #     False
        # )
        # is_crosslink_engine = self.META_INFO['engine_type'].get(
        #     'cross_link_engine',
        #     False
        # )
        is_quantification_engine = self.META_INFO['engine_type'].get(
            'quantification_engine',
            False
        )
        map_mods_node_exceptions = [
            'unify_csv'
        ]
        if is_search_engine or is_quantification_engine:
            self.map_mods()
        for engine_short_name in map_mods_node_exceptions:
            if engine_short_name in self.engine:
                self.map_mods()
                break
        self.stats['history'] = self.update_history_status(
            status='launching',
            history = self.stats['history']
        )

        requires_grouped_psms = self.META_INFO.get(
            'group_psms',
            False
        )
        if requires_grouped_psms:
            self.print_info(
                'Grouping PSMs',
                caller ='run'
            )
            self.time_point(tag='group_psms')
            self.params['grouped_psms'] = self._group_psms(
                os.path.join(
                    self.params['input_dir_path'],
                    self.params['input_file']
                ),
                validation_score_field = self.params['translations']['validation_score_field'],
                bigger_scores_better = self.params['translations']['bigger_scores_better']
            )
            self.print_execution_time(tag = 'group_psms')

        self.print_info(
            'Starting engine',
            caller = 'run'
        )
        report['preflight'] = self._preflight()
        report['execution'] = self._execute()
        report['postflight'] = self._postflight()

        if self.execute_return_code == 0:
            history_status = 'complete'
        else:
            history_status = self.execute_return_code

        self.stats['history'] = self.update_history_status(
            status = history_status,
            history = self.stats['history']
        )
        # We Use original params for second and final dump
        # but keep novel params that are passed from the unode
        # jsons will get bigger if junk is collected
        # NOTE: all keys starting with _ will be deleted before dump
        if self.io['output']['finfo']['is_compressed']:
            gz_output_file = os.path.join(
                self.io['output']['finfo']['dir'],
                self.io['output']['finfo']['file']
            )
            raw_output = os.path.join(
                self.params['output_dir_path'],
                self.params['output_file'],
                )
            self.print_info('Compressing output {0} > {1}'.format(
                os.path.basename(raw_output),
                os.path.basename(gz_output_file),
            ))
            with open( raw_output, 'rb') as f_in:
                with gzip.open( gz_output_file, 'wb') as f_out:
                    f_out.writelines(f_in)
            self.created_tmp_files.append( raw_output )

        # self.params.update( self.original_params )

        if self.params['remove_temporary_files']:
            for tmp_file in self.created_tmp_files:
                if os.path.exists(tmp_file):
                    os.remove( tmp_file )

        self.print_execution_time(tag = tag)

        report['output_file'] = os.path.join(
            self.io['output']['finfo']['dir'],
            self.io['output']['finfo']['file']
        )

        # report['output_md5'] = self.calc_md5(
        #     report['output_file']
        # )
        report['stats'] = self.stats
        report['params'] = self.params
        return report

    def set_params( self, params):
        self.params.update( params )
        return


    def collect_and_translate_params(self, params):
        '''
        Translates ursgal parameters into uNode specific syntax.

        1) Each unode.USED_SEARCH_PARAMS contains params that have
            to be passed to the uNode.
        2) params values are not translated is they [] or {}
        3) params values are translated using::

            uNode.USEARCH_PARAM_VALUE_TRANSLATIONS
            > translating only values, regardless of key
            uNode.USEARCH_PARAM_KEY_VALUE_TRANSLATOR
            > translating only key:value pairs to key:newValue

        Those lookups are found in kb/{engine}.py

        TAG:
            - v0.4
        '''
        # print( self.DEFAULT_PARAMS )
        translated_params = {}
        GROUPED_TRANSLATIONS = {}
        untranslated_params = {}
        for ukey, mDict in self.UNODE_UPARAMS.items():

            pvalue = params.get( ukey, mDict['default_value'] )
            ukey_t = mDict['ukey_translated']

            if pvalue == mDict['default_value']:
                translated_value = mDict['default_value_translated']
            else:
                if isinstance( pvalue, list):
                    translated_value = pvalue
                elif isinstance( pvalue, dict):
                    translated_value = pvalue
                else:
                    translated_value = mDict['uvalue_style_translation'].get(
                        pvalue,
                        pvalue
                    )

            untranslated_params[ ukey ] = pvalue

            translated_params[ mDict['ukey'] ] = translated_value
            translated_params[ '{ukey}_key'.format(**mDict) ] = ukey_t

            if ukey_t not in GROUPED_TRANSLATIONS.keys():
                GROUPED_TRANSLATIONS[ ukey_t ] = {}
            GROUPED_TRANSLATIONS[ ukey_t ].update(
                {
                    mDict['ukey'] : translated_value
                }
            )
        translated_params['_grouped_by_translated_key'] = \
            GROUPED_TRANSLATIONS

        return untranslated_params, translated_params


        # exit("Translation is not done yet ....")
        # translated_params = {}
        # for mapped_unode_param in self.USED_USEARCH_PARAMS:
        #     assert mapped_unode_param in list(params.keys()), '''
        #     Missing required parameter {0}.
        #     All engine parameters (in kb.{1}.USED_USEARCH_PARAMS)
        #     have to be passed in params.
        #     '''.format(mapped_unode_param, self.engine, )

        #     ursgal_value = params[ mapped_unode_param ]
        #     # print(ursgal_value, type( ursgal_value ))
        #     if isinstance( ursgal_value, list) is True:
        #         translated_value = ursgal_value
        #     elif isinstance( ursgal_value, dict) is True:
        #         translated_value = ursgal_value
        #         # print( '''>>?<''' )
        #     else:
        #         # -- USEARCH_PARAM_KEY_VALUE_TRANSLATOR --
        #         LOOKUP = self.USEARCH_PARAM_KEY_VALUE_TRANSLATOR
        #         if mapped_unode_param in LOOKUP.keys():

        #             assert ursgal_value in LOOKUP[ mapped_unode_param ].keys(), '''
        # {0} is defined in kb.{1}.USEARCH_PARAM_KEY_VALUE_TRANSLATOR,
        # yet the ursgal_value {2}
        # has no specific translation defined.'''.format(
        #                 mapped_unode_param,
        #                 self.engine,
        #                 ursgal_value
        #             )
        #             translated_value = \
        #                 LOOKUP[ mapped_unode_param ][ ursgal_value ]
        #         # -- USEARCH_PARAM_VALUE_TRANSLATIONS --
        #         else:
        #             LOOKUP = self.USEARCH_PARAM_VALUE_TRANSLATIONS
        #             if ursgal_value in LOOKUP.keys():
        #                 lookup_list = list( LOOKUP.keys() )
        #                 index       = lookup_list.index( ursgal_value )
        #                 lookup_key  = lookup_list[ index ]
        #                 # print(ursgal_value, lookup_key)

        #                 if lookup_key == ursgal_value and type(lookup_key) == type(ursgal_value):
        #                     # print(ursgal_value, lookup_key)

        #                     translated_value = LOOKUP.get(ursgal_value, None)
        #                     # print(translated_value)
        #                     if translated_value is None:
        #                         translated_value = ursgal_value
        #                 else:
        #                     translated_value = ursgal_value
        #             else:
        #                 translated_value = ursgal_value
        #     translated_params[ mapped_unode_param ] = translated_value
        # return translated_params


    def time_point( self, tag=None, diff=True, format_time=False, stop=False ):
        '''
        Stores time_points in self.stats['time_points'] given a tag.
        returns time since tag was inserted if tag already exists.

        '''
        value = None
        if tag is not None:
            now = time.time()
            if tag in self.stats['time_points'].keys():
                start_time = self.stats['time_points'][ tag ]['start']

                if 'stop' in self.stats['time_points'][ tag ].keys():
                    now = self.stats['time_points'][ tag ]['stop']
                if diff:
                    value = now - start_time
                    if stop:
                        self.stats['time_points'][ tag ]['stop'] = now
                else:
                    value = start_time

            else:
                self.stats['time_points'][ tag ] = {'start' : now }
                value = now

            if format_time:
                value = time.ctime(
                    value
                )
        return value

    def update_history_status( self, engine=None, history=None, status='pending', history_addon=None ):
        if history is None:
            raise Exception("Legacy code implicitly updated history ... please change code!")

            # history = self.stats['history']
        if engine is None:
            engine = self.engine
        history = self.update_history_with_basic_unode_info(
            history= history,
            engine = engine
        )
        history[-1]['status'] = status
        if history_addon is not None:
            history[-1]['history_addon'] = history_addon
        return history

    def update_history_with_basic_unode_info(self, history=None, engine=None):
        # careful, self.engine != engine!

        #last istory entry
        init_empty_history_entry = False
        if len( history ) == 0:
            init_empty_history_entry = True
        else:
            last_history_entry = history[-1]

            if last_history_entry['engine'] != engine:
                init_empty_history_entry = True

            if last_history_entry['engine'] == engine and last_history_entry['status'] == 'complete':
                init_empty_history_entry = True

        if init_empty_history_entry:
            history.append(
                {
                    'engine'         : engine,
                    'ursgal_version' : ursgal.__version__,
                    'META_INFO'      : self.meta_unodes[ engine ].META_INFO,  # NOT self.META_INFO because self is the UController and not the search engine!!!
                    'finfo'          : self.io['input']['finfo']
                }
            )
        return history

        # entries_in_history = 0
        # last_engine_history_pos = 0
        # for pos, entry in enumerate(history):
        #     if entry['engine'] == engine:
        #         entries_in_history += 1
        #         last_engine_history_pos = pos

        # assert entries_in_history <= 1, '''
        # Found multiple entries in the history for this engine ({0}).
        # This should not happen. Consider re-running the pipeline.
        # '''.format( enigne )
        # if entries_in_history == 0:
        #     history.append(
        #         {
        #             'engine'    : engine,
        #             'startups'  : [],
        #             'META_INFO' : self.meta_unodes[ engine ].META_INFO,  # NOT self.META_INFO because self is the UController and not the search engine!!!
        #             'finfo'     : self.io['input']['finfo']
        #         }
        #     )
        # history_entry = history[-1]
        # assert history_entry['engine'] == engine, '''
        # Last entry in history is not from this engine ({0}).
        # This should not happen. Consider re-running the pipeline.

        # history : {1}
        # '''.format( engine, history  )
        # return history


if __name__ == '__main__':
    print('Yesss!')
