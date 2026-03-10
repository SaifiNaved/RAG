"""

from celery import Celery
from kombu import Queue
from src.configs import background_task_settings
from src.chroma_db import get_chroma_client
from celery.signals import worker_process_init
from src.configs import chroma_settings
from chromadb import CloudClient



celery_app = Celery("worker",
                     broker=background_task_settings.message_broker,
                     backend=background_task_settings.task_result )

celery_app.conf.task_queue = (
    Queue('document_queue')
)

celery_app.conf.task_routes = {
    "src.backgroundtask.tasks.main" : {"queue" : "document_queue"}    
}


celery_app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1
)

chroma_client = None
@worker_process_init.connect
def init_chroma_client():
    try :
        global chroma_client
        if chroma_client == None :  
            chroma_client = CloudClient(
                tenant=chroma_settings.tenant,
                database=chroma_settings.database,
                api_key=chroma_settings.api_key
            )
        
    except Exception as e : 
        raise RuntimeError(f"Fail to connect to chroma cloude {e}")
    
def get_chroma_client():
    global chroma_client
    return chroma_client

"""