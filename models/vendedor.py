from sql_alchemy import banco


class VendedorModel(banco.Model):
    __tablename__ = 'vendedores'
    id_vendedor = banco.Column(banco.Integer, primary_key=True)
    nome_vendedor = banco.Column(banco.String(50))
    telefone_vendedor = banco.Column(banco.String(11))
    cnpj_vendedor = banco.Column(banco.String(14))
    email_vendedor = banco.Column(banco.String(50))
    senha_vendedor = banco.Column(banco.String(30))

    def __init__(self, nome_vendedor, telefone_vendedor, cnpj_vendedor, email_vendedor, senha_vendedor):
        self.nome_vendedor = nome_vendedor
        self.telefone_vendedor = telefone_vendedor
        self.cnpj_vendedor = cnpj_vendedor
        self.email_vendedor = email_vendedor
        self.senha_vendedor = senha_vendedor

    def json(self):
        return {
            'id_vendedor': self.id_vendedor,
            'nome_vendedor': self.nome_vendedor,
            'telefone_vendedor': self.telefone_vendedor,
            'vendedor-cnpj_vendedor': self.cnpj_vendedor
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

    def atualizar_vendedor(self, nome_vendedor, telefone_vendedor, cnpj_vendedor):
        self.nome_vendedor = nome_vendedor
        self.telefone_vendedor = telefone_vendedor
        self.cnpj_vendedor = cnpj_vendedor

    def deletar_vendedor(self):
        banco.session.delete(self)
        banco.session.commit()
