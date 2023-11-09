from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
# Necesario para hacer funcionar la descarga de archivos.
import os


def encrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message).decode('utf-8')

def decrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(message)), AES.block_size).decode('utf-8')
    return decrypted_message

def generate_keys():
    # Genera un nuevo par de claves.
    key = RSA.generate(2048)
    # Obtiene la clave pública.
    publicKey = key.publickey().export_key('PEM')
    # Obtiene la clave privada
    privateKey = key.export_key('PEM')

    tempDir = os.path.join("static","temp")
    os.makedirs(tempDir, exist_ok=True)

    publicFile = os.path.join(tempDir, "public_key.key")
    privateFile = os.path.join(tempDir, "private_key.key")

    with open(publicFile, "w") as file:
        file.write(publicKey.decode("utf-8"))

    with open(privateFile, "w") as file:
        file.write(privateKey.decode("utf-8"))

