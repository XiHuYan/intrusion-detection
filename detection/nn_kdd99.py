from __future__ import print_function
import numpy as np
from os.path import join, abspath, dirname
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Lambda
from keras.layers import Embedding
from keras.layers import Convolution1D,MaxPooling1D, Flatten
from keras.datasets import imdb
from keras import backend as K
from sklearn.cross_validation import train_test_split
import pandas as pd
from keras.utils.np_utils import to_categorical

from sklearn.preprocessing import Normalizer
from keras.models import Sequential
from keras.layers import Convolution1D, Dense, Dropout, Flatten, MaxPooling1D
from keras.utils import np_utils
import numpy as np
import sys
file_path = abspath(__file__)
sys.path.append(dirname(dirname(file_path)))
import h5py
from keras.layers import LSTM, GRU, SimpleRNN
from utils.load_data import load_kdd_txt, label_trans
from utils import settings

batch_size = 64
def build_model(input_dim=41, output_dim=5):
	model = Sequential()
	model.add(Dense(1024,input_dim=input_dim,activation='relu'))  
	model.add(Dropout(0.01))
	model.add(Dense(768,activation='relu'))  
	model.add(Dropout(0.01))
	model.add(Dense(512,activation='relu'))  
	model.add(Dropout(0.01))
	model.add(Dense(256,activation='relu'))  
	model.add(Dropout(0.01))
	model.add(Dense(128,activation='relu'))  
	model.add(Dropout(0.01))
	model.add(Dense(output_dim))
	model.add(Activation('softmax'))
	return model

def build_cnn(input_dim=41, output_dim=5):
	cnn = Sequential()
	cnn.add(Convolution1D(64, 3, border_mode="same",activation="relu",input_shape=(input_dim, 1)))
	cnn.add(Convolution1D(64, 3, border_mode="same", activation="relu"))
	cnn.add(MaxPooling1D(pool_length=(2)))
	cnn.add(Convolution1D(128, 3, border_mode="same", activation="relu"))
	cnn.add(Convolution1D(128, 3, border_mode="same", activation="relu"))
	cnn.add(MaxPooling1D(pool_length=(2)))
	cnn.add(Flatten())
	cnn.add(Dense(128, activation="relu"))
	cnn.add(Dropout(0.5))
	cnn.add(Dense(output_dim, activation="softmax"))
	return cnn

def restore_model(path):
	model = load_model(path)
	print(model.summary())
	return model

if __name__=='__main__':
	traindata = load_kdd_txt(join(settings.DATA_DIR, 'kdd99/kdd_train_10'))
	testdata = load_kdd_txt(join(settings.DATA_DIR ,'kdd99/kdd_test_10'))

	X = traindata[:,:-1]
	Y = traindata[:,-1]

	C = testdata[:,-1]
	T = testdata[:,:-1]

	# transform train&test txt labels
	txt_label = list(Y) + list(C)
	n_train_samples = len(Y)
	encoded_label = label_trans(txt_label)		# multilabel vectors
	Y = encoded_label[:n_train_samples]
	C = encoded_label[n_train_samples:]

	trainX = Normalizer().fit_transform(X)
	testT = Normalizer().fit_transform(T)

	y_train = np.array(Y)
	y_test = np.array(C)
	print('encoded shape', y_train.shape)

	input_dim = trainX.shape[1]
	output_dim = y_train.shape[1]
	model = build_model(input_dim, output_dim)
	model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
	# train 
	model.fit(trainX, y_train, 
		epochs=50, 
		validation_data=(testT, y_test), 
		batch_size=batch_size
		)

	'''
	# train with cnn, cnn single input (input_dim, 1)
	trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
	testT = np.reshape(testT, (testT.shape[0], testT.shape[1], 1))
	model.fit(trainX, y_train,
		epochs=10,
		validation_data=(testT, y_test),
		batch_size=batch_size
		)
	'''


	os.makedirs(join(settings.OUT_DIR, 'kdd99'), exist_ok=True)
	model.save(join(settings.OUT_DIR, 'kdd99/nn_model.h5'))

	#model = restore_model(join(settings.OUT_DIR, 'kdd99/nn_model.h5'))