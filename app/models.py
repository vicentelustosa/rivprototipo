from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  __tablename__ = "user"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  nome = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=False) 
  tel = db.Column(db.Integer, nullable=False)
  senha = db.Column(db.String(80), nullable=False)
  adm = db.Column(db.Boolean, default=False)
  status = db.Column(db.Boolean, default=True)

  def __init__ (self, nome, email, tel, senha, adm, status):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.tel = tel
    self.adm = adm
    self.status = status

  def __repr__ (self):
    return f'Teste: {self.nome}.'

class Cliente(db.Model):
   __tablename__ = "cliente"
   id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, primary_key=True)
   dt_nasc = db.Column(db.String(80), nullable=False)
   placa_carro = db.Column(db.String(80), nullable=False)

   user = db.relationship('User', foreign_keys=id)

   def __init__(self, id, dt_nasc, placa_carro):
     self.id = id
     self.dt_nasc = dt_nasc
     self.placa_carro = placa_carro

   def __repr__(self):
     return f'Cliente: {self.id}.'

class Empresa(db.Model):
  __tablename__ = "empresa"
  id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, primary_key=True)
  cnpj = db.Column(db.String(80), nullable=False) 

  user = db.relationship('User', foreign_keys=id)

  def __init__ (self, id, cnpj):
    self.id = id
    self.cnpj = cnpj

  def __repr__ (self):
    return f'Empresa: {self.id}.'

class Estacionamento(db.Model):
  __tablename__ = "estacionamento"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  id_emp = db.Column(db.Integer, db.ForeignKey('empresa.id'))
  nome = db.Column(db.String(80), nullable=False)
  endereco = db.Column(db.String(100), nullable=False)
  qt_vagas = db.Column(db.Integer, nullable=False)

  empresa = db.relationship('Empresa', foreign_keys=id_emp)

  def __init__ (self, id_emp, nome, endereco, qt_vagas):
    self.id_emp = id_emp
    self.nome = nome
    self.endereco = endereco
    self.qt_vagas = qt_vagas

  def __repr__ (self):
    return f'Estacionamento: {self.id}.'

class Vaga(db.Model):
  __tablename__ = "vaga"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  id_estac = db.Column(db.Integer, db.ForeignKey('estacionamento.id'))

  estacionamento = db.relationship('Estacionamento', foreign_keys=id_estac)

  def __init__ (self, id_estac):
    self.id_estac = id_estac

  def __repr__ (self):
    return f'Vaga: {self.id}.'

class Reserva(db.Model):
  __tablename__ = "reserva"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  id_vaga = db.Column(db.Integer, db.ForeignKey('vaga.id'))
  id_client = db.Column(db.Integer, db.ForeignKey('cliente.id'))
  dt_inicial = db.Column(db.String(80), nullable=False)
  dt_final = db.Column(db.String(80), nullable=False)
  preco =  db.Column(db.Float, nullable=False)
  status = db.Column(db.Boolean, default=True)

  vaga = db.relationship('Vaga', foreign_keys=id_vaga)
  cliente = db.relationship('Cliente', foreign_keys=id_client)

  def __init__ (self, id_vaga, id_client, dt_inicial, dt_final, preco, status):
    self.id_vaga = id_vaga
    self.id_client = id_client
    self.dt_inicial = dt_inicial
    self.dt_final = dt_final
    self.preco = preco
    self.status = status

  def __repr__ (self):
    return f'Reserva: {self.id}.'