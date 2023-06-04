import qrcode
import io
from Crypto.PublicKey import RSA
import rsa

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base58
from Crypto.Hash import RIPEMD160, SHA256

#Note: Don't name file qrcode.py as module is also qrcode

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


# get the private key in PEM format
private_key_pem = key.export_key()
(pubkey, privkey) = rsa.newkeys(256)

with open('key_storage//file.txt', 'a') as f:
    f.write(str(address))
    f.write("\n") 
    f.write(str(pubkey))
    f.write("\n")

# create a QR code image from the private key PEM data
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(private_key_pem)
qr.add_data("***")
qr.add_data(privkey)
qr.add_data("***")
qr.add_data(pubkey)
qr.make()

# create an in-memory file object to store the QR code image
img = qr.make_image(fill_color="black", back_color="white")
qr_img = io.BytesIO()
img.save(qr_img, 'PNG')

# save the QR code image to a file
with open('qr5.png', 'wb') as f:
    f.write(qr_img.getvalue())


import cv2
from pyzbar import pyzbar

# load the QR code image
image = cv2.imread('qr5.png')

# find and decode QR codes in the image
qr_codes = pyzbar.decode(image)

# print the data from the first QR code
#print(qr_codes[0].data.decode('utf-8'))  
data =  str(qr_codes[0].data.decode('utf-8'))

k1 , k2, k3 = data.split("***")

print(k1)
print(k2)
print(k3)
