from datetime import datetime
from flask import Flask, json, render_template, request, send_file, jsonify
import functions as f
import zipfile
import os


app = Flask(__name__)


# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    if request.method == 'POST':
        # Verifica si se ha enviado un archivo
        if 'file' in request.files:
            file = request.files['file']
            key = request.form['key']
            mode = request.form['mode']
            type = request.form['type']
            
            print(mode)
            
            if mode == 'encrypt':
                encrypted_message = f.encrypt_file(file, key, type)
                return send_file("static/temp/archivo_encriptado.gpg", as_attachment=True,download_name="encrypted_message.gpg", mimetype="application/text")
            elif mode == 'decrypt':
                print('got here')
                decrypted_message = f.decrypt_file(file, key, type)
                return send_file("static/temp/archivo_desencriptado.txt", as_attachment=True,download_name="decrypted_message.txt", mimetype="application/text")

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
        #Si se genera una petición POST, con el modo de 'download', entonces el usuario quiere descargar el archivo que se especifica en el select, o eliminarlo, interactuar con este.
        elif mode == "download":
            # Obtenemos el tipo de acción (Descargar o Eliminar), y el nombre del archivo con el que se interactua.
            fileName = request.form['filename']
            type = request.form['type']
            print("requested a " +  type + " for file " + fileName )
            # Si tipo es 'get' entonces el usuario quiere descargar el archivo.
            if type=="get":
                return send_file(os.path.join("static","public_keys",fileName),download_name=fileName,mimetype="application/text")
            # Si el tipo es 'remove', entonces el usuario quiere eliminar el archivo.
            if type=="remove":
                passwd = request.form['passwd']
                print("Password Inputed: " + passwd)
                with open("static/data.json","r") as jsonData:
                    data = json.load(jsonData)
                    correct = data.get("adminPasswd")
                if passwd == correct:
                    answer = f.removeFile("public_keys/"+fileName)
                    print(answer)
        elif mode == "load":
            print("Usuario quiere cargar archivo.")
            # Obtén las variables necesarias:
            Id = request.form['identifier']
            file = request.files['file']
            # Comprobamos si el archivo con este nuevo nombre, existe o no entre las claves guardadas.
            # Además, en la misma función, comprobamos si el archivo es una clave exportada u otro archivo random no deseado.
            if f.canBeLoaded(Id, file, "static/public_keys"):
                print("File can be loaded to system")
                file.seek(0)  # Mover el puntero al principio del archivo

                 # Leer el contenido del archivo y eliminar los caracteres de nueva línea
                file_content = file.read().decode('utf-8').strip()

                # Imprimir el contenido (opcional)
                print("File content:", file_content)

                # Escribir el contenido en un nuevo archivo
                with open(f"static/public_keys/{Id}.key", "w", encoding="utf-8") as filed:
                    filed.write(file_content)

            else:
                print("File is not allowed in the system")
    # Si se genera una petición GET, significa que la aplicación requiere de obtener una lista string con las claves públicas del servidor
    if request.method == 'GET':
        # Obtiene los nombres de los archivos
        keys = f.load_keys()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud Ajax, devuelve las claves como JSON
            return jsonify({"claves": keys})
        else:
            # Si es una solicitud normal, renderiza la plantilla HTML
            return render_template("database.html", claves=keys)



    return render_template("database.html")


@app.route("/casimetrico/", methods=['GET','POST'])
def casimetrico():
    print(request.method)
    # Si se genera una petición GET, significa que la aplicación requiere de obtener una lista string con las claves públicas del servidor
    if request.method == 'GET':
        # Obtiene los nombres de los archivos
        keys = f.load_keys()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud Ajax, devuelve las claves como JSON
            return jsonify({"claves": keys})
        else:
            # Si es una solicitud normal, renderiza la plantilla HTML
            return render_template("casimetrico.html", claves=keys)
        
    # Si se genera una petición POST, eso quiere decir que uno de los formularios, encriptar o desencriptar han sido enviados.
    if request.method == 'POST':
        mode = request.form['mode']
        if mode == "encrypt":
            if 'file' in request.files:
                file = request.files['uncryptedFile']
                keyname = request.form['stored_key']
                publickey = request.files['public_key']
                print(keyname)
        if mode == "decrypt":
            print("a")



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