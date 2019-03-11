"""Read mgf file and write RT lookup pickle
"""
import hashlib
import os
import pickle
import re


def md5(fname):
    # from https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def generate_spectra(fh):
    """Generate spectra from openend mgf handle.

    Args:
        fh (IO): file obj
    Yields:
        spec_dict (dict): Dict contaning spec data
    """
    for line in fh:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('BEGIN IONS'):
            spec_dict = {
                'data': []
            }
        elif '=' in line:
            key, val = line.split('=', 1)
            spec_dict[key] = val
        elif line[0].isdigit():
            mz, i = line.strip().split()
            spec_dict['data'].append(
                (float(mz), float(i))
            )
        elif line.startswith('END IONS'):
            yield spec_dict


def main(input_file, output_file, rt_pickle_name, spec_id_regex, run_id_regex):
    """ead mgf file and write RT lookup pickle.

    Args:
        input_file (str): MGF input file path
        output_file (str): Outputfile name
        rt_pickle_name (str): Name of the RT pickle file
        spec_id_regex (str): Regex to extract spec ID from mgf title
        run_id_regex (str): Regex to extract run ID from mgf title

    Returns:
        Outputfile with RT pickle md5 hash
    """
    PRINT_MISSING_RT_WARNING = True
    lookup_path = os.path.join(
        os.path.dirname(input_file),
        rt_pickle_name
    )
    if os.path.exists(lookup_path):
        with open(lookup_path, 'rb') as fin:
            rt_dict = pickle.load(fin)
    else:
        rt_dict = {}
    input_base_wo_suffix, suff = os.path.splitext(os.path.basename(input_file))
    if input_base_wo_suffix not in rt_dict:
        tmp = {
            'rt_2_scan': {},
            'scan_2_rt': {},
            'scan_2_mz': {},
            'unit': 'minute'  # in mgf, its always seconds, but to stay compatible ..
        }
        spec_id_regex = re.compile(spec_id_regex)

        # rt = 0   # dev mgf has no rt ...

        with open(input_file) as fin:
            for spec_dict in generate_spectra(fin):
                spec_id = spec_id_regex.match(spec_dict['TITLE']).group(1)
                rt = float(spec_dict['RTINSECONDS']) / 60
                precursor_mz = float(spec_dict['PEPMASS'].strip())

                tmp['rt_2_scan'][rt] = int(spec_id)
                tmp['scan_2_rt'][int(spec_id)] = rt
                tmp['scan_2_mz'][int(spec_id)] = precursor_mz
        rt_dict[input_base_wo_suffix] = tmp
        with open(lookup_path, 'wb') as fout:
            pickle.dump(rt_dict, fout)
    with open(output_file, 'wt') as fout:
        md5_sum = md5(lookup_path)
        fout.write(md5_sum)
    return output_file
