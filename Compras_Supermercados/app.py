from flask import Flask, render_template, request, url_for, flash, session, redirect 
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

@app.route('/home/cadastro', methods= ['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.cadastro(form) == True:
            return redirect('/login')
        else:
            return "Ocorreu um erro ao cadastrar usuário"  # Caso contrário, exibe mensagem de erro
    else:
        return render_template('cadastro.html')

@app.route('/home/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/home/adicionar-item', methods=['GET', 'POST'])
def adicionar_item():
    if request.method == 'POST':
        form = request.form
        if database.adicionar_item(form) == True:
            return redirect('/home')
    return render_template('adicionar.html')

@app.route('/home/editar-lista')
def editar_lista():
    return render_template('editar.html')

if __name__ == '__main__':
    app.run(debug=True)