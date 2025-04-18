import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("bancodedados")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                   (username TEXT, email TEXT PRIMARY KEY, senha TEXT)''')
    
    cursor.execute(''' CREATE TABLE IF NOT EXISTS itens     
                   (id INTEGER PRIMARY KEY, nome TEXT, quantia REAL,
                   valor REAL)''')
    
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
    cursor.execute('''INSERT TO usuarios(username, email, senha)
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
    
    cursor.execute('''SELECT senha FROM usuarios WHERE email = ? ''', (formulario['email']))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    return check_password_hash(senha_criptografada[0], formulario['password'])

if __name__ == '__main__':
    criar_tabelas()
    print("Hello, world!")