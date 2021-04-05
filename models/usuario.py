from operator import imod
from flask.helpers import url_for
from sql_alchemy import banco
from flask import request
from requests import post

MAILGUN_DOMAIN ='sandbox0d61b2ebba334f26ad71a55b10995ae8.mailgun.org'
MAILGUN_API_KEY = 'cabaf6f4cee771af940f6c2bc3ddda22-b6d086a8-040f8119'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@petfriends.com'


class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'
    id_usuario = banco.Column(banco.Integer, primary_key=True)
    nome_usuario = banco.Column(banco.String(50))
    telefone_usuario = banco.Column(banco.String(11))
    cpf_usuario = banco.Column(banco.String(11))
    email_usuario = banco.Column(banco.String(50),nullable=False, unique=True)
    senha_usuario = banco.Column(banco.String(30), nullable=False)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, nome_usuario, telefone_usuario, cpf_usuario, email_usuario, senha_usuario, ativado):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
        self.cpf_usuario = cpf_usuario
        self.email_usuario = email_usuario
        self.senha_usuario = senha_usuario
        self.ativado = ativado

    def enviar_confirmacao_email(self):
        #http://127.0.0.1:5000/confirmacao/
        link = request.url_root[:-1] + url_for('usuarioconfirmado',id_usuario=self.id_usuario)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                    'to': self.email_usuario,
                    'subject': 'Confirmação de Cadastro',
                    'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                    'html': '<html><p>\
                        Confirme seu cadastro clicando no link a seguir:<a href="{}">CONFIRMAR EMAIL</a>\
                            </p><html>'.format(link)
                        })
        
        

    def json(self):
        return {
            'id_usuario': self.id_usuario,
            'nome_usuario': self.nome_usuario,
            'telefone_usuario': self.telefone_usuario,
            'cpf_usuario': self.cpf_usuario,
            'email_usuario': self.email_usuario,
            'ativado': self.ativado
                }

    @classmethod
    def achar_usuario(cls, id_usuario):
        usuario = cls.query.filter_by(id_usuario=id_usuario).first()  # SELECT * FROM usuario WHERE id_usuario = $id_usuario
        if usuario:
            return usuario
        return None

    @classmethod
    def achar_por_login(cls, email_usuario):
        usuario = cls.query.filter_by(email_usuario=email_usuario).first()
        if usuario:
            return usuario
        return None

    def salvar_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_usuario(self, nome_usuario, telefone_usuario, cpf_usuario, email_usuario, senha_usuario):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
        self.cpf_usuario = cpf_usuario
        self.email_usuario == email_usuario
        self.senha_usuario == senha_usuario

    def deletar_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
