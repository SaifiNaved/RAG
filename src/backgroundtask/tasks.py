
"""

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os 
from dotenv import load_dotenv
from src.backgroundtask.worker import get_chroma_client
from chromadb.utils.embedding_functions import GoogleGenaiEmbeddingFunction
from src.configs import llm_settings , chroma_settings
from src.backgroundtask.worker import celery_app
load_dotenv()

CHUNKSIZE = int(os.getenv("CHUNKSIZE"))
CHUNKOVERLAP = int(os.getenv("CHUNKOVERLAP"))


def load_document( document_path : str ) : 
    loader = PDFPlumberLoader(file_path=document_path)
    loaded_doc = loader.load()
    return loaded_doc

def chunk_document(documents: list[Document]) : 
    splitter = RecursiveCharacterTextSplitter( chunk_size = CHUNKSIZE , chunk_overlap = CHUNKOVERLAP , add_start_index= True)
    chunks = splitter.split_documents(documents=documents) 
    return chunks

def get_collection (chroma_client) : 
    try : 
        collection = chroma_client.get_or_create_collection(
            name=chroma_settings.collection,
            embedding_function = GoogleGenaiEmbeddingFunction(
                api_key_env_var="LLM_API_KEY",
                model_name=llm_settings.embedding_model
            )
        )
        return collection
    except Exception as e : 
        raise RuntimeError(f"Failed to get collection {e}")
    

def add_embeddings(documents : list[Document] , collection) : 
    try:
        docs = []
        docs_id = []
        start = 1
        for item in documents : 
            docs.append(item.page_content)
            docs_id.append(str(start))
            start+=1
            print(start)
        collection.add(
            ids= docs_id, 
            documents=docs
        )
    except Exception as e : 
        raise RuntimeError (f"Failed to store embeddings {e}")

@celery_app.task(bind=True, autoretry_for=[Exception], retry_kwargs={'max_retries': 3} )
def main(metadata : dict) : 
    loaded_document = load_document(metadata["file_path"])
    chunked_document = chunk_document(loaded_document)
    chroma_client = get_chroma_client()
    coll = get_collection(chroma_client)
    add_embeddings(chunked_document , coll)

"""