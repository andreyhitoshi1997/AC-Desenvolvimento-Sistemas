from sql_alchemy import banco
from flask import url_for
from flask import request
from requests import post
import mailgun

domain = mailgun.MAILGUN_DOMAIN 
site_key = mailgun.MAILGUN_API_KEY
from_title = mailgun.FROM_TITLE
from_email = mailgun.FROM_EMAIL

class VendedorModel(banco.Model):
    __tablename__ = 'vendedores'
    id_vendedor = banco.Column(banco.Integer, primary_key=True)
    nome_vendedor = banco.Column(banco.String(50))
    telefone_vendedor = banco.Column(banco.String(11))
    cnpj_vendedor = banco.Column(banco.String(14))
    email_vendedor = banco.Column(banco.String(50))
    senha_vendedor = banco.Column(banco.String(30))
    endereco_vendedor = banco.Column(banco.String(40))
    numero_end_vendedor = banco.Column(banco.String(10))
    complemento_vendedor = banco.Column(banco.String(30))
    bairro_vendedor = banco.Column(banco.String(20))
    cep_vendedor = banco.Column(banco.String(8))
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, nome_vendedor, telefone_vendedor, cnpj_vendedor, email_vendedor, senha_vendedor, endereco_vendedor, numero_end_vendedor, complemento_vendedor, bairro_vendedor, cep_vendedor, ativado):
        self.nome_vendedor = nome_vendedor
        self.telefone_vendedor = telefone_vendedor
        self.cnpj_vendedor = cnpj_vendedor
        self.email_vendedor = email_vendedor
        self.senha_vendedor = senha_vendedor
        self.endereco_vendedor = endereco_vendedor
        self.numero_end_vendedor = numero_end_vendedor
        self.complemento_vendedor = complemento_vendedor
        self.bairro_vendedor = bairro_vendedor
        self.cep_vendedor = cep_vendedor
        self.ativado = ativado

    def enviar_email_confirmacao_vendedor(self):
        #http://127.0.0.1:5000/confirmacao_vendedor/
        link_vendedor = request.url_root[:-1] + url_for('vendedorconfirmado', id_vendedor=self.id_vendedor)
        return post('https://api.mailgun.net/v3/{}/messages'.format(domain),
                    auth=('api', site_key),
                    data={'from': '{} <{}>'.format(from_title, from_email),
                    'to': self.email_vendedor,
                    'subject': 'Confirmação de Cadastro',
                    'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link_vendedor),
                    'html': '<html><p>\
                        Confirme seu cadastro clicando no link a seguir:<a href="{}">CONFIRMAR EMAIL</a>\
                            </p><html>'.format(link_vendedor)
                        })

    def json(self):
        return {
            'nome_vendedor': self.nome_vendedor,
            'telefone_vendedor': self.telefone_vendedor,
            'cnpj_vendedor': self.cnpj_vendedor,
            'email_vendedor': self.email_vendedor,
            'endereco_vendedor': self.endereco_vendedor,
            'numero_end_vendedor': self.numero_end_vendedor,
            'complemento_vendedor': self.complemento_vendedor,
            'bairro_vendedor': self.bairro_vendedor,
            'cep_vendedor': self.cep_vendedor,
            'ativado': self.ativado
        }

    @classmethod
    def achar_vendedor(cls, id_vendedor):
        vendedor = cls.query.filter_by(id_vendedor=id_vendedor).first()  # SELECT * FROM vendedor WHERE id_vendedor = $id_vendedor
        if vendedor:
            return vendedor
        return None

    @classmethod
    def achar_por_login(cls, email_vendedor):
        vendedor = cls.query.filter_by(email_vendedor=email_vendedor).first()
        if vendedor:
            return vendedor
        return None

    def salvar_vendedor(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_vendedor(self, nome_vendedor, telefone_vendedor, cnpj_vendedor, email_vendedor, senha_vendedor, endereco_vendedor, numero_end_vendedor, complemento_vendedor, bairro_vendedor, cep_vendedor, ativado):
        self.nome_vendedor = nome_vendedor
        self.telefone_vendedor = telefone_vendedor
        self.cnpj_vendedor = cnpj_vendedor
        self.email_vendedor == email_vendedor
        self.senha_vendedor == senha_vendedor
        self.endereco_vendedor = endereco_vendedor
        self.numero_end_vendedor = numero_end_vendedor
        self.complemento_vendedor = complemento_vendedor
        self.bairro_vendedor = bairro_vendedor
        self.cep_vendedor = cep_vendedor
        self.ativado == ativado

    def deletar_vendedor(self):
        banco.session.delete(self)
        banco.session.commit()
