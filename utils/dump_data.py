import numpy as np
import pandas as pd
from os.path import join
import matplotlib.pyplot 
from sklearn.preprocessing import LabelEncoder

def dump_part_test(rpath, wpath, percent=10):
	with open(wpath, 'w') as wf:
		with open(rpath, 'r') as f:
			lines = f.readlines()
			n_lines = len(lines)
			for i in range(int(n_lines * percent*1./100)):
				wf.write(lines[i])

if __name__=='__main__':
	per = 10
	dump_part_test(join(settings.DATA_DIR, 'corrected'), join(settings.DATA_DIR, 'kdd_test_{}'.format(per)), per)
	print('done')