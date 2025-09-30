# controllers.py
# Faz a ligação entre o Model (dados) e o Flask (rotas)

from model import EstoqueModel, UsuarioModel

class EstoqueController:
    """Classe que coordena as ações entre Model e rotas"""
    def __init__(self):
        # cria instâncias do estoque e usuário
        self.estoque_model = EstoqueModel()
        self.usuario_model = UsuarioModel()

    def cadastrar_produto(self, id, nome, categoria, tamanho, quantidade, preco_compra, preco_venda, fornecedor, imagem=None):
        """Cadastra um novo produto no estoque"""
        self.estoque_model.adicionar_produto(id, nome, categoria, tamanho, quantidade, preco_compra, preco_venda, fornecedor, imagem)

    def listar_produtos(self):
        """Retorna a lista de produtos"""
        return self.estoque_model.listar_produtos()

    def remover_produto(self, indice):
        """Remove um produto do estoque"""
        self.estoque_model.remover_produto(indice)

    def autenticar_usuario(self, usuario, senha):
        """Verifica se usuário e senha estão corretos"""
        return self.usuario_model.autenticar(usuario, senha)

    def listar_estoque_baixo(self):
        """Lista apenas os produtos com quantidade baixa"""
        return self.estoque_model.listar_estoque_baixo()
