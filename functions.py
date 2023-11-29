from Crypto.Cipher import AES, DES
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
        
        # Guarda el archivo encriptado
        with open("static/temp/archivo_encriptado.gpg", 'w') as encrypted_file:
            encrypted_file.write(encrypted_data)
    
    elif type == "DES":
        print("Cifra con DES")
        key = key[:8].ljust(8, b'\0')
    
        cipher = DES.new(key, DES.MODE_OFB)

        original_data = original_data.ljust(len(original_data) + (8 - len(original_data) % 8) % 8, b'\0')
        
        msg = cipher.iv + cipher.encrypt(original_data)
    
        with open("static/temp/archivo_encriptado.gpg", 'wb') as encrypted_file:
            # Convierte los bytes a ASCII antes de escribir
            encrypted_file.write(msg)
    
    return 1

def decrypt_file(file, key, type):
    key = key.encode('utf-8')
    

    if type == "AES":
        print("Cifra con AES")
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

    elif type == "DES":
        
        key = key[:8].ljust(8, b'\0')
        
        cipher = DES.new(key, DES.MODE_OFB)
        
        ciphertext = file.read()
        
        decrypted_text = cipher.decrypt(ciphertext)
        
        decrypted_text = decrypted_text.rstrip(b'\0')
        
        
        # decrypted_ascii = decrypted_text.decode('utf-8')
        
        with open("static/temp/archivo_desencriptado.txt", 'wb') as decrypted_file:
            # Convierte los bytes a ASCII antes de escribir
            decrypted_file.write(decrypted_text)
    # Devuelve el contenido desencriptado
    return 1
