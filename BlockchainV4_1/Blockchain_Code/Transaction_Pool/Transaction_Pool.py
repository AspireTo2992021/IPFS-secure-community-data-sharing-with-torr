
import datetime
import hashlib
from inspect import signature
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import random 
import rsa 
from rsa.key import PrivateKey , PublicKey
from validate import validate_vote, validate_signature, change_dictionary_keys,convert_transaction_data_to_bytes,transaction_data_to_bytes
from Transaction_sigining_utils import signing_transaction,signing_access_request_to_frontend

def encrypt_transaction(obj):
    publickey = PublicKey(8928429708723078367968408861159334506063110426565729327112925060107811252957539657740519188800753824003801730358296590317594677676593972782731522508866801, 65537)
    mes = str(obj).encode()
    print(f"encoded text = {mes} length :  {len(mes)} ")
    em = rsa.encrypt(mes, publickey)
    return em 


# Creating a Web App
tp = Flask(__name__) # tp for transaction pool 


nodes = ["http://127.0.0.1:5001/","http://127.0.0.1:5002/","http://127.0.0.1:5003/"]
#nodes = ["http://127.0.0.1:5001/"]


class Connect_nodes :
    def __init__(self):
        # Connecting all nodes
        for node in nodes :
            l = []
            d = {}
            for connect_node in nodes :
                if connect_node is not node :
                    l.append(connect_node)
            d["nodes"]=l 
            r = requests.post(f"{node}/connect_node",json = d )
            print(f"reuslt of connection of {node}'th node ",r.json())

connection1 = Connect_nodes()



#not completed 
def validate2(public_key , signature , Transaction_data):
    try: 
        print("In validate 2.0 pk : ")   
        print(public_key)
        print("signature: ")
        print(signature) 
        validate_signature(public_key, signature, transaction_data_to_bytes(Transaction_data))
                   
        print("In validate 2")
        return True
    except Exception as e :
       print(f'Error from validate_transaction in validation pool {e} ')
       return f'Failed to vote {e}', 400   

def validate(public_key , signature , Transaction_data) : 
    """    resp = request.get_json()
    resp = eval(resp)
    resp = eval(resp["data"])
    print(resp)
    print("In transaction pool for validating signature")"""
    #print(f'public_key : {public_key}')
    #print(f'Transaction data {Transaction_data} \n ')
    #Transaction_data = change_dictionary_keys(Transaction_data)

    try:     
        #print(validate_signature(resp["public_key"] ,  resp["signature"] , convert_transaction_data_to_bytes(resp["TransactionData"])))
        #print(f'resp ')
        #print(f' public_key : {resp["public_key"]} , signature : {resp["signature"] } transaction_in_bytes : {convert_transaction_data_to_bytes(Transaction_data)}')
        #print(convert_transaction_data_to_bytes(Transaction_data))
        validate_signature(public_key, signature, convert_transaction_data_to_bytes(Transaction_data))
        #print(Transaction_data)
        
        return True
    except Exception as e :
       print(f'Error from validate_transaction in validation pool {e} ')
       return f'Failed to vote {e}', 400
    
 #validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes)

#function to be a part of front end
@tp.route('/test_sign', methods = ['POST']) 
def test_sign():
    #{receiver:"receiver",cid:"cid"}
    json = request.get_json() 
    signing_transaction(json) 
    return "test_sign() ended"




@tp.route('/file_access_verification', methods = ['POST']) 
def sign_access_request():
    print("code for signing request")
    
    obj = request.get_json()
    obj = eval(obj)
    print(obj)
    obj = eval(obj["data"])

    print("------------------sdad---------------")
    Transaction_data = change_dictionary_keys( obj["TransactionData"])
    print("Transaction_data , ",Transaction_data)
    if(validate(obj["public_key"],obj["signature"],Transaction_data)!=True):
        return f'Validation Failed' , 300
    #sign access request
    x=validate_vote(Transaction_data)

    """ t =  obj["TransactionData"]
    Transanction_data=dict()
    Transanction_data["sender"] = t["sender"]
    Transanction_data["cid"] = t["cid"]
    print("Transaction data: " )
    print(Transanction_data)

    print(validate2(obj["public_key"],obj["signature"],Transanction_data))

    if(validate2(obj["public_key"],obj["signature"],Transanction_data)!=True):
        print("validation failed")
        return f'Validation Failed' , 300"""
    #sign access request
    access_grant=validate_vote(Transaction_data)
    print("-----------------------------------------------")
    print(f'validate vote outpur {access_grant}')
    if(not access_grant):
        response = {"message" :"Request not granted", "code" : 0 }
        print("na")
        #return signed obect
        return jsonify(response)
    
    Transaction = dict()
    Transaction["receiver"] = Transaction_data["sender"]
    Transaction["cid"] = Transaction_data["cid"]
    
    response = signing_access_request_to_frontend(Transaction)
    return jsonify(response),200

    
    # return sign object



@tp.route('/add_transaction', methods = ['POST'])
def add_transactions():
    obj = request.get_json()
    obj = eval(obj)
    obj = eval(obj["data"])

    Transaction_data = change_dictionary_keys( obj["TransactionData"])
    print("Transaction_data , ",Transaction_data)
    if(validate(obj["public_key"],obj["signature"],Transaction_data)!=True):
        return f'Validation Failed' , 300
    #sign access request
    x=validate_vote(Transaction_data)
    print(f'validate vote outpur {x}')
    if(False):
        response = {"message" :"Request granted", "code" : 0 }
        print("na")
        #return signed obect
        return jsonify(response)

    transaction_keys = ['sender','receiver','cid']
    #signature = obj["signature"]
    obj = Transaction_data
    #obj["signature"] = signature 
    print("----------------")
    if not all(key in obj for key in transaction_keys):
        return 'keys inappropriate'
    print(f'obj : {obj} type : {type(obj)}')

    """url = 'https://www.w3schools.com/python/demopage.php'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, json = myobj)

"""
#assign node randomly
    mine_node = random.choice(nodes)
    #print("mine_node")
    #mine_node = "http://127.0.0.1:5001/"
    
    #valid node: directling applying largest chain to all nodes.
    # need to work here as corrupt node can create fake longest chain resulting in mess 
    
    """
    #need to use assymetric cyrptography  between transaction pool and nodes.
    #Assymetric cryptography between transaction pool and hadcoin)mode_5001.py is complete


    """
    #encypting transaction
    
    """
    r is for response code
    suppose due some reasons like loss of data wile communication , decryption soes not happen 
    properly at the backend , then transaction pool should try again. The reason we use while loop
    because we will resend the encrypted data
    """
    r = 500 

    while r == 500:
        encoded_transaction = {}
        #encoded_transaction["t"] = str(encrypt_transaction(obj))
        encoded_transaction["t"] = str(obj)
        for node in nodes :
            requests.get(f"{node}/replace_chain")
        #mine block
        #requests.post(f"{mine_node}/add_transaction",json=obj)
        
        response=requests.post(f"{mine_node}/add_transaction",json=json.dumps(encoded_transaction)) 
            # problem is cannot send obj which is dictionary to json , which accepts JSON form
            #above proble, is solved
            
        print(response) 
        print(type(response))
        r=response.status_code
        if(r==500):
                print("******************************************************************************************************************")
                continue

        #result = requests.get(f"http://192.168.0.128:5001/mine_block")
        result = requests.get(f"{mine_node}/mine_block")

        #Replace chain for all nodes
        for node in nodes :
            requests.get(f"{node}/replace_chain")
        print(f"result node : {mine_node}")
        print(f"result: {result.json()} typr : {type(result)} content type : {result.headers['Content-Type']}")
        return jsonify(result.json())

   
@tp.route('/check', methods = ['GET'])  
def check():
        return "working"
    





#Running transaction pool on 6000
if __name__ == '__main__':
    tp.debug = True
    tp.run(port=5000)