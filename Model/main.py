from datetime import datetime
from elasticsearch import helpers, Elasticsearch
import csv
import pandas as pd

train_data_path = '../testdata/train.csv'
test_data_path = '../testdata/test.csv'
train = pd.read_csv(train_data_path); print(train.shape)
test = pd.read_csv(test_data_path); print(test.shape)
train.head()
test.head()
CHUNKSIZE = 100

index_name_train = "loan_prediction_train"
doc_type_train = "av-lp_train"

index_name_test = "loan_prediction_test"
doc_type_test = "av-lp_test"


def index_data(data_path, chunksize, index_name, doc_type):
    f = open(data_path)
    csvfile = csv.DictReader(f)
    es = Elasticsearch()
    try:
        es.indices.delete(index=index_name, ignore=[400, 404])
    except:
        pass
    es.indices.create(index_name,ignore=400)
    try:
        helpers.bulk(es, csvfile, index=index_name, doc_type=doc_type)
        """
        Use "es.index(entry data)" to insert/update new data
        """
        es.indices.refresh()
    except AssertionError as error:
        print("!!!!!!"+error)
        pass


index_data(train_data_path, CHUNKSIZE, index_name_train, doc_type_train) # Indexing train data
index_data(test_data_path, CHUNKSIZE, index_name_test, doc_type_test) # Indexing test data
