from flask_restful import Resource, reqparse
from models.vendedor import VendedorModel
from flask.helpers import make_response


def returnVendedores():
    return Vendedor


class Vendedores(Resource):
    def get(self):
        return {'Vendedores': [vendedor.json() for vendedor in VendedorModel.query.all()]}


class Vendedor(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("id_vendedor", type=int, required=True, help="O campo 'nome' não pode ser nulo!")
    argumentos.add_argument("nome_vendedor")
    argumentos.add_argument("telefone_vendedor")
    argumentos.add_argument("vendedor_email")

    def get(self, id_vendedor):
        vendedor = VendedorModel.find_vendedor(id_vendedor)
        if vendedor:
            return vendedor.json()
        return make_reponse(render_template("vendedores.html", message="Vendedor not found"), 404)


    def post(self, id_vendedor):
        if VendedorModel.find_vendedor(id_vendedor):
            return {'message': 'Vendedor id "{}" already exists.'.format(id_vendedor)}, 400
        dados = Vendedor.argumentos.parse_args()
        vendedor = VendedorModel(**dados)
        vendedor.save_vendedor()
        return vendedor.json()

    def put(self, id_vendedor):
        dados = Vendedor.argumentos.parse_args()
        vendedor_atualizar = VendedorModel.find_vendedor(id_vendedor)
        if vendedor_atualizar:
            vendedor_atualizar.update_vendedor(**dados)
            vendedor_atualizar.save_vendedor()
            return vendedor_atualizar.json(), 200
        vendedor_novo = VendedorModel(id_vendedor, **dados)
        vendedor_novo.save_vendedor()
        return vendedor_novo.json(), 201

    def delete(self, id_vendedor):
        vendedor = VendedorModel.find_vendedor(id_vendedor)
        if vendedor:
            vendedor.delete_vendedor()
            return {'message': 'Vendedor deleted.'}
        return {'message': 'vendedor not found'}, 404
