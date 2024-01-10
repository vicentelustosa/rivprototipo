from flask_restful import Resource
from flask import jsonify
from app.resources import api
from app.models import User

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({'id': user.id, 'nome': user.nome, 'email': user.email})

api.add_resource(UserResource, '/api/user/<int:user_id>')
