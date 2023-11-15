from datetime import datetime
from flask import Flask, render_template, request
import functions as f
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode
app = Flask(__name__)


# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']
        mode = request.form['mode']

        if mode == 'encrypt':
            encrypted_message = f.encrypt_message(message, key)
            return render_template('csimetrico.html', encrypted_message=encrypted_message, mode=mode)
        elif mode == 'decrypt':
            decrypted_message = f.decrypt_message(message, key)
            return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)

    return render_template("csimetrico.html")

@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")

@app.route("/otro/")
def otro():
    return render_template("otro.html")



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

#comienzo del cifrado hibrido


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_with_rsa(public_key, message):
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return b64encode(ciphertext).decode()

def decrypt_with_rsa(private_key, ciphertext):
    decrypted_message = private_key.decrypt(
        b64decode(ciphertext),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()

def encrypt_with_aes(key, message):
    cipher = Cipher(algorithms.AES(key), modes.CFB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return b64encode(ciphertext).decode()

def decrypt_with_aes(key, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CFB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(b64decode(ciphertext)) + decryptor.finalize()
    return decrypted_message.decode()

# Uso del cifrado híbrido
private_key, public_key = generate_key_pair()

message_to_encrypt = "Hola, este es un mensaje secreto."

# Cifrado asimétrico con RSA
encrypted_message_rsa = encrypt_with_rsa(public_key, message_to_encrypt)
print("Mensaje cifrado con RSA:", encrypted_message_rsa)

# Generación de una clave simétrica para el cifrado simétrico
symmetric_key = b"UnaClaveSimetrica"
print("Clave simétrica generada:", symmetric_key)

# Cifrado simétrico con AES
encrypted_message_aes = encrypt_with_aes(symmetric_key, message_to_encrypt)
print("Mensaje cifrado con AES:", encrypted_message_aes)

# Descifrado simétrico con AES
decrypted_message_aes = decrypt_with_aes(symmetric_key, encrypted_message_aes)
print("Mensaje descifrado con AES:", decrypted_message_aes)

# Descifrado asimétrico con RSA
decrypted_message_rsa = decrypt_with_rsa(private_key, encrypted_message_rsa)
print("Mensaje descifrado con RSA:", decrypted_message_rsa)
