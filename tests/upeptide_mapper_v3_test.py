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
    'censorTHIS*',
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
        upapa_class = self.uc.unodes['upeptide_mapper_1_0_0']['class'].import_engine_as_python_function(
            'UPeptideMapper_v3'
        )
        self.database_path =  os.path.join(
            'tests',
            'data',
            'Test.fasta'
        )
        with open(self.database_path, 'w') as io:
            for line in TEST_FASTA:
                print(line.strip(), file=io )
        # print(upapa_class)
        self.upapa_class = upapa_class(
            fasta_database = self.database_path
        )

    def test_purge_fasta(self):
        self.upapa_class.purge_fasta_info( 'Test.fasta' )
        self.assertFalse(
            'Test.fasta' in self.upapa_class.protein_sequences.keys()
        )
        self.assertFalse(
            'Test.fasta' in self.upapa_class.protein_indices.keys()
        )
        self.assertFalse(
            'Test.fasta' in self.upapa_class.peptide_2_protein_mappings.keys()
        )

    def test_fasta_id_parsed_and_available(self):
        input_fastas = []
        for line in TEST_FASTA:
            if line.startswith('>'):
                input_fastas.append( line[1:].strip() )

        self.assertEqual(
            sorted( self.upapa_class.protein_sequences['Test.fasta'].keys() ),
            sorted( input_fastas )
        )

    def test_peptide_mapping_1(self):
        self.upapa_class.map_peptides(
            [ 'ELVIS' ],
            'Test.fasta'
        )
        self.assertEqual(
            [ (d['id'], d['start']) for d in self.upapa_class.peptide_2_protein_mappings['Test.fasta']['ELVIS'] ],
            [
                ('Protein1', 1),
                ('Protein3', 6),
            ]
        )

    def test_peptide_mapping_2(self):
        maps = self.upapa_class.map_peptides( ['VISHE'], 'Test.fasta')['VISHE']
        self.assertEqual( len(maps), 1 )
        for mapping in maps:
            self.assertEqual(
                'Protein3',
                mapping['id']
            )

    def test_incremental_cache_buildups(self):
        '''

        '''
        self.upapa_class.cache_database(
            self.database_path,
            'Test.fasta'
        )
        # map with one parsed fasta
        maps = self.upapa_class.map_peptides( ['KLEINER'], 'Test.fasta')['KLEINER']
        # print(maps)
        # print(maps)
        self.assertEqual( len(maps), 1)
        tmp_database_path =  os.path.join(
            'tests',
            'data',
            'tmp_Test.fasta'
        )
        with open(tmp_database_path, 'w') as io:
            for line in TEST_FASTA_TWO:
                print(line.strip(), file=io )

        self.upapa_class.cache_database(
            tmp_database_path,
            'tmp_Test.fasta'
        )
        # exit()
        # print(self.upapa_class.automatons)
        # print(s)
        maps = self.upapa_class.map_peptides(
            ['KLEINER'],
            'Test.fasta'
        )['KLEINER']
        # print(self.upapa_class.peptide_2_protein_mappings)
        # print(maps)
        self.assertEqual(
            len(maps),
            1
         )
        # exit()
        self.assertEqual(
            len(
                self.upapa_class.map_peptides(
                    ['KLEINER'],
                    'tmp_Test.fasta'
                )['KLEINER']
            ),
            1
         )

        os.remove(tmp_database_path)


    # def test_peptide_lt_word_len(self):
    #     expected = {
    #         'Protein1' : {
    #             'pre'   : 'V',
    #             'post'  : 'L',
    #             'start' : 4,
    #             'end'   : 5,
    #             'id'    : 'Protein1'
    #         },
    #         'ugly_fasta': {
    #             'pre'   : 'H',
    #             'post'  : '-',
    #             'start' : 6,
    #             'end'   : 7,
    #             'id'    : 'ugly_fasta'
    #         },

    #     }
    #     maps = self.upapa_class.map_peptide( peptide='IS', fasta_name='Test.fasta')
    #     self.assertEqual( len(maps), 4 )
    #     for mapping in maps:
    #         if mapping['id'] == 'Protein1':
    #             self.assertEqual(
    #                 expected['Protein1'],
    #                 mapping
    #             )
    #         if mapping['id'] == 'ugly_fasta':
    #             self.assertEqual(
    #                 expected['ugly_fasta'],
    #                 mapping
    #             )

    # def test_peptide_gt_word_len(self):
    #     expected = {
    #         'Protein1' : {
    #             'pre'   : 'L',
    #             'post'  : '-',
    #             'start' : 3,
    #             'end'   : 10,
    #             'id'    : 'Protein1'
    #         }
    #     }
    #     maps = self.upapa_class.map_peptide( peptide='VISLIVES', fasta_name='Test.fasta')
    #     self.assertEqual( len(maps), 1 )
    #     for mapping in maps:
    #         if mapping['id'] == 'Protein1':
    #             self.assertEqual(
    #                 expected['Protein1'],
    #                 mapping
    #             )

   
    # def test_peptide_gt_word_but_not_continous(self):
    #     self.assertEqual(
    #         self.upapa_class.map_peptide(
    #             peptide='WHYELVIS',
    #             fasta_name='Test.fasta'
    #         ),
    #         []
    #     )

    # def test_multiple_occurrence_in_one_seq(self):
    #     maps = self.upapa_class.map_peptide( peptide='AAAAAAAAAA', fasta_name='Test.fasta')
    #     self.assertEqual( len(maps), 2 )
    #     sorted_maps = sorted( maps, key= lambda x: x['start'])
    #     self.assertEqual(
    #         sorted( maps, key= lambda x: x['start']),
    #         sorted(
    #             [
    #                 {
    #                     'pre'   : '_',
    #                     'post'  : '_',
    #                     'start' : 11,
    #                     'end'   : 20,
    #                     'id'    : 'T1'
    #                 },
    #                 {
    #                     'pre'   : '_',
    #                     'post'  : '-',
    #                     'start' : 41,
    #                     'end'   : 50,
    #                     'id'    : 'T1'
    #                 }

    #             ], key= lambda x: x['start']
    #         )
    #     )

    # def test_multiple_occurrence_with_opverlap_in_one_seq(self):
    #     maps = self.upapa_class.map_peptide(
    #         peptide='GGGGGGG',
    #         fasta_name='Test.fasta'
    #     )
    #     self.assertEqual( len(maps), 4 )
    #     self.assertEqual(
    #         sorted([ m['start'] for m in maps] ),
    #         [1,2,3,4]
    #     )
    #     if regex_module_installed:
    #         #test short sequence, regex does not work with overlap
    #         maps = self.upapa_class.map_peptide(
    #             peptide='GGGG',
    #             fasta_name='Test.fasta'
    #         )
    #         self.assertEqual( len(maps), 7 )

    # def test_sort_independece(self):
    #     map_1 = self.upapa_class.map_peptide(
    #         peptide    = 'FORWARD',
    #         fasta_name = 'Test.fasta'
    #     )
    #     map_2 = self.upapa_class.map_peptide(
    #         peptide    = 'DRAWROF',
    #         fasta_name = 'Test.fasta'
    #     )
    #     map_3 = self.upapa_class.map_peptide(
    #         peptide    = 'FORWA',
    #         fasta_name = 'Test.fasta'
    #     )
    #     map_4 = self.upapa_class.map_peptide(
    #         peptide    = 'AWROF',
    #         fasta_name = 'Test.fasta'
    #     )
    #     map_5 = self.upapa_class.map_peptide(
    #         peptide    = 'AORRW',
    #         fasta_name = 'Test.fasta'
    #     ) # should not work..

    #     self.assertEqual(len(map_1), 1)
    #     self.assertEqual(len(map_2), 1)
    #     self.assertEqual(len(map_3), 1)
    #     self.assertEqual(len(map_4), 1)
    #     self.assertEqual(len(map_5), 0)


if __name__ == '__main__':
    unittest.main()
