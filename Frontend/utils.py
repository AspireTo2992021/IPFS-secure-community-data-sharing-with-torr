import os
import zipfile
import ipfsApi
import requests
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base58
from Crypto.Hash import RIPEMD160, SHA256



class fileManipulate:

    public_key = 1
    zipName = 1
    zip = 1 
    address=1
    ipfsResult = 1  

    def __init__(self , zip_filename):
        self.zipName =  zip_filename+".zip"
        self.zip = zipfile.ZipFile("zipFiles//"+zip_filename+".zip", "w") 

    def get_key_from_chain(self,address) : 
        node = "127.0.0.1:5001"
        transaction = dict()
        transaction["address"] =  address
        response = requests.get(f'http://{node}/get_public_key',json=transaction)    
        print(response)
        response =  response.json()
        f = open("key receive trial.txt", "a")
        f.write(response["public_key"])
        f.close()

    def fetch_key(self,address: str):
        
        # Load the private key from file
        try:
            with open( "public_key_storage//"+address+".pem", 'rb') as f:
                
                self.public_key = RSA.import_key(f.read())
                self.address = address
                return ["ended successfully", 0]
                
        except FileNotFoundError:
             print("wrong address", address )
             return ["wrong address", 1]


    def encrypt_file(self,file):

        # Encrypt the file using the public key
        cipher = PKCS1_OAEP.new(self.public_key)
        with open(file+'.txt', 'rb') as f:
            plaintext = f.read()
        encrypted_data = cipher.encrypt(plaintext)

        # Write the encrypted data to a file
        with open("encrypted_file//"+self.address+'.bin', 'wb') as f:
            f.write(encrypted_data)
        #write encrypted file to zip    
        
        self.zip.write("encrypted_file//"+self.address+'.bin',self.address+'.bin')   
        
    def send_to_ipfs(self):
        # create a client instance to connect to the IPFS node
        api = ipfsApi.Client('127.0.0.1', 5001)
        self.ipfsResult = api.add("zipFiles//"+self.zipName)
        
        #do delete files in zipFiles to save space
        #os.remove("zipFiles//"+self.zipName)   

    def get_from_ipfs(self,hash):
        # not done
        api = ipfsApi.Client('127.0.0.1', 5001)
        s=api.get(hash)

        

# print the hash
# print(f"File uploaded to IPFS with hash {hash}")


# obj = fileManipulate("zip2")

# print("getting key ")
# obj.get_key_from_chain("b'65ZgcwtmdcCxDAKTCwSZu7miP9F2cuEuy2ewtaKrPj1AXrbPeL1DEwb'")

# obj.fetch_key(str(b'65ZgcwtmdcCxDAKTCwSZu7miP9F2cuEuy2ewtaKrPj1AXrbPeL1DEwb'))
# print(obj.public_key)
# obj.encrypt_file("data_files//file1")
# print(obj.zip.infolist())
# obj.zip.extractall("extracted_files")

# obj.send_to_ipfs()
# print(obj.ipfsResult)
# print("sdsd")
# #obj.get_from_ipfs('QmPrhUHdQQsLKJnhGBLYm918YqLF5SNBueJ6S1gf2iY8tE')

# #zip file from ipfs extraction 
# """
# with zipfile.ZipFile('QmYcCdRTe5TqjZVD1A45H4ENMt6mXZke7tG2sVXh77NqKU', 'r') as zip_file:
    
#     # list all files in the zip archive
#     print(zip_file.namelist())
    
#     # extract all files from the archive to a directory
#     zip_file.extractall('my_directory') """

# #decryption test  
# with open('key_storage\\'+obj.address+".pem", 'rb') as f:
#     private_key = RSA.import_key(f.read())      

# cipher = PKCS1_OAEP.new(private_key)
# with open('extracted_files\\'+obj.address+'.bin', 'rb') as f:
#     encrypted_data = f.read()
# decrypted_data = cipher.decrypt(encrypted_data)

# print("decrypted data: ")
# print(decrypted_data)


def get_key_from_chain(address) : 
        node = "127.0.0.1:5001"
        transaction = dict()
        transaction["address"] =  address
        response = requests.get(f'http://{node}/get_public_key',json=transaction)    
        print(response)
        response =  response.json()
        f = open("key receive trial.txt", "a")
        f.write(response["public_key"])
        f.close()
print("getting key ")
get_key_from_chain("b'65ZgcwtmdcCxDAKTCwSZu7miP9F2cuEuy2ewtaKrPj1AXrbPeL1DEwb'")
