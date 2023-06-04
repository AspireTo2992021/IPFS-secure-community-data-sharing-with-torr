
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import rsa 
from rsa.key import PrivateKey , PublicKey
# Part 1 - Building a self.blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        #self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
        f = open("store_chain_addresses.txt", "r")
        #note that file should not be empty, it should atleast contain []
        l=[]
        try :
         l = eval(f.read())
        except SyntaxError:
            print("file should not be empty, it should atleast contain []")
        except :
            print("something else went wrong")
        
        if len(l)==0:
                
                print("\n Creating self.blockchain")
                self.create_block(proof = 1, previous_hash = '0')
                print(self.chain)
                
        else:
                print("******************\n \n \n")
                print("\n Appending Existing self.blockchain\n")
                print(l)
                self.chain=l
                print("\n Chain: \n")
                print(self.chain)
       


    def add_transaction(self, address , public_key):
        self.transactions.append({'address' :  address ,
                                   'public_key':public_key})
        #reciver->list
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    

    def last_balance(self,account_id)->int:
        
        #if account is present in list return that account balance
        # else return 1
        
        chain = self.chain
        #print("Chain[-1:]",chain[-1:0:-1])
        for block in chain[-1:0:-1]:
            transactions = block["transactions"]
            #print("Check Transactions , in transaction")
            print(transactions)
            for t in transactions:
                if( t['address'] == account_id):
                    return t['public_key']
            return "address invalid"   
                
    
    def create_block(self, proof, previous_hash , timestamp):
        
        block = {'index': len(self.chain) + 1,
                 'timestamp': timestamp,
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        self.storing_chain()
        
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, timestamp,previous_hash, transaction):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256((str(timestamp) + str(previous_hash) + str(transaction)).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        timestamp = block['timestamp']
        previous_hash = block['previous_hash']
        transaction = block['transaction']
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return  hashlib.sha256((str(timestamp) + str(previous_hash) + str(transaction)).encode()).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            timestamp = block['timestamp']
            previous_hash = block['previous_hash']
            transaction = block['transaction']
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256((str(timestamp) + str(previous_hash) + str(transaction)).encode()).hexdigest()
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
        f = open("store_chain_addresses.txt", "w")
        f.write(str(self.chain))
        f.close()


# Blockchain2 stores addresses and keys
class Blockchain2 :


        
    def __init__(self) -> None:
        node_address = str(uuid4()).replace('-', '')

        # Creating a self.blockchain
        self.blockchain = Blockchain()
    # Mining a new block
    def mine_block(self):

        previous_block = self.blockchain.get_previous_block()
        #previous_proof = previous_block['proof']
        timestamp = str(datetime.datetime.now())
        previous_hash = previous_block['previous_hash']
        transaction = self.blockchain.transactions 
        proof = self.blockchain.proof_of_work(timestamp, previous_hash , transaction)
        previous_hash = self.blockchain.hash(previous_block)
        #self.blockchain.add_transaction(sender = node_address, receiver = 'trial', cid = 1)
        block = self.blockchain.create_block(proof, previous_hash,timestamp)
        response = {'message': 'Voted',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash'],
                    'transactions': block['transactions']}
        return jsonify(response), 200

    # Getting the full self.blockchain

    def get_chain(self):
        response = {'chain': self.blockchain.chain,
                    'length': len(self.blockchain.chain)}
        return jsonify(response), 200

    # Checking if the self.blockchain is valid

    def is_valid(self):
        is_valid = self.blockchain.is_chain_valid(self.blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The self.blockchain is valid.'}
        else:
            response = {'message': ' The self.blockchain is not valid.'}
        return jsonify(response), 200

    # Adding a new transaction to the self.blockchain

    def add_transaction(self,json):

        try:
            #json = request.get_json()
            print(json)
            """ privatekey = PrivateKey(8928429708723078367968408861159334506063110426565729327112925060107811252957539657740519188800753824003801730358296590317594677676593972782731522508866801, 65537, 7980915653698145733743157726237638799978472237195379029264833237274147403585013383151331546783311427120008301328966463986393148773098771649605914910996385, 7374407942153548754663164198054381032220371048027587764755178234877068538757363637, 1210731733145170777170546913627385186032517448732030360185540371933504973)
            # process of parsing

            
            js=json.replace("\\\\",'\\' )
            #print("js:\n",js)
            js=js[7:len(js)-1-1]

            js=eval(js) #str(bytes) to bytes"""
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
            
            transaction_keys = ['address', 'public_key']

            if not all(key in json for key in transaction_keys):
                return 'Some elements of the transaction are missing', 400
            index = self.blockchain.add_transaction(json['address'], json['public_key'])
            response = {'message': f'This transaction will be added to Block {index}'}
            return jsonify(response), 201

    # Part 3 - Decentralizing our self.blockchain



    # Connecting new nodes

    def connect_node(self):
        json = request.get_json()
        nodes = json.get('nodes')
        if nodes is None:
            return "No node", 400
        for node in nodes:
            self.blockchain.add_node(node)
        response = {'message': 'All the nodes are now connected. The self.blockchain now contains the following nodes:',
                    'total_nodes': list(self.blockchain.nodes)}
        return jsonify(response), 201

    # Replacing the chain by the longest chain if needed

    def replace_chain(self):
        is_chain_replaced = self.blockchain.replace_chain()
        if is_chain_replaced:
            response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                        'new_chain': self.blockchain.chain}
        else:
            response = {'message': 'All good. The chain is the largest one.',
                        'actual_chain': self.blockchain.chain}
        return jsonify(response), 200
        



