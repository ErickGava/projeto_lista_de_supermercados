from flask import Flask, render_template, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__)
app.secret_key = "Chave_muito_segura"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home/cadastro')
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.cadastro(form) == True:
            return render_template('login.html')
        else:
            return "Ocorreu um erro ao cadastrar usuário"  # Caso contrário, exibe mensagem de erro
    else:
        return render_template('cadastro.html')

@app.route('/home/login')
def login():
    return render_template('login.html')

@app.route('/home/criar-lista')
def criar_lista():
    return render_template('lista.html')

@app.route('/home/editar-lista')
def editar_lista():
    return render_template('editar.html')

if __name__ == '__main__':
    app.run(debug=True)