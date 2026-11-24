
import sys
from pathlib import Path
from bson import json_util

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from database import db

# Pasta onde os arquivos serão salvos
PASTA_BACKUP = BASE_DIR / "backup_mongodb"
PASTA_BACKUP.mkdir(exist_ok=True)

# Coleções que serão exportadas
colecoes = ["produtos", "vendas"]

for nome in colecoes:
    dados = list(db[nome].find())

    caminho = PASTA_BACKUP / f"{nome}.json"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(
            json_util.dumps(
                dados,
                indent=4,
                ensure_ascii=False
            )
        )

    print(f"Coleção: {nome}")
    print(f"Documentos exportados: {len(dados)}")
    print(f"Arquivo salvo: {caminho}")
    print("-" * 40)

print("Exportação concluída!")
