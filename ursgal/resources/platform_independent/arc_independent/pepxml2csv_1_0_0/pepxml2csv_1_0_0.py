#!/usr/bin/env python
"""
Converts Comet.pep.xml files into .csv
"""
import sys
import csv
import xml.etree.ElementTree as cElementTree


if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


def main(input_file=None, decoy_tag=None, output_file=None):
    '''
        Converts Comet.pep.xml files into .csv
    '''
    print("Converting Comet XML into CSV: {0}".format(input_file))
    NEW_HEADERS = [
        'Raw data location',
        'Spectrum ID',
        'Spectrum Title',
        'Retention Time (s)',
        'Rank',
        'Calc m/z',
        'Exp m/z',
        'Charge',
        'Sequence',
        'Modifications',
        'Comet:evalue',
        'Comet:xcorr',
        'Comet:spscore',
        'Comet:deltacn',
        'proteinacc_start_stop_pre_post_;',
        'Is decoy',
        'Start',
        'Stop',
    ]

    HEADER_TRANSLATIONS = {
        'spectrumNativeID': 'Spectrum Title',
        'start_scan': 'Spectrum ID',
        'assumed_charge': 'Charge',
        'retention_time_sec': 'Retention Time (s)',
        'peptide': 'Sequence',
        'expect': 'Comet:evalue',
        'xcorr': 'Comet:xcorr',
        'spscore': 'Comet:spscore',
        'deltacn': 'Comet:deltacn',
        'protein': 'proteinacc_start_stop_pre_post_;',
        'hit_rank': 'Rank'
    }

    PROTON = 1.00727646677

    with open(output_file, 'w') as result_file:
        print(f"[{'Info':^10s}] Writing Comet results, this can take a while...")

        csv_dict_write_object = csv.DictWriter(result_file, fieldnames=NEW_HEADERS)
        csv_dict_write_object.writeheader()

        print(f"[{'Sub':^10s}] Extracting info from XML file: {input_file}")
        cometXML = cElementTree.parse(input_file)
        row = 0

        for elem in cometXML.getroot():
            n_elements = len(elem.findall('{http://regis-web.systemsbiology.net/pepXML}spectrum_query'))
            print(f"[{'Info':^10s}] Total scans: {n_elements}")
            padding = len(str(n_elements))

            spectra_info = elem.attrib
            raw_data_location = raw_file = spectra_info['base_name'] + spectra_info['raw_data']
            for spectrum_query in elem:

                if 'spectrum_query' not in spectrum_query.tag:
                    continue

                row += 1
                if row % 500 == 0:
                    print(f"[{'Info':^10s}] Processing line number: {row: {padding}} / {n_elements: {padding}}",
                          end='\r')
                for search_result in spectrum_query:

                    n_search_hits = len(search_result)
                    if n_search_hits == 0:
                        continue

                    # General information about the Spectrum
                    info_spectrum_query = spectrum_query.attrib
                    for search_hit in search_result:

                        search_hit_info = search_hit.attrib
                        # Protein ID
                        proteins = [search_hit_info['protein']]

                        for search_hit_entry in search_hit:
                            # Peptide Modifications
                            tmp_mods = []
                            # Entry name
                            search_hit_tag = search_hit_entry.tag
                            if 'modification_info' in search_hit_tag:
                                # Extract all peptide modifications
                                for modification_entry in search_hit_entry:
                                    modification_entry_info = modification_entry.attrib
                                    position = modification_entry_info['position']
                                    mod_mass = modification_entry_info[
                                        'variable'] if 'variable' in modification_entry_info else \
                                        modification_entry_info['static']
                                    # Formatting modification
                                    new_mod = '{0}:{1}'.format(mod_mass, position)
                                    tmp_mods.append(new_mod)
                                # Concatenate into a string
                                modifications_ursgal_format = ';'.join(tmp_mods)
                                search_hit_info = {**search_hit_info, **{'Modifications': modifications_ursgal_format}}
                            elif 'search_score' in search_hit_tag:
                                score_info = search_hit_entry.attrib
                                search_hit_info = {**search_hit_info, **{score_info['name']: score_info['value']}}
                            elif 'alternative_protein' in search_hit_tag:
                                proteins.append(search_hit_entry.attrib['protein'])

                        search_hit_info = {**info_spectrum_query, **search_hit_info,
                                           **{'protein': ';'.join(proteins)}}
                        line_to_write = {}
                        for comet_header, translated_header in HEADER_TRANSLATIONS.items():
                            line_to_write[translated_header] = search_hit_info.get(comet_header, None)
                        line_to_write['Raw data location'] = raw_data_location
                        line_to_write['Modifications'] = search_hit_info.get('Modifications', None)
                        line_to_write['Exp m/z'] = (float(search_hit_info['precursor_neutral_mass']) / float(
                            search_hit_info['assumed_charge'])) + PROTON
                        line_to_write['Calc m/z'] = (float(search_hit_info['calc_neutral_pep_mass']) / float(
                            search_hit_info['assumed_charge'])) + PROTON
                        line_to_write['Is decoy'] = decoy_tag in line_to_write['proteinacc_start_stop_pre_post_;']
                        csv_dict_write_object.writerow(line_to_write)

    return output_file


if __name__ == '__main__':
    script = main(input_file=sys.argv[1], decoy_tag=sys.argv[2], output_file=sys.argv[3])
