from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('login.html')


@app.route('/registrate', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos= request.form.get('apellidos')
        email = request.form.get('email')
        password = request.form.get('password')
        return redirect('/pagprincipal')

    return render_template('registrate.html')

@app.route('/pagprincipal')
def principal():
    return render_template('pagprincipal.html')

@app.route('/recuperar', methods= ['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email= request.form.get('email')
        
        return redirect('/')
    return render_template('recuperar.html')
if __name__ == "__main__":
    app.run(debug=True)
