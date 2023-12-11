from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
# Necesario para hacer funcionar la descarga de archivos.
import os

from flask import jsonify


def pad(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length] * padding_length)

# Funcion que encripta un archivo simetricamente.
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
    
        cipher = DES.new(key, DES.MODE_CFB, iv=get_random_bytes(8))

        
        msg = cipher.encrypt(original_data)
    
        with open("static/temp/archivo_encriptado.gpg", 'wb') as encrypted_file:
            # Convierte los bytes a ASCII antes de escribir
            encrypted_file.write(cipher.iv + msg)
    
    return 1

# Funcion que desencrypta un archivo simetricamente.
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
        
        cipher = DES.new(key, DES.MODE_CFB, iv=file.read(8))
        
        ciphertext = file.read()
        
        decrypted_text = cipher.decrypt(ciphertext)     
        
        with open("static/temp/archivo_desencriptado.txt", 'wb') as decrypted_file:
            # Convierte los bytes a ASCII antes de escribir
            decrypted_file.write(decrypted_text)
    return 1


# Función que genera un nuevo par de claves
def generate_keys():
    # Genera un nuevo par de claves.
    key = RSA.generate(2048)
    # Obtiene la clave pública.
    publicKey = key.publickey().export_key('PEM')
    # Obtiene la clave privada
    privateKey = key.export_key('PEM')

    # Si la ruta static/temp no existe, la crea
    tempDir = os.path.join("static","temp")
    os.makedirs(tempDir, exist_ok=True)

    # Crea las rutas de los archivos.
    publicFile = os.path.join(tempDir, "public_key.key")
    privateFile = os.path.join(tempDir, "private_key.key")

    # Escribe los archivos
    with open(publicFile, "w") as file:
        file.write(publicKey.decode("utf-8"))

    with open(privateFile, "w") as file:
        file.write(privateKey.decode("utf-8"))

# Función que obtiene los nombres de los archivos de las claves en la base de datos.
def load_keys():
    #Directiorio de claves
    keys_dir = "static/public_keys"

    fileNames = os.listdir(keys_dir)
    print("Keys are: ")
    for x in fileNames:
        print("- " +x)

    return fileNames

# Función que elimina un archivo dentro de la carpeta static.
def removeFile(relative_from_static):
    file_path = os.path.join("static",relative_from_static)
    try:
        os.remove(file_path)
        return jsonify({"message": "Archivo eliminado exitosamente."})
    except FileNotFoundError:
        return jsonify({"message": "Archivo no encontrado."})
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el archivo: {str(e)}"})



## Funciones de validación de archivos.
# Esta función decide si un nuevo archivo .key, puede ser añadido al servidor, o si no cubre con todos los requisitos.
def canBeLoaded(ID,file, route):
    genName = ID + ".key"
    # Comprobamos que el nuevo archivo no existe.
    if genName in load_keys():
        return False
    
    # Comprobamos que el archivo es una clave pública.
    if not isPublic_key(file.read()):
        return False
    
    # Comprobamos que el archivo no es muy grande:
    if isBig(file, 1):
        return False


    return True


# Función utilizada para strings, para comprobar si son calves públicas o no.
def isPublic_key(content):
    # Si estos strings se encuentran en el archivo, sabemos que es una clave pública
    if b"BEGIN PUBLIC KEY" in content and b"END PUBLIC KEY" in content:
        return True
    
    ##
    # Suggestion: Otra manera de la que se podría hacer, sería, trata de cargar la clave al arnillo de confianza del servidor,
    # Si funciona, entonces la clave es pública y apta, no un txt con eso escrito y ya.
    # Si da error, entonces no es ni siquiera una clave.
    ##

    return False

# Función utilizada para comprobar si el tamaño de los archivos es muy grande.
def isBig(file, maxSize):
    # Obtén el tamaño del búfer del objeto BytesIO en bytes.
    size = len(file.getbuffer())
    print("Tamaño de archivo en bytes: " + str(size))
    # Lo pasamos a Kilobytes.
    sizeK = size/1024
    # Si es mayor a la cantidad determinada, entonces el archivo SI es muy grande.
    if sizeK > maxSize:
        return True
    
    return False


# Función de Kevin: encriptar asimétricamente
def encrypt_file(file, key):
    print("Esta función encripta el archivo en la variable 'file', utilizando la clave 'key'. ")


# Función de kevin: desencriptar asimétricamente.
def decrypt_file(file, keyFile):
    print("Esta función desencripta el archivo en la variable 'file', utilizando el archivo de clave privada en la variable 'keyFile'. ")


