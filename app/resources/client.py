from flask_restful import Resource
from flask import jsonify
from app.resources import api
from app.models import Cliente

class ClienteResource(Resource):
    def get(self, cliente_id):
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify({'id': cliente.id, 'dt_nasc': cliente.dt_nasc, 'placa_carro': cliente.placa_carro})

api.add_resource(ClienteResource, '/api/cliente/<int:cliente_id>')
