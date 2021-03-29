from flask.helpers import make_response
from flask_restful import Resource, reqparse
from flask import render_template
from models.vendedor import VendedorModel
from werkzeug.security import safe_str_cmp


atributos = reqparse.RequestParser()
atributos.add_argument('nome_vendedor', type=str, required=True, help="Ei! o seu 'nome' é obrigatório!")
atributos.add_argument('telefone_vendedor', type=str, required=True, help="Ei! o seu 'telefone' é obrigatório!")
atributos.add_argument('cnpj_vendedor', type=str, required=True, help="Ei! o seu 'cnpj' é obrigatório!")
atributos.add_argument('email_vendedor', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos.add_argument('senha_vendedor', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")


atributos_login = reqparse.RequestParser()
atributos_login.add_argument('email_vendedor', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos_login.add_argument('senha_vendedor', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")


class Vendedores(Resource):
    def get(self, id_vendedor):
        vendedor = VendedorModel.achar_vendedor(id_vendedor)
        if vendedor:
            return vendedor.json()
        return {"message": "Vendedor não encontrado."}, 404

    def put(self, id_vendedor):
        dados = atributos.parse_args()
        vendedor = VendedorModel.achar_vendedor(id_vendedor)
        if vendedor:
            vendedor.atualizar_vendedor(**dados)
            vendedor.salvar_vendedor()
            return {"message": "Vendedor atualizado com sucesso!"}, 200
        vendedor = VendedorModel(**dados)
        vendedor.salvar_vendedor()
        return {"message": "Vendedor criado com sucesso!"}, 201

    def delete(self, id_vendedor):
        vendedor = VendedorModel.achar_vendedor(id_vendedor)
        if vendedor:
            vendedor.deletar_vendedor()
            return {"message": "Vendedor deletado com sucesso!"}, 200
        return {"message": "Vendedor não encontrado."}, 404


class VendedorRegistro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if VendedorModel.achar_por_login(dados['email_vendedor']):
            return {"message": "O seu login '{}' já existe".format(dados['email_vendedor'])}
        vendedor = VendedorModel(**dados)
        vendedor.salvar_vendedor()
        return {"message": "Vendedor criado com sucesso!"}, 201


class VendedorLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos_login.parse_args()
        user = VendedorModel.achar_por_login(dados['email_vendedor'])
        if user and safe_str_cmp(user.senha_vendedor, dados['senha_vendedor']):
            return {'message': 'Login realizado com sucesso!'}, 200
        return{'message': 'Usuário ou senha incorretos.'}, 401


class VendedorLogout(Resource):
    def post(self):
        r = make_response(render_template("cadastro_vendedores.html", message="Deslogou com sucesso!"))
        r.set_cookie("email_vendedor", "")
        r.set_cookie("senha_vendedor", "")
        return r
