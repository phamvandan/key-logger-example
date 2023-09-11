import requests
import json
from config import *


CLIENT_NAME = "abc"

headers = {
  'Content-Type': 'application/json'
}

def send_data(text):
    url = SV + "/rec"
    payload = json.dumps({
    "client_name": CLIENT_NAME,
    "message": text
    })
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def set_client_name():
    global CLIENT_NAME
    url = SV + "/getname"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    CLIENT_NAME = response.text
    print('client name = ', CLIENT_NAME)
# set client name
set_client_name()