

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os 
from dotenv import load_dotenv
from src.chroma_db import get_chroma_client
from chromadb.utils.embedding_functions import GoogleGenaiEmbeddingFunction
from src.configs import llm_settings , chroma_settings

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

async def get_collection (chroma_client) : 
    try : 
        collection = None
        collection = await chroma_client.get_or_create_collection(
                name=chroma_settings.collection,
                embedding_function = GoogleGenaiEmbeddingFunction(
                    api_key_env_var="LLM_API_KEY",
                    model_name=llm_settings.embedding_model
                )
            )
        return collection
    except Exception as e : 
        raise RuntimeError(f"Failed to get collection ")
    

async def add_embeddings(documents : list[Document] , collection, user_id: str , document_id: str) : 
        try:
            docs = []
            docs_id = []
            page_no = 1
            for item in documents : 
                docs.append(item.page_content)
                docs_id.append(f"{document_id}_{page_no}")
                page_no+=1
                print(page_no)
            await collection.add(
                    ids= docs_id, 
                    documents=docs,
                    metadatas=[{"user_id": user_id, "document_id": document_id}] * len(docs)
                )
        except Exception as e : 
            raise RuntimeError (f"Failed to store embeddings ")


async def process_doc(file_path: str , user_id: str, document_id: str , chroma_client ) : 
        loaded_document = load_document(file_path)
        print(loaded_document[0].page_content)
        chunked_document = chunk_document(loaded_document)
        #(f"************Chunk length {len(chunk_document)}****************")
        #chroma_client =await get_chroma_client()
        coll = await get_collection(chroma_client)
        await add_embeddings(chunked_document , coll , user_id=user_id , document_id=document_id)