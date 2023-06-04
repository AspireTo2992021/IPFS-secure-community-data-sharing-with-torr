import ipfsApi
api = ipfsApi.Client('127.0.0.1', 8001)
res = api.add('dir//files//myText.txt')
print(res)
print(res["Hash"])
