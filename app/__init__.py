from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.api_cliente import api_cliente
from api.api_empresa import api_empresa
from api.api_estacionamento import api_estacionamento
from api.api_reserva import api_reserva
from api.api_user import api_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'R1v.t0p'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rivdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(api_user, url_prefix='/api/user')
app.register_blueprint(api_cliente, url_prefix='/api/cliente')
app.register_blueprint(api_empresa, url_prefix='/api/empresa')
app.register_blueprint(api_estacionamento, url_prefix='/api/estacionamento')
app.register_blueprint(api_reserva, url_prefix='/api/reserva')

from app import routes, models
