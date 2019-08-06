from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import urllib.parse
from sklearn import tree
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import io
import re
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
import os
from os.path import join, dirname, abspath
import sys
file_path = abspath(__file__)
sys.path.append(dirname(dirname(file_path)))
from utils import settings

normal_file_raw = join(settings.DATA_DIR, 'cisc2010/normalTrafficTraining.txt')
anomaly_file_raw = join(settings.DATA_DIR, 'cisc2010/anomalousTrafficTest.txt')

normal_file_parse = join(settings.DATA_DIR, 'cisc2010/normalRequestTraining.txt')
anomaly_file_parse = join(settings.DATA_DIR, 'cisc2010/anomalousRequestTest.txt')

def parse_file(file_in, file_out):
    fin = open(file_in)
    fout = io.open(file_out, "w", encoding="utf-8")
    lines = fin.readlines()
    res = []
    n_lines = len(lines)
    for i in range(n_lines):
        line = lines[i].strip()
        if line.startswith("GET"):
            res.append("GET" + line.split(" ")[1])
        elif line.startswith("POST") or line.startswith("PUT"):
            url = line.split(' ')[0] + line.split(' ')[1]
            j = 1
            while True:
                if lines[i + j].startswith("Content-Length"):
                    break
                j += 1
            j += 1
            data = lines[i + j + 1].strip()
            url += '?' + data
            res.append(url)
    for line in res:
        line = urllib.parse.unquote(line).replace('\n','').lower()
        fout.writelines(line + '\n')
    print ("finished parse ",len(res)," requests")
    fout.close()
    fin.close()

def loadData(file):
    with open(file, 'r', encoding="utf8") as f:
        data = f.readlines()
    result = []
    for d in data:
        d = d.strip()
        if (len(d) > 0):
            result.append(d)
    return result

def url_split(url):
    return ' '.join(re.split(r'[?&//]', url))

if __name__=='__main__':
    if not os.path.exists(anomaly_file_parse) or not os.path.exists(normal_file_parse):
        parse_file(normal_file_raw,normal_file_parse)
        parse_file(anomaly_file_raw,anomaly_file_parse)


    bad_requests = loadData(anomaly_file_parse)
    good_requests = loadData(normal_file_parse)

    all_requests = bad_requests + good_requests
    # use ' ' to split url, e.g. 'get/post param1=? param2=?'  
    #all_requests_depart = [url_split(line) for line in all_requests]
    
    yBad = [1] * len(bad_requests)
    yGood = [0] * len(good_requests)
    y = yBad + yGood

    print ("Total requests : ",len(all_requests))
    print ("Bad requests: ",len(bad_requests))
    print ("Good requests: ",len(good_requests))

    vectorizer = TfidfVectorizer(min_df=0.0, analyzer="char", sublinear_tf=True, ngram_range=(3, 3))
    X = vectorizer.fit_transform(all_requests)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=21)

    print ("Requests for Train: ",len(y_train))
    print ("Requests for Test: ",len(y_test))
    print ("Use Trigram (n=3). Split Train:Test = 8:2.\n")

    lgs = LogisticRegression()
    dtc = tree.DecisionTreeClassifier()
    linear_svm=LinearSVC(C=1)
    rfc = RandomForestClassifier(n_estimators=50)

    lgs.fit(X_train, y_train)
    joblib.dump(lgs, join(settings.OUT_DIR, 'cisc2010/logis.m'))  # joblib.load(model_path)
    dtc.fit(X_train, y_train)
    joblib.dump(dtc, join(settings.OUT_DIR, 'cisc2010/decisionTree.m'))
    print("logis score {:.4f}".format(lgs.score(X_test, y_test)))
    print("decision tree {:.4f}".format(dtc.score(X_test, y_test)))
