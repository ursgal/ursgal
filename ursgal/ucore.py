#!/usr/bin/env python
import re
import sys
import os
import csv
from ursgal import ukb
from ursgal import UNode
from collections import Counter, defaultdict

PROTON = ukb.PROTON

COLORS = {
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'BLINK': '\033[5m',
    'BLACK': '\033[30m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
    'GREY': '\033[90m',
    'BRED': '\033[91m',
    'BGREEN': '\033[92m',
    'BYELLOW': '\033[93m',
    'BBLUE': '\033[94m',
    'BMAGENTA': '\033[95m',
    'BCYAN': '\033[96m',
    'BWHITE': '\033[97m',
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


def print_current_params(params, old_params=None):
    '''
    Function to print current params

    Keyword Arguments:
            params (dict): parameter dict to print

    '''
    skipped_unchanged_params = 0
    print('\tCurrent parameters:')
    print('\t-->>')
    for k, v in sorted(params.items()):
        # if k in params['skipped_params_for_pprint_output']:
        #     continue
        if old_params is not None and k in old_params.keys():
            if params[k] == old_params[k]:
                skipped_unchanged_params += 1
        if isinstance(v, str) and len(v) > 70:
            printable_v = v[:10] + ' ... ' + v[-50:]
        else:
            printable_v = v
        print('{0: >42} : {1}'.format(k, printable_v))
    if old_params is not None and skipped_unchanged_params > 0:
        print('\t{0} parameters have not been changed since last printout, thus skipped '.format(
            skipped_unchanged_params))
    print()


def convert_ppm_to_dalton(ppm_value, base_mz=1000.0):
    '''
        Normalize the precision in ppm to 1000 Dalton

        Keyword Arguments:
            ppm_value (float): parts per million value to transform
            base_mz (float): factor for transformation


        Returns:
            float: value in Dalton
    '''
    return float(ppm_value) / float(base_mz)


def convert_dalton_to_ppm(da_value, base_mz=1000.0):
    '''
        Convert the precision in Dalton to ppm

        Keyword Arguments:
            da_value (float): Dalton value to transform
            base_mz (float): factor for transformation


        Returns:
            float: value in ppm
    '''
    return float(da_value) * float(base_mz)


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
    calc_mz = (mass + (charge * PROTON)) / charge
    return calc_mz

def calculate_mass(mz, charge):
    '''
    Calculate mass function

    Keyword Arguments:
        mz (float): mz of molecule/peak
        charge (int): charge for calculating mass


    Returns:
        float: calculated mass

    '''
    mz = float(mz)
    charge = int(charge)
    calc_mass = mz * charge - (charge * PROTON)
    return calc_mass


def digest(sequence, enzyme, count_missed_cleavages=None, no_missed_cleavages=False):
    '''
    Amino acid digest function

    Keyword Arguments:
        sequence (str): amino acid sequence to digest
        enzyme (tuple): enzyme properties used for cleavage ('aminoacid(s)', 'N/C(terminus)')
                        e.g. ('KR','C') for trypsin
        count_missed_cleavages (int): number of miss cleavages allowed

    Returns:
        list: list of digested peptides

    '''
    tmp = ''
    result = []
    additionals = list()
    # for backwards compatibility e.g. sole use of kwarg "no_missed_cleavages"
    # and no use of no_missed_cleavages
    if count_missed_cleavages is None: # i.e. not set
        if no_missed_cleavages is False:
            count_missed_cleavages = 2
        else:
            count_missed_cleavages = 0

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
    if count_missed_cleavages > len(result):
        count_missed_cleavages = len(result)

    if count_missed_cleavages == 0:
        additionals = result
    else:
        for r in range(len(result)):
            # r is the index of each fully-cleaved peptide in the list from above
            for mc in range(r, len(result) + 1):
                # now starting with 'r' we interrogate all other pepitdes and build further peptides
                # up to the desired number of missed cleavages
                if mc - r >= count_missed_cleavages:
                    continue
                if mc + 2 > len(result):
                    # i.e. if are over end of list
                    continue
                # need to add 2 to mc a it's a location marker.
                # mc is essentially the first peptide in the list
                newpep = ''.join(result[r: mc + 2])
                if newpep != '':
                    additionals.append(newpep)
        additionals += result
    return additionals

def pyteomics_cleave(sequence, rule, missed_cleavages=0, min_length=None, max_length=100):
    import itertools as it
    from collections import deque
    """This function has been taken and modified from Pyteomics

    Levitsky, L.I.; Klein, J.; Ivanov, M.V.; and Gorshkov, M.V. (2018)
    "Pyteomics 4.0: five years of development of a Python proteomics framework",
    Journal of Proteome Research. DOI: 10.1021/acs.jproteome.8b00717

    Cleaves a polypeptide sequence using a given rule.

    Parameters
    ----------
    sequence : str
        The sequence of a polypeptide (in one-letter uppercase notation).

    rule : regex
        a `regular expression <https://docs.python.org/library/re.html#regular-expression-syntax>`_
        describing the site of cleavage. It is recommended
        to design the regex so that it matches only the residue whose C-terminal
        bond is to be cleaved. All additional requirements should be specified
        using `lookaround assertions
        <http://www.regular-expressions.info/lookaround.html>`_.
    missed_cleavages : int, optional
        Maximum number of allowed missed cleavages. Defaults to 0.
    min_length : int or None, optional
        Minimum peptide length. Defaults to :py:const:`None`.
    max_length: int or None, optional
        Maximum peptide length. Defaults to 100.

    Returns
    -------
    out : list
        A list of tuples with (peptide sequence, start position, stop position).
        Positions are starting with 1 for the first amino acid.
    """
    peptides = []
    ml = missed_cleavages+2
    trange = range(ml)
    cleavage_sites = deque([0], maxlen=ml)
    if min_length is None:
        min_length = 1
    cl = 1
    for i in it.chain([x.end() for x in re.finditer(rule, sequence)],
                   [None]):
        cleavage_sites.append(i)
        if cl < ml:
            cl += 1
        for j in trange[:cl-1]:
            seq = sequence[cleavage_sites[j]:cleavage_sites[-1]]
            if seq and min_length <= len(seq) <= max_length:
                peptides.append((seq, j, cleavage_sites[-1]))
    return peptides


def parse_fasta(io):
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


def reformat_peptide(regex_pattern, unimod_name, peptide):
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
                mods.append((int(pos), uni_mod, 'old', 0))

    compiled_pattern = re.compile(regex_pattern)

    peptide = peptide.replace('_', '')  # strip the underscores

    matched_mod_position = []
    for match_number, match in enumerate(re.finditer(compiled_pattern, peptide)):
        original_match_start = match.start()
        original_match_end = match.end()
        match_length = original_match_end - original_match_start
        if unimod_name is None:
            mod_name = match.group(0)
        else:
            mod_name = unimod_name
        mods.append((
            original_match_start,
            mod_name,
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

        new_mods.append('{0}:{1}'.format(
            mod_name,
            pos
        ))
        if mod_info == 'new':
            have_seen_new_mods = True
        total_match_length += match_length

    peptide = re.sub(regex_pattern, '', peptide)
    if len(new_mods) > 0:
        formated_peptide = '{0}#{1}'.format(peptide, ';'.join(new_mods))
    else:
        formated_peptide = peptide
    # print( mods, '>>>> ', new_mods )
    return formated_peptide


def count_distinct_psms(csv_file_path=None, psm_defining_colnames=None):
    '''
    Returns a counter based on PSM-defining column names (i.e spectrum & peptide,
    but also score field because sometimes the same PSMs are reported
    with different scores...).
    '''

    psm_counter = Counter()
    with open(csv_file_path, 'r') as in_file:
        csv_input = csv.DictReader(
            in_file
        )
        output_fieldnames = list(csv_input.fieldnames)
        for line_dict in csv_input:
            psm = tuple([line_dict[x]
                         for x in psm_defining_colnames if x in line_dict.keys()])
            psm_counter[psm] += 1

    return psm_counter


def merge_rowdicts(list_of_rowdicts, psm_colnames_to_merge_multiple_values, joinchar='<|>'):
    '''
    Merges CSV rows. If the column values are conflicting, they
    are joined with a character (joinchar).
    '''
    merged_d = {}
    fieldnames = []
    for rowdict in list_of_rowdicts:
        for k in rowdict.keys():
            if k not in fieldnames:
                fieldnames.append(k)
    for fieldname in fieldnames:
        values = []
        for d in list_of_rowdicts:
            if fieldname in d.keys():
                values.append(d[fieldname])
        if fieldname in psm_colnames_to_merge_multiple_values.keys():
            no_empty_values = [v for v in values if v != '']
            values_as_floats = [float(value) for value in no_empty_values]

            if psm_colnames_to_merge_multiple_values[fieldname] == 'max_value':
                merged_d[fieldname] = max(values_as_floats)

            elif psm_colnames_to_merge_multiple_values[fieldname] == 'min_value':
                merged_d[fieldname] = min(values_as_floats)

            elif psm_colnames_to_merge_multiple_values[fieldname] == 'avg_value':
                merged_d[fieldname] = sum(values_as_floats)/len(values_as_floats)

            elif psm_colnames_to_merge_multiple_values[fieldname] == 'most_frequent':
                value_occurences = Counter(no_empty_values)
                most_common_value, most_occurences = value_occurences.most_common(1)[0]
                value_occurences_dict = dict(value_occurences)
                final_values = []
                for value in no_empty_values:
                    if value in final_values:
                        continue
                    if value_occurences_dict[value] == most_occurences:
                        final_values.append(value)
                merged_d[fieldname] = joinchar.join(final_values)
        
        else:
            if len(set(values)) == 1:
                merged_d[fieldname] = values[0]
            else:
                no_empty_values = [v for v in values if v != '']
                if len(set(no_empty_values)) == 1:
                    merged_d[fieldname] = no_empty_values[0]
                else:
                    merged_d[fieldname] = joinchar.join(values)
    return merged_d


def merge_duplicate_psm_rows(csv_file_path=None, psm_counter=None, psm_defining_colnames=None, psm_colnames_to_merge_multiple_values={}, joinchar='<|>', overwrite_file=True):
    '''
    Rows describing the same PSM (e.g. when two proteins share the
    same peptide) are merged to one row.
    '''
    rows_to_merge_dict = defaultdict(list)

    if overwrite_file:
        tmp_file = csv_file_path + ".tmp"
        os.rename(csv_file_path, tmp_file)
        out_file = csv_file_path
    else:
        tmp_file = csv_file_path
        out_file = csv_file_path.strip('.csv') + '_merged_duplicates.csv'
    UNode.print_info(
        'Merging rows of the same PSM...',
        caller='postflight'
    )
    # print('Merging rows of the same PSM...')
    csv_kwargs = {}
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'
    with open(tmp_file, 'r') as tmp, open(out_file, 'w', newline='') as out:
        tmp_reader = csv.DictReader(tmp)
        writer = csv.DictWriter(
            out,
            fieldnames=tmp_reader.fieldnames,
            **csv_kwargs
        )
        writer.writeheader()
        for row in tmp_reader:
            psm = tuple([row[x]
                         for x in psm_defining_colnames if x in row.keys()])
            # each unique combination of these should only have ONE row!
            # i.e. combination of seq+spec+score
            if psm_counter[psm] == 1:
                # no duplicate = no problem, we can just write the row again
                writer.writerow(row)
            elif psm_counter[psm] > 1:
                # we have to collect all rows of this psm, and merge + write
                # them later!
                rows_to_merge_dict[psm].append(row)
            else:
                raise Exception("This should never happen.")
        # finished parsing the old unmerged unified csv
        for rows_to_merge in rows_to_merge_dict.values():
            writer.writerow(
                merge_rowdicts(rows_to_merge, psm_colnames_to_merge_multiple_values, joinchar=joinchar)
            )
    # remove the old unified csv that contains duplicate rows
    if overwrite_file:
        os.remove(tmp_file)
    UNode.print_info(
        'Done.',
        caller='postflight'
    )
    return out_file


if __name__ == '__main__':
    pass
