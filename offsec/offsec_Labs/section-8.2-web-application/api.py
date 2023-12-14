#!/usr/bin/env python3

import requests

url = 'http://offsecwp.com:5002/'

probe = requests.get(url + '/console')
print(probe.text)