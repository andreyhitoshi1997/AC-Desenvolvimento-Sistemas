from sql_alchemy import banco


class EntregadorModel(banco.Model):
    __tablename__ = 'entregador'
    id_entregador = banco.Column(banco.Integer, primary_key=True)
    nome_entregador = banco.Column(banco.String(200))
    cpf_entregador = banco.Column(banco.String(12))
    telefone_entregador = banco.Column(banco.String(11))
    cnh_entregador = banco.Column(banco.String(100))
    email_entregador = banco.Column(banco.String(50))
    senha_entregador = banco.Column(banco.String(30))

    def __init__(self, nome_entregador, cpf_entregador, telefone_entregador, cnh_entregador, email_entregador, senha_entregador):
        self.nome_entregador = nome_entregador
        self.cpf_entregador = cpf_entregador
        self.telefone_entregador = telefone_entregador
        self.cnh_entregador = cnh_entregador
        self.email_entregador = email_entregador
        self.senha_entregador = senha_entregador

    def json(self):
        return {
            'id_entregador': self.id_entregador,
            'nome_entregador': self.nome_entregador,
            'cpf_entregador': self.cpf_entregador,
            'telefone_entregador': self.telefone_entregador,
            'cnh_entregador': self.cnh_entregador,
            'email_entregador': self.email_entregador
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
