from sql_alchemy import banco


class EntregadorModel(banco.Model):
    __tablename__ = 'entregador'
    id_entregador = banco.Column(banco.Integer, primary_key=True)
    nome_entregador = banco.Column(banco.String(200))
    telefone_entregador = banco.Column(banco.String(11))
    email_entregador = banco.Column(banco.String(100))
    cnh_entregador = banco.Column(banco.String(100))

    def __init__(self, nome_entregador, telefone_entregador, email_entregador, cnh_entregador):
        self.nome_entregador = nome_entregador
        self.telefone_entregador = telefone_entregador
        self.email_entregador = email_entregador
        self.cnh_entregador = cnh_entregador

    def json(self):
        return {
            'id_entregador': self.id_entregador,
            'nome_entregador': self.nome_entregador,
            'telefone_entregador': self.telefone_entregador,
            'email_entregador': self.email_entregador,
            'cnh_entregador': self.cnh_entregador
        }


    @classmethod
    def find_vendedor(cls, id_entregador):
        entregador = cls.query.filter_by(id_entregador=id_entregador).first()# SELECT * FROM vendedor WHERE id_vendedor = $id_vendedor
        if entregador:
            return entregador
        return None

    def save_entregador(self):
        banco.session.add(self)
        banco.session.commit()

    def update_entregador(self,id_vendedor, nome_vendedor, telefone_vendedor, vendedor_email):
        self.id_vendedor = id_vendedor
        self.nome_vendedor = nome_vendedor
        self.telefone_vendedor = telefone_vendedor
        self.vendedor_email = vendedor_email

    def delete_vendedor(self):
        banco.session.delete(self)
        banco.session.commit()
