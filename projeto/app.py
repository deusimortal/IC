from flask import Flask, render_template, redirect, url_for, session, flash, request
import sqlite3

app = Flask(__name__)
app.secret_key = 'seu_segredo_seguro'

#Função para verificar usuário no banco de dados
def verificar_usuario_no_banco(email, password):
    #conexão com o banco de dados
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email FROM usuarios WHERE email = ? AND senha = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    
    return user

#Função para carregar usuario
def carregar_usuario(user_id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, email FROM usuarios WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/funcionalidades')
def funcionalidades():
    return render_template('funcio.html')

@app.route('/ferramentas')
def ferramentas():
    return render_template('ferramentas.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = verificar_usuario_no_banco(email, password)
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Login inválido. Verifique suas credenciais.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Adicionar logica de cadstro
        pass
    return render_template('registrar.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar o dashboard', 'warning')
        return redirect(url_for('login'))
    
    user = carregar_usuario(session['user_id'])
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
