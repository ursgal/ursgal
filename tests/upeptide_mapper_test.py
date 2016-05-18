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
]


class UMapMaster(unittest.TestCase):
    def setUp(self):
        self.upapa_5 = umama.UPeptideMapper( word_len=5 )
        self.upapa_5.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA
        )

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
        self.assertEqual(
            self.upapa_5['Test.fasta']['ELVIS'],
            set([
                ('Protein1', 1),
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
            }
        }
        for mapping in self.upapa_5.map_peptide( peptide='IS', fasta_name='Test.fasta'):
            if mapping['id'] == 'Protein1':
                self.assertEqual(
                    expected['Protein1'],
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
