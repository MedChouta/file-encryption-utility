from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import base64
import sys
import os
from Encryptor import *

key = b'this is a key123'
iv = Random.get_random_bytes(AES.block_size)

def showhelp():
    print("Usage: {} [File] [Option]".format(sys.argv[0]))
    print("Options:\n\t-e: encrypt the file\n\t-d: decrypt the file")


if len(sys.argv) < 3:
    showhelp()
    exit()

elif sys.argv[2] == "-e":
    with open(sys.argv[1], "r+b") as file2Encrypt:
        data = file2Encrypt.read()
        encryptor = Encryptor(key, iv)  
        cipherText = encryptor.encrypt(data)
        cipherText = base64.b64encode(cipherText)
        with open("{}.enc".format(sys.argv[1]), "wb") as encryptedFile:
            encryptedFile.write(cipherText)
    os.remove(sys.argv[1])

elif sys.argv[2] == "-d":
    try:
        with open(sys.argv[1], "r+b") as file2Decrypt:
                data = base64.b64decode(file2Decrypt.read())
                decryptor = Encryptor(key, data[:AES.block_size])
                plainText = decryptor.decrypt(data)
                with open(sys.argv[1][:-4], "wb") as decryptedFile:
                    decryptedFile.write(plainText)
        os.remove(sys.argv[1])
    except:
        print("the file needs to be encrypted")
else:
    showhelp()