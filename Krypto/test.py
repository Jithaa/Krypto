import requests
BASE="http://127.0.0.1:5000/alert/"
response=requests.put(BASE+"create",{"name":"BTC","Value":45978})
print(response.json())
response=requests.get(BASE+"fetch_all")
print(response.json())