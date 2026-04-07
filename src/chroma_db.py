from src.configs import chroma_settings, llm_settings
from chromadb import CloudClient , AsyncHttpClient
from chromadb.utils.embedding_functions import ChromaCloudSpladeEmbeddingFunction, GoogleGenaiEmbeddingFunction
from chromadb import SparseVectorIndexConfig, VectorIndexConfig, Schema, K


chroma_client = None
async def get_chroma_client() : 
    try :
        global chroma_client
        if chroma_client == None :  
            chroma_client =await AsyncHttpClient(
                host=chroma_settings.host,
                ssl=True,
                tenant=chroma_settings.tenant,
                database=chroma_settings.database,
                headers= {'x-chroma-token': chroma_settings.api_key}
            )
        return chroma_client
    except Exception as e :    
        raise RuntimeError(f"Fail to connect to chroma cloude ")
    


def create_collection_schema() :
    schema = Schema()
    sparse_ef = ChromaCloudSpladeEmbeddingFunction()
    schema.create_index(
        config=SparseVectorIndexConfig(
            source_key=K.DOCUMENT,
            embedding_function=sparse_ef
        ),
        key="sparse_embedding"
    )
    schema.create_index(
        config=VectorIndexConfig(
            source_key=K.DOCUMENT,
            embedding_function=GoogleGenaiEmbeddingFunction(
                api_key_env_var="GOOGLE_API_KEY",
                model_name=llm_settings.embedding_model
            )
        )
    )
    return schema
        
collection = None

async def get_collection () : 
    global collection
    try : 
        if collection == None:
            await get_chroma_client()
            schema = create_collection_schema()
            collection =await chroma_client.get_or_create_collection(
                name=chroma_settings.collection,
                schema=schema
                #embedding_function = GoogleGenaiEmbeddingFunction(
                #    api_key_env_var="LLM_API_KEY",
                #    model_name=llm_settings.embedding_model
                #)
            )
        return collection
    except Exception as e : 
        raise RuntimeError(f"Failed to get collection")