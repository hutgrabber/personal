from Crypto.Cipher import DES, AES
First_Name = "Sparsh"
Last_Name = "Mehta"
UID = 119362914

def des_enc(input_str, des_key):
    des_cipher = DES.new(des_key, DES.MODE_ECB)
    desciphertext = des_cipher.encrypt(input_str)
    return desciphertext

def aes_enc(input_str, aes_key):
    aes_cipher = AES.new(aes_key, AES.MODE_ECB)
    aesciphertext = aes_cipher.encrypt(input_str)
    return aesciphertext

def invertbit(inputblock, b):
    l = len(inputblock)

    inputblock = list(bin(int.from_bytes(inputblock, "big"))[2:]) 
    for i in range(len(inputblock)):
        if(i == b-1):
            x = int(inputblock[i])
            x = 0 if x == 1 else 1
            inputblock[i] = str(x)
            break
    inputblock = int(''.join(inputblock),2).to_bytes(l,'big')
    return inputblock


def findbitdiff(original_cipher, new_cipher): 
    #original_cipher = list(bin(int.from_bytes(original_cipher, "big"))[2:])
    #new_cipher = list(bin(int.from_bytes(new_cipher, "big"))[2:])

    original_cipher=[bin(i)[2:].zfill(8) for i in original_cipher]
    new_cipher=[bin(i)[2:].zfill(8) for i in new_cipher]
    
    temp=0
    for i,j in zip(original_cipher,new_cipher):
        for x,y in zip(i,j):
            if(x!=y):
                temp+=1

    return temp

def des_input_av_test(inputblock, key, bitlist):
    diff_list = []
    originalcipher = des_enc(inputblock, key)
    for b in bitlist:
        newinput = invertbit(inputblock, b)
        newcipher = des_enc(newinput, key)
        numbitdifferences = findbitdiff(originalcipher, newcipher)
        diff_list.append(numbitdifferences)
    return diff_list

def des_key_av_test(inputblock, key, bitlist):
    
    diff_list = []
    originalcipher = des_enc(inputblock, key) 
    for b in bitlist:
        newkey = invertbit(key, b)
        newcipher = des_enc(inputblock, newkey)
        numbitdifferences = findbitdiff(originalcipher, newcipher)
        diff_list.append(numbitdifferences)
    return diff_list
    
def aes_input_av_test(inputblock, key, bitlist):
    diff_list = []
    originalcipher = aes_enc(inputblock, key)
    for b in bitlist:
        newinput = invertbit(inputblock, b)
        newcipher = aes_enc(newinput, key)
        numbitdifferences = findbitdiff(originalcipher, newcipher)
        diff_list.append(numbitdifferences)
    return diff_list

def aes_key_av_test(inputblock, key, bitlist):
    diff_list = []
    originalcipher = aes_enc(inputblock, key)
    for b in bitlist:
        newkey = invertbit(key, b)
        newcipher = aes_enc(inputblock, newkey)

        numbitdifferences = findbitdiff(originalcipher, newcipher)
        diff_list.append(numbitdifferences)
    return diff_list


if __name__ == "__main__":

    #Textbook examples validation: Both print output should be same in each case. This is just to verify the code works you can replace these with your own test cases.
    print("=========================TESTING_AES_INPUT_BOOK_EXAMPLE===============================")
    original = aes_enc(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98')
    new = aes_enc(b'\x00\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98')

    print(findbitdiff(original,new))
    print(aes_input_av_test(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98',[7]))

    print("=========================TESTING_AES_KEY_BOOK_EXAMPLE===============================")

    original = aes_enc(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98')
    new = aes_enc(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',b'\x0e\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98')

    print(findbitdiff(original,new))
    print(aes_key_av_test(b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xd6\xaf\x7f\x67\x98',[7]))

    print("=========================TESTING_DES_INPUT_BOOK_EXAMPLE===============================")
    original = des_enc(b'\x02\x46\x8a\xce\xec\xa8\x64\x20',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59')
    new = des_enc(b'\x12\x46\x8a\xce\xec\xa8\x64\x20',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59')

    print(findbitdiff(original,new))
    print(des_input_av_test(b'\x02\x46\x8a\xce\xec\xa8\x64\x20',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59',[3]))

    print("=========================TESTING_DES_KEY_BOOK_EXAMPLE===============================")

    original = des_enc(b'\x02\x46\x8a\xce\xec\xa8\x64\x20',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59')
    new = des_enc(b'\x02\x46\x8a\xce\xec\xa8\x64\x20',b'\x1f\x15\x71\xc9\x47\xd9\xe8\x59')

    print(findbitdiff(original,new))
    print(des_key_av_test(b'\x02\x46\x8a\xce\xec\xa8\x64\x20',b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59',[3]))

    av_val=aes_input_av_test(b'thisoneis16bytes',b'veryverylongkey!',[5, 29, 38])
    print(av_val)
    assert av_val==[65, 67, 68], "Test Case 1: aes_input failed"


    av_val=aes_key_av_test(b'thisoneis16bytes',b'veryverylongkey!',[5, 29, 38])
    print(av_val)
    assert av_val==[61, 65, 65], "Test Case 2: aes_key failed"

    dv_val=des_input_av_test(b'thisoneis16bytes',b'deskey!!',[3, 25, 36])
    print(dv_val)
    assert dv_val==[27, 35, 28], "Test Case 3: des_input failed"
    
    
    dv_val=des_key_av_test(b'thisoneis16bytes',b'deskey!!',[3, 25, 36])
    print(dv_val)
    assert dv_val==[56, 68, 64], "Test Case 4: des_key failed"
