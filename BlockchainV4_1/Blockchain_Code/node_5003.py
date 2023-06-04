
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import rsa 
from rsa.key import PrivateKey , PublicKey
from Blockchain import Blockchain2
# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        #self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
        f = open("store_chain.txt", "r")
        #note that file should not be empty, it should atleast contain []
        l=[]
        try :
         l = eval(f.read())
        except SyntaxError:
            print("file should not be empty, it should atleast contain []")
        except :
            print("something else went wrong")
        
        if len(l)==0:
                
                print("\n Creating Blockchain")
                self.create_block(proof = 1, previous_hash = '0')
                print(self.chain)
                
        else:
                print("******************\n \n \n")
                print("\n Appending Existing Blockchain\n")
                print(l)
                self.chain=l
                print("\n Chain: \n")
                print(self.chain)
       


    def add_transaction(self, sender, receiver:list, cid):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'cid': cid})
        #reciver->list
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    

    def check_access(self,account_id)->int:
        
        #if account is present in list return that account balance
        # else return 1
        access_list = list()
        chain = self.chain
        #print("Chain[-1:]",chain[-1:0:-1])
        """
                    "transactions": [
                {
                    "cid": "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
                    "receiver": "[\"b'3WFHHhTSrT8LTxM3q29bk9PFtvvhLDL4nE3y4FQA9iNP9fBiAtNDreZ'\", \"b'3bzvhHzonRKR77VBaZcL6vWM196Ebx3jiSMwLN2ewx9ByJLy7yKZE4M'\"]",
                    "sender": "b'3WFHHhTSrT8LTxM3q29bk9PFtvvhLDL4nE3y4FQA9iNP9fBiAtNDreZ'"
                }
        """
        for block in chain[-1:1:-1]:
            transactions = block["transactions"]
            print("Check Transactions , in transaction ",transactions)
            
            for t in transactions:
                if( t['sender'] == account_id):
                    access_list.append(t["cid"])
                if 1:    
                    for address in eval(t["receiver"]):
                        #print("*******************")
                        #print(address)
                        #print(type(address))
                        #print(str(address) == str(account_id))
                        if str(address) == account_id: 
                                access_list.append(t["cid"])
        
        return access_list
           
                
    

    def create_block(self, proof, previous_hash):
        
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        self.storing_chain()
        
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
 
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            self.storing_chain()
            return True
        return False

    def storing_chain(self):
        print("Writing in File \n")
        print(str(self.chain))
        f = open("store_chain.txt", "w")
        f.write(str(self.chain))
        f.close()

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5001
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_transaction(sender = node_address, receiver = 'trial', cid = 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Voted',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': ' The Blockchain is not valid.'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():


  try:
    json = request.get_json()
    print(json)
    """ privatekey = PrivateKey(8928429708723078367968408861159334506063110426565729327112925060107811252957539657740519188800753824003801730358296590317594677676593972782731522508866801, 65537, 7980915653698145733743157726237638799978472237195379029264833237274147403585013383151331546783311427120008301328966463986393148773098771649605914910996385, 7374407942153548754663164198054381032220371048027587764755178234877068538757363637, 1210731733145170777170546913627385186032517448732030360185540371933504973)
    # process of parsing

    
    js=json.replace("\\\\",'\\' )
    #print("js:\n",js)
    js=js[7:len(js)-1-1]

    js=eval(js) #str(bytes) to bytes"""
    json = eval(json)
    json = eval(json["t"])
    json['sender'] = str(json['sender'])
    json['receiver'] = str(json['receiver'])
    print(f'json is {json}')
  except:
      print("Error in add_transaction")
      #print(js)
      return "500",500
  else:
    """    dm =  rsa.decrypt(js, privatekey)
    json = dm.decode()
    json=eval(json)"""
    #print("json1: ",json1)
    #print("type of json: ", type(json1))
    
    transaction_keys = ['sender', 'receiver', 'cid']

    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['cid'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain



# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200
    
@app.route('/Accessible_files', methods = ['POST'])
def Accessible_file():
    # json = {"address" : "entered address"}
    json = request.get_json()
    transaction_keys = ['address']
    print(json)
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    l = blockchain.check_access(json["address"])
    if(len(l)==0):
        return "No Accessible Files ", 300
    d= dict()
    s = set(l)
    d["CID"] = list(s)
    return d,200 




#Part 4 - Second Blockchain 

chain2 = Blockchain2() 

@app.route('/mine_address_block', methods = ['POST'])
def mine__address_block():
    
    return chain2.mine_block()

@app.route('/get_address_chain', methods = ['GET'])
def address_chain():
    return chain2.get_chain()

@app.route('/get_public_key', methods = ['GET'])
def get_public_key():
    json =  request.get_json()
    transaction_keys=["address"]
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    address = json["address"]
    #address = eval(address)
    chain = chain2.get_chain2()
    
    
    #print(chain)
    for block in chain[-1:0:-1]:
        print("--------------------------------------------")
        print(block)
        if block["transactions"][0]["address"] == address :
            return jsonify(block["transactions"][0]) 
    js = dict()
    js["Message"] =  "Not found" 
    return jsonify(js) ,400

@app.route('/address_chain_valid', methods = ['POST'])
def address_chain_valid():
    return chain2.is_valid 

@app.route('/add_address', methods = ['POST'])
def add_address():
    json =  request.get_json()
    return chain2.add_transaction(json)



@app.route('/replace_address_chain', methods = ['POST'])
def replace_address_chain():
    return chain2.replace_chain()
    

# Running the app
if __name__ == '__main__':
    app.debug = True
    app.run(port=5003)
#app.run(host = '0.0.0.0', port = 5001)
