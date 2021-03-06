from flask_restful import Resource, reqparse
from flask import render_template,request
from models.produtos import ProdutosModel
from flask.helpers import make_response
from werkzeug.security import safe_str_cmp
import random
import sqlite3
import os 
# import traceback

atributos = reqparse.RequestParser()
atributos.add_argument('nome_produto', type=str, required=True, help="Ei! o 'nome' é obrigatório!")
atributos.add_argument('codigo_produto', type=str, required=True, help="Ei! o 'Codigo' é obrigatório!")
atributos.add_argument('descricao_produto', type=str, required=False)
atributos.add_argument('preco_produto', type=float, required=True, help="Ei! o 'preço' é obrigatório!")
atributos.add_argument('tipo_produto', type=str, required=True, help="Ei! o 'tipo' é obrigatório!")
atributos.add_argument('filtro_produto', type=str, required=True, help="Ei! o 'filtro' é obrigatório!")
atributos.add_argument('quantidade_produto', type=str, required=True, help="Ei! a 'quantidade' é obrigatória!")


class Produto(Resource):
    def put(self, id_produto):
        dados = atributos.parse_args()
        produto = ProdutosModel.listar_por_id(id_produto)
        if produto:
            produto.atualizar_produto(**dados)
            produto.salvar_produto()
            return make_response(render_template("home.html", message="Produto atualizado com sucesso!"), 200)
        produto = ProdutosModel(**dados)
        produto.salvar_produto()
        return make_response(render_template("home.html", message="Produto criado com sucesso!"), 201)

    def delete(self, id_produto):
        produto = ProdutosModel.listar_por_id(id_produto)
        if produto:
            produto.deletar_produto()
            return make_response(render_template("home.html", message="Produto deletado com sucesso!"), 200)
        return make_response(render_template("home.html", message="Produto não encontrado!"), 404)


class ProdutosRegistro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if ProdutosModel.achar_por_codigo(dados['codigo_produto']):
            return make_response(render_template("home.html", message="Você já cadastrou esse produto!"), 409)
        produtos = ProdutosModel(**dados)
        produtos.salvar_produto()
        return make_response(render_template("home.html", message="Produto cadastrado com sucesso!"), 201)


class ProdutosBuscaSimples(Resource):
    def get(self):
        return {'produto': [produto.json() for produto in ProdutosModel.query.all()]}


def listar_produtos():
    banco = sqlite3.connect("banco.db")
    cursor = banco.cursor()
    consulta = "SELECT nome_produto,preco_produto,descricao_produto, tipo_produto, filtro_produto FROM produto"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    produtos = []
    for linha in resultado:
        produtos.append({
            'nome_produto': linha[0],
            'preco_produto': linha[1],
            'descricao_produto': linha[2],
            'tipo_produto': linha[3],
            'filtro_produto': linha[4]})
    return produtos


def extensao_arquivo(filename):
    if '.' not in filename: 
        return ''
    return filename.rsplit('.', 1)[1].lower()


def salvar_arquivo_upload():
    import uuid
    if "foto" in request.files:
        foto = request.files["foto"]
    e = extensao_arquivo(foto.filename)
    if e in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
        u = uuid.uuid1()
        n = f"{u}.{e}"
        foto.save(os.path.join("fotos_produtos", n))
        return n
    return ""

"""
class ProdutosBuscaFiltro(Resource):
    def get(self, filtro_produto):
        produtos = ProdutosModel.listar_produtos_especifico(filtro_produto)
        if produtos:
            return produtos.json()
        return make_response(render_template("home.html", message="Produto não encontrado."), 404)
"""
