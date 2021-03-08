from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    id_usuario = banco.Column(banco.Integer, primary_key=True)
    nome_usuario = banco.Column(banco.String(50))
    telefone_usuario = banco.Column(banco.String(11))
    cpf_usuario = banco.Column(banco.String(11))
    email_usuario = banco.Column(banco.String(50))
    senha = banco.Column(banco.String(30))

    def __init__(self, nome_usuario, telefone_usuario, cpf_usuario, email_usuario, senha):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
        self.cpf_usuario = cpf_usuario
        self.email_usuario = email_usuario
        self.senha = senha

    def json(self):
        return {
            'id_usuario': self.id_usuario,
            'nome_usuario': self.nome_usuario,
            'telefone_usuario': self.telefone_usuario,
            'cpf_usuario': self.cpf_usuario
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

    def deletar_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
