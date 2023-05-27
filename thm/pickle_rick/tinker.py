import requests

url = 'http://10.10.160.253/login.php'

f = open('./demo.txt', 'r')
output = f.read()
ls = '/'.split(output)
print(ls)

# requests.post(url, data={
#     'username':u,
#     'password':p
# })