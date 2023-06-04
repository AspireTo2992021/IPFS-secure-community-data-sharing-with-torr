import rsa
(pubkey, privkey) = rsa.newkeys(256)

print(pubkey)
print(privkey)