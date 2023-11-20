from datetime import datetime
from flask import Flask, jsonify, render_template, request, send_file
import functions as f

app = Flask(__name__)


# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    print(request.method)
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
                decrypted_message = f.decrypt_file(file, key)
                return send_file("static/temp/archivo_desencriptado.txt", as_attachment=True,download_name="decrypted_message.txt", mimetype="application/text")

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