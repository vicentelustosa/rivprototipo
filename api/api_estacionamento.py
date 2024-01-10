from flask import Blueprint, jsonify, request, flash, redirect, url_for
from utils.utils import db
from utils.models import User, Estacionamento, Vaga

api_estacionamento = Blueprint("api_estacionamento", __name__)

@api_estacionamento.route('/api/estacionamento/cadastro', methods=['POST'])
def api_cadastro():
    user_id = request.form.get('user_id')
    nome = request.form.get('nome')
    endereco = request.form.get('endereco')
    qt_vagas = request.form.get('qt_vagas')

    if Estacionamento.query.filter_by(endereco=endereco).count() == 1:
        return jsonify({'error': 'Esses dados já foram utilizados! Por favor, tente outros.'})

    estac = Estacionamento(user_id, nome, endereco, qt_vagas)
    db.session.add(estac)
    db.session.commit()
    c = 0
    while int(c) < int(qt_vagas):
        c = c + 1
        vaga = Vaga(Estacionamento.query.filter_by(endereco=endereco).first().id)
        db.session.add(vaga)
        db.session.commit()

    return jsonify({'message': 'Cadastro concluído com sucesso!'})

@api_estacionamento.route('/api/estacionamento/listar', methods=['GET'])
def api_listar():
    user_id = request.args.get('user_id')
    estacs = Estacionamento.query.filter_by(id_emp=user_id).all()

    if User.query.filter_by(id=user_id).count() == 1:
        emp = User.query.get(user_id)
        return jsonify({'emp': emp.to_dict(), 'estacs': [estac.to_dict() for estac in estacs]})

    return jsonify({'error': 'Empresa não encontrada'})

@api_estacionamento.route('/api/estacionamento/editar/<int:id>', methods=['POST'])
def api_update(id):
    nome = request.form.get('nome')
    endereco = request.form.get('endereco')

    estac = Estacionamento.query.get(id)

    if Estacionamento.query.filter_by(endereco=endereco).count() == 1:
        return jsonify({'error': 'Esses dados já foram utilizados! Por favor, tente outros.'})

    estac.nome = nome
    estac.endereco = endereco
    db.session.commit()

    return jsonify({'message': 'Dados atualizados com sucesso!'})

@api_estacionamento.route('/api/estacionamento/deletar/<int:id>', methods=['POST'])
def api_delete(id):
    estac = Estacionamento.query.get(id)
    db.session.delete(estac)
    db.session.commit()

    return jsonify({'message': 'Estacionamento deletado com sucesso!'})
