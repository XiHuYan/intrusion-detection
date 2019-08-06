import numpy as np
import pandas as pd
from os.path import join, abspath, dirname, isfile
import os
import matplotlib.pyplot 
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

def load_kdd_txt(path):	
	data = []

	with open(path,'r') as f:
	    lines = f.readlines()
	    for line in lines:
	        data.append(line.strip().split(','))
	 
	data = np.array(data)

	cols = data.shape[1]
	encoder = LabelEncoder()

	for col in range(cols):
	    # str type, label not encoded
	    if data[0,col].isalpha():
	        data[:,col] = encoder.fit_transform(data[:,col])

	data[:,:-1] = data[:,:-1].astype(float)
	n_samples = len(data)
	return data[:int(n_samples * 0.1)]

def load_attacklabel_dict():
	td = {}
	# 5 attacks
	td['dos_attack'] = ['back','land','neptune','pod','smurf','teardrop']
	td['probing_attak'] = ['ipsweep','nmap','portsweep','satan']
	td['R2L_attack'] = ['ftp_write','guess_passwd','imap','multihop','phf','spy','snmpgetattack','xlock']
	td['U2R_attack'] = ['buffer_overflow','loadmodule','perl','named']
	td['normal'] = ['normal']

	at = {}
	for key in td.keys():
		value = td[key]
		for v in value:
			at[v] = key
	return at

def label_trans(text_label):
	attack_dict = load_attacklabel_dict()
	text_label_map = [attack_dict[l[:-1]] for l in text_label]
	text_label_map = np.reshape(text_label_map, (-1,1))

	encoder = MultiLabelBinarizer()
	encoded_label = encoder.fit_transform(text_label_map)
	return encoded_label



def fetch_from_file(FileName):
	temp_data = []
	flag = []
	max_length = 0
	for file_name in os.listdir(FileName):
		for files in os.listdir(join(FileName, file_name)):
			# when file_name is trainning, files is file, otherwise files is a directory
			if isfile(join(FileName, file_name, files)):
				#print(files + 'is a file')
				data_record = open(join(FileName, file_name, files)) 
				record = data_record.readlines()[0].strip().split(' ')
				max_length = max([len(record), max_length])
				fg = [1] if 'Attack' in file_name else [0]
				flag.append(fg)
				temp_data.append(record)
			else:
				record = []
				for file in os.listdir(join(FileName, file_name, files)):
					data_record = open(join(FileName, file_name, files, file)) 
					record.append(data_record.readlines()[0].strip().split(' '))
					max_length = max([len(record[-1]), max_length])
					fg = [1] if 'Attack' in file_name else [0]
					flag.append(fg)
				temp_data.extend(record)
	'''	
	data = []
	for i in temp_data:
		temp_list = [[0]] * 2948
	for idx, j in enumerate(i):
		temp_list[idx] = [j]
	data.append(np.array(temp_list))
	'''
	return np.array(temp_data), np.array(flag), max_length




