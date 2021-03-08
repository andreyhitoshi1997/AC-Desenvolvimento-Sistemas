from flask_restful import Resource, reqparse
from flask import render_template
from models.usuario import UserModel
from flask.helpers import make_response
# from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp


atributos = reqparse.RequestParser()
atributos.add_argument('nome_usuario', type=str, required=True, help="Ei! o seu 'nome' é obrigatório!")
atributos.add_argument('telefone_usuario', type=str, required=True, help="Ei! o seu 'telefone' é obrigatório!")
atributos.add_argument('cpf_usuario', type=str, required=True, help="Ei! o seu 'cpf' é obrigatório!")
atributos.add_argument('email_usuario', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos.add_argument('senha', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")

atributos_login = reqparse.RequestParser()
atributos_login.add_argument('email_usuario', type=str, required=True, help="Ei! o seu 'e-mail' é obrigatório!")
atributos_login.add_argument('senha', type=str, required=True, help="Ei! a sua 'senha' é obrigatória!")


class Usuario(Resource):
    def get(self, id_usuario):
        usuario = UserModel.achar_usuario(id_usuario)
        if usuario:
            return usuario.json()
        return {"message": "Usuário não encontrado."}, 404

    def delete(self, id_usuario):
        user = UserModel.achar_usuario(id_usuario)
        if user:
            user.deletar_usuario()
            return {'message': 'Usuário deletado com sucesso!'}
        return {'message': 'Usuário não encontrado!'}, 404


class UsuarioRegistro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if UserModel.achar_por_login(dados['email_usuario']):
            return {"message": "O seu login '{}' já existe".format(dados['email_usuario'])}
        user = UserModel(**dados)
        user.salvar_usuario()
        return {"message": "Usuario criado com sucesso!"}, 201


class UsuarioLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos_login.parse_args()
        user = UserModel.achar_por_login(dados['email_usuario'])
        if user and safe_str_cmp(user.senha, dados['senha']):
            # token_de_acesso = create_access_token(identity=user.id_usuario)
            return {'message': 'Login realizado com sucesso!'}, 200
        return{'message': 'Usuário ou senha incorretos.'}, 401


class UsuarioLogout(Resource):
    def post(self):
        r = make_response(render_template("cadastro_usuario.html", message="Deslogou com sucesso!"))
        r.set_cookie("email_usuario", "")
        r.set_cookie("senha", "")
        # jwt_id = get_raw_jwt()['jti']  # JWT Token Identifier
        # BLACKLIST.add(jwt_id)
        return r
