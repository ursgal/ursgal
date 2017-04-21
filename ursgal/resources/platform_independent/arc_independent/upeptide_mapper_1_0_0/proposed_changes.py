#!/usr/bin/env python

import ahocorasick


FASTA = [
    ('>MoA', 'A' * 5),
    ('>MoB', 'B' * 5),
    ('>MoC', 'C' * 5)
]

ALL_SEQS = '>>'.join( [ seq for (_id, seq) in FASTA ] )
# our mean delimiter that spares us the overlapping check :))
seqidx_to_fastaidx = {}

fullseq_pos = 0
for fasta_index, (_id, seq) in enumerate(FASTA):
    for x in range(len(seq)):
        fullseq_pos += 1
        seqidx_to_fastaidx[ fullseq_pos ] = fasta_index
    fullseq_pos += 2
    # our mean delimiter that spares us the overlapping check :))
# even sweeter with index bisecting in list of starting positions

au = ahocorasick.Automaton()
au.add_word('BBBB', ['BBBB', ':)'])
au.add_word('AABB', ['AABB', ':)'])
au.add_word('CCCC', ['CCCC', ':)'])
au.make_automaton()

for match in au.iter( ALL_SEQS ):
    seq_index, not_sure_what_do_with_this = match
    fastidx = seqidx_to_fastaidx[ seq_index ]
    print(match, 'match on', FASTA[ fastidx ])
