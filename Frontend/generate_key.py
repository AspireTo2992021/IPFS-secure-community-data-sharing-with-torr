import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base58
from Crypto.Hash import RIPEMD160, SHA256


def calculate_hash(data, hash_function="sha256"):
    if(type(data)==str):
        data = bytearray(data,"utf-8")

    if hash_function == "sha256" :
        h= SHA256.new()
        h.update(data)
        return h.hexdigest() 
    if hash_function == "ripemd160":
        h=RIPEMD160.new()
        h.update(data)
        return h.hexdigest()

key = RSA.generate(1024)
public_key = key.publickey().export_key()
hash_1 = calculate_hash(public_key, hash_function="sha256")
hash_2 = calculate_hash(hash_1, hash_function="ripemd160")
address = base58.b58encode(hash_2)

# Write the private key to a file
file_name = str(address)+'.pem'
with open('key_storage//'+file_name, 'wb') as f:
    f.write(key.export_key('PEM'))

with open('key_storage//addresses.txt', 'a') as f:
    f.write(str(address)+'\n')

# Write the public key to a file
file_name = str(address)+'.pem'
with open('public_key_storage//'+file_name, 'wb') as f:
    f.write(key.publickey().export_key('PEM'))

with open('public_key_storage//addresses.txt', 'a') as f:
    f.write(str(address)+'\n')    

