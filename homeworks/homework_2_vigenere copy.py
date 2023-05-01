import numpy as np
First_Name = "Sparsh"
Last_Name = "Mehta"
UID = 119362914
M = np.array([[17,17,5],[21,18,21],[2,2,19]])

def format_message(message):
    return message.replace(' ', '').upper()


def vigenere_enc(message, key):
    plain_text = format_message(message)
    newkey = list(key)
    if(len(plain_text) == len(newkey)):
        pass
    else:
        for n in range(len(plain_text) - len(key)):
            newkey.append(key[n % len(key)])
        newkey = ''.join(newkey)
        
    cipher = []
    for i in range(len(plain_text)):
        t = (ord(plain_text[i]) + ord(newkey[i])) % 26
        t += ord('A')
        cipher.append(chr(t))
    return(''.join(cipher))

def vigenere_dec(message, key):
    plain_text = format_message(message)
    newkey = list(key)

    if(len(plain_text) == len(newkey)):
        pass
    else:
        for n in range(len(plain_text) - len(key)):
            newkey.append(key[n % len(key)])
        newkey = ''.join(newkey)
    
    cipher = []
    for i in range(len(plain_text)):
        t = (ord(plain_text[i]) - ord(newkey[i])) % 26
        t += ord('A')
        cipher.append(chr(t))
    return(''.join(cipher))

def hill_enc(M, message):
    formatted = list(format_message(message))
    while(len(formatted) % 3 != 0):
        formatted.append('X')
    formatted=np.array([ord(i)-65 for i in formatted]).reshape(len(formatted) // 3,3)
    cipher = np.mod(formatted @ M, 26)
    cipher=list(cipher.flatten())
    cipher = ''.join(list(map(lambda x: chr(x+65), cipher)))
    return cipher


    

def main():
    message = "Test String"
    key = "KEY"
    print(vigenere_enc(message, key))
    print(vigenere_dec('DIQDWRBMLQ', key))
    print(hill_enc(M,'Test String'))

main()
