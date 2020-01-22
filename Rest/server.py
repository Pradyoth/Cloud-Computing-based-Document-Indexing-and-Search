from csv import DictReader

import requests
from flask import Flask, request,Response
import json
import hashlib
import jsonpickle
import pika
import pickle
from google.cloud import storage
import os
app = Flask(__name__)
CLOUD_STORAGE_BUCKET = "datacenter-project"
new_list = []
@app.route('/')
def hello_world():
    print("inside hello world..")
    # return 'Hello World!'
@app.route('/index/<file_name>',methods=['PUT','POST','GET',])
def index(file_name):
    #print(file_name)
    
    m = hashlib.md5()
    m.update(request.data)
    q = m.hexdigest()
    print("Hash value is ---------")
    print(q)
    response = {
        "hash":q
    }
    response_pickled = jsonpickle.encode(response)
    print(request.headers)
    print(request.data)
    headers = {'content-type': 'application/json'}
    dat = request.data.decode("utf-8")
    data = {
        "content": dat
    }

    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(file_name)
    blob.upload_from_string(dat, content_type='text/plain')
    

    message = pickle.dumps([file_name,q,dat])
    credentials=pika.PlainCredentials('guest','guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='work')
    channel.basic_publish(exchange='', routing_key='work', body=message)
    print(" [x] Sent Data ")
    connection.close()
    return Response(response=response_pickled,status=200,mimetype="application/json")

@app.route('/search/<search_query>',methods=['PUT','POST','GET',])
def search(search_query):
    print("Search query---")
    print(search_query)
    message = pickle.dumps([search_query])
    credentials=pika.PlainCredentials('guest','guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='work')
    channel.basic_publish(exchange='', routing_key='work', body=message)
    print(" [x] Sent Data ")
    connection.close()
    return Response(response="message received", status=200, mimetype="application/json")

@app.route('/get_url/',methods=['GET'])
def get_url():
    list_url =[]
    print("going into get url api")
    credentials = pika.PlainCredentials('guest','guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='urllist')

    for method_frame, properties, body in channel.consume('urllist'):

    # Display the message parts
    
        print(body)
        list_url = pickle.loads(body)


    # Acknowledge the message
        channel.basic_ack(method_frame.delivery_tag)

    # Escape out of the loop after 10 messages
        if method_frame.delivery_tag == 1:
            break

# Cancel the consumer and return any pending messages
    requeued_messages = channel.cancel()
    #print('Requeued %i messages' % requeued_messages)

# Close the channel and the connection
    channel.close()
    connection.close()
    response = {
             "list-of-URLS":list_url
            }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled,status=200,mimetype="application/json")
    
    


if __name__ == '__main__':
    app.run()

