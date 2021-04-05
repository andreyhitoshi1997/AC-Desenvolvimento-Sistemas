from sql_alchemy import banco
from flask import request
from requests import post
from flask.helpers import url_for

MAILGUN_DOMAIN ='sandbox0d61b2ebba334f26ad71a55b10995ae8.mailgun.org'
MAILGUN_API_KEY = 'cabaf6f4cee771af940f6c2bc3ddda22-b6d086a8-040f8119'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@petfriends.com'


class EntregadorModel(banco.Model):
    __tablename__ = 'entregador'
    id_entregador = banco.Column(banco.Integer, primary_key=True)
    nome_entregador = banco.Column(banco.String(200))
    cpf_entregador = banco.Column(banco.String(12))
    telefone_entregador = banco.Column(banco.String(11))
    cnh_entregador = banco.Column(banco.String(100))
    email_entregador = banco.Column(banco.String(50))
    senha_entregador = banco.Column(banco.String(30))
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, nome_entregador, cpf_entregador, telefone_entregador, cnh_entregador, email_entregador, senha_entregador,ativado):
        self.nome_entregador = nome_entregador
        self.cpf_entregador = cpf_entregador
        self.telefone_entregador = telefone_entregador
        self.cnh_entregador = cnh_entregador
        self.email_entregador = email_entregador
        self.senha_entregador = senha_entregador
        self.ativado = ativado

    def enviar_confirmacao_email_entregador(self):
        #http://127.0.0.1:5000/confirmacao_entregador/
        link = request.url_root[:-1] + url_for('entregadorconfirmado',id_entregador=self.id_entregador)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                    'to': self.email_entregador,
                    'subject': 'Confirmação de Cadastro',
                    'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                    'html': '<html><p>\
                        Confirme seu cadastro clicando no link a seguir:<a href="{}">CONFIRMAR EMAIL</a>\
                            </p><html>'.format(link)
                        })

    def json(self):
        return {
            'id_entregador': self.id_entregador,
            'nome_entregador': self.nome_entregador,
            'cpf_entregador': self.cpf_entregador,
            'telefone_entregador': self.telefone_entregador,
            'cnh_entregador': self.cnh_entregador,
            'email_entregador': self.email_entregador,
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

    def atualizar_entregador(self, nome_entregador, cpf_entregador, telefone_entregador, cnh_entregador, email_entregador, senha_entregador):
        if email_entregador == email_entregador:
            if senha_entregador == senha_entregador:
                self.nome_entregador = nome_entregador
                self.cpf_entregador = cpf_entregador
                self.telefone_entregador = telefone_entregador
                self.cnh_entregador = cnh_entregador


    def deletar_entregador(self):
        banco.session.delete(self)
        banco.session.commit()
