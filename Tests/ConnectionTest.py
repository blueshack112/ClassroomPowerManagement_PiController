import requests
r= requests.get('http://192.168.18.4:80/AreebaFYP/test.php')

print (r.text)
