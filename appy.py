# app.py
# Arquivo principal do Flask (rotas da aplicação)

import os
from flask import Flask, render_template, request, redirect, url_for, session
from controllers import EstoqueController
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "segredo123"  # usado para gerenciar sessão do login
controller = EstoqueController()

# Configuração para upload de imagens
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}  # tipos de arquivos permitidos

def allowed_filename(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ---------------- ROTAS ---------------- #

@app.route("/", methods=["GET", "POST"])
def login():
    """Tela de login"""
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        if controller.autenticar_usuario(usuario, senha):
            session["usuario"] = usuario
            return redirect(url_for("index"))
        return render_template("login.html", erro="Usuário ou senha inválidos!")
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Sai do sistema e volta para o login"""
    session.pop("usuario", None)
    return redirect(url_for("login"))


@app.route("/index")
def index():
    """Página inicial (menu principal)"""
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """Página de cadastro de produtos"""
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # pega dados do formulário
        id = request.form["id"]
        nome = request.form["nome"]
        categoria = request.form["categoria"]
        tamanho = request.form["tamanho"]
        quantidade = int(request.form["quantidade"])
        preco_compra = float(request.form["preco_compra"])
        preco_venda = float(request.form["preco_venda"])
        fornecedor = request.form["fornecedor"]

        # salva imagem se existir
        imagem = request.files.get("imagem")
        imagem_nome = None
        if imagem and imagem.filename and allowed_filename(imagem.filename):
            imagem_nome = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config["UPLOAD_FOLDER"], imagem_nome))

        # envia para o controller
        controller.cadastrar_produto(id, nome, categoria, tamanho, quantidade,
                                     preco_compra, preco_venda, fornecedor, imagem_nome)
        return redirect(url_for("listar"))

    return render_template("cadastro.html")


@app.route("/listar")
def listar():
    """Lista todos os produtos (com busca, filtros e ordenação)"""
    if "usuario" not in session:
        return redirect(url_for("login"))

    categoria = request.args.get("categoria", "").lower()
    tamanho = request.args.get("tamanho", "").lower()
    nome = request.args.get("nome", "").lower()
    ordenar = request.args.get("ordenar", "nome")
    ordem = request.args.get("ordem", "asc")

    produtos = controller.listar_produtos()

    # filtros
    if categoria:
        produtos = [p for p in produtos if categoria in p.categoria.lower()]
    if tamanho:
        produtos = [p for p in produtos if tamanho in p.tamanho.lower()]
    if nome:
        produtos = [p for p in produtos if nome in p.nome.lower()]

    # ordenação
    if ordenar == "nome":
        produtos.sort(key=lambda p: p.nome.lower(), reverse=(ordem == "desc"))
    elif ordenar == "preco":
        produtos.sort(key=lambda p: p.preco_venda, reverse=(ordem == "desc"))
    elif ordenar == "quantidade":
        produtos.sort(key=lambda p: p.quantidade, reverse=(ordem == "desc"))

    return render_template("listar.html", produtos=produtos,
                           categoria=categoria, tamanho=tamanho, nome=nome,
                           ordenar=ordenar, ordem=ordem)


@app.route("/produto/<int:indice>")
def produto(indice):
    """Mostra os detalhes de um produto"""
    if "usuario" not in session:
        return redirect(url_for("login"))
    produtos = controller.listar_produtos()
    if 0 <= indice < len(produtos):
        return render_template("produto.html", produto=produtos[indice], indice=indice)
    return redirect(url_for("listar"))


@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar(indice):
    """Edita os dados de um produto existente"""
    if "usuario" not in session:
        return redirect(url_for("login"))

    produtos = controller.listar_produtos()
    if not (0 <= indice < len(produtos)):
        return redirect(url_for("listar"))

    produto = produtos[indice]

    if request.method == "POST":
        # atualiza atributos
        produto.id = request.form["id"]
        produto.nome = request.form["nome"]
        produto.categoria = request.form["categoria"]
        produto.tamanho = request.form["tamanho"]
        produto.quantidade = int(request.form["quantidade"])
        produto.preco_compra = float(request.form["preco_compra"])
        produto.preco_venda = float(request.form["preco_venda"])
        produto.fornecedor = request.form["fornecedor"]

        # atualiza imagem se enviada
        imagem = request.files.get("imagem")
        if imagem and imagem.filename and allowed_filename(imagem.filename):
            imagem_nome = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config["UPLOAD_FOLDER"], imagem_nome))
            produto.imagem = imagem_nome

        return redirect(url_for("produto", indice=indice))

    return render_template("editar.html", produto=produto, indice=indice)


@app.route("/remover/<int:indice>")
def remover(indice):
    """Remove um produto do estoque"""
    if "usuario" not in session:
        return redirect(url_for("login"))
    controller.remover_produto(indice)
    return redirect(url_for("listar"))


if __name__ == "__main__":
    app.run(debug=True)
