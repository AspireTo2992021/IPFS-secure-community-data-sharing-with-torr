import os
import zipfile
import ipfsApi
import requests
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
import base58
from Crypto.Hash import RIPEMD160, SHA256
import rsa
from rsa import PublicKey


class AccessNetwork:

    public_key = ""
    filename=""
    address=1
    ipfsResult = 1  
    error = "" 
    node = "127.0.0.1:5001"
    #
    # aws= "ec2-43-206-122-178.ap-northeast-1.compute.amazonaws.com"
    aws = "ec2-13-231-72-255.ap-northeast-1.compute.amazonaws.com"
    aws2 = aws+":"+"5001"

    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                        'https': 'socks5://127.0.0.1:9050'}

    def __init__(self ):
        return 
    
   
        
    def setFilename(self,name):
        self.filename = name    

    def get_key_from_chain(self,address) : 
        
        
        transaction = dict()
        transaction["address"] =  address
        #response = requests.get(f'http://{self.node}/get_public_key',json=transaction)
        response = self.session.get(f'http://{self.aws2}/get_public_key',json=transaction)
        print("in get key from chain")    
        print(response.content)
        print(response.status_code)
        if(response.status_code == 400) : 
            self.error = "Invalid Address"
            return

        response =  response.json() 
        
        public_key = (eval(response["public_key"]))
        self.public_key = public_key
        



    def encrypt_key(self,key):
        encrypted_aes_key = rsa.encrypt(key, self.public_key)    
        return   encrypted_aes_key
    
        
    def send_to_ipfs(self,file_address):
        # create a client instance to connect to the IPFS node
        api = ipfsApi.Client('127.0.0.1', 8001)
        print(file_address)
        self.ipfsResult = api.add(file_address)
        
        
        #do delete files in zipFiles to save space
        #os.remove("zipFiles//"+self.zipName)   

    def get_from_ipfs(self,hash):
        # not done
        #api = ipfsApi.Client(host='127.0.0.1', port=8001)
        IPFS_FILE_URL = "http://127.0.0.1:8080/ipfs/"
        

        url = IPFS_FILE_URL + hash
        data = requests.get(url)
        
        return data

    def get_accessible_files_cid(self,address):
        transaction = dict()
        transaction["address"] = address
        print(transaction)
        print(type(address))
        response = self.session.post(f'http://{self.aws2}/Accessible_files',json=transaction)
        return response


    def send_to_pool(self,transaction):
        while(1):  
            try :
                response=self.session.post(f"http://{self.aws}:5000/add_transaction",json=json.dumps(transaction)) 
                return response
            except Exception as e :
                print(e)
                return "Error"    

   

""" Encryption Utils   """
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




def generate_transaction_data(sender,receiver,cid)->dict:
    return {
        "sender": sender,
        "receiver": receiver,
        "cid" : cid
    }

def convert_transaction_data_to_bytes(transaction_data):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["sender"]= str(transaction_data["sender"])
    new_transaction_data["receiver"] = str(transaction_data["receiver"])
    new_transaction_data["cid"] = str(transaction_data["cid"])
    return json.dumps(new_transaction_data,indent=2).encode('utf-8')

def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        return pkcs1_15.new(public_key_object).verify(transaction_hash, signature)