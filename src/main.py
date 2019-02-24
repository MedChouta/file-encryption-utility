from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import base64
import sys
import os
from Encryptor import *

iv = Random.get_random_bytes(AES.block_size)

def encrypt(fileName, key):
    with open(fileName, "r+b") as file2Encrypt:
        data = file2Encrypt.read()
        encryptor = Encryptor(key, iv)  
        cipherText = encryptor.encrypt(data)
        cipherText = base64.b64encode(cipherText)
        with open("{}.enc".format(fileName), "wb") as encryptedFile:
            encryptedFile.write(cipherText)
    os.remove(fileName)

def decrypt(fileName, key):
    try:
        with open(fileName, "r+b") as file2Decrypt:
                data = base64.b64decode(file2Decrypt.read())
                decryptor = Encryptor(key, data[:AES.block_size])
                plainText = decryptor.decrypt(data)
                with open(fileName[:-4], "wb") as decryptedFile:
                    decryptedFile.write(plainText)
        os.remove(fileName)
    except:
        print("Cannot decrypt this file")