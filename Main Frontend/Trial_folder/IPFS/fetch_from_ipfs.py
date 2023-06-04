# import ipfshttpclient

# client = ipfshttpclient.connect()  # Connect to the IPFS daemon
# hash = "QmX1fwC2QF9ELNzDdYjcwteTZpwpUpNcLqxGnwyzKjfoeH"  # IPFS hash of the file to download
# data = client.get(hash)  # Download the file from IPFS
# with open('my_file.txt', 'wb') as f:
#     f.write(data.read())
from flask import request
import requests
import ipfsApi
api = ipfsApi.Client(host='127.0.0.1', port=8001)
IPFS_FILE_URL = "http://127.0.0.1:8080/ipfs/"
hash = 'QmZXWuMBMakGmi5f2wi5YmuHQf8EMC1pXjQyAwdGGWFDyZ'
#hash = 'QmYBXFckMP5YmPZdvLQUHnPEKWkcNBxD1RiphqLiw89MoS'
url = IPFS_FILE_URL + hash
h = {"Accept-Encoding": "identity"}
data = requests.get(url, stream=True, verify=False, headers=h)

print(data.content.decode())

print(data)