from Crypto.Cipher import AES, ChaCha20
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def pad(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length] * padding_length)

def encrypt_file(file, key, type):
    
  
    key = key.encode('utf-8')
    
    # Lee el contenido del archivo
    original_data = file.read()

    if type == "AES":
        print("Cifra con AES")
        # Crea un objeto AES en modo ECB con la clave proporcionada y realiza el relleno del mensaje.
        cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
        
        # Encripta el contenido del archivo y convierte el resultado a formato base64.
        encrypted_data = b64encode(cipher.encrypt(pad(original_data, AES.block_size))).decode('utf-8')
    
    elif type == "ChaCha20" and len(key) != 32:
        print("Cifra con ChaCha20")
        
        # Crea un objeto ChaCha20 en modo de cifrado
        cipher = ChaCha20.new(key=key, nonce=b'\x00'*8)
        # Realiza el relleno del mensaje
        padded_data = pad(original_data, 64)
        # Cifra el mensaje
        encrypted_data = cipher.encrypt(padded_data)
    else:
        print("La clave para ChaCha20 debe tener 32 bytes.")
    
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
