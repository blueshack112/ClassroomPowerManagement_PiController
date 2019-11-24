import requests
r= requests.get('http://192.168.8.102:80/AreebaFYP/test.php')

print (r.text)
