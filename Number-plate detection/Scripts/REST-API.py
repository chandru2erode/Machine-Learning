#!/usr/bin/python
import sys
import requests
import base64
import json, csv

IMAGE_PATH = sys.argv[1]
SECRET_KEY = 'sk_58338b00f93bab02f7f09c53'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=in&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)

f = open('Output_file.json','w+') 
# Creating a file for Output storage 
f.write(json.dumps(r.json(), indent=2))
f.close()
#with open('Output_json_file.json', 'r') as infile, open('Output_file.txt', 'w+') as outfile:
 #   temp = infile.read().replace("{","")
 #   outfile.write(temp)
# Converting image to text and writing it in the file 
# Closing the file
json = open('Output_file.json',"r")
data = json.load(json)
fo = open("Outputfile.txt","w+")
fo.write(data[0]["plate"])
fo.close()