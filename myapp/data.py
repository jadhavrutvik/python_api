from django.test import TestCase
import requests
import json
 
# Create your tests here.
 
 
URL = "http://127.0.0.1:8000/get/"
 
def get_data(id=None):
    r = requests.get(url = URL)
    data = r.json()
    # print(data)
 
# get_data()
    
   
def post_data():
    data = {
        'name':'ashutosh'
    }
 
    json_data = json.dumps(data)
    r = requests.post(url = URL, data = json_data)
    data = r.json()
    # print(data)
# post_data()



def delete_data(id):
    data = {
        "id":id
    }
 
    json_data = json.dumps(data)
    r = requests.delete(url=URL,data=json_data)

# delete_data(1)