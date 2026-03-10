🚀 Modular RAG Pipeline: Document Intelligence & Embedding Service
This project is a production-grade backend service designed for secure document management and automated AI embedding pipelines. It features a modular architecture to handle user authentication, cloud-native object storage, and vector database synchronization.

# 🛠️ Tech Stack
Backend: FastAPI (Python) 
Security: JWT Authentication & Authorization 
AI Orchestration: LangChain & Google Gemini Pro 
Vector Database: ChromaDB (Cloud Hosted) 
Object Storage: MinIO (Dockerized) 
Database: PostgreSQL (User & Metadata)

# ✨ Key Features
Secure User Management: Full registration and login flow secured by JWT tokens and Access Control.
Automated Ingestion: A "Fetch-and-Process" workflow that automatically triggers document processing upon upload.
Smart Chunking: Utilizes LangChain for intelligent text splitting and Google Gemini for high-dimensional vector embeddings.
Hybrid Storage: Combines local Dockerized MinIO for raw files with ChromaDB Cloud for searchable embeddings and Postgre for user & metadata.

# ⚙️ Setup & Installation

## 1. Clone the Repository

```
git clone https://github.com/SaifiNaved/RAG
cd RAG
```

## 2. Configure Environment Variables

```
# Database & Security
POSTGRES_URL=your_postgresql_url
ALGORITHM=HS256
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_TIME=30

# MinIO Configuration
MINIO_USER=minio_admin
MINIO_PASSWORD=minio_password
MINIO_SERVICE_ENDPOINT=localhost:9000
BUCKET_NAME=documents

# File & Staging
PART_SIZE=5242880
ALLOWED_SIZE=10485760
STAGING_DIR=./temp_staging

# LangChain & AI
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
LLM_API_KEY=your_google_gemini_key
EMBEDDING_MODEL=models/embedding-001

# ChromaDB Cloud
CHROMA_HOST=your_chroma_cloud_host
CHROMA_API_KEY=your_chroma_api_key
TENANT=default
DATABASE=default
COLLECTION=document_embeddings
```

## 3. Spin up Infrastructure

```
docker-compose up -d
```

## 4. Run the Application

```
pip install -r requirements.txt
uvicorn main:app --reload
```

# 🏗️ Architecture FlowAuth:
1 Auth: User logs in and receives a JWT.
2 Upload: User uploads a document via the Document Service.
3 Storage: File is stored in MinIO and metadata is saved in PostgreSQL.
4 Pipeline: The system automatically fetches the file to the STAGING_DIR, chunks it using LangChain, and generates embeddings via Google Gemini.
5 Sync: Vectors are persisted in ChromaDB Cloud for future retrieval.
