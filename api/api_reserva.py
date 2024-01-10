from flask import Blueprint, jsonify, request, flash, redirect, url_for
from utils.utils import db
from utils.models import Reserva, Vaga
from flask_login import current_user

api_reserva = Blueprint("api_reserva", __name__)

@api_reserva.route('/api/reserva/cadastro', methods=['POST'])
def api_cadastro_reserva():
    id_vaga = request.form.get('id_vaga')
    dt_inicial = request.form.get('dt_inicial')
    dt_final = request.form.get('dt_final')

    if Reserva.query.filter_by(id_vaga=id_vaga).filter_by(dt_inicial=dt_inicial).count() == 1:
        return jsonify({'error': 'Essa vaga já foi reservada! Por favor, tente outra.'})

    reserva = Reserva(id_vaga, current_user.id, dt_inicial, dt_final, 0, True)
    db.session.add(reserva)
    db.session.commit()

    return jsonify({'message': 'Cadastro concluído com sucesso!'})
