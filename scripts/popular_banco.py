
import os
import sys
from datetime import datetime

# Permite importar o database.py que está na pasta principal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db

produtos_col = db["produtos"]

agora = datetime.now()

# Os produtos estão organizados em uma lista com:
# nome, categoria, marca, modelo, condição,
# descrição, preço de compra, preço de venda,
# quantidade e garantia.

dados_produtos = [

    # COMPUTADORES
    ("PC Gamer Ryzen 5 5600", "Computadores", "AMD", "Ryzen 5 5600 / RTX 3060", "Seminovo", "Computador gamer revisado", 2800, 3599.90, 2, 90),
    ("PC Gamer Ryzen 5 5500", "Computadores", "AMD", "Ryzen 5 5500 / RX 6600", "Seminovo", "Computador para jogos em Full HD", 2400, 3199.90, 1, 90),
    ("PC Intel Core i5 10400F", "Computadores", "Intel", "i5 10400F / GTX 1650", "Seminovo", "Computador para jogos e uso geral", 1700, 2299.90, 2, 90),
    ("PC Ryzen 5 5600G", "Computadores", "AMD", "Ryzen 5 5600G / Vega 7", "Seminovo", "Computador com vídeo integrado", 1500, 2099.90, 1, 90),
    ("PC Intel Core i3 10100F", "Computadores", "Intel", "i3 10100F / RX 570", "Usado", "Computador de entrada", 1200, 1699.90, 2, 90),

    # CONSOLES
    ("PlayStation 5 Slim Digital", "Consoles", "Sony", "PS5 Slim Digital", "Seminovo", "Console revisado e higienizado", 2200, 2799.90, 2, 90),
    ("PlayStation 5 Slim com leitor", "Consoles", "Sony", "PS5 Slim Disc", "Seminovo", "Console com leitor de discos", 2450, 3099.90, 1, 90),
    ("PlayStation 4 Slim 1TB", "Consoles", "Sony", "PS4 Slim 1TB", "Seminovo", "Console revisado", 950, 1399.90, 3, 90),
    ("Xbox Series S 512GB", "Consoles", "Microsoft", "Series S 512GB", "Seminovo", "Console compacto de nova geração", 1350, 1799.90, 2, 90),
    ("Nintendo Switch V2", "Consoles", "Nintendo", "Switch V2", "Seminovo", "Console portátil e de mesa", 850, 1199.90, 2, 90),
    ("Nintendo Switch OLED", "Consoles", "Nintendo", "Switch OLED", "Seminovo", "Console com tela OLED", 1250, 1699.90, 1, 90),

    # NOTEBOOKS
    ("Notebook Lenovo IdeaPad 3", "Notebooks", "Lenovo", "IdeaPad 3 Ryzen 5", "Seminovo", "Notebook para estudos e trabalho", 1700, 2199.90, 1, 90),
    ("Notebook Acer Aspire 5", "Notebooks", "Acer", "Aspire 5 Core i5", "Seminovo", "Notebook para produtividade", 1900, 2499.90, 1, 90),
    ("Notebook Dell Inspiron", "Notebooks", "Dell", "Inspiron Core i5", "Usado", "Notebook para uso diário", 1500, 1999.90, 1, 90),

    # PLACAS DE VÍDEO E COMPONENTES
    ("Placa de vídeo RTX 3050 8GB", "Peças", "NVIDIA", "RTX 3050 8GB", "Seminovo", "Placa de vídeo para jogos", 850, 1099.90, 2, 90),
    ("Placa de vídeo RX 6600 8GB", "Peças", "AMD", "RX 6600 8GB", "Seminovo", "Placa de vídeo Full HD", 950, 1299.90, 2, 90),
    ("Placa de vídeo GTX 1660 Super", "Peças", "NVIDIA", "GTX 1660 Super 6GB", "Usado", "Placa de vídeo para jogos", 650, 899.90, 1, 90),
    ("Processador Ryzen 5 5600", "Peças", "AMD", "Ryzen 5 5600", "Novo", "Processador AM4 de seis núcleos", 650, 799.90, 3, 90),
    ("Processador Ryzen 5 5600G", "Peças", "AMD", "Ryzen 5 5600G", "Seminovo", "Processador com vídeo integrado", 550, 699.90, 2, 90),
    ("Memória RAM DDR4 16GB", "Peças", "Kingston", "Fury 16GB 3200MHz", "Novo", "Memória DDR4 para computadores", 180, 249.90, 5, 90),
    ("SSD NVMe 500GB", "Peças", "Kingston", "NV2 500GB", "Novo", "Armazenamento SSD NVMe", 180, 249.90, 5, 90),
    ("Fonte Corsair 550W", "Peças", "Corsair", "CV550 550W", "Novo", "Fonte para computadores", 280, 369.90, 3, 90),

    # PERIFÉRICOS
    ("Monitor LG UltraGear 27", "Periféricos", "LG", "27GN65R 144Hz", "Seminovo", "Monitor gamer Full HD", 500, 699.90, 2, 90),
    ("Teclado Mecânico Redragon", "Periféricos", "Redragon", "Kumara RGB", "Seminovo", "Teclado mecânico RGB", 120, 179.90, 3, 90),
    ("Mouse Gamer Logitech G203", "Periféricos", "Logitech", "G203 Lightsync", "Novo", "Mouse gamer com iluminação RGB", 100, 149.90, 4, 90),
    ("Headset HyperX Cloud Stinger", "Periféricos", "HyperX", "Cloud Stinger", "Seminovo", "Headset para jogos", 150, 219.90, 2, 90),
    ("Controle DualSense PS5", "Periféricos", "Sony", "DualSense", "Seminovo", "Controle sem fio para PlayStation 5", 250, 349.90, 3, 90),
    ("Controle Xbox Wireless", "Periféricos", "Microsoft", "Xbox Wireless Controller", "Seminovo", "Controle sem fio para Xbox e PC", 220, 299.90, 2, 90),
    ("Webcam Logitech C920", "Periféricos", "Logitech", "C920 HD Pro", "Seminovo", "Webcam Full HD para reuniões e transmissões", 250, 329.90, 1, 90),
    ("Mousepad Gamer Grande", "Periféricos", "Redragon", "Mousepad Extended", "Novo", "Mousepad de superfície estendida", 35, 59.90, 6, 30),
]


def popular_banco():

    existentes = set(produtos_col.distinct("nome"))

    novos_produtos = []

    for item in dados_produtos:

        nome, categoria, marca, modelo, condicao, descricao, compra, venda, quantidade, garantia = item

        if nome in existentes:
            continue

        produto = {
            "nome": nome,
            "categoria": categoria,
            "marca": marca,
            "modelo": modelo,
            "descricao": descricao,
            "preco_compra": float(compra),
            "preco_venda": float(venda),
            "quantidade": int(quantidade),

            "especificacoes": {
                "condicao": condicao,
                "garantia_dias": garantia
            },

            "historico_precos": [
                {
                    "preco": float(venda),
                    "data": agora
                }
            ],

            "data_cadastro": agora,
            "ativo": True
        }

        novos_produtos.append(produto)

    if novos_produtos:
        resultado = produtos_col.insert_many(novos_produtos)
        print(f"{len(resultado.inserted_ids)} produtos cadastrados!")
    else:
        print("Todos os produtos desta lista já estavam cadastrados.")

    print(f"Total de produtos na coleção: {produtos_col.count_documents({})}")


if __name__ == "__main__":
    popular_banco()
