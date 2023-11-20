from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def encrypt_file(file, key):
    key = key.encode('utf-8')
    
    # Lee el contenido del archivo
    original_data = file.read()

    # Crea un objeto AES en modo ECB con la clave proporcionada y realiza el relleno del mensaje.
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)

    # Encripta el contenido del archivo y convierte el resultado a formato base64.
    encrypted_data = b64encode(cipher.encrypt(pad(original_data, AES.block_size))).decode('utf-8')

    # Guarda el archivo encriptado
    with open("static/temp/archivo_encriptado.gpg", 'w') as encrypted_file:
        encrypted_file.write(encrypted_data)
    
    return 1

def decrypt_file(file, key):
    key = key.encode('utf-8')

    # Lee el contenido del archivo encriptado
    encrypted_data = file.stream.read()

    # Crea un objeto AES en modo ECB con la clave proporcionada y realiza el relleno del mensaje.
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)

    # Desencripta el contenido del archivo y realiza el despad (elimina el relleno).
    decrypted_data = unpad(cipher.decrypt(b64decode(encrypted_data)), AES.block_size).decode('utf-8')

    # Guarda el archivo desencriptado
    decrypted_file_path = "static/temp/archivo_desencriptado.txt"
    with open(decrypted_file_path, 'w') as decrypted_file:
        decrypted_file.write(decrypted_data)

    # Devuelve el contenido desencriptado
    return decrypted_data
