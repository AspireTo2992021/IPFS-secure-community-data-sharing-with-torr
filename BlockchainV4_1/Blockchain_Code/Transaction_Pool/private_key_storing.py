import base58
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from Crypto import Random


# how to store a private key and read it back

key = RSA.generate(1024)
k=key
print("private key:")
print(k)
#.txt or .pem both can be used
f = open('mykey_transactin_pool.txt','wb')
f.write(key.export_key('PEM'))
f.close()

f = open('mykeyy.txt','r')
key = RSA.import_key(f.read())

print(f' type of k {type(k)} , type of key = {type(key)} are they both equal{k==key}')

pk = k.publickey().export_key()
pkey=key.publickey().export_key()
print(f'are both public key equal : {pk==pkey}')
print()
print(pk)
print()
print(pkey)