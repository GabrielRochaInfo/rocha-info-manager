import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client[DB_NAME]

def testar_conexao():
    try:
        client.admin.command("ping")
        print("MongoDB conectado com sucesso!")
        print(f"Banco de dados: {DB_NAME}")
        return True
    except Exception as erro:
        print(f"Erro ao conectar: {erro}")
        return False