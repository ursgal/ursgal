#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest
import pprint
# from ursgal import umapmaster as umama
import pprint
import os
try:
    import regex
    regex_module_installed = True
except:
    regex_module_installed = False
    


TEST_FASTA = [
    '>Protein1\n',
    'ELVISLIVES\n',
    '\n',
    '>Protein2\n',
    'KLEINERPENNER\n',
    '>Protein3\n',
    'WHYISELVIS\n',
    'HELEAVING\n',
    '>T1',
    'AAAAAAA___AAAAAAAAAA_____AAAAA__________AAAAAAAAAA',
    #----+----|----+----|----+----|----+----|----+----|
    '>Overlapping',
    'GGGGGGGGGG',
    '>ugly_fasta',
    'FCKTHIS*',
    '>SortingPepCorrect_1',
    'FORWARDKKK',
    '>SortingPepCorrect_2',
    'DRAWROFKKK',
    '>SortingPepCorrect_3',
    'FROWARDKKK',
]

TEST_FASTA_TWO = [
    '>Ze_other_protein2\n',
    'KLEINERRETTER\n',
]


class UMapMaster(unittest.TestCase):
    def setUp(self):
        self.uc = ursgal.UController( verbose = False )
        upapa_class = self.uc.unodes['upeptide_mapper_1_0_0']['class'].import_engine_as_python_function('UPeptideMapper_v2')
        self.upapa_class = upapa_class( word_len=5 )
        self.upapa_class.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA
        )

    def test_incremental_fcache_buildup_and_global_access(self):
        '''
        This is not longer relevant, we have no global access on the peptide
        mapper any more
        '''
        # map with empty
        self.upapa_class.purge_fasta_info('Test.fasta')
        maps = self.upapa_class.map_peptide( peptide='KLEINER', fasta_name='Test.fasta')
        # print(maps)
        self.assertEqual( len(maps), 0)

        # parse one fasta via a unode ..
        self.upapa_class.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA
        )
        # map with one parsed fasta
        maps = self.upapa_class.map_peptide( peptide='KLEINER', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 1)
        # parse another fasta via a different unode ..
        self.upapa_class.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA_TWO
        )
        # map with two parsed fastas

        maps = self.upapa_class.map_peptide( peptide='KLEINER', fasta_name='Test.fasta')
        print(maps)
        self.assertEqual( len(maps), 2)

    def test_fasta_id_parsed_and_available(self):
        input_fastas = []
        for line in TEST_FASTA:
            if line.startswith('>'):
                input_fastas.append( line[1:].strip() )

        self.assertEqual(
            sorted(self.upapa_class.fasta_sequences['Test.fasta'].keys()),
            sorted( input_fastas )
        )

    def test_peptide_eq_word_len(self):
        # print( self.upapa_class['Test.fasta'].keys())
        # print( ''.join(sorted('ELVIS')))
        # print( self.upapa_class['Test.fasta'][''.join(sorted('ELVIS'))] )
        self.assertEqual(
            self.upapa_class['Test.fasta'][''.join(sorted('ELVIS'))],
            set([
                ('Protein1', 1),
                ('Protein1', 5), # new srted algorithm to reduce mem print :)
                ('Protein1', 6),
                ('Protein3', 4),
                ('Protein3', 5),
                ('Protein3', 6)
            ])
        )

    def test_peptide_eq_word_len_2(self):
        maps = self.upapa_class.map_peptide( peptide='VISHE', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 1 )
        for mapping in maps:
                self.assertEqual(
                    'Protein3',
                    mapping['id']
                )

    def test_peptide_lt_word_len(self):
        expected = {
            'Protein1' : {
                'pre'   : 'V',
                'post'  : 'L',
                'start' : 4,
                'end'   : 5,
                'id'    : 'Protein1'
            },
            'ugly_fasta': {
                'pre'   : 'H',
                'post'  : '-',
                'start' : 6,
                'end'   : 7,
                'id'    : 'ugly_fasta'
            },

        }
        maps = self.upapa_class.map_peptide( peptide='IS', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 4 )
        for mapping in maps:
            if mapping['id'] == 'Protein1':
                self.assertEqual(
                    expected['Protein1'],
                    mapping
                )
            if mapping['id'] == 'ugly_fasta':
                self.assertEqual(
                    expected['ugly_fasta'],
                    mapping
                )

    def test_peptide_gt_word_len(self):
        expected = {
            'Protein1' : {
                'pre'   : 'L',
                'post'  : '-',
                'start' : 3,
                'end'   : 10,
                'id'    : 'Protein1'
            }
        }
        maps = self.upapa_class.map_peptide( peptide='VISLIVES', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 1 )
        for mapping in maps:
            if mapping['id'] == 'Protein1':
                self.assertEqual(
                    expected['Protein1'],
                    mapping
                )

    def test_purge_fasta(self):
        self.upapa_class.purge_fasta_info( 'Test.fasta')
        self.assertFalse(
            'Test.fasta' in self.upapa_class.keys()
        )

    def test_peptide_gt_word_but_not_continous(self):
        self.assertEqual(
            self.upapa_class.map_peptide(
                peptide='WHYELVIS',
                fasta_name='Test.fasta'
            ),
            []
        )

    def test_multiple_occurrence_in_one_seq(self):
        maps = self.upapa_class.map_peptide( peptide='AAAAAAAAAA', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 2 )
        sorted_maps = sorted( maps, key= lambda x: x['start'])
        self.assertEqual(
            sorted( maps, key= lambda x: x['start']),
            sorted(
                [
                    {
                        'pre'   : '_',
                        'post'  : '_',
                        'start' : 11,
                        'end'   : 20,
                        'id'    : 'T1'
                    },
                    {
                        'pre'   : '_',
                        'post'  : '-',
                        'start' : 41,
                        'end'   : 50,
                        'id'    : 'T1'
                    }

                ], key= lambda x: x['start']
            )
        )

    def test_multiple_occurrence_with_opverlap_in_one_seq(self):
        maps = self.upapa_class.map_peptide(
            peptide='GGGGGGG',
            fasta_name='Test.fasta'
        )
        self.assertEqual( len(maps), 4 )
        self.assertEqual(
            sorted([ m['start'] for m in maps] ),
            [1,2,3,4]
        )
        if regex_module_installed:
            #test short sequence, regex does not work with overlap
            maps = self.upapa_class.map_peptide(
                peptide='GGGG',
                fasta_name='Test.fasta'
            )
            self.assertEqual( len(maps), 7 )

    def test_sort_independece(self):
        map_1 = self.upapa_class.map_peptide(
            peptide    = 'FORWARD',
            fasta_name = 'Test.fasta'
        )
        map_2 = self.upapa_class.map_peptide(
            peptide    = 'DRAWROF',
            fasta_name = 'Test.fasta'
        )
        map_3 = self.upapa_class.map_peptide(
            peptide    = 'FORWA',
            fasta_name = 'Test.fasta'
        )
        map_4 = self.upapa_class.map_peptide(
            peptide    = 'AWROF',
            fasta_name = 'Test.fasta'
        )
        map_5 = self.upapa_class.map_peptide(
            peptide    = 'AORRW',
            fasta_name = 'Test.fasta'
        ) # should not work..

        self.assertEqual(len(map_1), 1)
        self.assertEqual(len(map_2), 1)
        self.assertEqual(len(map_3), 1)
        self.assertEqual(len(map_4), 1)
        self.assertEqual(len(map_5), 0)


if __name__ == '__main__':
    unittest.main()
