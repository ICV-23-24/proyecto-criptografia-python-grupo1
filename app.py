from datetime import datetime
from flask import Flask, render_template, request, send_file
import functions as f
import zipfile
import os


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


# Database route, aquí los usuarios pueder importar y exportar claves públicas, .
@app.route("/database/", methods=['GET','POST'])
def database():
    #Si se genera una petición POST, con el modo de 'generar', entonces genera una clave pública y privada nuevas.
    if request.method == 'POST':
        # Obtén el modo del formulario, 'generate' significa que el usuario necesita un nuevo par de claves.
        mode = request.form['mode']
        if mode == "generate":
            print("Generando claves...")
            f.generate_keys()

            #public file path
            publicFile = os.path.join("static","temp","public_key.key")
            #private file path
            privateFile = os.path.join("static","temp","private_key.key")

            # Creamos un .zip para contener ambos archivos....
            zipFile = "static/temp/keys.zip"
            with zipfile.ZipFile(zipFile, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(publicFile,"public_key.key")
                zipf.write(privateFile,"private_key.key")

            # Enviamos a descargar las claves.
            return send_file(zipFile, as_attachment=True, download_name="keys.zip", mimetype="application/zip")


    return render_template("database.html")


@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")





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