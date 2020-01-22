import requests
import json
import sys
#from elasticsearch import Elasticsearch
endpoint = sys.argv[1]
def index():
    # print("inside image..")
    file_list = ["sample.txt","data.txt","center.txt","project.txt","ongoing.txt"]
    #file_name = "sample.txt"
    for i in file_list:
        headers = {'content-type':'application/json'}
        file = open(i,'rb').read()
        url = 'http://127.0.0.1:5000/index/' + str(i)
        response = requests.put(url,data=file,headers=headers)
        print(response.text)

def search():
    url = []
    headers = {'content-type':'application/json'}
    search_text = "how does flask work"
    search_url = 'http://127.0.0.1:5000/search/' + str(search_text)
    response2 = requests.put(search_url, data=search_text, headers=headers)
    url_list = 'http://127.0.0.1:5000/get_url/'
    response3 = requests.get(url_list, headers=headers)

    urls=(response3.json()["list-of-URLS"])
    for i in urls:
        print(i)
    

if endpoint == 'index':
    index()
else:
    search()
