First_Name = "Sparsh"
Last_Name = "Mehta"
UID = 119362914

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import binascii as ba

keys = RSA.generate(2048)

def rsa_enc_public(inputblock, keypair):
    encryptor = PKCS1_v1_5.new(keypair.publickey())
    ciphertext = encryptor.encrypt(inputblock)
    return ciphertext

def rsa_dec_private(cipherblock, keypair):
    decryptor = PKCS1_v1_5.new(keypair)
    plaintext = decryptor.decrypt(cipherblock, None)
    return plaintext


msg = b'A message for encryption'
enc = rsa_enc_public(msg,keys)
dec = rsa_dec_private(enc,keys)

print("Encrypted - ",str(ba.hexlify(enc))[2:-1])
print()
print("Decrypted - ",str(dec)[2:-1])