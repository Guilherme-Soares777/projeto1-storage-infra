import os
import boto3
import redis
from botocore.client import Config
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Cliente S3
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('AWS_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(signature_version='s3v4'),
    region_name=os.getenv('AWS_REGION')
)

# Cliente Valkey (compatível com a biblioteca redis)
valkey_client = redis.Redis.from_url(os.getenv('VALKEY_URL', 'redis://localhost:6379'), decode_responses=True)

def obter_presigned_url_com_cache(bucket_name, chave_s3, expiracao_segundos=300):
    chave_cache = f"url_presigned:{chave_s3}"

    # 1. Tenta buscar a URL diretamente do Valkey (CACHE HIT)
    url_cached = valkey_client.get(chave_cache)
    if url_cached:
        print("⚡ [CACHE HIT] URL recuperada instantaneamente da memória (Valkey)!")
        return url_cached

    # 2. Se não existir no cache (CACHE MISS), gera via S3 e armazena no Valkey
    print("🐢 [CACHE MISS] Gerando nova Presigned URL no S3...")
    url_gerada = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': chave_s3},
        ExpiresIn=expiracao_segundos
    )

    # Armazena no Valkey definindo o TTL (Time-to-Live) igual ao tempo de expiração da URL
    valkey_client.setex(chave_cache, expiracao_segundos, url_gerada)
    print("✅ URL salva no cache do Valkey!")
    return url_gerada

if __name__ == "__main__":
    bucket = "meu-primeiro-bucket"
    chave = "relatorios/documento_teste.txt"

    print("--- Primeira chamada (Deve dar CACHE MISS) ---")
    url1 = obter_presigned_url_com_cache(bucket, chave)
    print(f"Link: {url1}\n")

    print("--- Segunda chamada imediata (Deve dar CACHE HIT) ---")
    url2 = obter_presigned_url_com_cache(bucket, chave)
    print(f"Link: {url2}")