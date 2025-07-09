from flask import Flask, render_template,request,redirect, flash,url_for, session,jsonify
from models import db,Cliente
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os



app = Flask(__name__)
app.secret_key = 'um_valor_bem_secreto_e_dificil_de_adivinhar_123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']

db.init_app(app)


from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Você precisa fazer login primeiro!')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('/index.html')

@app.route("/login", methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    cliente = Cliente.query.filter_by(nome=nome, senha=senha).first()

    
    if cliente:
        session['logged_in'] = True
        return redirect(url_for('bronze'))  # redireciona para página protegida
    else:
        flash('Usuário ou senha inválidos!')
        return redirect('/')


@app.route('/agendamento')
@login_required
def bronze():
    return render_template('agendamento.html', estoque=estoque)

estoque = {
    'fitas': 0,
    'produtos': 0
}

@app.route('/atualizar_estoque', methods=['POST'])
def atualizar_estoque():
    data = request.get_json()
    # Atualiza o estoque
    estoque['fitas'] = int(data['fitas'])
    estoque['produtos'] = int(data['produtos'])
    # Retorna o estoque atualizado como JSON
    return jsonify (estoque)

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu com sucesso!')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)