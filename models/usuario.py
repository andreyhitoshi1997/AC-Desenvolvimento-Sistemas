from operator import imod
from flask.helpers import url_for
from sql_alchemy import banco
from flask import request
from requests import post
import mailgun
domain = mailgun.MAILGUN_DOMAIN
api_key = mailgun.MAILGUN_API_KEY
from_title = mailgun.FROM_TITLE
from_email = mailgun.FROM_EMAIL 


class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'
    id_usuario = banco.Column(banco.Integer, primary_key=True)
    nome_usuario = banco.Column(banco.String(50))
    telefone_usuario = banco.Column(banco.String(11))
    cpf_usuario = banco.Column(banco.String(11))
    email_usuario = banco.Column(banco.String(50), nullable=False, unique=True)
    senha_usuario = banco.Column(banco.String(30), nullable=False)
    endereco_usuario = banco.Column(banco.String(40))
    numero_end_usuario = banco.Column(banco.String(10))
    complemento_usuario = banco.Column(banco.String(30))
    bairro_usuario = banco.Column(banco.String(20))
    cep_usuario = banco.Column(banco.String(8))
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, nome_usuario, telefone_usuario, cpf_usuario, email_usuario, senha_usuario, endereco_usuario, numero_end_usuario, complemento_usuario, bairro_usuario, cep_usuario, ativado):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
        self.cpf_usuario = cpf_usuario
        self.email_usuario = email_usuario
        self.senha_usuario = senha_usuario
        self.endereco_usuario = endereco_usuario
        self.numero_end_usuario = numero_end_usuario
        self.complemento_usuario = complemento_usuario
        self.bairro_usuario = bairro_usuario
        self.cep_usuario = cep_usuario
        self.ativado = ativado

    def enviar_confirmacao_email(self):
        
        link = request.url_root[:-1] + url_for('usuarioconfirmado',id_usuario=self.id_usuario)
        return post('https://api.mailgun.net/v3/{}/messages'.format(domain),
                    auth=('api', api_key),
                    data={'from': '{} <{}>'.format(from_title, from_email),
                    'to': self.email_usuario,
                    'subject': 'Confirmação de Cadastro',
                    'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                    'html': '<html><p>\
                        Confirme seu cadastro clicando no link a seguir:<a href="{}">CONFIRMAR EMAIL</a>\
                            </p><html>'.format(link)
                        })

    def json(self):
        return {
            'nome_usuario': self.nome_usuario,
            'telefone_usuario': self.telefone_usuario,
            'cpf_usuario': self.cpf_usuario,
            'email_usuario': self.email_usuario,
            'endereco_usuario': self.endereco_usuario,
            'numero_end_usuario': self.numero_end_usuario,
            'complemento_usuario': self.complemento_usuario,
            'bairro_usuario': self.bairro_usuario,
            'cep_usuario': self.cep_usuario,
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

    def atualizar_usuario(self, nome_usuario, telefone_usuario, cpf_usuario, email_usuario, senha_usuario, endereco_usuario, numero_end_usuario, complemento_usuario, bairro_usuario, cep_usuario, ativado):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
        self.cpf_usuario = cpf_usuario
        self.email_usuario == email_usuario
        self.senha_usuario == senha_usuario
        self.endereco_usuario = endereco_usuario
        self.numero_end_usuario = numero_end_usuario
        self.complemento_usuario = complemento_usuario
        self.bairro_usuario = bairro_usuario
        self.cep_usuario = cep_usuario
        self.ativado == ativado

    def deletar_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
