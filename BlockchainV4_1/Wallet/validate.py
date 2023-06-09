from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

#from node.block import Block



def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        return pkcs1_15.new(public_key_object).verify(transaction_hash, signature)


def change_dictionary_keys(resp2):
        Transaction_data = dict()
        #resp2=eval(resp2)
        Transaction_data["sender"] = resp2["sender_address"]
        Transaction_data["receiver"] = resp2["receiver_address"]
        Transaction_data["amount"] = resp2["amount"]
        return {
        "sender": resp2["sender_address"],
        "receiver": resp2["receiver_address"],
        "amount" :  resp2["amount"]
    }


""" 
class NodeTransaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = ""
        self.signature = ""

    @staticmethod
    def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        pkcs1_15.new(public_key_object).verify(transaction_hash, signature)

    def validate_funds(self, sender_address: bytes, amount: int) -> bool:
        sender_balance = 0
        current_block = self.blockchain
        while current_block:
            if current_block.transaction_data["sender"] == sender_address:
                sender_balance = sender_balance - current_block.transaction_data["amount"]
            if current_block.transaction_data["receiver"] == sender_address:
                sender_balance = sender_balance + current_block.transaction_data["amount"]
            current_block = current_block.previous_block
        if amount <= sender_balance:
            return True
        else:
            return False
"""