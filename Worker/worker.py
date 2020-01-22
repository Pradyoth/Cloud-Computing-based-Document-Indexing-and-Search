import redis
import pika
import json
import pickle
import requests
from elasticsearch import Elasticsearch
from google.cloud import storage
import os

CLOUD_STORAGE_BUCKET = "datacenter-project"

credentials = pika.PlainCredentials('guest','guest')
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='work')
url_list =[]

def callback(ch,method,properties,body):
    
    redisHash = redis.Redis(host="redis", db=1)
    things = []
    file_list = [] # obtained from Redis by matching the hash values
    things.append(pickle.loads(body))
    #print(len(things[0]))
    if (len(things[0]) ==3):
        file_name,hash_value,contents = pickle.loads(body)
        print(file_name)
        #print(hash_value)
        print(contents)
        # print("received %r" % body)
        data = {
            "contents":contents
        }
        redisHash.set(hash_value,file_name)
        # val2 = redisHash.get(hash_value)
        # print(val2)
        url = "http://localhost:9200/test/articles/"+str(hash_value)
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r.status_code)
    else:
        search_query = pickle.loads(body)
        print(search_query[0])
        es = Elasticsearch()
        res = es.search(index="test",body={"query":{"match":{"contents":search_query[0]}}})
        # print(res['hits']['hits'])
        doc_scores = {}
        for result in res['hits']['hits']:
            id = result['_id']
            score = result['_score']
            doc_scores[id] = score
        for key,value in doc_scores.items():
            # print(key,value)
            print("file name obtained from redis for the search is %s" %(redisHash.get(key)))
            file_name = redisHash.get(key).decode("utf-8")
            file_list.append(file_name)
        print(file_list)
        
        gcs = storage.Client()
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
        files = bucket.list_blobs()
        for file in files:
            if file.name in file_list:
                #print(file.public_url)
                url_list.append(file.public_url)
        print(url_list)
        message = pickle.dumps(url_list)
        credentials=pika.PlainCredentials('guest','guest')
        parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='urllist')
        channel.basic_publish(exchange='', routing_key='urllist', body=message)
        print(" [x] Sent URL list ")
        connection.close()
        url_list.clear()


channel.basic_consume(queue='work', on_message_callback=callback, auto_ack=True)
channel.start_consuming()



