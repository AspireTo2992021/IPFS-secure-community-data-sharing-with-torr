import rsa
import rsa.randnum
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

with open('c.enc', 'rb') as f :
    key = f.readline()
    #print(key)
    key = key[0:-1]
    #print(key)
    iv = f.read(16)
    d = f.read()
    rsa_priv_key = rsa.PrivateKey(61452923054399835053317147689966183362298115752943498508878325187325798425151, 65537, 24977058934648342254225992386249435035421855834646290655521602483769401304073, 86536540433177659375691145624637666358531, 710138431081063925653791062376416021)
    print(key)
    print(iv)
    # print(d)

    decrypted_aes_key = rsa.decrypt(key, rsa_priv_key)
