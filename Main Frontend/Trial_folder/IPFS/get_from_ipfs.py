from flask import request
import requests
import ipfsApi

api = ipfsApi.Client(host='127.0.0.1', port=8001)
IPFS_FILE_URL = "http://127.0.0.1:8080/ipfs/"
#hash = 'QmZXWuMBMakGmi5f2wi5YmuHQf8EMC1pXjQyAwdGGWFDyZ'
hash = 'QmbXHiYHdxm3VcJGCade9VfmtKodTxWxbDY1bVhz7LKe2Q'
hash2 ='QmcQK5ZRpQQFQ3CJ6dt1ufe2jA86hnFUQLwve8SB4DVWCM'
url = IPFS_FILE_URL + hash2
h = {"Accept-Encoding": "identity"}
data = requests.get(url, stream=True, verify=False, headers=h)
print(data.status_code)
print(data.content)
