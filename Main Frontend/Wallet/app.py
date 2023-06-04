import datetime
import hashlib
import json
from flask import Flask, jsonify, request , render_template , redirect , url_for
import requests
from uuid import uuid4
from urllib.parse import urlparse
from wallet import validate_signature 
from wallet import Transaction
from wallet import initialize_wallet
#from utils import scan_QR_code,validate_QR_Code ,convert_transaction_data_to_bytes
#from validate import change_dictionary_keys

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base58

import os
from flask_dropzone import Dropzone
from forms import QRCodeData
import secrets
import cv2
import qrcode
from pyzbar import pyzbar
from utils import AccessNetwork ,calculate_hash

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import rsa.randnum
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from rsa import PublicKey ,PrivateKey
import requests


#Assumption : front end will use /make_transaction to send transaction 
""""
{
'receiver_address' = '',
'amount'=''
}

"""
#Assumption: private key right now is static, after integration with frontend , private key will be taken from QR code.
#therefore methods should be changed accordingly

key_file_path = "../RequiredFiles/key.json" 
download_file_path = "static/Downloaded_from_ipfs.enc"


app = Flask(__name__)
app.config['DEBUG']=True
print(app.config)

dir_path = os.path.dirname(os.path.realpath(__file__))
app.config['SECRET_KEY'] = 'bf9b1b2111ab03c26782b1e7da3fd366fc5e127b'
app.config['UPLOAD_FOLDER'] = 'static/files'

app.config.update(
    UPLOADED_PATH=os.path.join(dir_path, 'static'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1
)
app.config['DROPZONE_REDIRECT_VIEW'] = 'user_authorisation_QR'

dropzone = Dropzone(app)


#app.config["SERVER_NAME"] = 'localhost:3000'

#take transaction input 
# sign it
#send it to pool

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


decoded_info = ""
N = AccessNetwork()
file = FileField("File", validators=[InputRequired()])
privateKeyOfWallet = ""
encryptionPrivateKey = ""
encryptionPublicKey = ""
address = ""




@app.route('/', methods=['GET',"POST"])
@app.route("/decqr", methods=["GET", "POST"])
def decqr():
    if request.method == 'POST':
        global decoded_info
        f = request.files.get('file')
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".png"
       

        file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)
        f.save(file_location)

        print(file_location)
        # read and decode QRCode
        img = cv2.imread(file_location)

        qr_codes = pyzbar.decode(img)
        data =  str(qr_codes[0].data.decode('utf-8'))
        os.remove(file_location)
        print(data)
        k1 , k2, k3 = data.split("***")
        
        global privateKeyOfWallet,encryptionPrivateKey ,encryptionPublicKey
        privateKeyOfWallet = RSA.import_key((k1))
        encryptionPrivateKey=eval(k2)
        encryptionPublicKey = eval(k3)

        print("************************************")
        print(f"data from qr {data}")
        
        
        decoded_info = data

        redirect(url_for('user_authorisation_QR'))
        print("redirect failed")
        return render_template("layout.html")
        
    else:
       return render_template("upload.html")

@app.route("/decoded")
def decoded():
    global decoded_info
    redirect(url_for('user_authorisation_QR'))
    return render_template("decoded.html", data=decoded_info)

@app.route("/user_authorisation_QR")
def user_authorisation_QR():
    #name = scan_QR_code()
    print(decoded_info)
    try :
        k1 , k2, k3 = decoded_info.split("***")
    except : 
         return render_template("not_eligible.html")
    privatekey = RSA.import_key(k1)
    public_key = privatekey.publickey().export_key()
    hash_1 = calculate_hash(public_key, hash_function="sha256")
    hash_2 = calculate_hash(hash_1, hash_function="ripemd160")
    global address
    address = base58.b58encode(hash_2)
    print(address)
    N.get_key_from_chain(str(address))
    print(str(N.public_key) == (k3))
    if  str(N.public_key) == (k3):
        return redirect(url_for('send_to_ipfs'))
        print("redirecting")
    return render_template("not_eligible.html")

@app.route("/get_cids",methods=['GET',"POST"])
def get_cids():
     
     global address
     print("**************")
     print(address)
     A = AccessNetwork()
     R = A.get_accessible_files_cid(str(address))
     print(R)
     E="" 
     M = ""
     data=""
     if(R.status_code == 400):
          E= "Wrong Request"
     elif (R.status_code == 300) :
          M = "No Accessible files"
     elif(R.status_code == 200):
          print(eval( R.content.decode())["CID"])
          data = eval( R.content.decode())["CID"]
          return render_template("get_cids.html",cids=data) 
     else : 
          E = "Something went Wrong"  
     return render_template('Invalid_Credential.html', Credential_variable =" : "+E+M)    
  

@app.route("/send_to_ipfs",methods=['GET',"POST"])
def send_to_ipfs():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        r = request.form["address"]
        addresses = r.split(" ")
        print(r)
        
        # set the key and initialization vector (IV)
        key = get_random_bytes(16)
        iv = get_random_bytes(16)

        # create the AES cipher object
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # open the input and output files
        with open(app.config['UPLOAD_FOLDER'].replace('/','\\')+"\\"+file.filename, 'rb') as input_file, open(app.config['UPLOAD_FOLDER'].replace('/','\\')+"\\"+file.filename.replace('.txt','Encrypted')+'.enc', 'wb') as output_file:
            # read the input file contents
            plaintext = input_file.read()

            # add padding to the plaintext so that its length is a multiple of 16 bytes
            padding_length = 16 - (len(plaintext) % 16)
            padded_plaintext = plaintext + bytes([padding_length] * padding_length)
            
            # encrypt the padded plaintext
            ciphertext = cipher.encrypt(padded_plaintext)

            # write the IV and ciphertext to the output file
            A = AccessNetwork()
            for address in addresses : 
                A.get_key_from_chain(address)
                
                if(A.error == "Invalid Address"):
                     error = "Address: " + address
                     print("In invalid address")
                     return render_template('Invalid_Credential.html', Credential_variable =error)
                     print("Skipped")
                encrypted_key=A.encrypt_key(key)
                output_file.write("Address:\n".encode("utf-8"))
                output_file.write((address).encode("utf-8"))
                output_file.write("\n".encode("utf-8"))
                output_file.write((encrypted_key))
                output_file.write("\n".encode("utf-8"))
            output_file.write("\n---keys_over---\n".encode("utf-8"))    
            output_file.write((iv))
            output_file.write("\n".encode("utf-8"))
            output_file.write(ciphertext)
            output_file.close()
            A.send_to_ipfs(app.config['UPLOAD_FOLDER'].replace('/','\\')+"\\"+file.filename.replace('.txt','Encrypted')+'.enc')
            
            print(A.ipfsResult)
            os.remove(app.config['UPLOAD_FOLDER'].replace('/','\\')+"\\"+file.filename.replace('.txt','Encrypted')+'.enc')
            # Send cid and addresses to transaction pool
            transaction = dict()
            transaction["cid"] = A.ipfsResult['Hash']
            transaction["receiver_address"] = [eval(i) for i in addresses]
            
            try:
                owner = initialize_wallet(privateKeyOfWallet) 
            except:
                error = ":- Enter QR"
                return render_template('Invalid_Credential.html', Credential_variable =error)
            owner = initialize_wallet(privateKeyOfWallet)    
            T = Transaction(owner ,receiver_address = transaction["receiver_address"],cid = transaction["cid"])
            T.sign()
            resp = T.add_public_key_to_transaction(owner.public_key)
            print("Transaction from fe ",resp)
            r=A.send_to_pool(resp)
            print(r)
    
        return "File has been uploaded. CID = " + transaction["cid"]
    return render_template('send_to_ipfs.html', form=form)

def decrypte_downloaded_file():
    
    Address_found = False
    print("from decrypt file " , address)

    with open(download_file_path, 'rb') as f:

        for line in f :
               add= line[0:58]
               print(add[2:57])
               add = line[2:57]
               print(add == address , type(add) ,type(address))
               

               if(Address_found == True) :
                       print("from address found", line[0:15] , type(line))
                       s = "---keys_over---" 
                       print(line[0:15] == s.encode('utf-8') )
                       if line[0:15] ==  s.encode('utf-8')  :
                               #print("in if ")
                               
                               if True : 
                                    line = f.read(16)
                                    iv = line
                                    print(iv)
                                    print("***")
                                    
                                    

                               enc_data = f.read()
                               print(enc_data)
                               
                               decrypted_aes_key = rsa.decrypt(enc_aes_key, encryptionPrivateKey)
                               
                               print("dec aes key: ",decrypted_aes_key)
                               key = decrypted_aes_key[0:16]
                               
                               cipher = AES.new(key, AES.MODE_CBC, iv)

                               ciphertext = enc_data[1:] #[1:] because while writing file we are adding "\n" to file then padded cipher text. When we perform enc_data = f.read() , enc_data = "\n"+padded cipher text , which ruins the padding , thats why we remove "\n" to have enc_data = padded cipher text

                               #padding 
                               #padding_length = 16 - (len(ciphertext) % 16)
                               #ciphertext = ciphertext + bytes([padding_length] * padding_length)  
                               #print("padding length {1}", padding_length , "cipher text" , ciphertext)
                               #padding_length = 16 - (len(ciphertext) % 16)
                               #print("padding length {1}", padding_length , "cipher text" , ciphertext)
                                
                                # decrypt the ciphertext
                               padded_plaintext = cipher.decrypt((ciphertext))
                               print(padded_plaintext)  
                                # remove the padding from the plaintext
                               padding_length = padded_plaintext[-1]
                               print("padding length ", padding_length)
                               plaintext = padded_plaintext[:-padding_length]

                                # write the plaintext to the output file
                                
                               print("output from file")
                               print(plaintext)
                               return plaintext.decode('utf-8')  


                               
                       else :
                               print("from else", add)
                               continue                                              

               if (add == address):
                       print(line)
                       print(add == address)
                       Address_found = True  
                       enc_aes_key = f.readline()
                       enc_aes_key = enc_aes_key[0:-1]
                       print("enc aes key : ",enc_aes_key ) 

     
@app.route("/get_from_ipfs",methods=['GET',"POST"])
def get_from_ipfs():
    #json = {cid = "entered cid"}
    if request.method == 'POST':
        json = request.form["cid"]
        cid = json

        A = AccessNetwork() 
        data = A.get_from_ipfs(cid)
        if(data.status_code!=200):
             error = "CID: " + cid
             return render_template('Invalid_Credential.html', Credential_variable =error)
                     
        with open(download_file_path, 'wb') as f:
            f.write(data.content)

        data = decrypte_downloaded_file()
        return render_template('get_from_ipfs.html', Decrypted_data = data)
    
    return render_template('get_from_ipfs.html')


    
              

 



    




#user_autorisation_QR()



# @app.route("/vote")
# def vote():
#     return render_template("vote.html")

# @app.route("/not_eligible")
# def not_eligible():
#     return render_template("not_eligible.html")


# def send_to_pool(transaction):
#  while(1):  

#     try :
#         response=requests.post(f"http://127.0.0.1:5000/add_transaction",json=json.dumps(transaction)) 
#         return response
#     except Exception as e :
#         print(e)

      

# @app.route('/make_transaction',methods=['POST'])
# def transaction():
#     json = request.get_json()
#     transaction_keys = [ 'receiver_address', 'amount']
#     if not all(key in json for key in transaction_keys):
#         return 'Some elements of the transaction are missing', 400
#     try: 
#         f = open(download_file_path,'r')
#         private_key = RSA.import_key(f.read())
        
#         owner = initialize_wallet(private_key)    
#         T = Transaction(owner ,receiver_address = json["receiver_address"],amount = json["amount"])
#         T.sign()
#         #sending to transaction pool
#         resp = send_to_pool(T.send_to_nodes(owner.public_key)) #for now we need to send public key as it will be checking signing details
   
#     except Exception as e :
#        print(f'Error from Wallet IN method in transaction ')
#        return "Failed to Vote" , 400
    
#     #returning result back to front end
#     return jsonify(resp)


# @app.route('/test_make_transaction',methods=['POST'])
# def test_transaction():
    
#     if request.method == 'POST':
#         if request.form.get('action1') == 'id1':
#             json = {"receiver_address" : "candidate 1" ,"amount":1}
#         elif  request.form.get('action2') == 'id2':
#             json = {"receiver_address" : "candidate 2" ,"amount":1}
#         else:
#            json = {"receiver_address" : "candidate 3" ,"amount":1}
   

#     print(json)
#     ##########################################
#     #json = request.get_json()
#     #json = {"receiver_address " : "avs" ,"amount":1}
#     transaction_keys = [ "receiver_address", "amount"]
#     if not all(key in json for key in transaction_keys):
#        return f'From test_make_transaction Some elements of the transaction are missing ', 400
    
#     f = open(download_file_path,'r')
#     private_key = RSA.import_key(f.read())
#     public_key = private_key.publickey().export_key()

#     owner = initialize_wallet(private_key)    
#     T = Transaction(owner ,receiver_address = json["receiver_address"],amount = json["amount"])
#     T.sign()
#         #sending to transaction pool
#         #resp = send_to_pool(T.send_to_nodes())
#         #print(f'publick key {owner.public_key}')
#     resp = T.send_to_nodes(owner.public_key)
#     try:   
#         r=send_to_pool(resp)
   

#         print(f'response from pool {r.headers["Content-Type"]}')
#         #resp = eval(resp["data"])
#         print(f'output from transaction pool: {r.json()}')   
#         #Transaction_data = change_dictionary_keys(resp["TransactionData"])

      
#         #print(validate_signature(resp["public_key"] ,  resp["signature"] , convert_transaction_data_to_bytes(resp["TransactionData"])))
#         #print(f'resp ')
#         #print(f' public_key : {resp["public_key"]} , signature : {resp["signature"] } transaction_in_bytes : {convert_transaction_data_to_bytes(Transaction_data)}')
#         #print(convert_transaction_data_to_bytes(Transaction_data))
#         #f'{validate_signature(resp["public_key"] ,  resp["signature"], convert_transaction_data_to_bytes(Transaction_data))}'
#         r = r.json()
        

#         print("------------------------------------------------------------")
#         print(r.keys())
#         print('code' in r.keys())
#         if("code" in r.keys()): 
#             return render_template("no_vote.html")
#         else:
            
#             block_number = r["index"]

#             prev_hash = r["previous_hash"]
#             nonce = r["proof"]
#             timestamp =  r["timestamp"]

#             #'transactions': [{'input': [{'amount': 1, 'receiver': 'candidate 1'}, {'amount': 0, 'sender': ""}], 'output': [{'current_balance': 1, 'sender': ""}]}
#             transaction = r["transactions"]
#             input  = transaction[0]["output"]
#             output = transaction[0]["input"]

#             output_sender_dict = input[0]

#             input_receiver_dict = output[1]
#             input_sender_dict = output[0]
#             return render_template('info_table.html' , block_number=block_number , prev_hash=prev_hash , nonce=nonce ,timestamp=timestamp,output_sender_dict=output_sender_dict ,input_receiver_dict1=input_receiver_dict ,input_sender_dict1=input_sender_dict)


#         #return r.json() , 200
#     except Exception as e :
#        print(f'Error from Wallet IN method test_make_transaction{e} ')
#        response = {"message" : "something went wrong try again" , "code" : 400}
#        return jsonify(response), 400
    
#     #returning result back to front end
#     #return jsonify(resp)
# """def send_to_pool_test(transaction ,  public_key):
#     validate_signature(public_key,transaction.signature ,)
# """


app.debug = True

app.run('0.0.0.0',3000)







