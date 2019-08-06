import numpy as np
import os
import re
from collections import defaultdict as dd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from gensim.models import Word2Vec
from urllib.parse import unquote
word2vec_dims = 32


def load_file(path):
    data = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.strip())
    return data

#  正则过滤log的模式
def regx_filter(data):
    pattern = r'^(?P<remote_addr>.*?) - (?P<remote_user>.*) \[(?P<time_local>.*?) \+[0-9]+?\] "(?P<request>.*?)" ' \
                      '(?P<status>.*?) (?P<body_bytes_sent>.*?) "(?P<http_referer>.*?)" "(?P<http_user_agent>.*?)"$'
    pattern = re.compile(pattern)
    return [ [x for x in pattern.findall(line)[0] if x!='-'] for line in data if len(pattern.findall(line))>0]

# Get url from requests
def url_filter(req):
    return req.strip(("GETPOSTHTTP/1.1"))

# split url to list
def url_split(url):
    split_pat = r'[/&?]'
    res = re.split(split_pat, url)
    res_ = [x.strip() for x in res if x!='' and x!=' ']
    return res_

def cal_idf(docs):
    dic = dd(int)
    #total_docs = len(docs)
    cnt = 0
    for doc in docs:
        for wd in doc:
            dic[wd] += 1
            cnt += 1
    idf = {}
    for wd in dic:
        idf[wd] = np.log(cnt*1.0/dic[wd])
    return idf

def w2v_transform(doc, model, idf):
    vec = []
    weight_sum = 0
    for feat in doc:
        if feat in model.wv:
            vec.append(idf[feat] * model.wv[feat])
            weight_sum += idf[feat]
    if len(vec)==0:
        return None
    else:
        vec = np.sum(vec, axis=0)/weight_sum
    return vec

if __name__ == '__main__':
    data = load_file(r'C:\Users\Administrator\Desktop\ELK\DATA\weblog.txt')
    data = regx_filter(data)
    #print(data[0])

    # get items except timestamp
    L = []
    for line in data:
        line_str = "".join(line)
        if 'GET' in line_str or "POST" in line_str:
            L.append([line[0], url_filter(line[2]), line[3], line[4], line[5]])
    
    # parse '%' from url with unquote
    url_ = []
    for l in L:
        url_.append(unquote(l[1]))
    #print(url_data)

    # split url and transform
    url_data = [' '.join(url_split(l)) for l in url_]       # string type input, please
    ''' tfidf-tranformer '''
    counter = CountVectorizer()
    x = counter.fit_transform(url_data).toarray()       # Sparse !!
    transformer = TfidfTransformer()
    url_vectors = transformer.fit_transform(x).toarray()    # sparse !!
    #print(url_vectors[0])

    ''' word2vec transformer '''
    w2v = Word2Vec(url_data, size=word2vec_dims)
    idf = cal_idf(url_data)
    url_vectors = [w2v_transform(doc, w2v, idf) for doc in url_data]
    #print(url_vectors[0])
        