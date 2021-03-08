from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask.helpers import make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não pode estar em branco")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode estar em branco")
atributos.add_argument('nome_usuario')
atributos.add_argument('telefone_usuario')
atributos.add_argument('email_usuario')
atributos.add_argument('cpf_usuario')

class User(Resource):
    #/usuarios/{id_usuario}
    def get(self, id_usuario):
        usuario = UserModel.find_user(id_usuario)
        if usuario:
            return usuario.json()
        return {"message": "Usuario não encontrado"}, 404

    def delete(self, id_usuario):
        user = UserModel.find_user(id_usuario)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found'}, 404


class UserRegister(Resource):
    #/cadastro
    def post(self):
        
        dados = atributos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {"message": "O seu login '{}' já existe".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {"message": "Usuario criado com sucesso!"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])
        if user and safe_str_cmp(user.senha, dados['senha']):
            #token_de_acesso = create_access_token(identity=user.id_usuario)
            
            return {}, 200
        return{'message': 'Usuario ou senha incorretos'},401