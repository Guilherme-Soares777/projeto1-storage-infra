import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('AWS_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(signature_version='s3v4'),
    region_name=os.getenv('AWS_REGION')
)

def enviar_arquivo():
    bucket_name = "meu-primeiro-bucket"
    caminho_local = "src/documento_teste.txt"
    nome_no_s3 = "documentos/documento_teste.txt"

    print(f"📤 Enviando '{caminho_local}' para o bucket '{bucket_name}'...")

    try:
        s3_client.upload_file(
            Filename=caminho_local,
            Bucket=bucket_name,
            Key=nome_no_s3
        )
        print("✅ Upload realizado com sucesso!")
        print(f"📁 Objeto salvo no S3 com a chave: {nome_no_s3}")
    except Exception as e:
        print(f"❌ Erro ao enviar arquivo: {e}")

if __name__ == "__main__":
    enviar_arquivo()
    