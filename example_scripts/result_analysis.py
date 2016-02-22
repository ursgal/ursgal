#!/usr/bin/env python3.4
# encoding: utf-8

import os
import csv
import ursgal
import sys
import shutil
from Bio import SeqIO

'''
The function Cre_PCGSD acts on a high resolution dataset and was thought to be the target of the last function comparative_analysis. 
The latter should compare the outputs of database and denovo engines. '''

def Cre_PCGSD ():
    database_path = 'C:/Cre_PCGSD/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta' #path to fasta database
    uc = ursgal.UController(
        profile = 'QExactive+',
        params = {
            'database' : database_path ,
            #'modifications' : [
            #    'M,opt,any,Oxidation',        # Met oxidation
            #    'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
            #    '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
            #],
        }
    )
    uc.scan_rt_lookup_path = 'C:/Cre_PCGSD/_ursgal_lookup.pkl' #path to pkl files

    if sys.platform == 'win32':
        msamanda = 'msamanda_1_0_0_5242'
    else: 
        msamanda = 'msamanda_1_0_0_5243'

    engine_list = [
        #'omssa',
        #'xtandem_piledriver',
        #'msgf',
        # msamanda,
        #'novor',
        'pepnovo',
        #'uninovo',
    ]
    mgf_path = 'C:/Cre_PCGSD/' #path to mgf files
    mgf_files = []
    for elem in os.listdir(mgf_path):
        if elem.endswith('.mgf'):
            mgf_files.append(mgf_path+elem)
    #        break #for only one mgf file

    unified_file_list = []
    for mgf_file in mgf_files:
        for engine in engine_list:
            unified_search_result_file = uc.search(
                input_file = mgf_file,
                engine     = engine,
                force      = True
            )
            unified_file_list.append(unified_search_result_file)

    uc.visualize(
        input_files    = unified_file_list,
        engine         = 'venndiagram',
    )

    return

def comparative_analysis( path_to_mgf, database_path ):
    
    #extracting information from the json helper file
    file_json_path = path_to_mgf.rstrip('.mgf')+'___unified.u_helper.u.json'
    if os.path.exists(file_json_path):
        json = ursgal.UNode().load_json(json_path = file_json_path)
        paths_of_dirs = json[0]['dir']
        unified_paths = json[0]['full']
        list_of_engines = json[0]['last_search_engine']
        engine_jsons = json[0]['json']
    else:
        print('NO JSON-FILE FOUND!')
    
    #check for denovo engines
    denovo = []
    search_engines = []
    json_paths = []

    #merge name of json-file with path to directory for getting complete path
    for engine in list_of_engines:
        for path in paths_of_dirs:
            for json in engine_jsons:
                if engine in path and engine in json:
                    json_paths.append(path+'\\'+json)

    #find out which engines are denovo engines/search engines                    
    for engine in list_of_engines:
        for path in json_paths:
            if engine in path:
                json_content = ursgal.UNode().load_json(json_path = path)
                for elem in json_content[3]['history']:
                    if 'denovo_engine' in json_content[3]['history'][json_content[3]['history'].index(elem)]['META_INFO']['engine_type'] \
                    and json_content[3]['history'][json_content[3]['history'].index(elem)]['META_INFO']['engine_type']['denovo_engine'] == True:
                        denovo.append(engine)
                    if 'search_engine' in json_content[3]['history'][json_content[3]['history'].index(elem)]['META_INFO']['engine_type'] \
                    and json_content[3]['history'][json_content[3]['history'].index(elem)]['META_INFO']['engine_type']['search_engine'] == True:
                        search_engines.append(engine)

    #search for all spectrums and sequences that were found in all search engines
    SE_spectrums = {}                    
    for i, engine in enumerate(search_engines):
        for path in unified_paths:
            if engine in path:
                with open(path) as unified:
                    reader = csv.DictReader(unified)
                    if i == 0:
                        for elem in reader:
                            SE_spectrums[elem['Spectrum Title']] = (elem['Sequence'],elem['Modifications'])
                    else:
                        tmp = {}
                        for elem in reader:
                            tmp[elem['Spectrum Title']] = (elem['Sequence'],elem['Modifications'])
                        for title in SE_spectrums.keys():
                            if title in tmp.keys() and SE_spectrums[title] == tmp[title]:
                                continue
                            else:
                                SE_spectrums[title] = '-'
    same_in_all_SEs = {} #gets all spectrum titles and sequences that were found in all search engines
    for title in SE_spectrums.keys():
        if SE_spectrums[title] != '-':
            same_in_all_SEs[title] = SE_spectrums[title]
        else:
            continue
    #print(same_in_all_SEs)
    print('Search engines found ',len(same_in_all_SEs.keys()),' overlapping hits.')

    #search for all spectrums and sequences that were found in all denovo engines
    denovo_spectrums = {}                    
    for i, engine in enumerate(denovo):
        for path in unified_paths:
            if engine in path:
                with open(path) as unified:
                    reader = csv.DictReader(unified)
                    if i == 0:
                        for elem in reader:
                            denovo_spectrums[elem['Spectrum Title']] = (elem['Sequence'],elem['Modifications'])
                    else:
                        tmp = {}
                        for elem in reader:
                            tmp[elem['Spectrum Title']] = (elem['Sequence'],elem['Modifications'])
                        for title in denovo_spectrums.keys():
                            if title in tmp.keys() and denovo_spectrums[title] == tmp[title]:
                                continue
                            else:
                                denovo_spectrums[title] = '-'
    same_in_all_denovos = {} #gets all spectrum titles and sequences that were found in all search engines
    for title in denovo_spectrums.keys():
        if denovo_spectrums[title] != '-':
            same_in_all_denovos[title] = denovo_spectrums[title]
        else:
            continue
    #print(same_in_all_denovos)
    print('Denovo engines found ',len(same_in_all_denovos.keys()),' overlapping hits.')
    
    #were sequences, that were found by search engines, also found by denovo engines?
    same_in_SE_denovo = {}
    for engine in denovo:
        #print(engine)
        for path in unified_paths:
            if engine in path:
                with open(path) as unified:
                    reader = csv.DictReader(unified)
                    tmp = {}
                    for elem in reader:
                        tmp[elem['Spectrum Title']] = (elem['Sequence'],elem['Modifications'])
                    for title in same_in_all_SEs.keys():
                        if title in tmp.keys() and same_in_all_SEs[title] == tmp[title]:
                            same_in_SE_denovo[engine] = {}
                            same_in_SE_denovo[engine][title] = (elem['Sequence'],elem['Modifications'])
                        else:
                            continue
    #print(same_in_SE_denovo)
    for engine in same_in_SE_denovo.keys():
        print('Out of ',len(same_in_all_SEs.keys()),' search engine hits ',engine,' found ',len(same_in_SE_denovo.keys()),' hits')
    #print(same_in_SE_denovo)

    #spectrum/sequence hits that were found with denovo engines, but not with search engines
    only_denovo = {}
    for engine in denovo:
        #print(engine)
        for path in unified_paths:
            if engine in path:
                with open(path) as unified:
                    reader = csv.DictReader(unified)
                    tmp = {}
                    for elem in reader:
                        tmp[elem['Spectrum Title']] = (elem['Sequence'],elem['Modifications'])
                    for title in tmp.keys():
                        if title not in same_in_all_SEs.keys():
                            only_denovo[engine] = {}
                            only_denovo[engine][title] = (elem['Sequence'],elem['Modifications'])
                        else:
                            continue

    #which sequences, that were only found by denovo engines can actually be found in the fasta database?
    only_denovo_in_fasta = {}
    for engine in only_denovo.keys():
        for title in only_denovo[engine].keys():
            for seq_record in SeqIO.parse(database_path,'fasta'):
                #print(seq_record.seq)
                if only_denovo[engine][title][0] in seq_record.seq:
                    only_denovo_in_fasta[engine] = {}
                    only_denovo_in_fasta[engine][title] = (elem['Sequence'],elem['Modifications'])
                else:
                    continue

    for engine in only_denovo.keys():
        if engine in only_denovo_in_fasta.keys():
            print('Out of ',len(only_denovo[engine].keys()),'hits only found by ',engine,' , ',len(only_denovo_in_fasta[engine].keys()),' hits could be found in fasta database')
        else:
            print('Out of ',len(only_denovo[engine].keys()),'hits only found by ',engine,' , 0 hits could be found in fasta database')
    return

def main():
    Cre_PCGSD()
    #mgf_path = ''
    #database_path = ''
    #comparative_analysis(mgf_path, database_path)
    return

if __name__ == '__main__':
    main()
