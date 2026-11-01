import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

def conectar_bd():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
        return None

def inicializar_tabela():
    conn = conectar_bd()
    if not conn:
        return

    cursor = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS metadados_arquivos (
        id SERIAL PRIMARY KEY,
        nome_arquivo VARCHAR(255) NOT NULL,
        chave_s3 VARCHAR(255) NOT NULL,
        tamanho_bytes BIGINT,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cursor.execute(query)
        conn.commit()
        print("✅ Tabela 'metadados_arquivos' criada/validada no PostgreSQL com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")
    finally:
        cursor.close()
        conn.close()

def registrar_upload(nome_arquivo, chave_s3, tamanho_bytes):
    conn = conectar_bd()
    if not conn:
        return

    cursor = conn.cursor()
    query = """
    INSERT INTO metadados_arquivos (nome_arquivo, chave_s3, tamanho_bytes)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    try:
        cursor.execute(query, (nome_arquivo, chave_s3, tamanho_bytes))
        id_registro = cursor.fetchone()[0]
        conn.commit()
        print(f"✅ Metadados persistidos no BD com sucesso! ID do registro: {id_registro}")
    except Exception as e:
        print(f"❌ Erro ao inserir metadados: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🚀 Conectando e criando estrutura no PostgreSQL...")
    inicializar_tabela()
    registrar_upload("documento_teste.txt", "documentos/documento_teste.txt", 57)
    