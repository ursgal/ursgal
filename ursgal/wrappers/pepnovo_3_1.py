#!/usr/bin/env python
import ursgal
import os
import subprocess
import csv


class pepnovo_3_1( ursgal.UNode ):
    """
    PepNovo v3.1 UNode
    http://proteomics.ucsd.edu/Software/PepNovo/

    Reference:
    Ari M. Frank, Mikhail M. Savitski, Michael L. Nielsen, Roman A. Zubarev, and Pavel A. Pevzner (2007) De Novo Peptide Sequencing and Identification with Precision Mass Spectrometry, J. Proteome Res. 6:114-123.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'PepNovo',
        'version'            : 'v3.1',
        'release_date'       : None,
        'engine_type' : {
            'de_novo_search_engine' : True,
        },
        'input_extensions'   : ['.mgf'],
        'output_extensions'  : ['.csv'],
        'utranslation_style' : 'pepnovo_style_1',
        'in_development'     : False,
        'create_own_folder'  : True,
        'include_in_git'     : False,
        'distributable'      : True,
        'engine' : {
            'linux' : {
                '64bit' : {
                    'exe'            :'PepNovo_bin',
                    'url'            : '',
                    'zip_md5'        : '8f9d9125e79d7b27ffb6d60c0ccc0c97',
                    'additional_exe' : [],
                }
            },
            'darwin' : {
               '64bit' : {
                   'exe'             : 'PepNovo_bin',
               }
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'PepNovo.exe',
                }
            },
        },
        'citation' : \
            'Ari M. Frank, Mikhail M. Savitski, Michael L. Nielsen, Roman A. '\
            'Zubarev, and Pavel A. Pevzner (2007) De Novo Peptide Sequencing '\
            'and Identification with Precision Mass Spectrometry, J. Proteome '\
            'Res. 6:114-123.',
    }

    def __init__(self, *args, **kwargs):
        super(pepnovo_3_1, self).__init__(*args, **kwargs)
        self.available_mods = {
                    'Carbamidomethyl': {'fix': ('C', '+57'),
                                       'opt': ('HDE', '+57')},
                                       # 'N-term': 'NT+CAM'},
                    'Trp->Kynurenin': {'opt': ('W', '+4')},
                    'Cation:K': {'opt': ('SKNPLRVIEMDGA', '+38')},
                    'Cation:Na': {'opt': ('QVPNYTHDESFAMILG', '+22')},
                    'Acetyl': {'opt': ('LTSYGVMPDAK', '+42'),
                               'N-term': '^+42'},
                    'Carbamyl': {'opt': ('PANMETGDLFIQSVK', '+43')},
                    'Dehydrated': {'opt': ('EDST', '-18')},
                    'Dimethyl': {'opt': ('K', '+28')},
                    'Dioxidation': {'opt': ('MW', '+32')},
                    'Formyl': {'opt': ('ST', '+28')},
                    'Oxidation': {'opt': ('MHWDKNP', '+16')},
                    'Deamidated': {'opt': ('NQ', '+1')},
                    'Methyl': {'opt': ('CHKNQR', '+14'),
                               'N-term': '^+14'},
                    'Phospho': {'opt': ('STY', '+80')},
                    'Gln->pyro-Glu': {'opt': ('Q', '-17')},
                    'Amidated': {'C-term': '$-1'},
                    'Label:18O(1)': {'C-term': '$+2'},
                    }

        pass


    def preflight( self ):
        '''
        Formatting the command line via self.params

        Returns:
                dict: self.params
        '''
        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        self.params['translations']['tmp_output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file'] + '.tmp'
        )
        self.created_tmp_files.append( self.params['translations']['tmp_output_file_incl_path'])

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        if self.params['translations']['precursor_mass_tolerance_unit'] == 'ppm':
            self.params['translations']['precursor_mass_tolerance_plus'] = ursgal.ucore.convert_ppm_to_dalton(
                self.params['translations']['precursor_mass_tolerance_plus'],
                base_mz=self.params['translations']['base_mz']
            )
            self.params['translations']['precursor_mass_tolerance_minus'] = ursgal.ucore.convert_ppm_to_dalton(
                self.params['translations']['precursor_mass_tolerance_minus'],
                base_mz=self.params['translations']['base_mz']
            )
        print(
            '''
            [ WARNING ] precursor_mass_tolerance_plus and precursor_mass_tolerance_minus
            [ WARNING ] need to be combined for pepnovo_3_1 (use of symmetric tolerance window).
            [ WARNING ] The arithmetic mean is used.
            '''
        )
        self.params['translations']['precursor_mass_tolerance'] = ( float(self.params['translations']['precursor_mass_tolerance_plus']) + \
                                                    float(self.params['translations']['precursor_mass_tolerance_minus']) ) \
                                                / 2.0

        if self.params['translations']['frag_mass_tolerance_unit'] == 'ppm':
            self.params['translations']['frag_mass_tolerance'] = ursgal.ucore.convert_ppm_to_dalton(
                self.params['translations']['frag_mass_tolerance'],
                base_mz=self.params['base_mz']
            )

        if self.params['translations']['denovo_model_dir'] == None:
            self.params['translations']['denovo_model_dir'] = os.path.join(
                os.path.dirname(self.exe),
                'Models'
            )

        modifications = []
        for mod in self.params[ 'mods' ][ 'fix' ]:
            mod_available = False
            if mod['name'] in self.available_mods.keys():
                if 'fix' in self.available_mods[ mod['name'] ].keys():
                    if mod['aa'] in self.available_mods[ mod['name'] ]['fix'][0]:
                        modifications.append(mod['aa'] + self.available_mods[ mod['name'] ]['fix'][1])
                        mod_available = True
            if mod_available == False:
                print('''
                    [ WARNING ] PepNovo does not support your given modification
                    [ WARNING ] Continue without modification {0}'''.format(mod)
                    )

        for mod in self.params[ 'mods' ][ 'opt' ]:
            mod_available = False
            if mod['name'] in self.available_mods.keys():
                for term in ['N-term', 'C-term']:
                    if term in mod['pos']:
                        if term in self.available_mods[ mod['name'] ].keys():
                            modifications.append(self.available_mods[ mod['name'] ][term])
                            mod_available = True
                if 'opt' in self.available_mods[ mod['name'] ].keys():
                    if mod['aa'] in self.available_mods[ mod['name'] ]['opt'][0]:
                        modifications.append(mod['aa'] + self.available_mods[ mod['name'] ]['opt'][1])
                        mod_available = True
            if mod_available == False:
                print('''
                    [ WARNING ] PepNovo does not support your given modification
                    [ WARNING ] Continue without modification {0}'''.format(mod)
                    )

        self.params[ 'command_list' ] = [
            self.exe, # path 2 executable
            '-file', '{mgf_input_file}'.format( **self.params['translations']), # SpectrumFile (*.mzXML, *.mgf, *.ms2)
            '-model', '{denovo_model}'.format( **self.params['translations']), # (currently only CID_IT_TRYP is available)
            '-fragment_tolerance', '{frag_mass_tolerance}'.format(**self.params['translations']), # ion tolerances (in Da)
            '-pm_tolerance', '{precursor_mass_tolerance}'.format(**self.params['translations']), # precursor ion tolerance (in Da)
            '-digest', '{enzyme}'.format(**self.params['translations']),
            '-num_solutions', '{num_match_spec}'.format(**self.params['translations']),
            '-model_dir', '{denovo_model_dir}'.format(**self.params['translations']),  # - directory where model files are kept (default ./Models)
            '-PTMs', ':'.join(modifications),  # - separated by a colons (no spaces) e.g., M+16:S+80:N+1
        ]
        if self.params['translations']['pepnovo_tag_length']:
            if self.params['translations']['pepnovo_tag_length'] >= 3 and self.params['translations']['pepnovo_tag_length'] <= 6:
                self.params[ 'command_list' ].extend([
                    '-tag_length', '{pepnovo_tag_length}'.format(**self.params['translations'])
                    ]) # < 3-6> - returns peptide sequence of the specified length (only lengths 3-6 are allowed).

        translations = self.params['translations']['_grouped_by_translated_key']
        for param in [
            '-output_cum_probs',
            '-output_aa_probs',
            '-prm',
            '-prm_norm',
            '-use_spectrum_charge',
            '-use_spectrum_mz',
            '-no_quality_filter',
        ]:
            if list(translations[param].values())[0] == True:
                self.params[ 'command_list' ].append( param )

        if self.params['translations']['precursor_isotope_range'] != '0' :
            self.params[ 'command_list' ].append( '-correct_pm' )

        if self.params['translations']['min_output_score'] >= 0 and self.params['translations']['min_output_score'] <= 1.0:
            self.params[ 'command_list' ].extend([ '-min_filter_prob', '{min_output_score}'.format(**self.params['translations']) ])

        return self.params

    def _execute(self):
        if len(self.params['command_list']) != 0:
            proc = subprocess.Popen(
                self.params['command_list'],
                stdout = subprocess.PIPE,
            )
        else:
            print('Command list is empty, nothing to do here...')
            print('_execute failed ....', self.params['command_list'])
            execute_answer.append( 'Command list is empty' )
            self.execute_return_code = 500

        if proc is not None:
            output_file = open(self.params['translations']['tmp_output_file_incl_path'], 'w')
            # pint('Printing output to file, this can take a while ...')
            for line in proc.stdout:
                if line.startswith(b'>>'):
                    print(
                        'processing spectrum number: ',
                        line.strip().decode('utf').split('.')[1],
                        end = '\r'
                    )

                line_decoded = line.strip().decode('utf')
                print( line_decoded, file = output_file )
            output_file.close()

            # catching the executable's exit code to detect crashes:
            proc.communicate()[0]
            self.execute_return_code = proc.returncode
            assert self.execute_return_code in [0, None], '''
  \n{0} crashed!

  The executable
    {1}
  terminated with Error code {2} .
  Inspect the printouts above for possible causes and verify that all input files are valid.
            '''.format( self.engine, os.path.relpath(self.exe), self.execute_return_code)

        self.print_execution_time(tag='execution')
        return


    def postflight( self ):
        '''
        Reformats the PepNovo output file
        '''
        filepath = self.params['translations']['tmp_output_file_incl_path']

        print('[ PARSING  ] Loading unformatted Pepnovo results ...')

        #extract spectrum titles and spectrum ids from the pepnovo output file and also
        #save the spectrum ids in result_dict as keys.
        #Furthermore, the headers are extracted and saved into the list "headers"
        with open(filepath,'r') as pepnovo_outputfile:
            result_dict = {}
            spectrumtitle_list = []
            id_list = []
            save_headers = True
            for line in pepnovo_outputfile:
                if line.startswith('>>'):
                    line_list = line.split(' ')
                    result_dict[line_list[2]] = []
                    id_list.append(line_list[2])
                    spectrumtitle_list.append(line_list[3])
                if 'No solutions found' in line:
                    continue
                if line.startswith('#') and save_headers == True:
                    headers = line.strip('\n').split('\t')
                    save_headers = False

        #extend and translate headers
        header_translations = self.UNODE_UPARAMS['header_translations']['uvalue_style_translation']
        translated_headers = []
        for header in headers:
            if header == '':
                continue
            translated_headers.append(
                header_translations.get(header, header)
            )
        translated_headers.append('output_aa_probs')
        translated_headers.append('Spectrum Title')
        translated_headers.append('Modifications')
        translated_headers.append('Raw data location')
        translated_headers.append('Retention Time (s)')
        translated_headers.append('Calc m/z')
        translated_headers.insert(1,'Spectrum ID')

        #this section extraction from the pepnovo outputfile and stores it with the corresponding
        #spectrum ids in result_dict
        save_data = False
        spectrum_count = 0
        with open(filepath,'r') as pepnovo_outputfile:
            for line in pepnovo_outputfile.readlines():
                if line.startswith('>>'):
                    spectrum_count += 1 #just counts the number of read spectra, so that the spectrum ids can be correctly accessed in id_list
                    continue
                if line.startswith('#Index'):
                    save_data = True #specifies that the next lines should be saved in result_dict
                    result_line = []
                    continue
                if line != '\n' and save_data == True:
                    line_list = line.strip('\n').split('\t')
                    aa_probs = []
                    #this loop takes the aa probabilities from the line and puts them into a ;-separated string
                    for elem in line_list:
                        if any(c.isalpha() for c in elem) == True:
                            nr_aa = 0
                            # if spectrum_count == 1:
                            seq_index = line_list.index(elem) #specifying seq_index for the next section, but only one time
                            for char in elem:
                                if char.isalpha():
                                    nr_aa +=1
                            line_list.reverse()
                            for i in range(nr_aa):
                                aa_probs.append(line_list[0])
                                del line_list[0]
                        else:
                            continue
                    aa_probs.reverse()
                    aa_probs = ';'.join(aa_probs)
                    line_list.reverse()
                    line_list.append(aa_probs)
                    result_line.append(line_list)
                #in this part the result_line is actually saved to result_dict
                if line == '\n' and save_data == True:
                    result_dict[id_list[spectrum_count-1]] = result_line
                    save_data = False
                    continue

        print('[ Writing  ] Rewriting Pepnovo Outputfile...')

        #this section reads all sequences from result_dict, detects modifications
        #and stores them together with the corresponding aa (last_aa) and the position in moddict.
        #Afterwards, modifications get translated, deleted from sequence and stored with the old sequences as keys
        #in translated_PTMs
        translated_PTMs = {}
        for spec_id in result_dict:
            for rnk_list in result_dict[spec_id]:
                seq = rnk_list[seq_index]
                mod = ''
                moddict = {}
                seqlist = list(seq)
                for x,elem in enumerate(seq):
                    if not elem.isalpha():  #takes everything that is not a letter and adds it to mod
                        mod += elem
                        position = seqlist.index(elem)
                        del seqlist[seqlist.index(elem)] #deletes everythin that is not a letter from seqlist
                        #this counts only for the case, when a sequence ends with a modified aa
                        if seq.endswith(mod) and x == len(seq)-1:
                            if mod not in moddict:
                                moddict[mod] = (last_aa, position)
                            else:
                                #this expression facilitates the making of a list, when several of the same mods are in a seq
                                positionlist = []
                                if type(moddict[mod]) == list:
                                    positionlist = moddict[mod]
                                    positionlist.append((last_aa, position))
                                    moddict[mod] = (positionlist)
                                else:
                                    positionlist.append(moddict[mod])
                                    positionlist.append((last_aa, position))
                                    moddict[mod] = (positionlist)
                                mod = ''
                    elif mod in moddict:
                        #this expression facilitates the making of a list, when several of the same mods are in a seq
                        positionlist = []
                        if type(moddict[mod]) == list:
                            positionlist = moddict[mod]
                            positionlist.append((last_aa, position))
                            moddict[mod] = (positionlist)
                        else:
                            positionlist.append(moddict[mod])
                            positionlist.append((last_aa, position))
                            moddict[mod] = (positionlist)
                        last_aa = elem
                        mod = ''
                    elif mod == '':
                        last_aa = elem
                        continue
                    else:
                        #here, the modifications are actually stored in moddict
                        moddict[mod] = (last_aa, position)
                        last_aa = elem
                        mod = ''
                #this does still count for every rnk_list
                #in this part, the modifications are translated
                modstring = ''
                modlist = []
                for key in self.available_mods:
                    for subkey in self.available_mods[key]:
                        for mod in moddict:
                            if mod in self.available_mods[key][subkey]:
                                if type(self.available_mods[key][subkey]) == tuple:
                                    if type(moddict[mod]) == list:
                                        for elem in moddict[mod]:
                                            if elem[0] in self.available_mods[key][subkey][0]:
                                                modlist.append((str(key),int(elem[1])))
                                    elif type(moddict[mod]) == tuple:
                                        if moddict[mod][0] in self.available_mods[key][subkey][0]:
                                            modlist.append((str(key),int(moddict[mod][1])))
                                else:
                                    modlist.append((str(key),int(moddict[mod][1])))
                modlist = sorted(modlist, key=lambda x: x[1])
                for mod in modlist:
                    modstring += mod[0] + ':'+ str(mod[1]) + ';'
                #this part produces sequences without modifications
                newseq = ''
                for char in seq:
                    if char.isalpha():
                        newseq += char
                translated_PTMs[seq]= (newseq,modstring)

        #this section deletes the modifications from the aa sequences
        translated_PTMs_new = {}
        for spec_id in result_dict:
            for rnk_list in result_dict[spec_id]:
                if type(rnk_list) == str:
                    break
                for PTM in translated_PTMs.keys():
                    if PTM == rnk_list[8]:
                        rnk_list[8] = translated_PTMs[PTM][0]
                        translated_PTMs_new[translated_PTMs[PTM][0]] = (PTM,translated_PTMs[PTM][1])
        translated_PTMs = translated_PTMs_new

        #in this section the new reorganized pepnovo outputfile gets written from the collected information
        pepnovo_outputfile_new = open(self.params['translations']['output_file_incl_path'],'w')
        for header in translated_headers:
            pepnovo_outputfile_new.write(header+',')
        pepnovo_outputfile_new.write('\n')
        for x,spec_id in enumerate(id_list):
            for a in range(len(result_dict[spec_id])):
                if len(result_dict[spec_id]) == 1:
                    break
                else:
                    pepnovo_outputfile_new.write(
                    result_dict[spec_id][a][0]+','
                    +spec_id+',')
                    for b in range(1,len(result_dict[spec_id][a])):
                        pepnovo_outputfile_new.write(
                        result_dict[spec_id][a][b]+',')
                    if result_dict[spec_id][a][8] in translated_PTMs:
                        mods = translated_PTMs[result_dict[spec_id][a][8]][1]
                    pepnovo_outputfile_new.write(spectrumtitle_list[x]+',')
                    pepnovo_outputfile_new.write(mods+',')
                    pepnovo_outputfile_new.write(self.params['translations']['mgf_input_file']+',')
                    pepnovo_outputfile_new.write('False')
                    pepnovo_outputfile_new.write('\n')

        pepnovo_outputfile_new.close()

        return

