from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch('localhost:9200')

def create_index(index_name):
	es.indices.create(index_name, ignore=400)

def insert_single(index_name, doc_type, idc, body):
	es.index(index=index_name, doc_type=doc_type, id=idc, body=body)

def insert_batch(index_name, doc_type, idc, body_list):
	for idx, body in enumerate(body_list):
		action = {
			"_index": index_name,
			"_type": index_type,
			#"_id": idc, #_id 也可以默认生成，不赋值
			"_source": body
		}
		ACTIONS.append(action)
	success, _ = helpers.bulk(es, ACTIONS, index=index_name, raise_on_error=True)

# get all values in index_name, with params: 'doc_type'
def get(index_name, doc_type, idc):
	return es.get(index=index_name, doc_type='test_doc', id=idc)

def search_all(index_name):
	body = {
		"query":{
			"match_all":{}
		}
	}
	# return es.search(index=index_name,doc_type=doc_type)
	return es.search(index=index_name, body=body)

# search single value in single item
def search_term(index_name, item_name, value):
	body = {
		"query":{
			'term':{
				item_name:value
			}
		}
	}
	return es.search(index=index_name, body=body)

# search multi values in single item
def search_terms(index_name, item_name, values):
	res = []
	for value in values:
		temp = search_term(index_name, item_name, value)
		res.append(temp)
	return res

# match item:value
def match(index_name, item_name, value):
	body = {
		"query":{
			"match":{
				item_name:value
			}
		}
	}
	return es.search(index_name, body=body)

# search query_value in multi_fields
def multi_fields_match(index_name, query_value, fields):
	body = {
		"query":{
			"multi_match":{
				"query" : query_value,
				"fields": fields
			}
		}
	}
	return es.search(index_name, body=body)



if __name__=='__main__':
	index_name = 'first-index'
	# create index, directly writing index is also ok
	'''
	for nv in ['python', 'android', 'ios']:
		body = {'name':nv}
		insert_single(index_name, 'test_doc', 1, body)
	'''
	print(multi_fields_match(index_name, 'name', 'ios', []))


