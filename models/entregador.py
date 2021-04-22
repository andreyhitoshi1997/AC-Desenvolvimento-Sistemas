from sql_alchemy import banco
from flask import request
from requests import post
from flask.helpers import url_for
import mailgun

domain = mailgun.MAILGUN_DOMAIN
api_key = mailgun.MAILGUN_API_KEY
title = mailgun.FROM_TITLE
email = mailgun.FROM_EMAIL


class EntregadorModel(banco.Model):
    __tablename__ = 'entregador'
    id_entregador = banco.Column(banco.Integer, primary_key=True)
    nome_entregador = banco.Column(banco.String(200))
    cpf_entregador = banco.Column(banco.String(12))
    telefone_entregador = banco.Column(banco.String(11))
    cnh_entregador = banco.Column(banco.String(100))
    email_entregador = banco.Column(banco.String(50))
    senha_entregador = banco.Column(banco.String(30))
    endereco_entregador = banco.Column(banco.String(40))
    numero_end_entregador = banco.Column(banco.String(10))
    complemento_entregador = banco.Column(banco.String(30))
    bairro_entregador = banco.Column(banco.String(20))
    cep_entregador = banco.Column(banco.String(8))
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, nome_entregador, cpf_entregador, telefone_entregador, cnh_entregador, email_entregador, senha_entregador, endereco_entregador, numero_end_entregador, complemento_entregador, bairro_entregador, cep_entregador, ativado):
        self.nome_entregador = nome_entregador
        self.cpf_entregador = cpf_entregador
        self.telefone_entregador = telefone_entregador
        self.cnh_entregador = cnh_entregador
        self.email_entregador = email_entregador
        self.senha_entregador = senha_entregador
        self.endereco_entregador = endereco_entregador
        self.numero_end_entregador = numero_end_entregador
        self.complemento_entregador = complemento_entregador
        self.bairro_entregador = bairro_entregador
        self.cep_entregador = cep_entregador
        self.ativado = ativado

    def enviar_confirmacao_email_entregador(self):
        # http://127.0.0.1:5000/confirmacao_entregador/
        link = request.url_root[:-1] + url_for('entregadorconfirmado', id_entregador=self.id_entregador)
        return post('https://api.mailgun.net/v3/{}/messages'.format(domain),
                    auth=('api', api_key),
                    data={'from': '{} <{}>'.format(title, email),
                    'to': self.email_entregador,
                    'subject': 'Confirmação de Cadastro',
                    'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                    'html': '<html><p>\
                        Confirme seu cadastro clicando no link a seguir:<a href="{}">CONFIRMAR EMAIL</a>\
                            </p><html>'.format(link)
                        })

    def json(self):
        return {
            'nome_entregador': self.nome_entregador,
            'cpf_entregador': self.cpf_entregador,
            'telefone_entregador': self.telefone_entregador,
            'cnh_entregador': self.cnh_entregador,
            'email_entregador': self.email_entregador,
            'endereco_entregador': self.endereco_entregador,
            'numero_end_entregador': self.numero_end_entregador,
            'complemento_entregador': self.complemento_entregador,
            'bairro_entregador': self.numero_end_entregador,
            'cep_entregador': self.cep_entregador,
            'ativado': self.ativado
        }

    @classmethod
    def achar_entregador(cls, id_entregador):
        entregador = cls.query.filter_by(id_entregador=id_entregador).first()  # SELECT * FROM usuario WHERE id_usuario = $id_usuario
        if entregador:
            return entregador
        return None

    @classmethod
    def achar_por_login(cls, email_entregador):
        entregador = cls.query.filter_by(email_entregador=email_entregador).first()
        if entregador:
            return entregador
        return None

    def salvar_entregador(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_entregador(self, nome_entregador, cpf_entregador, telefone_entregador, cnh_entregador, email_entregador, senha_entregador, endereco_entregador, numero_end_entregador, complemento_entregador, bairro_entregador, cep_entregador, ativado):
        if email_entregador == email_entregador:
            if senha_entregador == senha_entregador:
                self.nome_entregador = nome_entregador
                self.cpf_entregador = cpf_entregador
                self.telefone_entregador = telefone_entregador
                self.cnh_entregador = cnh_entregador
                self.endereco_entregador = endereco_entregador
                self.numero_end_entregador = numero_end_entregador
                self.complemento_entregador = complemento_entregador
                self.bairro_entregador = bairro_entregador
                self.cep_entregador = cep_entregador
                self.ativado == ativado

    def deletar_entregador(self):
        banco.session.delete(self)
        banco.session.commit()
