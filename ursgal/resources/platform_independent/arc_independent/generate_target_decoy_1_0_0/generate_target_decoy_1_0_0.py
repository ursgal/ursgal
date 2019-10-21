#!/usr/bin/env python
# encoding: utf-8
"""
Generates a taget decoy database with consitent shuffled peptides
or reverse proteins

usage:
./generate_target_decoy_1_0_0.py <fastaDB1 fastaDB2 fastaDB3 ... fastaDBn>



Copyright 2013
by
Johannes Barth
Daniel Jaeger
Christian Fufezan
Stefan Schulze

"""

from __future__ import print_function
import sys
import random
import itertools
from collections import defaultdict as ddict
import ursgal
import re


def main(
    input_files=None,
    output_file=None,
    enzyme=None,
    decoy_tag='decoy_',
    mode='shuffle_peptide',
    convert_aa_in_motif=None,  # 'new_aa,motif,position_to_be_replaced'
):

    # first do the redundancy check of aa seqeucnes...
    sequenceFastaDict = ddict(list)
    print("Checking for redundancy of protein sequences...", file=sys.stderr)
    for fastaFile in input_files:
        for fastaID, sequence in ursgal.ucore.parse_fasta(open(fastaFile, "r")):
            if 'REVERSED' in fastaID:
                continue
            sequenceFastaDict[sequence].append(fastaID)
    print("Done!", file=sys.stderr)

    perDict = {}
    fastaDict = {}
    goodLookUp = {}
    unmutableTPSet = set()  # has to be on pep level since we add some later during ranking
    mutableTPSet = set()

    def generateMergedFastaKey(IDList):
        """Format the fastaID in the right way """
        if len(IDList) > 1:
            key = '{0}_NumberOfIdenticalSequences_{1}'.format(
                IDList[0],
                len(IDList)
            )
        else:
            key = '{0}'.format(IDList[0])
        return key

    def generateConvertedSequence(sequence, convert_aa_in_motif):
        '''
        Check if sequence has motif and if yes, replace specified aminoacid.
        
        Returns:
            str: new/converted sequence
        '''
        new_aa, motif, position = convert_aa_in_motif.split(',')
        matches = []
        for match in re.finditer(motif, sequence):
            matches.append(match.span())
        new_sequence = ''
        prev_end = 0
        for start, end in matches:
            new_sequence += sequence[prev_end:start]
            new_sequence += sequence[start:start + int(position)] + new_aa +\
                sequence[start + int(position) + 1:end]
            prev_end = end
        new_sequence += sequence[prev_end:len(sequence)]
        return new_sequence

    uniqueModels = list()
    nonUniqueModels = list()
    listNonUniqueModels = list()

    final_output = {}

    cleavage_aa, site, inhibitor = enzyme.split(';')

    counter = 0
    for sequence, fastaIDList in sequenceFastaDict.items():
        fastaID = generateMergedFastaKey(fastaIDList)
        if len(fastaIDList) > 1:
            nonUniqueModels.append(fastaID)
            listNonUniqueModels += fastaIDList
        else:
            uniqueModels.append(fastaID)
        #print(fastaID,file = sys.stderr )
        counter += 1
        if counter % 100 == 0:
            print(
                'Processing sequence #{0}/{1}'.format(
                    counter,
                    len(sequenceFastaDict.keys())
                ),
                end='\r',
                file=sys.stderr
            )
        
        if convert_aa_in_motif is not None:
            sequence = generateConvertedSequence(sequence, convert_aa_in_motif)

        if mode == 'reverse_protein':
            if sequence[-1] == '*':
                sequence_without_terminator = sequence[:-1]
            else:
                sequence_without_terminator = sequence

            final_output[fastaID] = {
                'new_sequence_target': '{0}'.format(
                    sequence_without_terminator
                ),
                'new_sequence_decoy' : '{0}'.format(
                    sequence_without_terminator[::-1]
                )
            }
        elif mode == 'shuffle_peptide':
            peptideList = ursgal.ucore.digest(
                sequence,
                (cleavage_aa, site),
                no_missed_cleavages=True
            )
            fastaDict[fastaID] = {
                'seqLen'                   : len(sequence),
                'peptides'                 : peptideList,
                'lengthOfDecoyablePetides' : 1
            }

            for n, peptide in enumerate(peptideList):
                # print(peptide)
                character_to_preserve_C = ''
                character_to_preserve_N = ''
                terminal_peptide_N = False
                terminal_peptide_C = False
                if n == 0 :
                    terminal_peptide_N = True
                if n == len(peptideList) - 1:
                    terminal_peptide_C = True
                if site == 'C':
                    if peptide[-1] in cleavage_aa:
                        character_to_preserve_C = peptide[-1]
                        if peptide[0] in inhibitor and terminal_peptide_N is False:
                            character_to_preserve_N = peptide[0]
                            peptideWithoutCleavageAA = peptide[1 :-1]
                        else:
                            peptideWithoutCleavageAA = peptide[:-1]
                    else:
                        peptideWithoutCleavageAA = peptide
                elif site == 'N':
                    if peptide[0] in cleavage_aa:
                        character_to_preserve_N = peptide[0]
                        if peptide[-1] in inhibitor and terminal_peptide_C is False:
                            character_to_preserve_C = peptide[-1]
                            peptideWithoutCleavageAA = peptide[1 :-1]
                        else:
                            peptideWithoutCleavageAA = peptide[1:]
                    else:
                        peptideWithoutCleavageAA = peptide
                else:
                    print('''
                        No cleavage site for {0} defined.
                        Please add this information to uparams.py
                        (enzyme --> generate_target_decoy_style_1)
                        '''.format(enzyme))
                    sys.exit(1)
                aaString = ''.join(sorted(peptide))
                if aaString not in perDict.keys():
                    perDict[aaString] = {
                        'permutations'  : [],
                        'pepProtTuples' : set(),
                        'peptides'      : set(),
                        'mutable'       : True,
                        'permutated'    : False
                    }

                if len(peptide) < 8:
                    if perDict[aaString]['permutated'] is False:
                        for permutation in itertools.permutations(peptideWithoutCleavageAA, len(peptideWithoutCleavageAA)):
                            permutedSequence = '{0}{1}{2}'.format(
                                character_to_preserve_N,
                                ''.join(permutation),
                                character_to_preserve_C
                            )
                            check = check_decoy_sequence(
                                permuted_sequence=permutedSequence,
                                cleavage_site=site,
                                inhibitor=inhibitor,
                                terminal_peptide_N=terminal_peptide_N,
                                terminal_peptide_C=terminal_peptide_C,
                                preserved_C=character_to_preserve_C,
                                preserved_N=character_to_preserve_N,
                            )
                            if check is False:
                                continue
                            perDict[aaString]['permutations'].append(
                                permutedSequence)

                        perDict[aaString]['permutations'] = list(
                            set(perDict[aaString]['permutations'])
                        )
                        perDict[aaString]['permutated'] = True

                    if peptide in perDict[aaString]['permutations']:
                        perDict[aaString]['permutations'].remove(peptide)

                    perDict[aaString]['pepProtTuples'].add((peptide, fastaID))
                    perDict[aaString]['peptides'].add(peptide)
                else:
                    if perDict[aaString]['mutable']:
                        a = 50000  # math.factorial(len(list2shuffle)) * 10
                        list2shuffle = list(peptideWithoutCleavageAA)
                        while a:
                            random.shuffle(list2shuffle)

                            shuffled_peptide = '{0}{1}{2}'.format(
                                character_to_preserve_N,
                                ''.join(list2shuffle),
                                character_to_preserve_C
                            )

                            check = check_decoy_sequence(
                                permuted_sequence=shuffled_peptide,
                                cleavage_site=site,
                                inhibitor=inhibitor,
                                terminal_peptide_N=terminal_peptide_N,
                                terminal_peptide_C=terminal_peptide_C,
                                preserved_C=character_to_preserve_C,
                                preserved_N=character_to_preserve_N,
                            )

                            if shuffled_peptide != peptide and check is True:
                                if shuffled_peptide not in perDict[aaString]['permutations']:
                                    perDict[aaString]['permutations'].append(
                                        shuffled_peptide)
                                    perDict[aaString]['pepProtTuples'].add(
                                        (peptide, fastaID))
                                    perDict[aaString]['peptides'].add(peptide)
                                    break
                            a -= 1
                        if a == 0:
                            perDict[aaString]['mutable'] = False
                            unmutableTPSet.add(peptide)

        else:
            print('Mode {0} not specified'.format(mode))
            sys.exit(1)

    if mode == 'shuffle_peptide':
        for aaString in perDict.keys():
            if len(perDict[aaString]["permutations"]) >= len(perDict[aaString]["peptides"]):
                for peptide, fastaID in perDict[aaString]["pepProtTuples"]:
                    randomPos = random.randrange(
                        len(perDict[aaString]["permutations"]))
                    if peptide not in mutableTPSet:
                        goodLookUp[peptide] = perDict[
                            aaString]["permutations"][randomPos]
                    mutableTPSet.add(peptide)
                    fastaDict[fastaID][
                        'lengthOfDecoyablePetides'] += len(aaString)

            elif len(perDict[aaString]['permutations']) == 0:
                unmutableTPSet |= perDict[aaString]['peptides']

        for aaString in perDict.keys():
            if 0 < len(perDict[aaString]['permutations']) < len(perDict[aaString]['peptides']):
                tmp = sorted([(fastaDict[fastaID]['seqLen'] / fastaDict[fastaID]['lengthOfDecoyablePetides'] ,
                               fastaID, peptide) for peptide, fastaID in perDict[aaString]['pepProtTuples']])

                for n, (coverage, fastaID, peptide) in enumerate(tmp):
                    if n >= len(perDict[aaString]['permutations']):
                        unmutableTPSet.add(peptide)
                        #print('Forever alone :', peptide , file = sys.stderr )
                    else:
                        mutableTPSet.add(peptide)
                        goodLookUp[peptide] = perDict[
                            aaString]['permutations'][n]
                        fastaDict[fastaID][
                            'lengthOfDecoyablePetides'] += len(aaString)
        print(
            'Mutable: {0}, not mutable : {1}, i.e. {2:4.3f}%'.format(
                len(mutableTPSet),
                len(unmutableTPSet),
                100.0 * len(unmutableTPSet) / len(mutableTPSet)
            ),
            file=sys.stderr
        )
        c = ddict(int)
        counter = 0
        for sequence, fastaIDList in sequenceFastaDict.items():
            fastaID = generateMergedFastaKey(fastaIDList)
            counter += 1
            if counter % 100 == 0:
                print(
                    'Buffering new sequence #{0}/{1}'.format(
                        counter,
                        len(sequenceFastaDict)
                    ),
                    end="\r",
                    file=sys.stderr
                )

            if convert_aa_in_motif is not None:
                sequence = generateConvertedSequence(sequence, convert_aa_in_motif)

            peptideList = ursgal.ucore.digest(
                sequence,
                (cleavage_aa, site),
                no_missed_cleavages=True
            )
            originalSequence = []
            shuffledSequence = []
            for peptide in peptideList:
                originalSequence.append(peptide)
                if peptide not in goodLookUp.keys():
                    shuffledPeptide = peptide
                else:
                    shuffledPeptide = goodLookUp[peptide]
                shuffledSequence.append(shuffledPeptide)
                if peptide in unmutableTPSet:
                    c[peptide] += 1
            new_sequence_target = "".join(originalSequence)
            new_sequence_decoy = "".join(shuffledSequence)
            if len(new_sequence_decoy) == 0 or len(new_sequence_target) == 0:
                print(
                    "WARNING: FastaID: {0} has sequence with length zero".format(
                        fastaID
                    ),
                    file=sys.stderr
                )
                continue
            final_output[fastaID] = {
                'new_sequence_target' : new_sequence_target,
                'new_sequence_decoy'  : new_sequence_decoy
            }
        unmutable_peptides = output_file + '_unmutable_peptides.txt'
        print(
            'Writing unmutable peptides in {0}'.format(
                unmutable_peptides
            ),
            file=sys.stderr
        )

        with open(unmutable_peptides , 'w') as io:
            for v, k in sorted([(v, k) for k, v in c.items()], reverse=True):
                print(
                    '{0: >10}\t{1}'.format(
                        v,
                        k
                    ),
                    file=io
                )

    print(file=sys.stderr)
    # NOTE the reduncdancy printout:
    print(
        '=== Number of NON UNIQUE protein models with the same sequence ==='
    )
    print(
        '{0} These were merged to {1} new protein model names'.format(
            len(listNonUniqueModels),
            len(nonUniqueModels)
        ),
        file=sys.stderr
    )

    print(
        '=== Number of UNIQUE protein models ==='
    )
    print(
        '{0}'.format(
            len(uniqueModels)
        ),
        file=sys.stderr
    )

    opened_output_file = open(
        output_file,
        'w'
    )
    if sys.platform == 'win32':
        line_ending = '\n'
    else:
        line_ending = '\r\n'
    total_sequences_2_write = len(final_output.keys())
    for n, (fastaID, sequence_dict) in enumerate(final_output.items()):
        if n % 100 == 0:
            print(
                'Writing new sequence #{0}/{1}'.format(
                    n,
                    total_sequences_2_write
                ),
                end="\r",
                file=sys.stderr
            )
        new_sequence_target = sequence_dict['new_sequence_target']
        new_sequence_decoy = sequence_dict['new_sequence_decoy']
        # targets, just print the sequence
        print(">{0}".format(fastaID), file=opened_output_file, end=line_ending)
        for pos, _ in enumerate(new_sequence_target):
            print(_, end="", file=opened_output_file)
            if (pos + 1) % 80 == 0:
                print(file=opened_output_file, end=line_ending)
        print('', file=opened_output_file, end=line_ending)
        # decoy, print the shuffled peptides

        print(">{0}{1}".format(decoy_tag, fastaID),
              file=opened_output_file, end=line_ending)

        for pos, _ in enumerate(new_sequence_decoy):
            print(_, end="", file=opened_output_file)
            if (pos + 1) % 80 == 0:
                print(file=opened_output_file, end=line_ending)
        print('', file=opened_output_file, end=line_ending)

    print(file=sys.stderr)

    return output_file


def check_decoy_sequence(
    permuted_sequence=None,
    cleavage_site=None,
    inhibitor=None,
    terminal_peptide_N=False,
    terminal_peptide_C=False,
    preserved_C=None,
    preserved_N=None
):
    allowed_decoy = True
    if cleavage_site == 'C':
        if permuted_sequence[0] in inhibitor and terminal_peptide_N is False:
            if permuted_sequence[0] not in preserved_N:
                allowed_decoy = False
    elif cleavage_site == 'N':
        if permuted_sequence[-1] in inhibitor and terminal_peptide_C is False:
            if permuted_sequence[-1] not in preserved_C:
                allowed_decoy = False
    return allowed_decoy

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(__doc__)
    else:
        output_file = 'BSA_target_decoy_test.fasta'
        name_of_db = main(
            sys.argv[1:],
            output_file,
            enzyme=('RK;C;P'),
            mode='shuffle_peptide'
        )
        print(name_of_db)
