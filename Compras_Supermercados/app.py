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
    lista_de_produtos = database.mostrar_produtos(session['email'])
    print(lista_de_produtos)
    return render_template('home.html', produtos = lista_de_produtos)

@app.route('/home/cadastro', methods= ['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.cadastro(form) == True:
            return redirect('/home/login')
        else:
            return "Ocorreu um erro ao cadastrar usuário"  # Caso contrário, exibe mensagem de erro
    else:
        return render_template('cadastro.html')

@app.route('/home/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form = request.form
        if database.login(form) == True:
            session['email'] = form['email']
            return redirect('/home')
        else:
            return "Ocorreu um erro ao efetuar o login!"
    return render_template('login.html')

@app.route('/home/excluir-usuario', methods=['GET'])
def excluir_usuario():
    email = session['email']
    database.excluir_usuario(email)
    return redirect(url_for('index'))

@app.route('/home/adicionar-item', methods=['GET', 'POST'])
def adicionar_item():
    if request.method == 'POST':
        form = request.form
        if database.adicionar_item(form, session['email']) == True:
            return redirect('/home')
    return render_template('adicionar.html')

@app.route('/home/editar-item/<int:id>', methods=['GET', 'POST'])
def editar_item(id):
    if request.method == 'GET':
        produto = database.pegar_produto(id)
        return render_template('editar.html', produto = produto)
    if request.method == 'POST':
        nome = request.form['nome_produto']
        quantidade = request.form['quantidade_produto']
        valor = request.form['valor_produto']
        
        database.salvar_item(nome, quantidade, valor, id)
        return redirect('/home')
    
@app.route('/home/excluir-item/<int:id>')
def excluir_item(id):
    database.excluir_item(id)
    return redirect('/home')

if __name__ == '__main__':
    app.run(debug=True)