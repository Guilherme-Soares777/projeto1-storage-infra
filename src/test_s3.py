import boto3
from botocore.client import Config

# Configura o cliente boto3 apontando para o MinIO local
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='admin',
    aws_secret_access_key='password123',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

def testar_s3():
    bucket_name = "meu-primeiro-bucket"
    
    print("🚀 Conectando ao MinIO local via API S3...")
    
    # Cria o Bucket
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' criado com sucesso!")
    except Exception as e:
        print(f"ℹ️ Status ao criar bucket: {e}")

    # Lista os Buckets existentes
    resposta = s3_client.list_buckets()
    print("\n🪣 Buckets ativos no ambiente:")
    for bucket in resposta.get('Buckets', []):
        print(f" - {bucket['Name']}")

# CHAMADA OBRIGATÓRIA DA FUNÇÃO (sem recuo/indentação):
if __name__ == "__main__":
    testar_s3()