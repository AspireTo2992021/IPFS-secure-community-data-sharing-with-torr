import cv2
from pyzbar import pyzbar

# load the QR code image
image = cv2.imread('qr2.png')

# find and decode QR codes in the image
qr_codes = pyzbar.decode(image)

# print the data from the first QR code
#print(qr_codes[0].data.decode('utf-8'))  
data =  str(qr_codes[0].data.decode('utf-8'))

k1 , k2, k3 = data.split("***")

print(k1)
print(k2)
print(k3)