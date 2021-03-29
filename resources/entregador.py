from flask_restful import Resource, reqparse
from flask import render_template
from models.entregador import EntregadorModel
from flask.helpers import make_response
from werkzeug.security import safe_str_cmp


atributos = reqparse.RequestParser()
atributos.add_argument('nome_entregador', type=str, required=True, help="Ei! o seu 'nome' é obrigatório!")
atributos.add_argument('cpf_entregador', type=str, required=True, help="Ei! o seu 'cpf' é obrigatório!")
atributos.add_argument('telefone_entregador', type=str, required=True, help="Ei! o seu 'telefone' é obrigatório!")
atributos.add_argument('cnh_entregador', type=str, required=True, help="Ei! a sua 'cnh' é obrigatória!")
atributos.add_argument('email_entregador', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos.add_argument('senha_entregador', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")

atributos_login = reqparse.RequestParser()
atributos_login.add_argument('email_entregador', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos_login.add_argument('senha_entregador', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")


class Entregadores(Resource):
    def get(self, id_entregador):
        entregador = EntregadorModel.achar_entregador(id_entregador)
        if entregador:
            return entregador.json()
        return {"message": "Entregador não encontrado."}, 404

    def put(self, id_entregador):
        dados = atributos.parse_args()
        entregador = EntregadorModel.achar_entregador(id_entregador)
        if entregador:
            entregador.atualizar_entregador(**dados)
            entregador.salvar_entregador()
            return {"message": "Entregador atualizado com sucesso!"}, 200
        entregador = EntregadorModel(**dados)
        entregador.salvar_entregador()
        return {"message": "Entregador criado com sucesso!"}, 201

    def delete(self, id_entregador):
        entregador = EntregadorModel.achar_entregador(id_entregador)
        if entregador:
            entregador.deletar_entregador()
            return {'message': 'Entregador deletado com sucesso!'}
        return {'message': 'Entregador não encontrado!'}, 404


class EntregadorRegistro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if EntregadorModel.achar_por_login(dados['email_entregador']):
            return {"message": "O seu login '{}' já existe".format(dados['email_entregador'])}
        entregador = EntregadorModel(**dados)
        entregador.salvar_entregador()
        return {"message": "Entregador criado com sucesso!"}, 201


class EntregadorLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos_login.parse_args()
        entregador = EntregadorModel.achar_por_login(dados['email_entregador'])
        if entregador and safe_str_cmp(entregador.senha_entregador, dados['senha_entregador']):
            return {'message': 'Login realizado com sucesso!'}, 200
        return{'message': 'Usuário ou senha incorretos.'}, 401


class EntregadorLogout(Resource):
    def post(self):
        r = make_response(render_template("cadastro_entregador.html", message="Deslogou com sucesso!"))
        r.set_cookie("email_entregador", "")
        r.set_cookie("senha_entregador", "")
        # jwt_id = get_raw_jwt()['jti']  # JWT Token Identifier
        # BLACKLIST.add(jwt_id)
        return r
