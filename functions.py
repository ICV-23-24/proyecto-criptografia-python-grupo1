from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode

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

def AES(file_name, encryption_key):
    # Nombre del archivo
    file_name = "archivo.txt"

    # Lee el contenido del archivo
    with open(file_name, 'r') as file:
        original_data = file.read()

    # Define una clave
    encryption_key = "1234"

    # Encripta el contenido del archivo
    encrypted_data = encrypt_message(original_data, encryption_key)

    # Guarda el archivo encriptado
    with open("archivo_encriptado.txt", 'w') as encrypted_file:
        encrypted_file.write(encrypted_data)

def DES(encryption_key2):
    # Desencripta el archivo encriptado
    with open("archivo_encriptado.txt", 'r') as encrypted_file2:
        encrypted_data2 = encrypted_file2.read()

    decrypted_data = decrypt_message(encrypted_data2, encryption_key2)

    # Guarda el archivo desencriptado
    with open("archivo_desencriptado.txt", 'w') as decrypted_file:
        decrypted_file.write(decrypted_data)