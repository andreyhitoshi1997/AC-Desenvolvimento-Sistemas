from models.entregador import EntregadorModel
from models.vendedor import VendedorModel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_restful import Api
from models.usuario import UsuarioModel
from resources.vendedor import Vendedores, VendedorConfirmado, VendedorRegistro, VendedorLogin, VendedorLogout
from resources.usuario import UsuarioConfirmado, Usuarios, UsuarioRegistro, UsuarioLogin, UsuarioLogout
from resources.entregador import Entregadores, EntregadorConfirmado, EntregadorRegistro, EntregadorLogin, EntregadorLogout
from resources.produtos import Produto, ProdutosRegistro, ProdutosBuscaSimples
from werkzeug.security import safe_str_cmp
import secretkeys
import requests
import json


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


def is_human_vendedor(captcha_response):

    """ Validating recaptcha response from google server
    Returns True captcha test passed for submitted form else returns False.
    """
    secret = secretkeys.SECRET_KEY_VENDEDOR
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


def is_human_usuario(captcha_response):

    """Validating recaptcha response from google server
    Returns True captcha test passed for submitted form else returns False."""
    secret = secretkeys.SECRET_KEY_USUARIO
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


def is_human_entregador(captcha_response):
    # Validating recaptcha response from google server
    # Returns True captcha test passed for submitted form else returns False.
    secret = secretkeys.SECRET_KEY_ENTREGADOR
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


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
    if request.method == 'POST':
        nome_vendedor = request.form['nome_vendedor']
        telefone_vendedor = request.form['telefone_vendededor']
        cnpj_vendedor = request.form['cnpj_vendedor']
        email_vendedor = request.form['email_vendedor']
        senha_vendedor = request.form['senha_vendedor']
        endereco_vendedor = request.form['endereco_vendedor']
        numero_end_vendedor = request.form['numero_end_vendedor']
        complemento_vendedor = request.form['complemento_vendedor']
        bairro_vendedor = request.form['bairro_vendedor']
        cep_vendedor = request.form['cep_vendedor']
        captcha_response = request.form['g-recaptcha-response']
        if is_human_vendedor(captcha_response):
            VendedorModel(nome_vendedor, telefone_vendedor, cnpj_vendedor, email_vendedor, senha_vendedor, endereco_vendedor, numero_end_vendedor, complemento_vendedor, bairro_vendedor, cep_vendedor)
            status = 'Enviado com sucesso'
        else:
            status = 'Im not a robot não pode ficar vazio!.'
        flash(status)
    return render_template('cadastro_vendedores.html')


@app.route('/cadastro_usuario', methods=["GET", "POST"])
def usuario():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        telefone_usuario = request.form['telefone_usuario']
        cpf_usuario = request.form['cpf_usuario']
        email_usuario = request.form['email_usuario']
        senha_usuario = request.form['senha_usuario']
        endereco_usuario = request.form['endereco_usuario']
        numero_end_usuario = request.form['numero_end_usuario']
        complemento_usuario = request.form['complemento_usuario']
        bairro_usuario = request.form['bairro_usuario']
        cep_usuario = request.form['cep_usuario']
        captcha_response = request.form['g-recaptcha-response']
        if is_human_usuario(captcha_response):
            UsuarioModel(nome_usuario, telefone_usuario, cpf_usuario, email_usuario, senha_usuario, endereco_usuario, numero_end_usuario, complemento_usuario, bairro_usuario, cep_usuario)
            status = 'Enviado com sucesso'
        else:
            status = 'Im not a robot não pode ficar vazio!.'
        flash(status)
    return render_template('cadastro_usuario.html')


@app.route('/cadastro_entregador', methods=["GET", "POST"])
def entregador():
    if request.method == 'POST':
        nome_entregador = request.form['nome_entregador']
        cpf_entregador = request.form['cpf_entregador']
        telefone_entregador = request.form['telefone_entregador']
        cnh_entregador = request.form['cnh_entregador']
        email_entregador = request.form['email_entregador']
        senha_entregador = request.form['senha_entregador']
        endereco_entregador = request.form['endereco_entregador']
        numero_end_entregador = request.form['numero_end_entregador']
        complemento_entregador = request.form['complemento_entregador']
        bairro_entregador = request.form['bairro_entregador']
        cep_entregador = request.form['cep_entregador']
        captcha_response = request.form['g-recaptcha-response']
        if is_human_entregador(captcha_response):
            EntregadorModel(nome_entregador, cpf_entregador, telefone_entregador, cnh_entregador, email_entregador, senha_entregador, endereco_entregador, numero_end_entregador, complemento_entregador, bairro_entregador, cep_entregador)
            status = 'Enviado com sucesso'
        else:
            status = 'Im not a robot não pode ficar vazio!'
        flash(status)
        return redirect(url_for('cadastro_entregador'))
    return render_template('cadastro_entregador.html', sitekey=secretkeys.SECRET_KEY_ENTREGADOR)


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
api.add_resource(Produto, '/produto/<int:id_produto>')  # POST
api.add_resource(ProdutosRegistro, '/produto/registro')  # POST
api.add_resource(ProdutosBuscaSimples, '/produto/busca')  # GET
# api.add_resource(ProdutosBuscaFiltro, '/produto/busca/<string:filtro_produto>')  # GET

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
