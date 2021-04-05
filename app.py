from flask import Flask, render_template, request
from flask_restful import Api
from models.usuario import UsuarioModel
from resources.vendedor import Vendedores, VendedorConfirmado, VendedorRegistro, VendedorLogin, VendedorLogout
from resources.usuario import UsuarioConfirmado, Usuarios, UsuarioRegistro, UsuarioLogin, UsuarioLogout
from resources.entregador import Entregadores, EntregadorConfirmado, EntregadorRegistro, EntregadorLogin, EntregadorLogout
from werkzeug.security import safe_str_cmp


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/main_home')
def main_home():
    # if login_ok(request):
    return render_template('home_login.html')
    # return render_template('login.html', message="Sem autorização")


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/cadastros')
def cadastros():
    return render_template('cadastros.html')


@app.route('/cadastro_vendedor')
def vendedor():
    return render_template('cadastro_vendedores.html')


@app.route('/cadastro_usuario')
def usuario():
    return render_template('cadastro_usuario.html')


@app.route('/cadastro_entregador')
def entregador():
    return render_template('cadastro_entregador.html')


@app.route('/produtos')
def produtos():
    # if login_ok(request):
    return render_template('produtos.html')


def login_ok(req):
    login = req.cookies.get("login")
    senha = req.cookies.get("senha")
    user = UsuarioModel.achar_por_login(login)
    return user is not None and safe_str_cmp(user.senha, senha)


api.add_resource(VendedorRegistro, '/vendedor_cadastro')  # POST
api.add_resource(VendedorLogin, '/vendedor_login')  # POST
api.add_resource(VendedorLogout, '/logout')  # POST
api.add_resource(Vendedores, '/vendedores/<int:id_vendedor>')  # GET
api.add_resource(Usuarios, '/usuarios/<int:id_usuario>')
api.add_resource(UsuarioRegistro, '/usuario_cadastro')  # POST
api.add_resource(UsuarioLogin, '/usuario_login')  # POST
api.add_resource(UsuarioLogout, '/logout')  # POST
api.add_resource(Entregadores, '/entregador/<int:id_entregador>')
api.add_resource(EntregadorRegistro, '/entregador_cadastro')  # POST
api.add_resource(EntregadorLogin, '/entregador_login')  # POST
api.add_resource(EntregadorLogout, '/logout')  # POST
api.add_resource(UsuarioConfirmado, '/confirmacao/<int:id_usuario>')  # GET
api.add_resource(VendedorConfirmado, '/confirmacao_vendedor/<int:id_vendedor>')  # GET
api.add_resource(EntregadorConfirmado, '/confirmacao_entregador/<int:id_entregador>')  # GET

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
