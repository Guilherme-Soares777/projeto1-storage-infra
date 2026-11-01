# 🚀 Cloud Storage & Caching Architecture (AWS Simulation)

Projeto prático de arquitetura de nuvem simulando serviços essenciais da AWS (**Amazon S3, Amazon RDS e Amazon ElastiCache**) em ambiente local utilizando **Docker**, **Python (Boto3)** e **Valkey**.

---

## 🏛️ Mapeamento da Arquitetura

| Serviço Local | Equivalente AWS | Papel na Arquitetura |
| :--- | :--- | :--- |
| **MinIO** | **Amazon S3** | Armazenamento de objetos (Bucket, Upload, Download, Presigned URLs). |
| **PostgreSQL** | **Amazon RDS (PostgreSQL)** | Persistência de metadados relacionais dos arquivos. |
| **Valkey** | **Amazon ElastiCache (Redis)** | Cache em memória para URLs pré-assinadas com redução de latência. |

---

## 🛠️ Recursos Implementados

- **Ingestão no S3 via SDK Boto3:** Manipulação programática de buckets e objetos.
- **Segurança com Presigned URLs:** Geração de links efémeros com tempo de expiração (TTL) para leitura segura de arquivos privados.
- **Persistência Relacional de Metadados:** Gravação de logs de upload no PostgreSQL (nome, caminho S3, tamanho em bytes e timestamp).
- **Estratégia de Caching (Cache Hit / Cache Miss):** Armazenamento de Presigned URLs no Valkey em memória para evitar requisições repetitivas à API do S3.
- **Isolamento e Segurança (DevSecOps):** Gestão de credenciais via variáveis de ambiente (`.env`).

---

## 🔧 Como Executar o Projeto

### 1. Clonar o repositório e subir a infraestrutura
```bash
git clone [https://github.com/SEU-USUARIO/projeto1-storage-infra.git](https://github.com/SEU-USUARIO/projeto1-storage-infra.git)
cd projeto1-storage-infra
docker compose up -d