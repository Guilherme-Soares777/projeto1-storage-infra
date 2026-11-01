import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('AWS_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(signature_version='s3v4'),
    region_name=os.getenv('AWS_REGION')
)

def descarregar_e_gerar_url():
    bucket_name = "meu-primeiro-bucket"
    nome_no_s3 = "documentos/documento_teste.txt"
    caminho_destino = "src/documento_descarregado.txt"

    # 1. Download direto via SDK boto3
    print(f"📥 A descarregar '{nome_no_s3}' do bucket '{bucket_name}'...")
    try:
        s3_client.download_file(
            Bucket=bucket_name,
            Key=nome_no_s3,
            Filename=caminho_destino
        )
        print(f"✅ Ficheiro descarregado localmente para: {caminho_destino}")
    except Exception as e:
        print(f"❌ Erro ao descarregar ficheiro: {e}")

    # 2. Geração de Presigned URL temporária (válida por 5 minutos / 300 segundos)
    print("\n🔗 A gerar Presigned URL para acesso temporário...")
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': nome_no_s3
            },
            ExpiresIn=300
        )
        print("✅ Presigned URL gerada com sucesso!")
        print(f"\nCopie e cole este link no navegador (válido por 5 min):\n{url}")
    except Exception as e:
        print(f"❌ Erro ao gerar URL: {e}")

if __name__ == "__main__":
    descarregar_e_gerar_url()