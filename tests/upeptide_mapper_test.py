#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import unittest
import pprint
from ursgal import umapmaster as umama


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
    'FCKTHIS*'
]

TEST_FASTA_TWO = [
    '>Ze_other_protein2\n',
    'KLEINERRETTER\n',
]


class UMapMaster(unittest.TestCase):
    def setUp(self):
        self.upapa_5 = umama.UPeptideMapper( word_len=5 )
        self.upapa_5.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA
        )
        self.uc = ursgal.UController( verbose = False )

    def test_incremental_fcache_buildup_and_global_access(self):
        # map with empty
        maps = self.uc.upeptide_mapper.map_peptide( peptide='KLEINER', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 0)

        # parse one fasta via a unode ..
        self.uc.unodes['merge_csvs_1_0_0']['class'].upeptide_mapper.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA
        )
        # map with one parsed fasta
        maps = self.uc.upeptide_mapper.map_peptide( peptide='KLEINER', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 1)
        # parse another fasta via a different unode ..
        self.uc.unodes['generate_target_decoy_1_0_0']['class'].upeptide_mapper.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA_TWO
        )
        # map with two parsed fastas

        maps = self.uc.upeptide_mapper.map_peptide( peptide='KLEINER', fasta_name='Test.fasta')
        print(maps)
        self.assertEqual( len(maps), 2)

    def test_fasta_id_parsed_and_available(self):
        input_fastas = []
        for line in TEST_FASTA:
            if line.startswith('>'):
                input_fastas.append( line[1:].strip() )

        self.assertEqual(
            sorted(self.upapa_5.fasta_sequences['Test.fasta'].keys()),
            sorted( input_fastas )
        )

    def test_peptide_eq_word_len(self):
        # print( self.upapa_5['Test.fasta'].keys())
        # print( ''.join(sorted('ELVIS')))
        # print( self.upapa_5['Test.fasta'][''.join(sorted('ELVIS'))] )
        self.assertEqual(
            self.upapa_5['Test.fasta'][''.join(sorted('ELVIS'))],
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
        maps = self.upapa_5.map_peptide( peptide='VISHE', fasta_name='Test.fasta')
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
        maps = self.upapa_5.map_peptide( peptide='IS', fasta_name='Test.fasta')
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
        maps = self.upapa_5.map_peptide( peptide='VISLIVES', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 1 )
        for mapping in maps:
            if mapping['id'] == 'Protein1':
                self.assertEqual(
                    expected['Protein1'],
                    mapping
                )

    def test_purge_fasta(self):
        self.upapa_5.purge_fasta_info( 'Test.fasta')
        self.assertFalse(
            'Test.fasta' in self.upapa_5.keys()
        )

    def test_peptide_gt_word_but_not_continous(self):
        self.assertEqual(
            self.upapa_5.map_peptide(
                peptide='WHYELVIS',
                fasta_name='Test.fasta'
            ),
            []
        )

    def test_multiple_occurrence_in_one_seq(self):
        maps = self.upapa_5.map_peptide( peptide='AAAAAAAAAA', fasta_name='Test.fasta')
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
        maps = self.upapa_5.map_peptide( peptide='GGGGGGG', fasta_name='Test.fasta')
        self.assertEqual( len(maps), 4 )
        self.assertEqual(
            sorted([ m['start'] for m in maps] ),
            [1,2,3,4]
        )

if __name__ == '__main__':
    unittest.main()
