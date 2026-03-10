from dotenv import load_dotenv
import os

load_dotenv()

class Chroma_Settings(): 
    api_key :str= os.getenv("CHROMA_API_KEY")
    tenant : str = os.getenv("TENANT")
    database : str = os.getenv("DATABASE")
    collection : str = os.getenv("COLLECTION")
    host : str = os.getenv("HOST")

chroma_settings = Chroma_Settings()

class LLM_Settings() : 
    llm_api_key: str = os.getenv("LLM_API_KEY")
    embedding_model = os.getenv("EMBEDDING_MODEL")
llm_settings = LLM_Settings()

class Background_Task_Settings(): 
    message_broker : str = os.getenv("MESSAGE_BROKER_URL")
    task_result : str = os.getenv("BG_TASK_RESULTS")
background_task_settings = Background_Task_Settings() 