from flask import Blueprint, jsonify, request
from utils.utils import db
from utils.models import User, Empresa, Reserva
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

api_empresa = Blueprint("api_empresa", __name__)

@api_empresa.route('/api/empresa/cadastro', methods=['POST'])
def api_cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    cnpj = request.form.get('cnpj')
    tel = request.form.get('tel')
    senha = request.form.get('senha')
    csenha = request.form.get('csenha')

    if senha != "" and csenha != "" and senha != csenha:
        return jsonify({'error': 'Senhas diferentes!'})

    if ((User.query.filter_by(email=email)) or (User.query.filter_by(tel=tel)) or (
            User.query.filter_by(cnpj=cnpj))).count() == 1:
        return jsonify({'error': 'Esses dados já foram utilizados! Por favor, tente outros.'})

    senha = hashlib.sha256(request.form.get('senha').encode()).hexdigest()
    u = User(nome, email, tel, senha, False, True)
    db.session.add(u)
    db.session.commit()
    e = Empresa(u.id, cnpj)
    db.session.add(e)
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

@api_empresa.route('/api/empresa/perfil', methods=['GET'])
def api_perfil():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    reservas = Reserva.query.all()

    if Empresa.query.filter_by(id=user.id).count() == 1:
        empresa = Empresa.query.filter_by(id=user.id).first()
        return jsonify({'user': user.to_dict(), 'empresa': empresa.to_dict(), 'reservas': [r.to_dict() for r in reservas]})

    return jsonify({'error': 'Empresa não encontrada'})

@api_empresa.route('/api/empresa/update/<int:user_id>', methods=['POST'])
def api_update(user_id):
    nome = request.form.get('nome')
    email = request.form.get('email')
    cnpj = request.form.get('cnpj')
    tel = request.form.get('tel')

    user = User.query.get(user_id)
    empresa = Empresa.query.get(user_id)
    user.nome = nome
    user.email = email
    user.tel = tel
    empresa.cnpj = cnpj

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

@api_empresa.route('/api/empresa/desativar/<int:user_id>', methods=['POST'])
def api_delete(user_id):
    user = User.query.get(user_id)
    user.status = 0
    db.session.commit()

    return jsonify({'message': 'Usuário desativado com sucesso!'})

@api_empresa.route('/api/empresa/alterar_senha', methods=['POST'])
def api_update_senha():
    user_id = request.form.get('user_id')
    user = User.query.filter_by(id=user_id).first()

    senha = request.form.get('senha')
    csenha = request.form.get('csenha')

    if senha != csenha:
        return jsonify({'error': 'Senhas diferentes!'})

    user.senha = hashlib.sha256(request.form.get('senha').encode()).hexdigest()
    db.session.commit()

    return jsonify({'message': 'Senha atualizada com sucesso!'})

@api_empresa.route('/api/empresa/reservas', methods=['GET'])
def api_listar_reservas():
    user_id = request.args.get('user_id')
    reservas = Reserva.query.filter_by(id_empresa=user_id).all()

    if Empresa.query.filter_by(id=user_id).count() == 1:
        empresa = Empresa.query.filter_by(id=user_id).first()
        return jsonify({'empresa': empresa.to_dict(), 'reservas': [r.to_dict() for r in reservas]})

    return jsonify({'error': 'Empresa não encontrada'})

@api_empresa.route('/api/empresa/reserva/editar/<int:id>', methods=['POST'])
def api_update_reserva(id):
    id_empresa = request.form.get('id_empresa')
    id_vaga = request.form.get('id_vaga')
    dt_inicial = request.form.get('dt_inicial')

    reserva = Reserva.query.get(id)

    if Reserva.query.filter_by(id_vaga=id_vaga).filter_by(dt_inicial=dt_inicial).count() == 1:
        return jsonify({'error': 'Esses dados já foram utilizados! Por favor, tente outros.'})

    reserva.id_empresa = id_empresa
    reserva.id_vaga = id_vaga
    reserva.dt_inicial = dt_inicial
    db.session.commit()

    return jsonify({'message': 'Dados atualizados com sucesso!'})

@api_empresa.route('/api/empresa/reserva/desativar/<int:id>', methods=['POST'])
def api_delete_reserva(id):
    reserva = Reserva.query.get(id)
    db.session.delete(reserva)
    db.session.commit()

    return jsonify({'message': 'Reserva deletada com sucesso!'})

@api_empresa.route('/api/empresa/reserva/finalizar/<int:id>', methods=['POST'])
def api_finalizar_reserva(id):
    reserva = Reserva.query.get(id)
    reserva.status = False
    db.session.commit()

    return jsonify({'message': 'Reserva concluída com sucesso!'})