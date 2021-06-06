from flask.helpers import make_response
from flask_restful import Resource, reqparse
from flask import render_template,request
from models.vendedor import VendedorModel
from werkzeug.security import safe_str_cmp
import traceback
import os

atributos = reqparse.RequestParser()
atributos.add_argument('nome_vendedor', type=str, required=True, help="Ei! o seu 'nome' é obrigatório!")
atributos.add_argument('telefone_vendedor', type=str, required=True, help="Ei! o seu 'telefone' é obrigatório!")
atributos.add_argument('cnpj_vendedor', type=str, required=True, help="Ei! o seu 'cnpj' é obrigatório!")
atributos.add_argument('email_vendedor', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos.add_argument('senha_vendedor', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")
atributos.add_argument('endereco_vendedor', type=str, required=True, help="Ei! o seu 'endereço' é obrigatório!")
atributos.add_argument('numero_end_vendedor', type=str, required=True, help="Ei! o seu 'número de endereço' é obrigatório!")
atributos.add_argument('complemento_vendedor', type=str, required=False)
atributos.add_argument('bairro_vendedor', type=str, required=True, help="Ei! o seu 'bairro' é obrigatório!")
atributos.add_argument('cep_vendedor', type=str, required=True, help="Ei! o seu 'cep' é obrigatório!")
atributos.add_argument('ativado', type=bool)

atributos_login = reqparse.RequestParser()
atributos_login.add_argument('email_vendedor', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos_login.add_argument('senha_vendedor', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")
atributos.add_argument('ativado', type=bool)


class Vendedores(Resource):
    def get(self, id_vendedor):
        vendedor = VendedorModel.achar_vendedor(id_vendedor)
        if vendedor:
            return vendedor.json()
        return make_response(render_template("home.html", message= "Vendedor não encontrado."), 404)

    def put(self, id_vendedor):
        dados = atributos.parse_args()
        vendedor = VendedorModel.achar_vendedor(id_vendedor)
        if vendedor:
            vendedor.atualizar_vendedor(**dados)
            vendedor.salvar_vendedor()
            return {"message": "Vendedor atualizado com sucesso!"}, 200
        vendedor = VendedorModel(**dados)
        vendedor.salvar_vendedor()
        return make_response(render_template("home.html", message="Vendedor criado com sucesso!"), 201)

    def delete(self, id_vendedor):
        vendedor = VendedorModel.achar_vendedor(id_vendedor)
        if vendedor:
            vendedor.deletar_vendedor()
            return {"message": "Vendedor deletado com sucesso!"}, 200
        return make_response(render_template("home.html", message="Vendedor não encontrado."), 404)


class VendedorRegistro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if VendedorModel.achar_por_login(dados['email_vendedor']):
            return {"message": "O seu login '{}' já existe".format(dados['email_vendedor'])}
        vendedor = VendedorModel(**dados)
        vendedor.ativado = False
        try:
            vendedor.salvar_vendedor()
            vendedor.enviar_email_confirmacao_vendedor()
        except:
            vendedor.deletar_vendedor()
            traceback.print_exc()
            return make_response(render_template("cadastro_vendedores.html", message='Erro interno de servidor'), 500)
        return make_response(render_template("login.html", message="Sucesso! Cadastro pendente de confirmação via email"), 201)


class VendedorLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos_login.parse_args()
        user = VendedorModel.achar_por_login(dados['email_vendedor'])
        if user and safe_str_cmp(user.senha_vendedor, dados['senha_vendedor']):
            if user.ativado:
                return make_response(render_template("home.html", message='Login realizado com sucesso!'), 200)
            return make_response(render_template("login.html", message='Usuário não confirmado, por favor verifique seu e-mail'), 400)
        return make_response(render_template("login.html", message='Usuário ou senha incorretos.'), 401)


class VendedorLogout(Resource):
    def post(self):
        r = make_response(render_template("cadastro_vendedores.html", message="Deslogou com sucesso!"))
        r.set_cookie("email_vendedor", "")
        r.set_cookie("senha_vendedor", "")
        return r


class VendedorConfirmado(Resource):
    @classmethod
    def get(cls, id_vendedor):
        vendedor = VendedorModel.achar_vendedor(id_vendedor)
        if not vendedor:
            return {'message': 'Vendedor não encontrado'}, 404
        vendedor.ativado = True
        vendedor.salvar_vendedor()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('usuario_confirmado.html' ), 200, headers)



