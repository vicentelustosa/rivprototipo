from flask import Blueprint, jsonify, request
from utils.utils import db
from utils.models import User
from flask_login import login_user

api_user = Blueprint("api_user", __name__)

@api_user.route('/api/user/login', methods=['POST'])
def api_login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(senha):
        if user.status == 0:
            return jsonify({'error': 'Usuário inválido!'})
        else:
            login_user(user)
            return jsonify({'message': 'Login efetuado com sucesso!'})
    else:
        return jsonify({'error': 'Dados incorretos! Por favor, tente novamente.'})
