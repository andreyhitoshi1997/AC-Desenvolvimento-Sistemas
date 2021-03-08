from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuario'
    id_usuario = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    nome_usuario = banco.Column(banco.String(200))
    telefone_usuario = banco.Column(banco.String(11))
    email_usuario = banco.Column(banco.String(100))
    cpf_usuario = banco.Column(banco.String(11))

    def __init__(self, login, senha, nome_usuario, telefone_usuario, email_usuario, cpf_usuario):
        self.login = login
        self.senha = senha
        self.nome_usuario = nome_usuario
        self.telefone = telefone_usuario
        self.email_usuario = email_usuario
        self.cpf_usuario = cpf_usuario

    def json(self):
        return {
            'id_usuario': self.id_usuario,
            'nome_usuario': self.nome_usuario,
            'telefone_usuario': self.telefone_usuario,
            'email_usuario': self.email_usuario,
            'cpf_usuario': self.cpf_usuario
        }

    @classmethod
    def find_user(cls, id_usuario):
        usuario = cls.query.filter_by(id_usuario=id_usuario).first()# SELECT * FROM usuario WHERE id_usuario = $id_usuario
        if usuario:
            return usuario
        return None

    @classmethod
    def find_by_login(cls, login):
        usuario = cls.query.filter_by(login=login).first()
        if usuario:
            return usuario
        return None


    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
