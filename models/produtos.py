from sql_alchemy import banco


class ProdutosModel(banco.Model):
    __tablename__ = 'produto'
    id_produto = banco.Column(banco.Integer, primary_key=True)
    nome_produto = banco.Column(banco.String(50), nullable=False)
    codigo_produto = banco.Column(banco.String(8), unique=True, nullable=False)
    descricao_produto = banco.Column(banco.String(100))
    preco_produto = banco.Column(banco.Float(precision=2))
    tipo_produto = banco.Column(banco.String(15))
    filtro_produto = banco.Column(banco.String(10))
    quantidade_produto = banco.Column(banco.String(10))
    peso_produto = banco.Column(banco.Float(precision=2))

    def __init__(self, nome_produto, codigo_produto, descricao_produto, preco_produto, tipo_produto, filtro_produto, quantidade_produto, peso_produto):
        self.nome_produto = nome_produto
        self.codigo_produto = codigo_produto
        self.descricao_produto = descricao_produto
        self.preco_produto = preco_produto
        self.tipo_produto = tipo_produto
        self.filtro_produto = filtro_produto
        self.quantidade_produto = quantidade_produto
        self.peso_produto = peso_produto

    def json(self):
        return {
            'nome_produto': self.nome_produto,
            'codigo_produto': self.codigo_produto,
            'descricao_produto': self.descricao_produto,
            'preco_produto': self.preco_produto,
            'tipo_produto': self.tipo_produto,
            'filtro_produto': self.filtro_produto,
            'quantidade_produto': self.quantidade_produto,
            'peso_produto': self.peso_produto
        }

    @classmethod
    def listar_por_id(cls, id_produto):
        produto = cls.query.filter_by(id_produto=id_produto).first()  # SELECT * FROM produto WHERE id_produto = $id_produto
        if produto:
            return produto
        return None

    @classmethod
    def achar_por_codigo(cls, codigo_produto):
        codigo = cls.query.filter_by(codigo_produto=codigo_produto).first()
        if codigo:
            return codigo
        return None

    """criar um @classmethod, def, de produtos, buscar apenas produtos em uma barra de buscas, retornar por nome
    (fazer checagem via nome, se um produto se chamar "shampoo cachorro 200 ml", e o usuário digitar "shampoo", retornar
    todos os produtos com "shampoo" no nome, independente se for na primeira ou ultima string, complicadinho, sim) """
    # @classmethod
    # def listar_produtos_busca(cls, nome_produto):

    """
        @classmethod
        def listar_produtos_especifico(cls, filtro_produto):
            produto_especifico = cls.query.filter_by(filtro_produto=filtro_produto)
            if produto_especifico:
                return produto_especifico
            return None
    """

    def salvar_produto(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_produto(self, nome_produto, codigo_produto, descricao_produto, preco_produto, tipo_produto, filtro_produto, quantidade_produto, peso_produto):
        self.nome_produto = nome_produto
        self.codigo_produto = codigo_produto
        self.descricao_produto = descricao_produto
        self.preco_produto = preco_produto
        self.tipo_produto = tipo_produto
        self.filtro_produto = filtro_produto
        self.quantidade_produto = quantidade_produto
        self.peso_produto = peso_produto

    def quantidade_selecionada(self, quantidade):
        return quantidade

    def deletar_produto(self):
        banco.session.delete(self)
        banco.session.commit()
