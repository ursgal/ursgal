#!/usr/bin/env python
'''
usage:
    ./upeptide_mapper_1_0_0.py <input_file> <output_file>


'''

from __future__ import print_function
import sys
import os
import csv
import ursgal
import re
from collections import Counter, defaultdict
import itertools
from copy import deepcopy
try:
    import regex as regex
    finditer_kwargs = { 'overlapped' : True }
except:
    print('[ WARNING  ] Standard re module cannot find overlapping pattern')
    print('[   INFO   ] Consider installing the regex module')
    print('[   INFO   ] pip install -r requirements.txt')
    import re as regex
    finditer_kwargs = {}
import bisect
# increase the field size limit to avoid crash if protein merge tags
# become too long does not work under windows
if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)



def main(input_file=None, output_file=None, params=None):
    '''
    Peptide mapping implementation as Unode.

    Arguments:
        input_file (str): input filename of csv
        output_file (str): output filename
        params (dict): dictionary containing ursgal params


    Results and fixes
        * All peptide Sequences are remapped to their corresponding protein,
          assuring correct start, stop, pre and post aminoacid.
        * It is determined if the corresponding proteins are decoy proteins.
          These peptides are reported after the mapping process.
        * Non-mappable peptides are reported. This can e.g. due to 'X' in
          protein sequences in the fasta file or other non-standard amino acids.
          These are sometimes replaced/interpreted/interpolated by the search
          engine.
          A recheck is performed if the peptides can be mapped containing an 'X'
          at any position. These peptides are also reported. If peptides can
          still not be mapped after re-mapping, these are reported as well.


    '''
    print(
        '''[ map_peps ] Mapping peptides from file {0}'''.format(
            os.path.basename(input_file),
        )
    )
    do_not_delete      = False
    created_tmp_files  = []
    target_decoy_peps  = set()
    non_mappable_peps  = set()
    pep_map_lookup     = {}
    joinchar           = params['translations']['protein_delimiter']
    if sys.platform == 'win32':
        try:
            import ahocorasick
        except:
            print(
'[ WARNING ] pyahocorasick can not be installed via pip on Windows at the moment\n'
'[ WARNING ] Falling back to UpeptideMapper_v2'
            )
            params['translations']['peptide_mapper_class_version'] = 'UPeptideMapper_v2'

    if params['translations']['peptide_mapper_class_version'] == 'UPeptideMapper_v2':
        upapa = UPeptideMapper_v2( word_len = params['translations']['word_len'])
        fasta_lookup_name = upapa.build_lookup_from_file(
            params['translations']['database'],
            force  = False,
        )
        class_etxra_args = [fasta_lookup_name]
    elif params['translations']['peptide_mapper_class_version'] == 'UPeptideMapper_v3':
        #silent default :)
        upapa = UPeptideMapper_v3( params['translations']['database'] )
        fasta_lookup_name = upapa.fasta_name
        class_etxra_args = [ fasta_lookup_name ]
    elif params['translations']['peptide_mapper_class_version'] == 'UPeptideMapper_v4':
        #silent default :)
        upapa = UPeptideMapper_v4( params['translations']['database'] )
        fasta_lookup_name = os.path.basename( params['translations']['database'] )
        class_etxra_args = []

    else:
        print(
            '[ map_peps ] peptide mapper class version unknown: {0}'.format(
                params['translations']['peptide_mapper_class_version']
            )
        )
        sys.exit(1)
    print(
        '''[ map_peps ] Using peptide mapper version: {0}'''.format(
            params['translations']['peptide_mapper_class_version']
        )
    )

    output_file_object = open(output_file, 'w')
    protein_id_output  = open(output_file + '_full_protein_names.txt', 'w')
    mz_buffer = {}
    csv_kwargs = {
        'extrasaction' : 'ignore'
    }
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'

    pep_map_lookup = {}

    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader(
            in_file
        )

        output_fieldnames = list(csv_input.fieldnames)
        for remove_fieldname in [
            'Start',
            'Stop',
            'gi',
            'Accession',
            'proteinacc_start_stop_pre_post_;'

        ]:
            if remove_fieldname not in output_fieldnames:
                continue
            output_fieldnames.remove(remove_fieldname)
        new_fieldnames = [
            'Is decoy',
            'Protein ID',
            'Sequence Start',
            'Sequence Stop',
            'Sequence Pre AA',
            'Sequence Post AA',
        ]

        for new_fieldname in new_fieldnames:
            if new_fieldname not in output_fieldnames:
                output_fieldnames.insert(-5,new_fieldname)
        csv_output = csv.DictWriter(
            output_file_object,
            output_fieldnames,
            **csv_kwargs
        )
        csv_output.writeheader()
        print('''[ map_peps ] Parsing and buffering csv''')
        import time
        csv_file_buffer = []
        tmp_peptide_set = set()
        for line_dict in csv_input:
            # we should add here all the J to I and L variants of MSAmanda...
            appended = False
            for aa_to_replace, replace_dict in sorted(params['translations']['aa_exception_dict'].items(), reverse=True):
                if aa_to_replace in line_dict['Sequence']:
                    if aa_to_replace in ['O']:
                        if 'unimod_name' in replace_dict.keys():
                            for r_pos, aa in enumerate(line_dict['Sequence']):
                                if aa == aa_to_replace:
                                    index_of_aa = r_pos + 1
                                    unimod_name = replace_dict['unimod_name']
                                    new_mod = '{0}:{1}'.format(
                                        unimod_name,
                                        index_of_aa
                                    )
                                    if line_dict['Modifications'] == '':
                                        line_dict['Modifications'] += new_mod
                                    else:
                                        line_dict['Modifications'] += ';{0}'.format(
                                            new_mod
                                        )
                        if len(replace_dict['original_aa']) == 1:
                            line_dict['Sequence'] = line_dict['Sequence'].replace(
                                aa_to_replace,
                                replace_dict['original_aa'][0]
                            )
                    elif aa_to_replace in ['J']:
                        repeat_count = line_dict['Sequence'].count(aa_to_replace)
                        #we need to do all combos for the positions of I and L in the seq...
                        positions = []
                        for index_of_aa, aa in enumerate(line_dict['Sequence']):
                            if aa == aa_to_replace:
                                positions.append( index_of_aa )
                        product_combos = []
                        new_peptides = set()
                        for combo_tuple in itertools.product(replace_dict['original_aa'],repeat=repeat_count):
                            # product_combos.append(n)
                            for pos, new_aa in enumerate(combo_tuple):
                                index_of_aa = positions[pos]
                                # text[:1] + 'Z' + text[2:]
                                remapped_peptide = '{0}{1}{2}'.format(
                                    line_dict['Sequence'][:index_of_aa],
                                    new_aa,
                                    line_dict['Sequence'][index_of_aa+1:],
                                )
                                tmp_peptide_set.add(
                                    remapped_peptide
                                )
                                line_dict['Sequence'] = remapped_peptide
                                csv_file_buffer.append( deepcopy(line_dict) )
                                appended = True
                    else:
                        print('''
[ WARNING ] New not covered case of aa exception for: "{0}"
[ WARNING ] Please adjust upeptide_mapper accordingly'''.format(aa_to_replace)
                        )
                        sys.exit(1)
            if appended is False:
                csv_file_buffer.append(line_dict)
            tmp_peptide_set.add( line_dict['Sequence'] )
        num_peptides = len(tmp_peptide_set)
        print('''[ map_peps ] Parsing and buffering csv done''')
        print(
            '''[ map_peps ] Mapping {0} peptides using mapper {1}'''.format(
                num_peptides,
                params['translations']['peptide_mapper_class_version']
            )
        )
        p2p_mappings  = upapa.map_peptides(
            list(tmp_peptide_set),
            *class_etxra_args
        )
        print('''[ map_peps ] Mapping peptides done''')
        total_lines = len(csv_file_buffer)
        #this assertion works for all but MSAmanda sinc J instaead of I or L is reported
        # print(set(tmp_peptide_set)-set(p2p_mappings.keys()))
        # print(len(set(tmp_peptide_set)-set(p2p_mappings.keys())))
        # assert len(p2p_mappings.keys()) == len(tmp_peptide_set)
        for line_nr, line_dict in enumerate(csv_file_buffer):
            if line_nr % 500 == 0:
                print(
                    '[ map_peps ] Processing line number: {0}/{1} .. '.format(
                        line_nr,
                        total_lines,
                    ),
                    end='\r'
                )
            # remap peptides to proteins, check correct enzymatic
            # cleavage and decoy assignment
            lookup_identifier = '{0}><{1}'.format(
                line_dict['Sequence'],
                fasta_lookup_name
            )
            if lookup_identifier not in pep_map_lookup.keys():
                tmp_decoy = set()
                upeptide_maps = p2p_mappings[line_dict['Sequence']]

                if upeptide_maps  == []:
                    print('''
[ WARNING ] The peptide {0} could not be mapped to the
[ WARNING ] given database {1}
[ WARNING ] {2}
[ WARNING ] This PSM will be skipped.
                        '''.format(
                            line_dict['Sequence'],
                            fasta_lookup_name,
                            ''
                        )
                    )
                    non_mappable_peps.add(line_dict['Sequence'])
                    continue

                sorted_upeptide_maps = [ protein_dict for protein_dict in sorted( upeptide_maps, key=lambda x: x['id'] ) ]

                protein_mapping_dict = None
                last_protein_id      = None
                for protein in sorted_upeptide_maps:
                    if protein_mapping_dict is None:
                        protein_mapping_dict = {
                            'Protein ID'       : protein['id'],
                            'Sequence Start'   : str(protein['start']),
                            'Sequence Stop'    : str(protein['end']),
                            'Sequence Pre AA'  : protein['pre'],
                            'Sequence Post AA' : protein['post'],
                        }
                    else:
                        if protein['id'] == last_protein_id:
                            tmp_join_char = ';'
                        else:
                            tmp_join_char = joinchar
                            protein_mapping_dict['Protein ID' ] += '{0}{1}'.format(tmp_join_char, protein['id'])

                        protein_mapping_dict['Sequence Start'   ] += '{0}{1}'.format(tmp_join_char, str(protein['start']))
                        protein_mapping_dict['Sequence Stop'    ] += '{0}{1}'.format(tmp_join_char, str(protein['end']))
                        protein_mapping_dict['Sequence Pre AA'  ] += '{0}{1}'.format(tmp_join_char, protein['pre'])
                        protein_mapping_dict['Sequence Post AA' ] += '{0}{1}'.format(tmp_join_char, protein['post'])

                    last_protein_id = protein['id']

                    # mzidentml-lib does not always set 'Is decoy' correctly
                    # (it's always 'false' for MS-GF+ results), this is fixed here:
                    if params['translations']['decoy_tag'] in protein['id']:
                        tmp_decoy.add('true')
                    else:
                        tmp_decoy.add('false')

                if len(protein_mapping_dict['Protein ID']) >= 2000:
                    print(
                        '{0}: {1}'.format(
                            line_dict['Sequence'],
                            protein_mapping_dict['Protein ID']
                        ),
                        file = protein_id_output
                    )
                    protein_mapping_dict['Protein ID'] = protein_mapping_dict['Protein ID'][:1990] + ' ...'
                    do_not_delete = True

                if len(tmp_decoy) >= 2:
                    target_decoy_peps.add(line_dict['Sequence'])
                    protein_mapping_dict['Is decoy'] = 'true'
                else:
                    protein_mapping_dict['Is decoy'] = list(tmp_decoy)[0]

                pep_map_lookup[ lookup_identifier ] = protein_mapping_dict

            line_dict.update( pep_map_lookup[lookup_identifier] )

            csv_output.writerow(line_dict)
    output_file_object.close()

    if len(target_decoy_peps) != 0:
        print(
'''[ WARNING ] {0}
[ WARNING ] These {1} peptides above (truncated to 100) occurred in a target as well as decoy protein
[ WARNING ] 'Is decoy' has been set to 'True' '''.format(
    target_decoy_peps if len(target_decoy_peps) <100 else list(target_decoy_peps)[:99],
    len(target_decoy_peps)
)
        )
    if len(non_mappable_peps) != 0:
        print(
'''[ WARNING ] {0}
[ WARNING ] These {1} peptides above (truncated to 100) could not be mapped to the database
[ WARNING ] Check Search and Database if neccesary'''.format(
    sorted(list(non_mappable_peps)) if len(list(non_mappable_peps)) < 100 else list(non_mappable_peps)[:99],
    len(non_mappable_peps)
)
        )
        #recheck these peptides if sequence has a 'X'
        # this is done by the peptide regex function in the unode... Use this instead?
        print('[ map_peps ] Attempting re-map of non-mappable peptides')
        peptide_has_X_in_sequence = set()
        mappable_after_all = set()
        for non_mappable_peptide in non_mappable_peps:
            if non_mappable_peptide == '':
                continue
            variants  = set()
            for pos, aa in enumerate(non_mappable_peptide):
                variants.add(
                    '{0}{1}{2}'.format(
                        non_mappable_peptide[:pos],
                        'X',
                        non_mappable_peptide[pos+1:],
                    )

                )
            # reset buffer...
            upapa.peptide_2_protein_mappings[fasta_lookup_name] = defaultdict(list)
            p2p_mappings  = upapa.map_peptides(
                list(variants),
                *class_etxra_args
            )
            if len(p2p_mappings.keys()) != 0:
                for p_with_x, maps in p2p_mappings.items():
                    if maps != []:
                        peptide_has_X_in_sequence.add( p_with_x )
                        mappable_after_all.add( non_mappable_peptide )
        print(
'''[ WARNING ] {0}
[ WARNING ] These {1} not mappable peptides (truncated to 100) have "X" in their sequence
[ WARNING ] {2} are part of the non-mappable peptides'''.format(
    sorted(list(peptide_has_X_in_sequence)) if len(peptide_has_X_in_sequence) < 100 else sorted(list(peptide_has_X_in_sequence))[:99],
    len(peptide_has_X_in_sequence),
    len(mappable_after_all)
)
        )
        not_mappable_after_all = non_mappable_peps - mappable_after_all
        if len(not_mappable_after_all) != 0:
            print(
'''[ WARNING ] {0}
[ WARNING ] These {1} peptides (truncated to 100) are indeed not mappable
[ WARNING ] Check of Search parameters and database is strongly recommended'''.format(
    not_mappable_after_all if len(not_mappable_after_all) < 100 else list(not_mappable_after_all)[:99],
    len(not_mappable_after_all),
)
            )

    if do_not_delete is False:
        created_tmp_files.append( output_file + '_full_protein_names.txt' )
    return created_tmp_files


class UPeptideMapper_v2( dict ):
    '''
    UPeptideMapper class offers ultra fast peptide to sequence mapping using
    a fast cache, hereafter referred to fcache.

    The fcache is build using the `build_lookup_from_file` or `build_lookup`
    functions. The fcache can be queried using the UPeptideMapper.map_peptide()
    function.

    Note:

        This is the deprectaed version of the peptide mapper which can be used
        by setting the parameter 'peptide_mapper_class_version' to 'UPeptideMapper_v2'.
        Otherwise the new mapper class version ('UPeptideMapper_v3') is used as default.

    '''
    def __init__(self, word_len = None ):
        self.fasta_sequences = {}
        self.word_len = word_len
        self.hits = {'fcache': 0, 'regex': 0}
        self.query_length = defaultdict(int)
        self.master_buffer = {}
        self.peptide_2_protein_mappings = {}
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
        print('[ upapa v2 ] UPeptideMapper is building the fast cache and regular sequence dict from a fasta')
        if fasta_name not in self.keys():
            force = True
            self[ fasta_name ] = {}
            self.fasta_sequences[ fasta_name ] = {}

        self.master_buffer[ fasta_name ] = {}
        # self.word_len = 6
        if force:
            for upapa_id, (id, seq) in enumerate(
                    ursgal.ucore.parse_fasta( fasta_stream )):
                print(
                    '[ upapa v2 ] Indexing sequence #{0} with word_len {1}'.format(
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
            # sorted 3.8GB
            s_pep = ''.join(sorted(pep))
            try:
                self[ fasta_name ][ s_pep ].add( (id, pos + 1) )
            except:
                self[ fasta_name ][ s_pep ] = set([ (id, pos + 1) ])

        return

    def map_peptides(self, peptide_list, fasta_name = None, force_regex = False ):
        '''
        Wrapper function to map a given peptide list in one batch.

        Args:
            peptide_list (list): list with peptides to be mapped
            fasta_name (str): name of the database


        '''
        if fasta_name not in self.peptide_2_protein_mappings.keys():
            self.peptide_2_protein_mappings[fasta_name] = defaultdict(list)
        for peptide in peptide_list:
            self.peptide_2_protein_mappings[fasta_name][peptide] = self.map_peptide(
                peptide,
                fasta_name = fasta_name,
            )

        return self.peptide_2_protein_mappings[fasta_name]

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
                    pattern = regex.compile( r'''{0}'''.format( peptide ))
                    # we have to through it by hand ...
                    # for fasta
                    for id, seq in self.fasta_sequences[ fasta_name ].items():
                        for match in pattern.finditer( seq, **finditer_kwargs ):
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
                        seq = self.fasta_sequences[ fasta_name ][ id ]

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
                                        self._format_hit_dict(
                                            seq, start, end, id
                                        )
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

        Note:
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



class UPeptideMapper_v3():
    '''
    UPeptideMapper V3

    New improved version which is faster and consumes less memory than earlier
    versions. Is the new default version for peptide mapping.

    Note:
        Uses the implementation of Aho-Corasick algorithm pyahocorasick.
        Please refer to https://pypi.python.org/pypi/pyahocorasick/ for more
        information.

    Warning:
        The new implementation is still in beta/testing phase. Please use, check
        and interpret accordingly



    '''
    def __init__(self, fasta_database ):
        self.fasta_name                 = os.path.basename(os.path.abspath( fasta_database ))

        self.protein_indices            = defaultdict(dict)
        self.protein_sequences          = defaultdict(dict)

        self.total_sequence_list        = defaultdict(list)
        self.protein_list               = defaultdict(list)

        self.fasta_counter              = defaultdict(int)
        self.len_total_sequence_string  = defaultdict(int)

        self.peptide_2_protein_mappings = {}
        self.total_sequence_string      = {}
        self.cache_database(fasta_database, self.fasta_name)

        self.automatons = {}


    def cache_database(self, fasta_database,  fasta_name):
        '''
        Function to cache the given fasta database.

        Args:
            fasta_database (str): path to the fasta database
            fasta_name (str): name of the database
                (e.g. os.path.basename(fasta_database))

        Note:

            If the same fasta_name is buffered again all info is purged from the
            class.
        '''
        if fasta_name in self.protein_indices.keys():
            self.purge_fasta_info(fasta_name)
            self.fasta_name = fasta_name
        for protein_pos, (protein_id, seq) in enumerate(ursgal.ucore.parse_fasta(open(fasta_database,'r').readlines())):
            if protein_pos % 5000 == 0:
                print(
                    '[ upapa v3 ] Buffering protein #{0} of database {1}'.format(
                        self.fasta_counter[fasta_name],
                        os.path.basename(fasta_database)
                    ),
                    end ='\r'
                )
            len_seq             = len(seq)

            self.protein_indices[fasta_name][protein_id] = {
                'start': self.len_total_sequence_string[fasta_name],
                'stop' : self.len_total_sequence_string[fasta_name] + len_seq
            }
            # self.total_sequence_string += seq
            self.total_sequence_list[fasta_name].append(seq)
            self.protein_list[fasta_name] += [ protein_id ] * len_seq
            self.protein_sequences[fasta_name][ protein_id ] = seq
            self.len_total_sequence_string[fasta_name] += len_seq
            self.fasta_counter[fasta_name] += 1
        print()
        # print('[ upapa v3 ] Joining protein sequences')
        self.total_sequence_string[fasta_name] = ''.join( self.total_sequence_list[fasta_name] )
        # print('[ upapa v3 ] Joining protein sequences done')
        return

    def map_peptides(self, peptide_list, fasta_name):
        '''
        Function to map a given peptide list in one batch.

        Args:
            peptide_list (list): list with peptides to be mapped
            fasta_name (str): name of the database
                (e.g. os.path.basename(fasta_database))

        Returns:
            peptide_2_protein_mappings (dict): Dictionary containing
                peptides as keys and lists of protein mappings as values of the
                given fasta_name

        Note:
            Based on the number of peptides the returned mapping dictionary
            can become very large.

        Warning:
            The peptide to protein mapping is resetted if a new list o peptides
            is mapped to the same database (fasta_name).

        Examples::

            peptide_2_protein_mappings['BSA1']['PEPTIDE']  = [
                {
                    'start' : 1,
                    'end'   : 10,
                    'pre'   : 'K',
                    'post'  : 'D',
                    'id'    : 'BSA'
                }
            ]
        '''
        import ahocorasick
        # if fasta_name not in self.peptide_2_protein_mappings.keys():
        self.peptide_2_protein_mappings[fasta_name] = defaultdict(list)

        # self.peptide_2_protein_mappings = defaultdict(list)
        self.automatons[fasta_name] = ahocorasick.Automaton()
        for idx, peptide in enumerate(peptide_list):
            #integrated buffering of peptides
            if peptide not in self.peptide_2_protein_mappings[fasta_name].keys():
                self.automatons[fasta_name].add_word(peptide, (idx, peptide))
        self.automatons[fasta_name].make_automaton()
        for match in self.automatons[fasta_name].iter(self.total_sequence_string[fasta_name]):
            idx, (p_idx, m_peptide) = match
            len_m_peptide = len(m_peptide)
            protein_name_end_index = self.protein_list[fasta_name][idx]
            protein_name_start_index = self.protein_list[fasta_name][idx-len_m_peptide+1]
            if protein_name_end_index != protein_name_start_index:
                #overlap between end and start of next sequence!!!
                # print(m_peptide)
                # print(protein_name_start_index)
                # print(protein_name_end_index)
                # sys.exit(1)
                continue
            protein_start_in_sequence_string = self.protein_indices[fasta_name][protein_name_end_index]['start']
            protein_stop_in_sequence_string  = self.protein_indices[fasta_name][protein_name_end_index]['stop']

            protein_seq = self.protein_sequences[fasta_name][protein_name_end_index]
            # protein_seq = self.total_sequence_string[protein_start_in_sequence_string:protein_stop_in_sequence_string]
            # assert protein_seq == self.protein_sequences[fasta_name][protein_name_end_index]
            stop_in_protein = idx - protein_start_in_sequence_string + 1
            start_in_protein = stop_in_protein - len(m_peptide)
            # print(m_peptide, start_in_protein, stop_in_protein)
            # print(protein_seq[start_in_protein: stop_in_protein])
            assert m_peptide == protein_seq[start_in_protein: stop_in_protein]
            pre_pos = start_in_protein - 1
            if pre_pos < 0:
                pre = '-'
            else:
                pre = protein_seq[ pre_pos ]
            try:
                post = protein_seq[ stop_in_protein ]
            except:
                post = '-'

            self.peptide_2_protein_mappings[fasta_name][m_peptide].append(
                {
                    'start' : start_in_protein + 1,
                    'end'   : stop_in_protein,
                    'pre'   : pre,
                    'post'  : post,
                    'id'    : protein_name_end_index
                }
            )

        return self.peptide_2_protein_mappings[fasta_name]

    def purge_fasta_info( self, fasta_name ):
        '''
        Purges regular sequence lookup and fcache for a given fasta_name
        '''
        print('[ upapa v3 ] Purging buffer for {0}'.format(fasta_name))
        del self.protein_list[fasta_name]
        del self.protein_indices[fasta_name]
        del self.protein_sequences[fasta_name]
        del self.total_sequence_string[fasta_name]
        del self.fasta_counter[fasta_name]
        del self.total_sequence_list[fasta_name]
        del self.len_total_sequence_string[fasta_name]
        if fasta_name in self.peptide_2_protein_mappings.keys():
            del self.peptide_2_protein_mappings[fasta_name]
        if fasta_name in self.automatons.keys():
            del self.automatons[fasta_name]


class UPeptideMapper_v4():
    '''
    UPeptideMapper V4

    Improved version of class version 3 (changes proposed by Christian)

    Note:
        Uses the implementation of Aho-Corasick algorithm pyahocorasick.
        Please refer to https://pypi.python.org/pypi/pyahocorasick/ for more
        information.



    '''
    def __init__(self, fasta_database ):

        # self.protein_indices            = {}
        self.protein_sequences          = {}

        self.total_sequence_list        = []

        self.protein_list               = []
        self.protein_start_indices      = []

        self.fasta_counter              = 0
        self.len_total_sequence_string  = 0

        self.peptide_2_protein_mappings = {}
        self.total_sequence_string      = {}
        self.cache_database(fasta_database)


    def cache_database(self, fasta_database):
        '''
        Function to cache the given fasta database.

        Args:
            fasta_database (str): path to the fasta database

        Note:

            If the same fasta_name is buffered again all info is purged from the
            class.
        '''

        for protein_pos, (protein_id, seq) in enumerate(ursgal.ucore.parse_fasta(open(fasta_database,'r').readlines())):
            if protein_pos % 5000 == 0:
                print(
                    '[ upapa v4 ] Buffering protein #{0} of database {1}'.format(
                        self.fasta_counter,
                        os.path.basename(fasta_database)
                    ),
                    end ='\r'
                )
            len_seq             = len(seq)

            self.total_sequence_list.append(seq)

            self.protein_list.append( protein_id )
            self.protein_start_indices.append( self.len_total_sequence_string +protein_pos) # protein start

            self.protein_sequences[ protein_id ] = seq
            self.len_total_sequence_string += len_seq  #offset for delimiter |
            self.fasta_counter += 1
        print()
        self.total_sequence_string = '|'.join( self.total_sequence_list )
        return

    def map_peptides(self, peptide_list):
        '''
        Function to map a given peptide list in one batch.

        Args:
            peptide_list (list): list with peptides to be mapped


        Returns:
            peptide_2_protein_mappings (dict): Dictionary containing
                peptides as keys and lists of protein mappings as values of the
                given fasta_name

        Note:
            Based on the number of peptides the returned mapping dictionary
            can become very large.

        Warning:
            The peptide to protein mapping is resetted if a new list o peptides
            is mapped to the same database (fasta_name).

        Examples::

            peptide_2_protein_mappings['PEPTIDE']  = [
                {
                    'start' : 1,
                    'end'   : 10,
                    'pre'   : 'K',
                    'post'  : 'D',
                    'id'    : 'BSA'
                }
            ]
        '''
        import ahocorasick
        self.peptide_2_protein_mappings = defaultdict(list)

        # self.peptide_2_protein_mappings = defaultdict(list)
        self.automaton =  ahocorasick.Automaton()
        for idx, peptide in enumerate(peptide_list):
            self.automaton.add_word(peptide, (idx, peptide))
        self.automaton.make_automaton()

        for match in self.automaton.iter(self.total_sequence_string):
            idx, (p_idx, m_peptide) = match
            len_m_peptide = len(m_peptide)

            protein_index = bisect.bisect( self.protein_start_indices, idx ) - 1
            protein_name  = self.protein_list[protein_index]
            protein_seq   = self.protein_sequences[protein_name]
            start_in_total_seq_string = self.protein_start_indices[protein_index]
            # print('Index',protein_index)
            stop_in_protein = idx - start_in_total_seq_string + 1
            start_in_protein = stop_in_protein - len(m_peptide)

            pre_pos = start_in_protein - 1

            # print(stop_in_protein)
            # print(start_in_protein)
            # print(pre_pos)
            if pre_pos < 0:
                pre = '-'
            else:
                pre = protein_seq[ pre_pos ]
            try:
                post = protein_seq[ stop_in_protein ]
            except:
                post = '-'

            self.peptide_2_protein_mappings[m_peptide].append(
                {
                    'start' : start_in_protein + 1,
                    'end'   : stop_in_protein,
                    'pre'   : pre,
                    'post'  : post,
                    'id'    : protein_name
                }
            )

        return self.peptide_2_protein_mappings




if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)

    params = {
        'translations' : {
            'modifications' : [
                'M,opt,any,Oxidation',        # Met oxidation
                'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
                '*,opt,Prot-N-term,Acetyl',    # N-Acteylation[]
            ],
            'aa_exception_dict' : {
                'J' : {
                    'original_aa' : ['I', 'L'],
                },
                'O' : {
                    'original_aa' : ['K'],
                    'unimod_name' : 'Methylpyrroline',
                },
            },
            'protein_delimiter'        : '<|>',
            'decoy_tag'                : 'decoy_',
            'word_len'                 : 6
        },
        'prefix' : None
    }
    params['translations']['database']                     = sys.argv[3]
    params['translations']['peptide_mapper_class_version'] = sys.argv[4]

    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        params         = params,
    )
