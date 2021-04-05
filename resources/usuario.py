from flask_restful import Resource, reqparse
from flask import render_template
from models.usuario import UsuarioModel
from flask.helpers import make_response
from werkzeug.security import safe_str_cmp
import traceback


atributos = reqparse.RequestParser()
atributos.add_argument('nome_usuario', type=str, required=True, help="Ei! o seu 'nome' é obrigatório!")
atributos.add_argument('telefone_usuario', type=str, required=True, help="Ei! o seu 'telefone' é obrigatório!")
atributos.add_argument('cpf_usuario', type=str, required=True, help="Ei! o seu 'cpf' é obrigatório!")
atributos.add_argument('email_usuario', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos.add_argument('senha_usuario', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")
atributos.add_argument('ativado', type=bool)
atributos_login = reqparse.RequestParser()
atributos_login.add_argument('email_usuario', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos_login.add_argument('senha_usuario', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")
atributos_login.add_argument('ativado', type=bool)


class Usuarios(Resource):
    def get(self, id_usuario):
        usuario = UsuarioModel.achar_usuario(id_usuario)
        if usuario:
            return usuario.json()
        return make_response(render_template(".html" , message= "Usuário não encontrado."), 404)

    def put(self, id_usuario):
        dados = atributos.parse_args()
        usuario = UsuarioModel.achar_usuario(id_usuario)
        if usuario:
            usuario.atualizar_usuario(**dados)
            usuario.salvar_usuario()
            return {"message": "Usuário atualizado com sucesso!"}, 200
        usuario = UsuarioModel(**dados)
        usuario.salvar_usuario()
        return make_response(render_template(".html", message= "Vendedor criado com sucesso!"), 201)

    def delete(self, id_usuario):
        user = UsuarioModel.achar_usuario(id_usuario)
        if user:
            user.deletar_usuario()
            return make_response(render_template(".html", message= 'Usuário deletado com sucesso!'), 200)
        return make_response(render_template(".html", message= 'Usuário não encontrado!'), 404)


class UsuarioRegistro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if UsuarioModel.achar_por_login(dados['email_usuario']):
            return {"message": "O seu login '{}' já existe".format(dados['email_usuario'])}
        user = UsuarioModel(**dados)
        user.ativado = False
        try:
            user.salvar_usuario()
            user.enviar_confirmacao_email()
        except:
            user.deletar_usuario()
            traceback.print_exc()
            return make_response(render_template("cadastro_usuario.html", message='Erro interno de servidor'), 500)
        return make_response(render_template("login.html", message= "Sucesso! Cadastro pendente de confirmação via email"), 201)


class UsuarioLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos_login.parse_args()
        user = UsuarioModel.achar_por_login(dados['email_usuario'])
        if user and safe_str_cmp(user.senha_usuario, dados['senha_usuario']):
            if user.ativado:
                # token_de_acesso = create_access_token(identity=user.id_usuario)
                return make_response(render_template("home.html", message= 'Login realizado com sucesso!'), 200)
            return make_response(render_template("login.html", message='Usuário não confirmado'), 400)
        return make_response(render_template("login.html", message='Usuário ou senha incorretos.'), 401)


class UsuarioLogout(Resource):
    def post(self):
        r = make_response(render_template("cadastro_usuario.html", message="Deslogou com sucesso!"))
        r.set_cookie("email_usuario", "")
        r.set_cookie("senha", "")
        # jwt_id = get_raw_jwt()['jti']  # JWT Token Identifier
        # BLACKLIST.add(jwt_id)
        return r


class UsuarioConfirmado(Resource):
    @classmethod
    def get(cls, id_usuario):
        user = UsuarioModel.achar_usuario(id_usuario)

        if not user:
            return {'message': 'Usuário não encontrado'}, 404

        user.ativado = True
        user.salvar_usuario()
        #return{'message':'Usuário confirmado com sucesso'}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('usuario_confirmado.html', email='email_usuario'), 200, headers)