First_Name = "Sparsh"
Last_Name = "Mehta"
UID = 119362914
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def caesar_str_enc(plain_text, key):
    plain_text_nospace =  ''.join(plain_text.split()).upper()
    encrypted = ""
    for i in plain_text_nospace:
        encrypted += alpha[(alpha.index(i) + key) % (len(alpha))]
    return encrypted

def caesar_str_dec(cipher_text, key):
    cipher_text_nospace =  ''.join(cipher_text.split()).upper()
    decrypted = ""
    for i in cipher_text_nospace:
        decrypted += alpha[(alpha.index(i) - key) % (len(alpha))]
    return decrypted

        

print("The Encrypted Text is - " + caesar_str_enc("A TEST SENTENCE", 2))
print("The Decrypted Text is - " + caesar_str_dec("CVGUVUGPVGPEG", 2))