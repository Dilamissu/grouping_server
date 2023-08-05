import requests
data = {"childs": [3]}
a = requests.patch('http://127.0.0.1:8000/api/activities/1/', data)
print(a)
