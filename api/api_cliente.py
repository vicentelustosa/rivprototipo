from flask import Blueprint, jsonify, request, flash, redirect, url_for
from app.__init__ import db
from app.models import User, Cliente, Reserva
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

api_client = Blueprint("api_client", __name__)

@api_client.route('/api/cliente/cadastro', methods=['POST'])
def api_cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    dt_nasc = request.form.get('dt_nasc')
    placa_carro = request.form.get('placa_carro')
    tel = request.form.get('tel')
    senha = request.form.get('senha')
    csenha = request.form.get('csenha')

    if senha != "" and csenha != "" and senha != csenha:
        return jsonify({'error': 'Senhas diferentes!'})

    if ((User.query.filter_by(email=email)) or (User.query.filter_by(tel=tel)) or (
            User.query.filter_by(placa_carro=placa_carro))).count() == 1:
        return jsonify({'error': 'Esses dados já foram utilizados! Por favor, tente outros.'})

    senha = hashlib.sha256(request.form.get('senha').encode()).hexdigest()
    u = User(nome, email, tel, senha, False, True)
    db.session.add(u)
    db.session.commit()
    c = Cliente(u.id, dt_nasc, placa_carro)
    db.session.add(c)
    db.session.commit()

    destinatario = email
    mensagem = MIMEMultipart()
    mensagem['From'] = 'justino.caio@escolar.ifrn.edu.br'
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'CADASTRO NO RIV'

    corpo_email = 'Olá, seja bem-vindo!'
    mensagem.attach(MIMEText(corpo_email, 'plain'))

    conexao_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    conexao_smtp.starttls()
    conexao_smtp.login('justino.caio@escolar.ifrn.edu.br', 'amjbqkzlvhchsqsn')

    texto_email = mensagem.as_string()
    conexao_smtp.sendmail('justino.caio@escolar.ifrn.edu.br', destinatario, texto_email)
    conexao_smtp.quit()

    return jsonify({'message': 'Cadastro concluído com sucesso! Faça o login para concluí-lo'})

@api_client.route('/api/cliente/perfil', methods=['GET'])
def api_perfil():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    reservas = Reserva.query.filter_by(id_client=user.id).all()

    if Cliente.query.filter_by(id=user.id).count() == 1:
        client = Cliente.query.filter_by(id=user.id).first()
        return jsonify({'user': user.to_dict(), 'client': client.to_dict(), 'reservas': [r.to_dict() for r in reservas]})

    return jsonify({'error': 'Cliente não encontrado'})

@api_client.route('/api/cliente/update/<int:user_id>', methods=['POST'])
def api_update(user_id):
    nome = request.form.get('nome')
    email = request.form.get('email')
    dt_nasc = request.form.get('dt_nasc')
    tel = request.form.get('tel')
    placa_carro = request.form.get('placa_carro')

    user = User.query.get(user_id)
    client = Cliente.query.get(user_id)
    user.nome = nome
    user.email = email
    user.tel = tel
    client.dt_nasc = dt_nasc
    client.placa_carro = placa_carro

    if User.query.filter_by(email=email).count() == 1 and User.query.filter_by(tel=tel).count() == 1:
        db.session.commit()
        return jsonify({'message': 'Dados atualizados com sucesso! Se deseja alterar o e-mail e o telefone, tente outros.'})

    elif User.query.filter_by(email=email).count() == 1 and User.query.filter_by(tel=tel).count() == 0:
        user.tel = tel
        db.session.commit()
        return jsonify({'message': 'Dados atualizados com sucesso! Se deseja alterar o e-mail, tente outro.'})

    elif User.query.filter_by(email=email).count() == 0 and User.query.filter_by(tel=tel).count() == 1:
        user.email = email
        db.session.commit()
        return jsonify({'message': 'Dados atualizados com sucesso! Se deseja alterar o telefone, tente outro.'})

    else:
        user.email = email
        user.tel = tel
        db.session.commit()
        return jsonify({'message': 'Dados atualizados com sucesso!'})

@api_client.route('/api/cliente/desativar/<int:user_id>', methods=['POST'])
def api_delete(user_id):
    user = User.query.get(user_id)
    user.status = 0
    db.session.commit()

    return jsonify({'message': 'Usuário desativado com sucesso!'})

@api_client.route('/api/cliente/alterar_senha', methods=['POST'])
def api_update_senha():
    user_id = request.form.get('user_id')
    user = User.query.filter_by(id=user_id).first()

    senha = request.form.get('senha')
    csenha = request.form.get('csenha')

    if senha != csenha:
        return jsonify({'error': 'Senha'})

@api_client.route('/api/cliente/reserva', methods=['GET'])
def api_listar_reservas():
    user_id = request.args.get('user_id')
    reservas = Reserva.query.filter_by(id_client=user_id).all()

    return jsonify({'reservas': [r.to_dict() for r in reservas]})

@api_client.route('/api/cliente/reserva/editar/<int:id>', methods=['POST'])
def api_update_reserva(id):
    id_client = request.form.get('id_client')
    id_vaga = request.form.get('id_vaga')
    dt_inicial = request.form.get('dt_inicial')

    reserva = Reserva.query.get(id)

    if Reserva.query.filter_by(id_vaga=id_vaga).filter_by(dt_inicial=dt_inicial).count() == 1:
        return jsonify({'error': 'Esses dados já foram utilizados! Por favor, tente outros.'})

    reserva.id_client = id_client
    reserva.id_vaga = id_vaga
    reserva.dt_inicial = dt_inicial
    db.session.commit()

    return jsonify({'message': 'Reserva atualizada com sucesso!'})

@api_client.route('/api/cliente/reserva/desativar/<int:id>', methods=['POST'])
def api_delete_reserva(id):
    reserva = Reserva.query.get(id)
    db.session.delete(reserva)
    db.session.commit()

    return jsonify({'message': 'Reserva deletada com sucesso!'})

@api_client.route('/api/cliente/reserva/finalizar/<int:id>', methods=['POST'])
def api_finalizar_reserva(id):
    reserva = Reserva.query.get(id)
    reserva.status = False
    db.session.commit()

    return jsonify({'message': 'Reserva concluída com sucesso!'})
