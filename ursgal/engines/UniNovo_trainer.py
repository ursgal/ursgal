#!/usr/bin/env python3.4
# encoding: utf-8

import os
import csv

'''This function was thought to be integrated into the ursgal workflow, to provide appropriate Uninovo training with ursgal-derived data.
Since the training function with Uninovo did not work, this function does only act as a converter of mgf files and search_engine unified csvs to
annotated spectrum files as they are requested by Uninovo as input for the training function.'''
def uninovo_trainer ():
	#path to mgf and sequence containing search_engine unified csv files
	path = ''
	
	#reduces the dataset for testing
	'''
	for elem in os.listdir(path):
		if elem.endswith('.mgf'):
			with open (path+elem.rstrip('.mgf')+'_new.mgf','w') as new_outputfile:
				with open (path+elem, 'r') as f:
					c = 0
					for line in f.readlines():
						c += 1
						new_outputfile.writelines(line)
						if c == 10000:
							break
		if elem.endswith('.csv'):
			with open (path+elem.rstrip('.csv')+'_new.csv','w') as new_outputfile:
				with open (path+elem, 'r') as f:
					c = 0
					for line in f.readlines():
						c += 1
						new_outputfile.writelines(line)
						if c == 10000:
							break

	'''
	#fetching the files
	print('[ PARSING  ] Fetching files...')
	mgf_files = []
	seq_files = []
	for elem in os.listdir(path):
		if elem.endswith('.mgf') and elem != 'annotated_mgf_file.mgf':
			mgf_files.append(elem)
		if elem.endswith('.csv') and elem != 'charge_count.csv':
			seq_files.append(elem)

	#associating mgf files with sequence-containing result files
	file_dict = {}
	for mgf_file in mgf_files:
		file_dict[mgf_file] = []
		for seq_file in seq_files:
			if mgf_file.rstrip('.mgf') in seq_file:
				file_dict[mgf_file].append(seq_file) 

	#browsing mgf-files and writing relevant data to the outputfile annotated_mgf_file
	annotated_mgf_file = open (path+'annotated_mgf_file.mgf','w')
	charge_counting_dict = {} #uninovo requests at least 5000 annotated spectra for each charge state. those are counted in this dict.
	temporary = [] #stores each spectrum first, then it gets either deleted or written to the outputfile
	write_data = False #decides if it will get written or not
	mgf_file_count = 0 #just for printing out the progress to the console
	spectrum_count = 0 #this is necessary for outputfile formatting
	hit = 0	#counts the number of spectra written to the outputfile
	print('[ PARSING  ] Loading information...')
	for mgf_file in file_dict.keys():
		mgf_file_count += 1
		seq_dict = {} #this dict stores the spectrum titles as keys with a list of sequences (and maybe modifications) as values
		mgf_path = path + mgf_file
		seq_path1 = path + file_dict[mgf_file][0]
		seq_path2 = path + file_dict[mgf_file][1]
		#in this section, all sequence-containing result files are read and relevant spectrum titles are first written into seq_dict
		#and then all relevant sequences are transfered to result_dict (relevant sequences are marked with a plus in the list in seq_dict)
		with open(seq_path1) as seq_file1:
			reader_seq_file1 = csv.DictReader(seq_file1)
			with open(seq_path2) as seq_file2:
				reader_seq_file2 = csv.DictReader(seq_file2)
				for elem in reader_seq_file1:
					if elem['Spectrum Title'] not in seq_dict:
						seq_dict[elem['Spectrum Title']] = []
						seq_dict[elem['Spectrum Title']].append([elem['Sequence']])#,[elem['Modifications']])
					else:
						seq_dict[elem['Spectrum Title']][0].append(elem['Sequence'])
						#seq_dict['Spectrum Title'][1].append(elem['Modifications'])
						#continue
				for elem in reader_seq_file2:
					if not elem['Spectrum Title'] in seq_dict.keys():
						continue
					else:
						if not elem['Sequence'] in seq_dict[elem['Spectrum Title']][0]:
							#del seq_dict[elem['Spectrum Title']]
							continue
						else:
							seq_dict[elem['Spectrum Title']][0] = elem['Sequence']
							seq_dict[elem['Spectrum Title']].append('+') # the plus is a marker for seqs that are ok
				result_dict = {}
				for title in seq_dict.keys():
					if '+' not in seq_dict[title]:
						continue
					else:
						result_dict[title] = seq_dict[title]
				#print(result_dict)
		#in this section´, the found sequences are written into the annotated mgf-file under the corresponding spectrums
		#additionally the charge states of all the written spectrums are counted for statistics
		with open(mgf_path,'r') as open_mgf_file:
			for line in open_mgf_file.readlines():
				temporary.append(line)
				if line.startswith('TITLE'):
					spectrum_count += 1
					write_data = False
					spectrumtitle = line.split('=')[1].rstrip('\n')
					#print('Spectrumtitle:',spectrumtitle)
					if spectrumtitle in result_dict.keys():
						write_data = True
				if line.startswith('CHARGE') and write_data == True:
					charge = line.split('=')[1].rstrip('\n')
					if charge not in charge_counting_dict.keys():
						charge_counting_dict[charge] = 1
					else:
						if charge_counting_dict[charge] >=5000:
							write_data = False
						else:
							charge_counting_dict[charge] +=1
					temporary.append('SEQ='+result_dict[spectrumtitle][0]+'\n')
					#print('Charge state:',charge)
					#print(charge_counting_dict)
					#break
				if line.startswith('END'):
					if write_data == True:
						if spectrum_count != 1 and hit == 0:
							temporary.remove('\n')
						hit += 1
						for elem in temporary:
							annotated_mgf_file.writelines(elem)
					print('[ Writing  ] Writing to outputfile from MGF-File_Nr.',mgf_file_count,'out of',len(file_dict.keys()),'--Written-Hits:',hit,end='\r')#'--Spectrum_Nr.',spectrum_count,'out of',len(open_seq_file1_lines),	
						#print(temporary)
					temporary = []		
		#break		
	annotated_mgf_file.close()

	#the counted charge states from the previous section are written to a simple csv in this section
	print('\n[ PARSING  ] Counting charge states...')
	charge_list = []
	charge_count_file = open(path+'charge_count.csv','w')
	for charge in charge_counting_dict.keys():
		charge_list.append(charge)
	for charge in charge_list:
		charge_count_file.writelines('Charge:'+charge+',')
	charge_count_file.writelines('\n')
	for charge in charge_list:
		charge_count_file.writelines(str(charge_counting_dict[charge])+',')
	charge_count_file.close()
				
	return

def main ():
	uninovo_trainer()
	return

if __name__ == '__main__':
    main()
