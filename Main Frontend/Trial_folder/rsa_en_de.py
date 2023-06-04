import rsa
import rsa.randnum
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# set the key and initialization vector (IV)
key = get_random_bytes(16)
iv = get_random_bytes(16)
print(key)
print(iv)

# create the AES cipher object
cipher = AES.new(key, AES.MODE_CBC, iv)

# open the input and output files
with open('input_file.txt', 'rb') as input_file, open('output_file.enc', 'wb') as output_file:
    # read the input file contents
    plaintext = input_file.read()

    # add padding to the plaintext so that its length is a multiple of 16 bytes
    padding_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)
    
    # encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

    # write the IV and ciphertext to the output file
    output_file.write(key)
    output_file.write(iv)
    output_file.write(ciphertext)

""" Decrypt """


# open the input and output files
with open('output_file.enc', 'rb') as input_file, open('output_file.txt', 'wb') as output_file:
    # read the IV and ciphertext from the input file
    key = input_file.read(16)
    iv=input_file.read(16)
    # create the AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = input_file.read()

    # decrypt the ciphertext
    padded_plaintext = cipher.decrypt(ciphertext)

    # remove the padding from the plaintext
    padding_length = padded_plaintext[-1]
    plaintext = padded_plaintext[:-padding_length]

    # write the plaintext to the output file
    output_file.write(plaintext)
    print("output from file")
    print(plaintext)



""" RSA """

(pubkey, privkey) = rsa.newkeys(256)

print(pubkey)
#print(privkey)

with open('public.pem', mode='w') as publicfile:
    publicfile.write(str(pubkey))
#print(privkey)

#aes_key = rsa.randnum.read_random_bits(128)
encrypted_aes_key = rsa.encrypt(key, pubkey)
decrypted_aes_key = rsa.decrypt(encrypted_aes_key, privkey)


""" stroring key in file and reading from file """    

with open('store_encrypted_key.pem', mode='w') as publicfile:
    s = str(encrypted_aes_key)
    s.replace('\\','\\\\')
    publicfile.write(str(s))

with open('store_encrypted_key.pem', mode='r') as publicfile:
    print("from file:")
    key = publicfile.read()
    print(key)
    if(eval(key) == encrypted_aes_key):
        print("equal")
    key = eval(key)
    decrypted_aes_key = rsa.decrypt(key, privkey)
    print("decr key")
    print(decrypted_aes_key)


# print(privkey)
# print(aes_key)
#print(encrypted_aes_key)
print(decrypted_aes_key)

