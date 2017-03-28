#!/usr/bin/env python3.4
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
try:
    import regex as regex
    finditer_kwargs = { 'overlapped' : True }
except:
    print('[ WARNING  ] Standard re module cannot find overlapping pattern')
    print('[   INFO   ] Consider installing the regex module')
    print('[   INFO   ] pip install -r requirements.txt')
    import re as regex
    finditer_kwargs = {}
import ahocorasick

# increase the field size limit to avoid crash if protein merge tags
# become too long does not work under windows
if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)



def main(input_file=None, output_file=None, params=None):
    '''
    Arguments:
        input_file (str): input filename of csv
        output_file (str): output filename
 
    '''
    print(
        '''[ pep_maps ] Mapping peptides from file {0}'''.format(
            os.path.basename(input_file),
        )
    )
    do_not_delete      = False
    created_tmp_files  = []
    target_decoy_peps  = set()
    non_enzymatic_peps = set()
    pep_map_lookup     = {}
    joinchar           = params['translations']['protein_delimiter']

    if params['translations']['peptide_mapper_version'] == 'upapa_v2':
        upapa = UPeptideMapper_v2( word_len = params['translations']['word_len'])
        fasta_lookup_name = upapa.build_lookup_from_file(
            params['translations']['database'],
            force  = False,
        )
    else:
        #silent default :)
        upapa = UPeptideMapper_v3( params['translations']['database'] )
        fasta_lookup_name = upapa.fasta_lookup_name

    print(
        '''[ map_peps ] Using peptide mapper version: {0}'''.format(
            params['translations']['peptide_mapper_version']
        )
    )
 


    output_file_object = open(output_file, 'w')
    protein_id_output = open(output_file + '_full_protein_names.txt', 'w')
    mz_buffer = {}
    csv_kwargs = {
        'extrasaction' : 'ignore'
    }
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'


    # total_lines = len(list(csv.reader(open(input_file,'r'))))

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
            for aa_to_replace, replace_dict in params['translations']['aa_exception_dict'].items():
                if aa_to_replace in line_dict['Sequence']:
                    #change mods only if unimod has to be changed...
                    if 'unimod_name' in replace_dict.keys():
                        for r_pos, aa in enumerate(line_dict['Sequence']):
                            if aa == aa_to_replace:
                                index_of_U = r_pos + 1
                                unimod_name = replace_dict['unimod_name']
                                if cam and replace_dict['original_aa'] == 'C':
                                    unimod_name = replace_dict['unimod_name_with_cam']
                                new_mod = '{0}:{1}'.format(
                                    unimod_name,
                                    index_of_U
                                )
                    line_dict['Sequence'] = line_dict['Sequence'].replace(
                        aa_to_replace,
                        replace_dict['original_aa']
                    )
            csv_file_buffer.append(line_dict)
            tmp_peptide_set.add( line_dict['Sequence'] )

        num_peptides = len(tmp_peptide_set)
        print('''[ map_peps ] Parsing and buffering csv done''')
        print(
            '''[ map_peps ] Mapping {0} peptides using mapper {1}'''.format(
                num_peptides,
                params['translations']['peptide_mapper_version']
            )
        )
        p2p_mappings  = upapa.map_peptides(
            list(tmp_peptide_set),
            fasta_lookup_name
        )        
        print('''[ map_peps ] Mapping peptides done''')
        total_lines = len(csv_file_buffer)
        assert len(p2p_mappings.keys()) == len(tmp_peptide_set)
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

                if upeptide_maps == []:
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
            '''
            [ WARNING ] The following peptides occured in a target as well as decoy protein
            [ WARNING ] {0}
            [ WARNING ] 'Is decoy' has been set to 'True' '''.format(
                target_decoy_peps,
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

        The UPeptideMapper is initialized during UNode instantiation thus all
        UNodes can access the mapper via self.upeptide_mapper.

    Warning:

        Ursgal keeps one upeptide_mapper alive during code execution and
        because the fcache requires a significant amount of memory, it is
        recommended that the user takes care of purging the mapper if not
        needed anymore, using the `UPeptideMapper.purge_fasta_info()` function.

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
            # sorted 3.8GB
            s_pep = ''.join(sorted(pep))
            try:
                self[ fasta_name ][ s_pep ].add( (id, pos + 1) )
            except:
                self[ fasta_name ][ s_pep ] = set([ (id, pos + 1) ])

        return

    def map_peptides(self, peptide_list, fasta_name = None, force_regex = False ):
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



class UPeptideMapper_v3( dict ):
    '''
    UPeptideMapper V3

    '''
    def __init__(self, fasta_database ):
        
        self.protein_list               = []
        self.protein_indices            = {}
        self.protein_sequences          = {}
        self.peptide_2_protein_mappings = {}
        self.total_sequence_string      = {}
        self.fasta_lookup_name          = os.path.basename(os.path.abspath( fasta_database ))
        counter                         = 0
        self.total_sequence_list        = defaultdict(list)
        self.len_total_sequence_string  = defaultdict(int)
        for protein_id, seq in ursgal.ucore.parseFasta(open(fasta_database,'r').readlines()):
            print( 'Buffering protein #{0}'.format(counter), end ='\r' )
            len_seq             = len(seq)
            
            self.protein_indices[protein_id] = {
                'start': self.len_total_sequence_string[self.fasta_lookup_name],
                'stop' : self.len_total_sequence_string[self.fasta_lookup_name] + len_seq
            }
            # self.total_sequence_string += seq
            self.total_sequence_list[self.fasta_lookup_name].append(seq)
            self.protein_list += [protein_id] * len_seq
            self.protein_sequences[protein_id] = seq
            self.len_total_sequence_string[self.fasta_lookup_name] += len_seq
            counter += 1
        print()
        print('Joining protein sequences')
        self.total_sequence_string[self.fasta_lookup_name] = ''.join( self.total_sequence_list[self.fasta_lookup_name] )
        print('Joining protein sequences done')


    def map_peptides(self, peptide_list, fasta_name):

        if fasta_name not in self.peptide_2_protein_mappings.keys():
            self.peptide_2_protein_mappings[fasta_name] = defaultdict(list)

        # self.peptide_2_protein_mappings = defaultdict(list)
        A = ahocorasick.Automaton()
        for idx, peptide in enumerate(peptide_list):
            A.add_word(peptide, (idx, peptide))
        A.make_automaton()
        for match in A.iter(self.total_sequence_string[fasta_name]):
            idx, (p_idx, m_peptide) = match
            len_m_peptide = len(m_peptide)
            protein_name_end_index = self.protein_list[idx]
            protein_name_start_index = self.protein_list[idx-len_m_peptide+1]
            if protein_name_end_index != protein_name_start_index:
                #overlap between end and start of next sequence!!!
                # print(m_peptide)
                # print(protein_name_start_index)
                # print(protein_name_end_index)
                # exit()
                continue
            protein_start_in_sequence_string = self.protein_indices[protein_name_end_index]['start']
            protein_stop_in_sequence_string  = self.protein_indices[protein_name_end_index]['stop']

            protein_seq = self.protein_sequences[protein_name_end_index]
            # protein_seq = self.total_sequence_string[protein_start_in_sequence_string:protein_stop_in_sequence_string]
            # assert protein_seq == self.protein_sequences[protein_name_end_index]
            stop_in_protein = idx - protein_start_in_sequence_string + 1
            start_in_protein = stop_in_protein - len(m_peptide)
            # print(m_peptide, start_in_protein, stop_in_protein)
            # print(protein_seq[start_in_protein: stop_in_protein])
            assert m_peptide == protein_seq[start_in_protein: stop_in_protein]
            pre_pos = start_in_protein - 1
            if pre_pos < 0:
                pre = '-'
            else:
                pre = protein_seq[pre_pos]
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


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(__doc__)
        exit()

    params = {
        'translations' : {
            'aa_exception_dict' : {
                'J' : {
                'original_aa' : 'L',
                },
                'O' : {
                    'original_aa' : 'K',
                    'unimod_name' : 'Methylpyrroline',
                },
                'U' : {
                    'original_aa' : 'C',
                    'unimod_name' : 'Delta:S(-1)Se(1)',
                    'unimod_name_with_cam' : 'SecCarbamidomethyl',
                },
            },
            'protein_delimiter'        : '<|>',
            'decoy_tag'                : 'decoy_',
            'word_len'                 : 6
        },
        'prefix' : None
    }
    params['translations']['database']               = sys.argv[3]
    params['translations']['peptide_mapper_version'] = sys.argv[4]

    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        params         = params,
    )
