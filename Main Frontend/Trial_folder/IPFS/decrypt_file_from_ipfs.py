# import ipfshttpclient

# client = ipfshttpclient.connect()  # Connect to the IPFS daemon
# hash = "QmX1fwC2QF9ELNzDdYjcwteTZpwpUpNcLqxGnwyzKjfoeH"  # IPFS hash of the file to download
# data = client.get(hash)  # Download the file from IPFS
# with open('my_file.txt', 'wb') as f:
#     f.write(data.read())
from flask import request
import requests
import ipfsApi

import rsa
from Crypto.Cipher import AES

#api = ipfsApi.Client(host='127.0.0.1', port=8001)
IPFS_FILE_URL = "http://127.0.0.1:8080/ipfs/"
#hash = 'QmZXWuMBMakGmi5f2wi5YmuHQf8EMC1pXjQyAwdGGWFDyZ'
hash = 'QmcQK5ZRpQQFQ3CJ6dt1ufe2jA86hnFUQLwve8SB4DVWCM'
hash2='QmQ4zdnHfTcBNKehpK5CDpVzw18zvcp4fbqx6KRXa4Gm6q'
hash3 = 'QmPT2kfdUCz8Pncy7ce2YrqWbqmcLdNJC8BkpUGB92Wjv4'
url = IPFS_FILE_URL + hash3
h = {"Accept-Encoding": "identity"}
data = requests.get(url, stream=True, verify=False, headers=h)


with open('downloaded_file.enc', 'wb') as f:
        f.write(data.content)


enc_aes_key = ""
address =  "b'3bzvhHzonRKR77VBaZcL6vWM196Ebx3jiSMwLN2ewx9ByJLy7yKZE4M'"
Address_found = False
succesor_address_found = False
rsa_priv_key = rsa.PrivateKey(61452923054399835053317147689966183362298115752943498508878325187325798425151, 65537, 24977058934648342254225992386249435035421855834646290655521602483769401304073, 86536540433177659375691145624637666358531, 710138431081063925653791062376416021)

with open('downloaded_file.enc', 'rb') as f:

        for line in f :
               add= line[0:58]
               print(add[2:57])
               print(add == address.encode('utf-8'))

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
                               
                               decrypted_aes_key = rsa.decrypt(enc_aes_key, rsa_priv_key)
                               
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
                                  


                               break 
                       else :
                               print("from else", add)
                               continue                                              

               if (add == address.encode('utf-8')):
                       print(line)
                       print(add == address.encode('utf-8'))
                       Address_found = True  
                       enc_aes_key = f.readline()
                       enc_aes_key = enc_aes_key[0:-1]
                       print("enc aes key : ",enc_aes_key )               
                
                

                
                


