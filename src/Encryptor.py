from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random

class Encryptor:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        self.key = pad(self.key, AES.block_size)
        encryptedData = AES.new(self.key, AES.MODE_CBC, self.iv)
        paddedData = pad(data, AES.block_size)
        cipherText = self.iv + encryptedData.encrypt(paddedData)
        return cipherText

    def decrypt(self, data):
        self.key = pad(self.key, AES.block_size)
        decryptedData = AES.new(self.key, AES.MODE_CBC, self.iv)
        plainText = decryptedData.decrypt(data)
        plainText = unpad(plainText, AES.block_size)
        return plainText[AES.block_size:]