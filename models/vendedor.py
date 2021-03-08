from sql_alchemy import banco


class VendedorModel(banco.Model):
    __tablename__ = 'vendedor'
    id_vendedor = banco.Column(banco.Integer, primary_key=True)
    nome_vendedor = banco.Column(banco.String(200))
    telefone_vendedor = banco.Column(banco.String(11))
    vendedor_email = banco.Column(banco.String(100))

    def __init__(self, id_vendedor, nome_vendedor, telefone_vendedor, vendedor_email):
        self.id_vendedor = id_vendedor
        self.nome_vendedor = nome_vendedor
        self.telefone_vendedor = telefone_vendedor
        self.vendedor_email = vendedor_email

    def json(self):
        return {
            'id_vendedor': self.id_vendedor,
            'nome_vendedor': self.nome_vendedor,
            'telefone_vendedor': self.telefone_vendedor,
            'vendedor-email': self.vendedor_email
        }


    @classmethod
    def find_vendedor(cls, id_vendedor):
        vendedor = cls.query.filter_by(id_vendedor=id_vendedor).first()# SELECT * FROM vendedor WHERE id_vendedor = $id_vendedor
        if vendedor:
            return vendedor
        return None

    def save_vendedor(self):
        banco.session.add(self)
        banco.session.commit()

    def update_vendedor(self,id_vendedor, nome_vendedor, telefone_vendedor, vendedor_email):
        self.id_vendedor = id_vendedor
        self.nome_vendedor = nome_vendedor
        self.telefone_vendedor = telefone_vendedor
        self.vendedor_email = vendedor_email

    def delete_vendedor(self):
        banco.session.delete(self)
        banco.session.commit()
