# model.py
# Contém as classes que representam os dados (Model)

class Produto:
    """Classe que representa um produto no estoque"""
    def __init__(self, id, nome, categoria, tamanho, quantidade, preco_compra, preco_venda, fornecedor, imagem=None):
        # atributos do produto
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.tamanho = tamanho
        self.quantidade = quantidade
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor
        self.imagem = imagem  # nome do arquivo da imagem

    def estoque_baixo(self):
        """Retorna True se a quantidade for menor que 10"""
        return self.quantidade < 10


class EstoqueModel:
    """Classe que guarda e manipula a lista de produtos"""
    def __init__(self):
        self.produtos = []  # lista de objetos Produto

    def adicionar_produto(self, id, nome, categoria, tamanho, quantidade, preco_compra, preco_venda, fornecedor, imagem=None):
        """Adiciona um novo produto na lista"""
        produto = Produto(id, nome, categoria, tamanho, quantidade, preco_compra, preco_venda, fornecedor, imagem)
        self.produtos.append(produto)

    def listar_produtos(self):
        """Retorna a lista de produtos"""
        return self.produtos

    def remover_produto(self, indice):
        """Remove um produto pelo índice na lista"""
        if 0 <= indice < len(self.produtos):
            self.produtos.pop(indice)

    def listar_estoque_baixo(self):
        """Retorna apenas os produtos com quantidade menor que 10"""
        return [p for p in self.produtos if p.estoque_baixo()]


class UsuarioModel:
    """Classe que representa o usuário do sistema"""
    def __init__(self):
        # usuário e senha padrão
        self.usuario = 'admin'
        self.senha = '1234'

    def autenticar(self, usuario, senha):
        """Verifica se usuário e senha estão corretos"""
        return usuario == self.usuario and senha == self.senha
