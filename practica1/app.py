from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId


client = MongoClient("mongodb://localhost:27017")
db = client["planifyprime"]
usuarios = db["misusuarios"]
tareas_collection= db["tareas"]

app = Flask(__name__)
app.secret_key = "algo_secreto"

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = usuarios.find_one({"email": email})

        if not usuario:
            flash("Correo no registrado")
            return render_template('login.html')

        if usuario["password"] != password:
            flash("Contraseña incorrecta")
            return render_template('login.html')

        return redirect('/pagprincipal')

    return render_template('login.html')


@app.route('/registrate', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        email = request.form.get('email')
        password = request.form.get('password')

        if usuarios.find_one({"email": email}):
            flash("Ese correo ya está registrado")
            return render_template('registrate.html')
        
        if "@" not in email or "." not in email:
            flash("Correo inválido")
            return render_template('registrate.html')

        usuarios.insert_one({
            "nombre": nombre,
            "apellidos": apellidos,
            "email": email,
            "password": password
        })

        return redirect('/pagprincipal')

    return render_template('registrate.html')


@app.route("/pagprincipal")
def principal():

    tareas = tareas_collection.find()

    return render_template(
        "pagprincipal.html",
        tareas=tareas
    )
    

@app.route("/agregar", methods=["POST"])
def agregar():

    texto = request.form.get("texto")

    if not texto:
        return redirect("/pagprincipal")

    tareas_collection.insert_one({
        "texto": texto,
        "estado": "Pendiente",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return redirect("/pagprincipal")

@app.route("/cambiar_estado/<id>/<estado>")
def cambiar_estado(id, estado):

    tareas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"estado": estado}}
    )

    return redirect("/pagprincipal")

@app.route('/recuperar', methods= ['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email= request.form.get('email')
        
        return redirect('/')
    return render_template('recuperar.html')
if __name__ == "__main__":
    app.run(debug=True)
