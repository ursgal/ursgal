#!/usr/bin/env python3.4
import re
import sys
import os

DIFFERENCE_14N_15N = 0.997035
PROTON             = 1.00727646677

COLORS = {
    'ENDC'      : '\033[0m',
    'BOLD'      : '\033[1m',
    'UNDERLINE' : '\033[4m',
    'BLINK'     : '\033[5m',

    'BLACK'     : '\033[30m',
    'RED'       : '\033[31m',
    'GREEN'     : '\033[32m',
    'YELLOW'    : '\033[33m',
    'BLUE'      : '\033[34m',
    'MAGENTA'   : '\033[35m',
    'CYAN'      : '\033[36m',
    'WHITE'     : '\033[37m',

    'GREY'      : '\033[90m',
    'BRED'      : '\033[91m',
    'BGREEN'    : '\033[92m',
    'BYELLOW'   : '\033[93m',
    'BBLUE'     : '\033[94m',
    'BMAGENTA'  : '\033[95m',
    'BCYAN'     : '\033[96m',
    'BWHITE'    : '\033[97m',
}

def terminal_supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise. Source:
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

if not terminal_supports_color():
    # disable terminal colors
    COLORS = {k: '' for k, v in COLORS.items()}

def print_current_params( params, old_params=None ):
    '''
    Function to print current params

    Keyword Arguments:
            params (dict): parameter dict to print

    '''
    skipped_unchanged_params = 0
    print('\tCurrent parameters:')
    print('\t-->>')
    for k, v in sorted( params.items() ):
        if k in params['skipped_params_for_pprint_output']:
            continue
        if old_params is not None and k in old_params.keys():
            if params[ k ] == old_params[k]:
                skipped_unchanged_params += 1
        if isinstance(v, str) and len(v) > 70:
            printable_v = v[:10] + ' ... ' + v[-50:]
        else:
            printable_v = v
        print('{0: >42} : {1}'.format(k, printable_v))
    if old_params is not None and skipped_unchanged_params > 0:
        print('\t{0} parameters have not been changed since last printout, thus skipped '.format(skipped_unchanged_params))
    print()


def convert_ppm_to_dalton( ppm_value, base_mz=1000.0 ):
    '''
        Normalize the precision in ppm to 1000 Dalton

        Keyword Arguments:
            ppm_value (float): parts per million value to transform
            base_mz (float): factor for transformation
          

        Returns:
            float: value in Dalton
    '''
    return float(ppm_value) / float(base_mz)


def calculate_mz(mass, charge):
    '''
    Calculate m/z function

    Keyword Arguments:
        mass (float): mass for calculating m/z
        charge (int): charge for calculating m/z
      

    Returns:
        float: calculated m/z

    '''
    mass = float(mass)
    charge = int(charge)
    calc_mz = ( mass + (charge * PROTON) ) / charge
    return calc_mz



def digest(sequence , enzyme, no_missed_cleavages = False):
    '''
    Amino acid digest function

    Keyword Arguments:
        sequence (str): amino acid sequence to digest
        enzyme (tuple): enzyme properties used for cleavage ('aminoacid(s)', 'N/C(terminus)')
                        e.g. ('KR','C') for trypsin
        no_missed_cleavages (bool): allow missed cleavages or not

    Returns:
        list: list of digestes peptides

    '''
    tmp = ''
    result = []
    additionals = list()
    cleavage_aa, site = enzyme
    for p, aa in enumerate(sequence):
        if aa == '*':
            continue
        tmp += aa
        if aa in cleavage_aa:
            if site == 'C':
                result.append(tmp)
                tmp = ''
            elif site == 'N':

                result.append(tmp[0:len(tmp) - 1])
                tmp = ''
                tmp += aa
    if tmp != '':
        result.append(tmp)
    if no_missed_cleavages:
        additionals = result
    else:
        for _ in range(len(result) - 1):
            try:
                additionals.append(
                    result[ _ ] + result[ _ + 1 ]
                )
            except:
                pass
            try:
                additionals.append(
                    result[ _ ] + result[ _ + 1 ] + result[ _ + 2 ])
            except:
                pass
        additionals += result
    return additionals


def parseFasta(io):
    '''
    Small function to efficiently parse a file in fasta format.

    Keyword Arguments:
        io (obj): openend file obj (fasta file)

    Yields:
        tuple: fasta_id and sequence
    '''
    id = None
    sequence = ''
    for line in io:
        line = line.strip()
        if line == '':
            continue
        if line[0] == '>':
            if id:
                yield(id, sequence)
            id = line[1:].strip()
            sequence = ''
        else:
            sequence += line
    if id:
        yield(id, sequence)


def reformat_peptide( regex_pattern, unimod_name, peptide ):
    '''
    reformats the MQ and Novor peptide string to ursgal format
    (ac)SSSLM(ox)RPGPSR --> SSSLMRPGPSR#Acetyl:0;Oxidation:5

    '''
    mods = []
    peptide = peptide.strip()
    if '#' in peptide:
        peptide, tmp_mods = peptide.split('#')
        if tmp_mods != '':
            for mod in tmp_mods.split(';'):
                uni_mod, pos = mod.split(':')
                mods.append( (int(pos), uni_mod, 'old', 0 ) )

    compiled_pattern = re.compile( regex_pattern )

    peptide = peptide.replace('_','')   #  strip the underscores

    matched_mod_position =[]
    for match_number, match in enumerate( re.finditer(compiled_pattern,peptide)):
        original_match_start       = match.start()
        original_match_end        = match.end()
        match_length                  = original_match_end - original_match_start

        mods.append( (
            original_match_start,
            unimod_name,
            'new',
            match_length
        ))

    mods.sort()
    new_mods = []
    total_match_length = 0
    have_seen_new_mods = False
    for pos, mod_name, mod_info, match_length in mods:

        if have_seen_new_mods:
            pos -= total_match_length

        new_mods.append( '{0}:{1}'.format(
            mod_name,
            pos
        ))
        if mod_info == 'new':
            have_seen_new_mods = True
        total_match_length += match_length

    peptide = re.sub( regex_pattern, '', peptide )
    if len(new_mods) > 0:
        formated_peptide = '{0}#{1}'.format( peptide, ';'.join( new_mods ) )
    else:
        formated_peptide = peptide
    # print( mods, '>>>> ', new_mods )
    return formated_peptide



if __name__ == '__main__':
    pass
