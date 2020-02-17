import requests

resp = requests.post('http://localhost:8080/dude', json={'age':'20h'})
print(resp)
print(resp.text)