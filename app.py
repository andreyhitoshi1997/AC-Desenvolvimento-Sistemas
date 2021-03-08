from flask import Flask, render_template, request
from flask_restful import Api
from models.usuario import UserModel
from resources.vendedor import Vendedor, VendedorRegistro, VendedorLogin, VendedorLogout
from resources.usuario import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout
from resources.entregador import Entregador, EntregadorRegistro, EntregadorLogin, EntregadorLogout
from werkzeug.security import safe_str_cmp


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


@app.route('/cadastro_vendedor')
def vendedor():
    return render_template('cadastro_vendedores.html')

@app.route('/cadastro_usuario')
def usuario():
    return render_template('cadastro_usuario.html')

@app.route('/cadastro_entregador')
def entregador():
    return render_template('cadastro_entregador.html')

@app.route('/home')
def home():
    if login_ok(request):
        pass
    return render_template("login.html", message="Sem autorização.")


def login_ok(req):
    login = req.cookies.get("login")
    senha = req.cookies.get("senha")
    user = UserModel.achar_por_login(login)
    return user is not None and safe_str_cmp(user.senha, senha)


# api.add_resource(Vendedor, '/vendedores/<int:id_vendedor>')
api.add_resource(VendedorRegistro, '/vendedor_cadastro')
api.add_resource(VendedorLogin, '/vendedor_login')
api.add_resource(VendedorLogout, '/logout')
# api.add_resource(Usuario, '/usuarios/<int:id_usuario>')
api.add_resource(UsuarioRegistro, '/usuario_cadastro')
api.add_resource(UsuarioLogin, '/usuario_login')
api.add_resource(UsuarioLogout, '/logout')
# api.add_resource(Entregador, '/entregador/<int:id_entregador>')
api.add_resource(EntregadorRegistro, '/entregador_cadastro')
api.add_resource(EntregadorLogin, '/entregador_login')
api.add_resource(EntregadorLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
