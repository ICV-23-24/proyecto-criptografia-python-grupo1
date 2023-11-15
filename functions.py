from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def encrypt_file(file_path, key):
    key = key.encode('utf-8')
    
    # Lee el contenido del archivo
    with open(file_path, 'rb') as file:
        original_data = file.read()

    # Crea un objeto AES en modo ECB con la clave proporcionada y realiza el relleno del mensaje.
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)

    # Encripta el contenido del archivo y convierte el resultado a formato base64.
    encrypted_data = b64encode(cipher.encrypt(pad(original_data, AES.block_size))).decode('utf-8')

    # Guarda el archivo encriptado
    with open("archivo_encriptado.txt", 'w') as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_file(encrypted_file_path, key):
    key = key.encode('utf-8')
    
    # Lee el contenido del archivo encriptado
    with open(encrypted_file_path, 'r') as file:
        encrypted_data = file.read()

    # Crea un objeto AES en modo ECB con la clave proporcionada y realiza el relleno del mensaje.
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)

    # Desencripta el contenido del archivo y realiza el despad (elimina el relleno).
    decrypted_data = unpad(cipher.decrypt(b64decode(encrypted_data)), AES.block_size)

    # Guarda el archivo desencriptado
    with open("archivo_desencriptado.txt", 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

# Ejemplo de uso:
# encrypt_file("archivo_original.txt", "tu_clave_secreta")
# decrypt_file("archivo_encriptado.txt", "tu_clave_secreta")


# def AES(file_name, encryption_key):
#     # Nombre del archivo
#     file_name = "archivo.txt"

#     # Lee el contenido del archivo
#     with open(file_name, 'r') as file:
#         original_data = file.read()

#     # Define una clave
#     encryption_key = "1234"

#     # Encripta el contenido del archivo
#     encrypted_data = encrypt_message(original_data, encryption_key)

#     # Guarda el archivo encriptado
#     with open("archivo_encriptado.txt", 'w') as encrypted_file:
#         encrypted_file.write(encrypted_data)

# def DES(encryption_key2):
#     # Desencripta el archivo encriptado
#     with open("archivo_encriptado.txt", 'r') as encrypted_file2:
#         encrypted_data2 = encrypted_file2.read()

#     decrypted_data = decrypt_message(encrypted_data2, encryption_key2)

#     # Guarda el archivo desencriptado
#     with open("archivo_desencriptado.txt", 'w') as decrypted_file:
#         decrypted_file.write(decrypted_data)