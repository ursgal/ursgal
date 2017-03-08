#!/usr/bin/env python3.4
# encoding: utf-8
"""
    Ursgal MappOrs

    :copyright: (c) 2014 by C. Fufezan, S. Schulze
    :licence: BSD, see LISCENSE for more details

"""
import ursgal
from ursgal.uparams import ursgal_params as urgsal_dict
from collections import defaultdict as ddict
import multiprocessing
import re
import os
import time

class UParamMapper( dict ):
    '''
    UParamMapper class offers interface to ursgal.uparams

    Be default, the ursgal.uparams are parsed and the UParamMapper class
    is set with the ursgal_params dictionary.
    '''
    version = '0.2.0'

    def __init__( self, *args, **kwargs):
        # kwargs['engine_path'] = ursgal.__file__
        super(UParamMapper, self).__init__(*args, **kwargs)

        assert len(args) <= 1, 'Can only be initialized with max one argument'
        if len(args) == 0:
            params_dict = urgsal_dict
        else:
            params_dict = args[0]

        self.update( params_dict )
        self.lookup = self.group_styles()
        self._eval_functions = {
            'cpus' : {
                'max'     : multiprocessing.cpu_count(),
                'max - 1' : multiprocessing.cpu_count() - 1,
            }
        }

    def _assert_engine(self, engine):
        assert engine is not None, 'must define engine!'
        return

    def _eval_default_value( self, ukey, uvalue ):
        rvalue = None
        if ukey in self._eval_functions.keys():
            if uvalue in self._eval_functions[ ukey ].keys():
                rvalue = self._eval_functions[ ukey ][ uvalue ]
                if ukey == 'cpus' and rvalue == 0:
                    rvalue = 1

        return rvalue

    def mapping_dicts( self, engine_or_engine_style):
        '''yields all mapping dicts'''
        if '_style_' in engine_or_engine_style:
            lookup_key = 'style_2_params'
            style = engine_or_engine_style
        else:
            lookup_key = 'engine_2_params'
            style = self.lookup['engine_2_style'].get(engine_or_engine_style, None)

        for uparam in self.lookup[ lookup_key ].get(engine_or_engine_style, []):
            sup = self[ uparam ]

            uvalue_style_translation = sup['uvalue_translation'].get(style, {})
            assert isinstance(uvalue_style_translation, dict), '''
            Syntax error in ursgal/uparams.py at key {0}
            '''.format( uparam )
            if len(uvalue_style_translation.keys()) != 0:
                # can be translated, at least by some engine
                # and thus is not a list of elements ;)
                translated_value = uvalue_style_translation.get(
                    sup['default_value'],
                    sup['default_value']
                )
            else:
                translated_value = sup['default_value']

            if '_uevaluation_req' in sup.get('uvalue_type',''):
                re_evaluated_value = self._eval_default_value(
                    uparam,
                    translated_value
                )
                if re_evaluated_value is not None:
                    translated_value = re_evaluated_value

            template = sup.copy()
            keys_to_delete = [
                'ukey_translation',
                'uvalue_translation',
                'available_in_unode'
            ]
            for k in keys_to_delete:
                del template[ k ]
            template.update(
                {
                    'style'                    : style,
                    'ukey'                     : uparam,
                    'ukey_translated'          : sup['ukey_translation'][ style ],
                    'default_value_translated' : translated_value,
                    'uvalue_style_translation' : uvalue_style_translation,
                    'triggers_rerun'           : sup.get('triggers_rerun', True)
                }
            )

            yield template

    def get_masked_params( self, mask = None):
        '''
        Lists all uparams and the fields specified in the mask

        e.g. upapa.get_masked_params( mask = ['uvalue_type'])
        will return
        {
            '-xmx' : {
                'uvalue_type' : "str",
            },
            'aa_exception_dict' : {
                'uvalue_type' : "dict",
            },
            ...
        }
        '''
        if mask is None:
            mask = []
        masked_params = {}
        for key, value in self.items():
            masked_params[ key ] = {}
            for mkey in mask:
                masked_params[ key ][ mkey ] = value.get(mkey, None)
        return masked_params


    def get_all_params( self, engine=None):
        self._assert_engine( engine )
        all_params = []
        for ukey in self.keys():
            if engine in self[ ukey ]['available_in_unode']:
                all_params.append( ukey )
        return all_params

    def group_styles(self):
        '''
        Parses self.items() and build up lookups.
        Additionally, consistency check is performed to guarantee that each
        engine is mapping only on one style.

        The lookup build and returned looks like::

            lookup = {
                'style_2_engine' : {
                    'xtandem_style_1' : [
                        'xtandem_sledgehamer',
                        'xtandem_cylone',
                        ...
                    ],
                    'omssa_style_1' ...
                },
                # This is done during uNode initializations
                # each unode will register its style with umapmaster
                #
                'engine_2_style' : {
                    'xtandem_sledgehamer' : 'xtandem_style_1', ...
                },
                'engine_2_params' : {
                    'xtandem_sledgehamer' : [ uparam1, uparam2, ...], ...
                },
                'style_2_params' : {
                    'xtandem_style_1' : [ uparam1, uparam2, ... ], ...
                },
                'params_triggering_rerun' : {
                    'xtandem_style_1' : [ uparam1, uparam2 .... ]
                }
            }
        '''
        lookup = {
            'style_2_engine' : ddict(set),
            'engine_2_style' : {},
            # these two are not in the docu yet ...
            'engine_2_params': ddict(list),
            'style_2_params': ddict(list),
            'params_triggering_rerun' : ddict(list)
        }
        for uparam, udict in sorted(self.items()):
            # print( uparam, end = '\t')
            # if uparam == 'force':
            #     print(udict)
            for style in udict['ukey_translation'].keys():
                try:
                    style_basename, style_version = style.split('_style_')
                except:
                    print('Syntax Error @ uparam {0}'.format(uparam))
                    print('style : {0}'.format( style ))
                    exit(1)
                vvv = False
                if style_basename == 'ucontroller':
                    vvv = True
                    # print('UController params {0}'.format( uparam ))
                # else:
                    # print()
                styles_seen = set()
                for engine in udict['available_in_unode']:
                    # if vvv:
                    #     print(engine )
                    if style_basename not in engine:
                        continue
                    # this style 2 engine lookup is not quite right ...
                    # This function requires unode meta info for proper
                    # mapping ....
                    # lookup['style_2_engine'][ style ].add( engine )
                    lookup['engine_2_params'][ engine ].append( uparam )

                    if style not in styles_seen:
                        lookup['style_2_params'][ style ].append( uparam )
                        if udict.get('triggers_rerun', True):
                            lookup['params_triggering_rerun'][ style ].append( uparam )
                        styles_seen.add( style )

                    parsed_e2s = lookup['engine_2_style'].get( engine, None)
                    if parsed_e2s is None:
                        lookup['engine_2_style'][ engine ] = style
                    else:
                        if parsed_e2s != style:
                            print(
                                '{0} was found to map on style {1} and {2}'.format(
                                    engine, parsed_e2s, style
                                )
                            )
        return lookup

    def _show_params_overview( self, engine=None):
        self._assert_engine( engine )
        # This can be done differently with the lookups now ...
        for param in sorted(self.get_all_params( engine=engine)):
            udefault_value     = self[ param ]['default_value']

            ukey_translation   = self[ param ]['ukey_translation'].get(
                'msgfplus_style_1', '??'
            )
            uvalue_translation = self[ param ]['uvalue_translation'].get(
                'msgfplus_style_1', {}
            )
            try:
                translated_default_param_value = uvalue_translation.get( param, 'n/d')
            except:
                translated_default_param_value = 'complex type'
            try:

                print(
                    'uParams {0: >30} : {1: <20} {2: >30} : {3: <20}'.format(
                        param,
                        udefault_value,
                        ukey_translation,
                        translated_default_param_value,
                    )
                )
            except:

                print('Failed on: ' , param)


class UPeptideMapper( dict ):
    '''
    UPeptideMapper class offers ultra fast peptide to sequence mapping using
    a fast cache, hereafter referred to fcache.

    The fcache is build using the `build_lookup_from_file` or `build_lookup`
    functions. The fcache can be queried using the UPeptideMapper.map_peptide()
    function.

    Note:

        The UPeptideMapper is initialized during UNode instantiation thus all
        UNodes can access the mapper via self.upeptide_mapper.

    Warning:

        Ursgal keeps one upeptide_mapper alive during code execution and
        because the fcache requires a significant amount of memory, it is
        recommended that the user takes care of purging the mapper if not
        needed anymore, using the `UPeptideMapper.purge_fasta_info()` function.

    '''
    def __init__(self, word_len = 6 ):
        self.fasta_sequences = {}
        self.word_len = word_len
        self.hits = {'fcache': 0, 'regex': 0}
        self.query_length = ddict(int)
        self.master_buffer = {}

        pass

    def build_lookup_from_file( self, path_to_fasta_file, force=True):
        '''
        Builds the fast cache and regular sequence dict from a fasta stream

        return the internal fasta name, i.e. dirs stripped away from the path
        '''
        abs_path = os.path.abspath( path_to_fasta_file )
        assert os.path.exists( abs_path ), '''
            file {0} not found'''.format( abs_path )

        internal_name = os.path.basename(abs_path)
        with open( abs_path, 'r') as io:
            self.build_lookup(
                fasta_name   = internal_name,
                fasta_stream = io.readlines(),
                force        = force,
            )
        return internal_name

    def build_lookup( self, fasta_name=None, fasta_stream=None, force=True ):
        '''
        Builds the fast cache and regular sequence dict from a fasta stream
        '''
        print('[   upapa  ] UPeptideMapper is building the fast cache and regular sequence dict from a fasta')
        if fasta_name not in self.keys():
            force = True
            self[ fasta_name ] = {}
            self.fasta_sequences[ fasta_name ] = {}

        self.master_buffer[ fasta_name ] = {}
        # self.word_len = 6
        if force:
            for upapa_id, (id, seq) in enumerate(
                    ursgal.ucore.parseFasta( fasta_stream )):
                print(
                    '[   upapa  ] Indexing sequence #{0} with word_len {1}'.format(
                        upapa_id,
                        self.word_len
                    ),
                    end = '\r'
                )
                if seq.endswith('*'):
                    seq = seq.strip('*')
                self.fasta_sequences[ fasta_name ][ id ] = seq
                self._create_fcache(
                    id         = id,
                    seq        = seq,
                    fasta_name = fasta_name,
                )
                # if upapa_id > 10000:
                #     break
            print()
        # input('bp')
        # exit(1)

    def _create_fcache(self, id=None, seq=None, fasta_name=None):
        '''
        Updates the fast cache with a given sequence
        '''
        for pos in range(len( seq ) - self.word_len + 1):
            pep = seq[ pos : pos + self.word_len ]
            # pep = pep.encode()

            # Raw 6.3GB
            # try:
            #     self[ fasta_name ][ pep ].add( (id, pos + 1) )
            # except:
            #     self[ fasta_name ][ pep ] = set([ (id, pos + 1) ])

            # sorted 3.8GB
            s_pep = ''.join(sorted(pep))
            # print(s_pep, type(s_pep))
            try:
                self[ fasta_name ][ s_pep ].add( (id, pos + 1) )
            except:
                self[ fasta_name ][ s_pep ] = set([ (id, pos + 1) ])

            # tree like ... 3.8 GB
            # current_depth = self[ fasta_name ]
            # for aa in sorted(pep):
            #     try:
            #         current_depth[ ord(aa) ]
            #     except:
            #         current_depth[ ord(aa) ] = {}
            #     current_depth = current_depth[ ord(aa) ]
            # try:
            #     current_depth['_'].add( (id, pos + 1) )
            # except:
            #     current_depth['_'] = set([ (id, pos + 1) ])

            # Counter compression 4.1 GB
            # current_depth = self[ fasta_name ]
            # # for aa in sorted(pep):
            # for aa, count in Counter(pep).items():
            #     aa_key = '{0}{1}'.format(aa, count)
            #     try:
            #         current_depth[ aa_key ]
            #     except:
            #         current_depth[ aa_key ] = {}
            #     current_depth = current_depth[ aa_key ]
            # try:
            #     current_depth['_'].add( (id, pos + 1) )
            # except:
            #     current_depth['_'] = set([ (id, pos + 1) ])

        return

    def map_peptide(self, peptide=None, fasta_name=None, force_regex=False):
        '''
        Maps a peptide to a fasta database.

        Returns a list of single hits which look for example like this::

            {
                'start' : 12,
                'end'   : 18,
                'id'    : 'Protein Id passed to the function',
                'pre'   : 'A',
                'post'  : 'V',
            }
        '''

        l_peptide                        = len(peptide)
        mappings                         = []
        required_hits                    = l_peptide - self.word_len

        self.query_length[ l_peptide ] += 1


        if fasta_name in self.keys():
            if peptide in self.master_buffer[fasta_name].keys():
                mappings = self.master_buffer[fasta_name][peptide]
            else:
                if l_peptide < self.word_len or force_regex:
                    self.hits['regex'] += 1
                    pattern = re.compile( r'''{0}'''.format( peptide ))
                    # we have to through it by hand ...
                    # for fasta
                    for id, seq in self.fasta_sequences[ fasta_name ].items():
                        for match in pattern.finditer( seq ):
                            start = match.start() + 1
                            end   = match.end()
                            hit = self._format_hit_dict(  seq, start, end, id )
                            mappings.append( hit )
                else:
                    self.hits['fcache'] += 1
                    tmp_hits = {}
                    # m = []
                    for pos in range( l_peptide - self.word_len + 1):
                        pep = peptide[ pos : pos + self.word_len ]
                        # pep = pep.encode()
                        # print( pep, peptide )
                        s_pep = ''.join(sorted(pep))

                        fasta_set = self[ fasta_name ].get(s_pep, None)
                        if fasta_set is None:
                            continue

                        for id, id_pos in fasta_set:
                            try:
                                tmp_hits[ id ].add( id_pos )
                            except:
                                tmp_hits[ id ] = set([id_pos ])

                    for id, pos_set in tmp_hits.items():
                        sorted_positions = sorted(pos_set)
                        seq              = self.fasta_sequences[ fasta_name ][ id ]

                        for n, pos in enumerate( sorted_positions ):
                            start = sorted_positions[n]
                            end   = sorted_positions[n] + l_peptide - 1

                            if n + required_hits >= len( sorted_positions):
                                break

                            expected_number = pos + required_hits
                            try:
                                observed_number = sorted_positions[ n + required_hits ]
                            except:
                                break

                            if expected_number == observed_number or required_hits == 0:
                                if seq[ start - 1 : end ] == peptide:
                                    # double check
                                    mappings.append(
                                        self._format_hit_dict( seq, start, end, id)
                                    )
                self.master_buffer[fasta_name][peptide] = mappings
        return mappings

    def _format_hit_dict( self, seq, start, end, id ):
        '''
        Creates a formated dictionary from a single mapping hit. At the same
        time evaluating pre and pos amino acids from the given sequence
        Final output looks for example like this::

            {
                'start' : 12,
                'end'   : 18,
                'id'    : 'Protein Id passed to the function',
                'pre'   : 'A',
                'post'  : 'V',
            }

        Note::
            If the pre or post amino acids are N- or C-terminal, respectively,
            then the reported amino acid will be '-'

        '''
        if start == 1:
            pre_aa = '-'
        else:
            pre_aa = seq[ start - 2]
        if end >= len(seq):
            post_aa = '-'
        else:
            post_aa = seq[ end ]
        hit = {
            'start' : start,
            'end'   : end,
            'id'    : id,
            'pre'   : pre_aa ,
            'post'  : post_aa,
        }
        return hit

    def purge_fasta_info( self, fasta_name ):
        '''
        Purges regular sequence lookup and fcache for a given fasta_name
        '''
        del self.fasta_sequences[ fasta_name ]
        del self[ fasta_name ]

if __name__ == '__main__':
    print('Yes!')
