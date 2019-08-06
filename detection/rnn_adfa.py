import numpy as np
import os
from os.path import join, abspath, dirname
from keras.preprocessing import sequence
from keras.layers import SimpleRNN, Embedding, Dense, LSTM, Dropout
from keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split

import sys
file_path = abspath(__file__)
sys.path.append(dirname(dirname(file_path)))
from utils import settings
from utils.load_data import fetch_from_file

batch_size = 32

def build_model(max_features, output_dim):
	#每个单词嵌入成一个向量，一个一维词序列嵌入成一个二维张量，RNN的输入维度是单个词向量的维度
	model = Sequential()
	model.add(Embedding(max_features, 64))		# embedding first
	model.add(SimpleRNN(64,return_sequences=True))  # replace SimpleRNN with LSTM
	model.add(Dropout(0.1))
	model.add(SimpleRNN(64, return_sequences=True))  
	model.add(Dropout(0.1))
	model.add(SimpleRNN(64, return_sequences=False))  
	model.add(Dropout(0.1))
	model.add(Dense(output_dim, activation='sigmoid'))
	return model

def restore_model(path):
	model = load_model(path)
	print(model.summary())
	return model

if __name__=="__main__":
	data, label, max_len = fetch_from_file(join(settings.DATA_DIR, 'adfa'))
	# pad
	data = sequence.pad_sequences(data, maxlen=max_len)
	# let each number(0~bound) is useful, max_features = max_index+1
	max_features = max(set(data.reshape(-1)))+1				
	print('data shape {}, max feature {}'.format(data.shape, max_features))

	# train test split
	train_x, test_x, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=0)
	# rnn model
	output_dim = label.shape[1]
	model = build_model(max_features, output_dim)
	model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
	history = model.fit(train_x, y_train,
	 epochs=3,
	 batch_size=batch_size,
	 validation_split=0.2)

	model.save(join(settings.OUT_DIR, 'adfa/rnn.h5'))
	#model = restore_model(join(settings.OUT_DIR, 'adfa/rnn.h5'))