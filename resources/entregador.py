from flask_restful import Resource, reqparse
from flask import render_template
from models.entregador import EntregadorModel
from flask.helpers import make_response
from werkzeug.security import safe_str_cmp
import traceback


atributos = reqparse.RequestParser()
atributos.add_argument('nome_entregador', type=str, required=True, help="Ei! o seu 'nome' é obrigatório!")
atributos.add_argument('cpf_entregador', type=str, required=True, help="Ei! o seu 'cpf' é obrigatório!")
atributos.add_argument('telefone_entregador', type=str, required=True, help="Ei! o seu 'telefone' é obrigatório!")
atributos.add_argument('cnh_entregador', type=str, required=True, help="Ei! a sua 'cnh' é obrigatória!")
atributos.add_argument('email_entregador', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos.add_argument('senha_entregador', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")
atributos.add_argument('ativado', type=bool)


atributos_login = reqparse.RequestParser()
atributos_login.add_argument('email_entregador', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos_login.add_argument('senha_entregador', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")
atributos.add_argument('ativado', type=bool)

class Entregadores(Resource):
    def get(self, id_entregador):
        entregador = EntregadorModel.achar_entregador(id_entregador)
        if entregador:
            return entregador.json()
        return make_response(render_template(".html", message= "Entregador não encontrado."), 404)

    def put(self, id_entregador):
        dados = atributos.parse_args()
        entregador = EntregadorModel.achar_entregador(id_entregador)
        if entregador:
            entregador.atualizar_entregador(**dados)
            entregador.salvar_entregador()
            return {"message": "Entregador atualizado com sucesso!"}, 200
        entregador = EntregadorModel(**dados)
        entregador.salvar_entregador()
        return make_response(render_template(".html", message= "Entregador criado com sucesso!"), 201)

    def delete(self, id_entregador):
        entregador = EntregadorModel.achar_entregador(id_entregador)
        if entregador:
            entregador.deletar_entregador()
            return make_response(render_template(".html", message= 'Entregador deletado com sucesso!'), 200)
        return make_response(render_template(".html", message= 'Entregador não encontrado!'), 404)


class EntregadorRegistro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if EntregadorModel.achar_por_login(dados['email_entregador']):
            return {"message": "O seu login '{}' já existe".format(dados['email_entregador'])}
        entregador = EntregadorModel(**dados)
        entregador.ativado = False
        try:
            entregador.salvar_entregador()
            entregador.enviar_confirmacao_email_entregador()
        except:
            entregador.deletar_entregador()
            traceback.print_exc()
            return make_response(render_template("cadastro_entregador.html",message= 'Erro interno de servidor'), 500)
        return make_response(render_template("login.html", message= "Sucesso! Cadastro pendente de confirmação via email"), 201)


class EntregadorLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos_login.parse_args()
        entregador = EntregadorModel.achar_por_login(dados['email_entregador'])
        if entregador and safe_str_cmp(entregador.senha_entregador, dados['senha_entregador']):
            if entregador.ativado:
                # token_de_acesso = create_access_token(identity=user.id_usuario)
                return make_response(render_template("home.html",message= 'Login realizado com sucesso!'), 200)
            return make_response(render_template("login.html", message= 'Usuário não confirmado'), 400)
        return make_response(render_template("login.html", message= 'Usuário ou senha incorretos.'), 401)


class EntregadorLogout(Resource):
    def post(self):
        r = make_response(render_template("cadastro_entregador.html", message="Deslogou com sucesso!"))
        r.set_cookie("email_entregador", "")
        r.set_cookie("senha_entregador", "")
        # jwt_id = get_raw_jwt()['jti']  # JWT Token Identifier
        # BLACKLIST.add(jwt_id)
        return r


class EntregadorConfirmado(Resource):
    @classmethod
    def get(cls, id_entregador):
        entregador = EntregadorModel.achar_entregador(id_entregador)

        if not entregador:
            return {'message': 'Usuário não encontrado'}, 404

        entregador.ativado = True
        entregador.salvar_entregador()
        #return{'message':'Usuário confirmado com sucesso'}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('usuario_confirmado.html'), 200, headers)
