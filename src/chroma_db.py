from src.configs import chroma_settings
from chromadb import CloudClient , AsyncHttpClient

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
    



        