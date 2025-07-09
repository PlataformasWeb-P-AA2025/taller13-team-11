from flask import Flask, jsonify, request,Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'una-clave-secreta-000001'

token = 'ed9f9c09d4f73f3df22f23c8fa4911655be936b5'
headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

@app.route("/")
def hello_world():
    return "<p>Hola mundo</p>"

@app.route('/listar_edificios')
def listar_edificios():
    r = requests.get(f"{API_URL}/edificios/", auth=AUTH)
    return jsonify(r.json())

@app.route('/crear_edificio', methods=['POST'])
def crear_edificio():
    data = request.json
    r = requests.post(f"{API_URL}/edificios/", data=data, auth=AUTH)
    return jsonify(r.json())

@app.route('/actualizar_edificio/<int:id>', methods=['PUT'])
def actualizar_edificio(id):
    data = request.json
    r = requests.put(f"{API_URL}/edificios/{id}/", data=data, auth=AUTH)
    return jsonify(r.json())

@app.route('/eliminar_edificio/<int:id>', methods=['DELETE'])
def eliminar_edificio(id):
    r = requests.delete(f"{API_URL}/edificios/{id}/", auth=AUTH)
    return jsonify({"status": r.status_code})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
