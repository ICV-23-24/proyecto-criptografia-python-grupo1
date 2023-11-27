from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
# Necesario para hacer funcionar la descarga de archivos.
import os

from flask import jsonify


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


def load_keys():
    #Directiorio de claves
    keys_dir = "static/public_keys"

    fileNames = os.listdir(keys_dir)

    return fileNames

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
