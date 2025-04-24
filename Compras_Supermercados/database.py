import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("bancodedados.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                   (username TEXT, email TEXT PRIMARY KEY, senha TEXT)''')
    
    cursor.execute(''' CREATE TABLE IF NOT EXISTS itens     
                   (id INTEGER PRIMARY KEY, nome TEXT, quantia REAL,
                   valor REAL, email TEXT, url TEXT)''')
    
def cadastro(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' SELECT COUNT (email) FROM usuarios WHERE email = ?''', (formulario['email'],))
    conexao.commit()
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    if quantidade_de_emails[0] > 0:
        print("E-mail já cadastrado! Escolha outro e-mail!!")
        return False
    
    senha_criptografada = generate_password_hash(formulario['senha'])
    cursor.execute('''INSERT INTO usuarios(username, email, senha)
                   VALUES (?, ?, ?)''', (formulario['username'], formulario['email'], senha_criptografada))
    conexao.commit()
    return True

def login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' SELECT COUNT (email) FROM usuarios WHERE email = ?''', (formulario['email'],))
    conexao.commit()
    quantidade_de_emails = cursor.fetchone()
    if quantidade_de_emails == 0:
        print("Email não cadastrado! Tente Novamente!")
        return False
    
    cursor.execute('''SELECT senha FROM usuarios WHERE email = ? ''', (formulario['email'],))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    return check_password_hash(senha_criptografada[0], formulario['password'])

def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM usuarios WHERE email = ?''', (email,))
    cursor.execute('''DELETE FROM itens WHERE email = ?''', (email,))
    conexao.commit()
    return True

def adicionar_item(formulario, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(""" INSERT INTO itens(nome, quantia, valor, email, url) VALUES (?,?,?,?,?)""", (formulario['nome_produto'], formulario['quantidade_produto'], formulario['valor_produto'], email, formulario['url']))
    conexao.commit()
    return True

def excluir_item(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(""" DELETE FROM itens WHERE id = ?""", (id,))
    conexao.commit()

def mostrar_produtos(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' SELECT * FROM itens WHERE email = ?''', (email,))
    conexao.commit()
    produtos = cursor.fetchall()
    return produtos

def pegar_produto(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' SELECT * FROM itens WHERE id = ?''', (id,))
    conexao.commit()
    produto = cursor.fetchone()
    return produto

def salvar_item(nome, quantidade, valor, id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' UPDATE itens SET nome = ?, quantia = ?, valor = ? WHERE id = ?''', (nome, quantidade, valor, id))
    conexao.commit()


if __name__ == '__main__':
    criar_tabelas()
    print("Hello, world!")