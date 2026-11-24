
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, testar_conexao
from bson import ObjectId
from datetime import datetime
import plotly.graph_objects as go

app = Flask(__name__)
app.secret_key = "rocha-info-chave-local"

produtos_col = db["produtos"]
vendas_col = db["vendas"]



@app.route("/")
def inicio():
    total_produtos = produtos_col.count_documents({})
    produtos_ativos = produtos_col.count_documents({"ativo": True})
    total_vendas = vendas_col.count_documents({})

    resultado_faturamento = list(vendas_col.aggregate([
        {
            "$group": {
                "_id": None,
                "total": {"$sum": "$total"}
            }
        }
    ]))

    faturamento = (
        resultado_faturamento[0]["total"]
        if resultado_faturamento else 0
    )

    vendas_recentes = list(
        vendas_col.find().sort("data_venda", -1).limit(5)
    )

    produtos_estoque_baixo = list(
        produtos_col.find({
            "ativo": True,
            "quantidade": {"$lte": 3}
        }).sort("quantidade", 1).limit(5)
    )

    return render_template(
        "index.html",
        total_produtos=total_produtos,
        produtos_ativos=produtos_ativos,
        total_vendas=total_vendas,
        faturamento=faturamento,
        vendas_recentes=vendas_recentes,
        produtos_estoque_baixo=produtos_estoque_baixo
    )

# LISTAR PRODUTOS
@app.route("/produtos")
def produtos():
    lista = list(produtos_col.find().sort("data_cadastro", -1))
    return render_template("produtos.html", produtos=lista)


# CADASTRAR PRODUTO
@app.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        try:
            preco_compra = float(request.form["preco_compra"])
            preco_venda = float(request.form["preco_venda"])
            quantidade = int(request.form["quantidade"])
            garantia = int(request.form["garantia"])

            if preco_compra < 0 or preco_venda < 0 or quantidade < 0 or garantia < 0:
                raise ValueError("Os valores não podem ser negativos.")

            produto = {
                "nome": request.form["nome"].strip(),
                "categoria": request.form["categoria"],
                "marca": request.form["marca"].strip(),
                "modelo": request.form["modelo"].strip(),
                "descricao": request.form["descricao"].strip(),
                "preco_compra": preco_compra,
                "preco_venda": preco_venda,
                "quantidade": quantidade,
                "especificacoes": {
                    "condicao": request.form["condicao"],
                    "garantia_dias": garantia
                },
                "historico_precos": [{
                    "preco": preco_venda,
                    "data": datetime.now()
                }],
                "data_cadastro": datetime.now(),
                "ativo": True
            }

            if not produto["nome"] or not produto["marca"]:
                raise ValueError("Nome e marca são obrigatórios.")

            produtos_col.insert_one(produto)
            flash("Produto cadastrado com sucesso!", "success")
            return redirect(url_for("produtos"))

        except (ValueError, KeyError):
            flash("Verifique os campos e informe valores válidos.", "error")

    return render_template("produto_form.html", produto=None)


# EDITAR PRODUTO
@app.route("/produtos/editar/<id>", methods=["GET", "POST"])
def editar_produto(id):
    if not ObjectId.is_valid(id):
        flash("Produto inválido.", "error")
        return redirect(url_for("produtos"))

    produto = produtos_col.find_one({"_id": ObjectId(id)})

    if not produto:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("produtos"))

    if request.method == "POST":
        try:
            preco_compra = float(request.form["preco_compra"])
            preco_venda = float(request.form["preco_venda"])
            quantidade = int(request.form["quantidade"])
            garantia = int(request.form["garantia"])

            if preco_compra < 0 or preco_venda < 0 or quantidade < 0 or garantia < 0:
                raise ValueError()

            historico = produto.get("historico_precos", [])

            if preco_venda != produto["preco_venda"]:
                historico.append({
                    "preco": preco_venda,
                    "data": datetime.now()
                })

            dados = {
                "nome": request.form["nome"].strip(),
                "categoria": request.form["categoria"],
                "marca": request.form["marca"].strip(),
                "modelo": request.form["modelo"].strip(),
                "descricao": request.form["descricao"].strip(),
                "preco_compra": preco_compra,
                "preco_venda": preco_venda,
                "quantidade": quantidade,
                "especificacoes": {
                    "condicao": request.form["condicao"],
                    "garantia_dias": garantia
                },
                "historico_precos": historico,
                "ativo": request.form.get("ativo") == "sim"
            }

            if not dados["nome"] or not dados["marca"]:
                raise ValueError()

            produtos_col.update_one(
                {"_id": ObjectId(id)},
                {"$set": dados}
            )

            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for("produtos"))

        except (ValueError, KeyError):
            flash("Verifique os campos e informe valores válidos.", "error")

    return render_template("produto_form.html", produto=produto)


# EXCLUIR PRODUTO
@app.route("/produtos/excluir/<id>", methods=["POST"])
def excluir_produto(id):
    if not ObjectId.is_valid(id):
        flash("Produto inválido.", "error")
        return redirect(url_for("produtos"))

    produtos_col.delete_one({"_id": ObjectId(id)})
    flash("Produto excluído com sucesso!", "success")
    return redirect(url_for("produtos"))



@app.route("/vendas")
def vendas():
    lista_vendas = list(vendas_col.find().sort("data_venda", -1))
    return render_template("vendas.html", vendas=lista_vendas)


@app.route("/vendas/nova", methods=["GET", "POST"])
def nova_venda():
    produtos = list(produtos_col.find({"ativo": True}).sort("nome", 1))

    if request.method == "POST":
        try:
            produto_id = ObjectId(request.form["produto_id"])
            quantidade = int(request.form["quantidade"])

            if quantidade <= 0:
                raise ValueError

            produto = produtos_col.find_one({
                "_id": produto_id,
                "ativo": True
            })

            if not produto:
                flash("Produto não encontrado ou inativo.", "erro")
                return redirect(url_for("nova_venda"))

            if produto.get("quantidade", 0) < quantidade:
                flash("Estoque insuficiente para essa venda.", "erro")
                return redirect(url_for("nova_venda"))

            preco_unitario = float(produto["preco_venda"])
            subtotal = preco_unitario * quantidade

            # Dá baixa no estoque somente se houver quantidade suficiente.
            resultado = produtos_col.update_one(
                {
                    "_id": produto_id,
                    "quantidade": {"$gte": quantidade}
                },
                {
                    "$inc": {"quantidade": -quantidade}
                }
            )

            if resultado.modified_count == 0:
                flash("Não foi possível atualizar o estoque. Confira a quantidade.", "erro")
                return redirect(url_for("nova_venda"))

            venda = {
                "cliente": {
                    "nome": request.form["cliente"].strip(),
                    "telefone": request.form.get("telefone", "").strip()
                },
                "itens": [
                    {
                        "produto_id": produto_id,
                        "nome_produto": produto["nome"],
                        "categoria": produto["categoria"],
                        "quantidade": quantidade,
                        "preco_unitario": preco_unitario,
                        "subtotal": subtotal
                    }
                ],
                "total": subtotal,
                "forma_pagamento": request.form["forma_pagamento"],
                "status": "Concluída",
                "observacoes": request.form.get("observacoes", "").strip(),
                "data_venda": datetime.now()
            }

            try:
                vendas_col.insert_one(venda)
            except Exception:
                # Se não conseguir salvar a venda, devolve o estoque.
                produtos_col.update_one(
                    {"_id": produto_id},
                    {"$inc": {"quantidade": quantidade}}
                )
                raise

            flash("Venda registrada com sucesso!", "sucesso")
            return redirect(url_for("vendas"))

        except (ValueError, KeyError):
            flash("Confira os dados informados na venda.", "erro")

    return render_template("venda_form.html", produtos=produtos)


@app.route("/vendas/excluir/<id>", methods=["POST"])
def excluir_venda(id):
    try:
        venda_id = ObjectId(id)
    except Exception:
        flash("Venda inválida.", "erro")
        return redirect(url_for("vendas"))

    venda = vendas_col.find_one({"_id": venda_id})

    if venda:
        # Devolve ao estoque os produtos que estavam na venda.
        for item in venda.get("itens", []):
            produtos_col.update_one(
                {"_id": item["produto_id"]},
                {"$inc": {"quantidade": item["quantidade"]}}
            )

        vendas_col.delete_one({"_id": venda_id})
        flash("Venda excluída e estoque atualizado.", "sucesso")
    else:
        flash("Venda não encontrada.", "erro")

    return redirect(url_for("vendas"))



# MENU PRINCIPAL DE RELATÓRIOS
@app.route("/relatorios")
def relatorios():
    return render_template("relatorios.html")


# RELATÓRIO 1: ESTOQUE BAIXO
@app.route("/relatorios/estoque-baixo")
def relatorio_estoque():
    estoque_baixo = list(produtos_col.aggregate([
        {
            "$match": {
                "quantidade": {"$lte": 3},
                "ativo": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "nome": 1,
                "categoria": 1,
                "quantidade": 1,
                "preco_venda": 1
            }
        },
        {"$sort": {"quantidade": 1}}
    ]))

    return render_template(
        "relatorio_estoque.html",
        estoque_baixo=estoque_baixo
    )


# RELATÓRIO 2: PRODUTOS POR CATEGORIA E PREÇO
@app.route("/relatorios/categoria-preco")
def relatorio_categoria_preco():
    categoria_filtro = request.args.get("categoria", "")

    try:
        preco_min = float(request.args.get("preco_min", 0))
        preco_max = float(request.args.get("preco_max", 100000))
    except ValueError:
        preco_min = 0
        preco_max = 100000

    filtro = {
        "preco_venda": {
            "$gte": preco_min,
            "$lte": preco_max
        }
    }

    if categoria_filtro:
        filtro["categoria"] = categoria_filtro

    produtos_filtrados = list(produtos_col.aggregate([
        {"$match": filtro},
        {
            "$project": {
                "_id": 0,
                "nome": 1,
                "categoria": 1,
                "marca": 1,
                "preco_venda": 1
            }
        },
        {"$sort": {"preco_venda": 1}}
    ]))

    categorias = produtos_col.distinct("categoria")

    return render_template(
        "relatorio_categoria_preco.html",
        produtos_filtrados=produtos_filtrados,
        categorias=categorias,
        categoria_filtro=categoria_filtro,
        preco_min=preco_min,
        preco_max=preco_max
    )



@app.route("/relatorios/faturamento-categoria")
def relatorio_faturamento():
    faturamento_categoria = list(vendas_col.aggregate([
        {"$unwind": "$itens"},
        {
            "$group": {
                "_id": "$itens.categoria",
                "total_vendido": {"$sum": "$itens.subtotal"},
                "quantidade_vendida": {"$sum": "$itens.quantidade"}
            }
        },
        {"$sort": {"total_vendido": -1}},
        {
            "$project": {
                "_id": 0,
                "categoria": "$_id",
                "total_vendido": 1,
                "quantidade_vendida": 1
            }
        }
    ]))

    grafico_html = None

    if faturamento_categoria:
        categorias = [
            item["categoria"] for item in faturamento_categoria
        ]

        valores = [
            float(item["total_vendido"]) for item in faturamento_categoria
        ]

        fig = go.Figure(data=[go.Pie(
            labels=categorias,
            values=valores,
            textinfo="label+percent",
            hovertemplate="%{label}<br>Faturamento: R$ %{value:.2f}<extra></extra>"
        )])

        fig.update_layout(
            title="Participação no faturamento por categoria",
            height=450,
            margin=dict(t=60, b=20, l=20, r=20)
        )

        grafico_html = fig.to_html(
            full_html=False,
            include_plotlyjs="cdn",
            config={"responsive": True}
        )

    return render_template(
        "relatorio_faturamento.html",
        faturamento_categoria=faturamento_categoria,
        grafico_html=grafico_html
    )

# RELATÓRIO 4: PRODUTOS MAIS VENDIDOS
@app.route("/relatorios/mais-vendidos")
def relatorio_mais_vendidos():
    produtos_mais_vendidos = list(vendas_col.aggregate([
        {"$unwind": "$itens"},
        {
            "$group": {
                "_id": "$itens.nome_produto",
                "quantidade_vendida": {
                    "$sum": "$itens.quantidade"
                },
                "faturamento": {
                    "$sum": "$itens.subtotal"
                }
            }
        },
        {"$sort": {"quantidade_vendida": -1}},
        {"$limit": 10},
        {
            "$project": {
                "_id": 0,
                "produto": "$_id",
                "quantidade_vendida": 1,
                "faturamento": 1
            }
        }
    ]))

    return render_template(
        "relatorio_mais_vendidos.html",
        produtos_mais_vendidos=produtos_mais_vendidos
    )


if __name__ == "__main__":
    testar_conexao()
    app.run(debug=True)
