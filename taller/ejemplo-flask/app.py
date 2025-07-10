from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'una-clave-secreta-000001'

# Token generado desde Django con drf_create_token o /api/token/
token = 'ed11f5fa01078f377b68f9da2f68221242614681'
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

# Ruta de prueba
@app.route("/")
def hello_world():
    return "<p>Hola mundo</p>"

# -----------------------
# EDIFICIOS
# -----------------------

# Listar Edificios
@app.route("/ver/edificios")
def ver_edificios():
    r = requests.get("http://localhost:8000/api/edificios/", headers=headers)

    if r.status_code == 200:
        data = r.json()
        edificios = data.get('results', []) if isinstance(data, dict) else []
    else:
        flash("Error al cargar edificios", 'danger')
        edificios = []

    return render_template("losedificios.html", edificios=edificios)


# Crear Edificio
@app.route("/crear/edificio", methods=['GET', 'POST'])
def crear_edificio():
    if request.method == 'POST':
        edificio_data = {
            'nombre': request.form['nombre'],
            'direccion': request.form['direccion'],
            'ciudad': request.form['ciudad'],
            'tipo': request.form['tipo']
        }

        r = requests.post("http://localhost:8000/api/edificios/",
                          json=edificio_data,
                          headers=headers)

        if r.status_code == 201:
            nuevo = json.loads(r.content)
            flash(f"Edificio '{nuevo['nombre']}' creado correctamente", 'success')
            return redirect(url_for('ver_edificios'))
        else:
            flash("Error al crear el edificio", 'danger')

    return render_template("crear_edificio.html")
    
# Actualizar Edificio
@app.route("/editar/edificio/<int:id>", methods=['GET', 'POST'])
def editar_edificio(id):
    r = requests.get(f"http://localhost:8000/api/edificios/{id}/", headers=headers)
    edificio = r.json()

    if request.method == 'POST':
        nuevo_dato = {
            'nombre': request.form['nombre'],
            'direccion': request.form['direccion'],
            'ciudad': request.form['ciudad'],
            'tipo': request.form['tipo']
        }

        r = requests.put(f"http://localhost:8000/api/edificios/{id}/", json=nuevo_dato, headers=headers)
        if r.status_code == 200:
            flash("Edificio actualizado correctamente", 'success')
            return redirect(url_for('ver_edificios'))
        else:
            flash("Error al actualizar edificio", 'danger')

    return render_template("editar_edificio.html", edificio=edificio)

# Eliminar Edificio
@app.route("/eliminar/edificio/<int:id>", methods=['POST'])
def eliminar_edificio(id):
    r = requests.delete(f"http://localhost:8000/api/edificios/{id}/", headers=headers)
    if r.status_code == 204:
        flash("Edificio eliminado correctamente", 'success')
    else:
        flash("Error al eliminar el edificio", 'danger')
    return redirect(url_for('ver_edificios'))

# -----------------------
# DEPARTAMENTOS
# -----------------------

# Listar Departamentos
@app.route("/ver/departamentos")
def ver_departamentos():
    r = requests.get("http://localhost:8000/api/departamentos/", headers=headers)

    if r.status_code == 200:
        data = r.json()
        departamentos = data.get('results', []) if isinstance(data, dict) else []
    else:
        flash("Error al cargar departamentos", 'danger')
        departamentos = []

    return render_template("losdepartamentos.html", departamentos=departamentos)


# Crear Departamento
@app.route("/crear/departamento", methods=['GET', 'POST'])
def crear_departamento():
    r_edi = requests.get("http://localhost:8000/api/edificios/", headers=headers)
    edificios = r_edi.json().get('results', []) if r_edi.status_code == 200 else []

    if request.method == 'POST':
        departamento_data = {
            'propietario': request.form['propietario'],
            'costo': request.form['costo'],
            'cuartos': request.form['cuartos'],
            'edificio': request.form['edificio']
        }
        r = requests.post("http://localhost:8000/api/departamentos/", json=departamento_data, headers=headers)
        if r.status_code == 201:
            flash("Departamento creado exitosamente", "success")
            return redirect(url_for('ver_departamentos'))
        else:
            flash("Error al crear el departamento", "danger")

    # Obtener departamentos existentes para mostrar en tabla
    r_deps = requests.get("http://localhost:8000/api/departamentos/", headers=headers)
    departamentos = r_deps.json().get('results', []) if r_deps.status_code == 200 else []

    return render_template("crear_departamento.html", edificios=edificios, departamentos=departamentos)

#Editar Departamento
@app.route("/editar/departamento/<int:id>", methods=['GET', 'POST'])
def editar_departamento(id):
    # Obtener el departamento a editar
    r_dep = requests.get(f"http://localhost:8000/api/departamentos/{id}/", headers=headers)
    departamento = r_dep.json()

    # Obtener todos los edificios
    r_edi = requests.get(f"http://localhost:8000/api/edificios/", headers=headers)
    edificios = r_edi.json().get('results', []) if r_edi.status_code == 200 else []

    if request.method == 'POST':
        nuevo_dato = {
            'propietario': request.form['propietario'],
            'costo': request.form['costo'],
            'cuartos': request.form['cuartos'],
            'edificio': request.form['edificio']  # esto debe ser la URL o el ID
        }

        r = requests.put(f"http://localhost:8000/api/departamentos/{id}/", json=nuevo_dato, headers=headers)
        if r.status_code == 200:
            flash("Departamento actualizado correctamente", 'success')
            return redirect(url_for('ver_departamentos'))
        else:
            flash("Error al actualizar departamento", 'danger')

    return render_template("editar_departamento.html", departamento=departamento, edificios=edificios)

# Eliminar Departamento
@app.route("/eliminar/departamento/<int:id>", methods=['POST'])
def eliminar_departamento(id):
    r = requests.delete(f"http://localhost:8000/api/departamentos/{id}/", headers=headers)
    if r.status_code == 204:
        flash("Departamento eliminado correctamente", 'success')
    else:
        flash("Error al eliminar el departamento", 'danger')
    return redirect(url_for('ver_departamentos'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
