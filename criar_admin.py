from flask import Flask
from models import db, Cliente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # cria tabelas se não existirem

    # verifica se já existe
    admin = Cliente.query.filter_by(nome='admin').first()
    if not admin:
        novo_cliente = Cliente(nome='admin', senha='1234', telefone='999999')
        db.session.add(novo_cliente)
        db.session.commit()
        print("Admin criado com sucesso!")
    else:
        print("Admin já existe.")



 
 