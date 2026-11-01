import os
import boto3
import psycopg2
from botocore.client import Config
from dotenv import load_dotenv

# Carrega credenciais do arquivo .env
load_dotenv()

# Instancia o cliente da API S3
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('AWS_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(signature_version='s3v4'),
    region_name=os.getenv('AWS_REGION')
)

def conectar_bd():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def pipeline_ingestao(caminho_local, pasta_s3):
    if not os.path.exists(caminho_local):
        print(f"❌ Arquivo '{caminho_local}' não encontrado localmente!")
        return

    nome_arquivo = os.path.basename(caminho_local)
    tamanho_bytes = os.path.getsize(caminho_local)
    chave_s3 = f"{pasta_s3}/{nome_arquivo}"
    bucket_name = "meu-primeiro-bucket"

    print(f"\n🚀 Iniciando Pipeline de Ingestão: {nome_arquivo} ({tamanho_bytes} bytes)")

    # 1. Envia o arquivo para o S3/MinIO
    try:
        s3_client.upload_file(caminho_local, bucket_name, chave_s3)
        print(f"  └─ ✅ Upload no S3 concluído: s3://{bucket_name}/{chave_s3}")
    except Exception as e:
        print(f"  └─ ❌ Erro ao enviar para o S3: {e}")
        return

    # 2. Persiste os metadados no PostgreSQL
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        query = """
        INSERT INTO metadados_arquivos (nome_arquivo, chave_s3, tamanho_bytes)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        cursor.execute(query, (nome_arquivo, chave_s3, tamanho_bytes))
        id_registro = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        print(f"  └─ ✅ Metadados gravados no PostgreSQL com sucesso! Registro ID: {id_registro}\n")
    except Exception as e:
        print(f"  └─ ❌ Erro ao salvar metadados no BD: {e}")

if __name__ == "__main__":
    # Testando a ingestão automática na pasta 'relatorios' do S3
    pipeline_ingestao("src/documento_teste.txt", "relatorios")
    