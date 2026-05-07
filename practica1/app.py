from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
from datetime import datetime


client = MongoClient("mongodb://localhost:27017")
db = client["planifyprime"]
usuarios = db["misusuarios"]

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


@app.route('/pagprincipal', methods=['GET', 'POST'])
def principal():

    if request.method == 'POST':

        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')

        nueva_tarea = {
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": "Pendiente",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        tareas.insert_one(nueva_tarea)

        return redirect('/pagprincipal')

    lista_tareas = list(tareas.find())

    return render_template(
        'pagprincipal.html',
        tareas=lista_tareas
    )

@app.route('/recuperar', methods= ['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email= request.form.get('email')
        
        return redirect('/')
    return render_template('recuperar.html')
if __name__ == "__main__":
    app.run(debug=True)
