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
    'WHYISELVISHELEAVING\n'

]


class UMapMaster(unittest.TestCase):
    def setUp(self):
        self.upapa_5 = umama.UPeptideMapper( word_len=5 )
        self.upapa_5.build_lookup(
            fasta_name = 'Test.fasta',
            fasta_stream = TEST_FASTA
        )

    def test_fasta_id_parsed_and_available(self):
        self.assertEqual(
            sorted(self.upapa_5.fasta_sequences['Test.fasta'].keys()),
            ['Protein1', 'Protein2', 'Protein3']
        )

    def test_peptide_eq_word_len(self):
        self.assertEqual(
            self.upapa_5['Test.fasta']['ELVIS'],
            set([
                ('Protein1', 1),
                ('Protein3', 6)
            ])
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
        for mapping in self.upapa_5.map_peptide( peptide='VISLIVES', fasta_name='Test.fasta'):
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


if __name__ == '__main__':
    unittest.main()
