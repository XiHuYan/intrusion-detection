from os.path import join, abspath, dirname
import os

DATA_DIR = join(dirname(dirname(__file__)), 'data')
OUT_DIR = join(dirname(dirname(__file__)), 'out')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)