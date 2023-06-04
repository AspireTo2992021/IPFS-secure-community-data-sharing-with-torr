import binascii
from email import message
import json
import base58
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto import Random
from Crypto.Hash import RIPEMD160, SHA256
from validate import validate_signature
import requests

class Owner:
    def __init__(self, private_key: RSA.RsaKey, public_key: bytes, address: bytes):
        self.private_key = private_key
        self.public_key = public_key
        self.address =address


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




def generate_transaction_data(sender_bitcoin_address , receiver_bitcoin_address,cid)->dict:
    return {
        "sender": sender_bitcoin_address,
        "receiver": receiver_bitcoin_address,
        "cid" : cid
    }

def convert_transaction_data_to_bytes(transaction_data):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["sender"]= str(transaction_data["sender"])
    new_transaction_data["receiver"] = str(transaction_data["receiver"])
    new_transaction_data["cid"] = str(transaction_data["cid"])
    return json.dumps(new_transaction_data,indent=2).encode('utf-8')


def initialize_wallet():
    #Assumption: private key right now is not static, after integration with frontend , private key will be taken from QR code.
    #therefore methods should be changed accordingly
    #intialize_wallet(private_key)
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key()
    hash_1 = calculate_hash(public_key, hash_function="sha256")
    hash_2 = calculate_hash(hash_1, hash_function="ripemd160")
    address = base58.b58encode(hash_2)
    return Owner(private_key, public_key, address)

def initialize_wallet(private_key):
    #intialize_wallet(private_key)
    
    public_key = private_key.publickey().export_key()
    hash_1 = calculate_hash(public_key, hash_function="sha256")
    hash_2 = calculate_hash(hash_1, hash_function="ripemd160")
    address = base58.b58encode(hash_2)
    return Owner(private_key, public_key, address)

class Transaction:
    def __init__(self, owner: Owner, receiver_address: bytes, cid: int, signature: str = ""):
        self.owner = owner
        self.receiver_address = receiver_address
        self.cid = cid
        self.signature = signature

    def generate_data(self) -> bytes:
        transaction_data = generate_transaction_data(self.owner.address, self.receiver_address, self.cid)
        #print(f'from generate_data method :{ convert_transaction_data_to_bytes(transaction_data)} ')
        return convert_transaction_data_to_bytes(transaction_data)

    def sign(self):
        transaction_data = self.generate_data()
        hash_object = SHA256.new(transaction_data)
        signature = pkcs1_15.new(self.owner.private_key).sign(hash_object)
        #self.signature = binascii.hexlify(signature).decode("utf-8")
        self.signature = signature
        """
        key = RSA.import_key(private_key.export_key())
        h = SHA256.new(message)
        signature = pkcs1_15.new(key).sign(h)

        """
        
        
    def sign_access_request(self,public_key):
        return {"data" : str({
            "TransactionData" : {"sender_address": self.owner.address,
                                "receiver_address": self.receiver_address,
                                    "cid": self.cid},
            "signature": self.signature,
            "public_key" : public_key
        })}
    


#to be moved to front end
def send_to_pool(transaction):
 while(1):  
    try :
        response=requests.post(f"http://127.0.0.1:5000/add_transaction",json=json.dumps(transaction)) 
        return response
    except Exception as e :
        print(e)
        return "Error"

def signing_transaction(json):

    f = open("mykey_transaction_pool.txt",'r')
    private_key = RSA.import_key(f.read())
    public_key = private_key.publickey().export_key()

    owner = initialize_wallet(private_key)    
    T = Transaction(owner ,receiver_address = json["receiver_address"],cid = json["cid"])
    T.sign()
        #sending to transaction pool
        #resp = send_to_pool(T.send_to_nodes())
        #print(f'publick key {owner.public_key}')
    resp = T.sign_access_request(owner.public_key)
  
    r=send_to_pool(resp)
    print(r)
    
def signing_access_request_to_frontend(json):

    f = open("mykey_transaction_pool.txt",'r')
    private_key = RSA.import_key(f.read())
    public_key = private_key.publickey().export_key()

    owner = initialize_wallet(private_key)    
    T = Transaction(owner ,receiver_address=json["receiver"],cid = json["cid"])
    T.sign()
        #sending to transaction pool
        #resp = send_to_pool(T.send_to_nodes())
        #print(f'publick key {owner.public_key}')
    resp = T.sign_access_request(owner.public_key)
  
    
    print(resp)
    return resp 


"""
private_key = RSA.generate(2048)
owner = initialize_wallet(private_key)
T =  Transaction(owner , "b" , 1 ) 
T.sign()
d = T.send_to_nodes(owner.public_key)

key = RSA.import_key((owner.public_key))
message = T.generate_data()
h = SHA256.new(message)
try:
    pkcs1_15.new(key).verify(h, T.signature)
    print ("The signature is valid.")
except (ValueError, TypeError):
   print ("The signature is not valid.")
      """

"""
private_key = RSA.generate(1024, randfunc=None, e=65537)

public_key = private_key.publickey().export_key()

print(private_key)
print(public_key)

private_key = RSA.generate(1024, randfunc=None, e=65537)
public_key = private_key.publickey().export_key()

print(type(private_key))
print(private_key)
print(public_key)"""



# how to store a public key and read it back
"""
key = RSA.generate(1024)
k=key
print("private key:")
print(k)
#.txt or .pem both can be used
f = open('mykeyy.txt','wb')
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
print(pkey)"""


#print("0x2B42EF59BB0".publickey().export_key())

#def check_if_exist(pk):
    # k=hash(pk)
    # b=check_if_exist_in_db(k)
    # if b==True:
    #   return "account exist"
    #else:
        #return "doesn't exist"

#check_if_exist("Preeeti")

"""
x = Random.new()
print(x)
print(x.read(10))
x = x.read(10)

k=x
#.txt or .pem both can be used
f = open('storeRand.txt','wb')
f.write(x)
f.close()

f = open('storeRand.txt','r')
k = (f.read())

if(k==x):
    print("True")
else: 
    print("false")
    print(x)
    print(k)"""