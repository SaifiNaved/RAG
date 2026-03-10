from minio import Minio 
from dotenv import load_dotenv
import os , json , uuid
from pathlib import Path
from src.document.exceptions import *
from fastapi import UploadFile , Depends
from minio.error import S3Error
from src.accounts.account_services import UserService
from src.accounts.models import Users
from sqlalchemy.ext.asyncio import AsyncSession
from src.document.model import Documents
from minio.helpers import ObjectWriteResult
from src.util import get_session

load_dotenv() 
#S3 configuration perameters 
S3_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
S3_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD") 
S3_ENDPOINT =  os.getenv("MINIO_SERVICE_ENDPOINT")
BUCKET_NAME = os.getenv("BUCKET_NAME")
PROJECT_PATH = Path(__file__).resolve().parents[2]
POLICY_PATH = PROJECT_PATH / "policy.json"
PART_SIZE = int(os.getenv("PART_SIZE"))
ALLOWED_SIZE = int(os.getenv("ALLOWED_SIZE"))
STAGING_DIR = os.getenv("STAGING_DIR")

# Upload File validation related perameters

ALLOWED_TYPES = { "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain" }

minio = Minio(endpoint=S3_ENDPOINT , access_key=S3_ACCESS_KEY , secret_key=S3_SECRET_KEY , secure=False)

# Method to ensure the bucket is created if not exist and policies are implemented.
def ensure_bucket_and_policy():
    if not minio.bucket_exists(BUCKET_NAME):
        minio.make_bucket(BUCKET_NAME)

    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        policy = json.load(f)

    minio.set_bucket_policy(BUCKET_NAME, json.dumps(policy))

class DocumentServices () : 

    def __init__ (self) : 
        pass 
    
    async def create_metadata (self, file:UploadFile ,result : ObjectWriteResult ,user : Users , db : AsyncSession) :
        doc_metadata = Documents(
            bucket_name = result.bucket_name ,
            document_name = result.object_name , 
            document_title = file.filename,
            document_type = file.content_type,
            document_path = f"{S3_ENDPOINT}/{result.bucket_name}/{result.object_name}",
            user_id = user.id
        )
        db.add(doc_metadata)
        await db.commit()
        await db.refresh(doc_metadata)
        return doc_metadata


    async def create_doc(self , file :UploadFile ) :
        if file.content_type not in ALLOWED_TYPES :
            raise UnsupportedFileType 

        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)
        if file.size > ALLOWED_SIZE :
            raise ContentTooLarge
        
        try : 
            doc_metadata = minio.put_object(
                BUCKET_NAME ,
                object_name=f"{uuid.uuid4()}_{file.filename}" ,
                data=file.file,
                length=-1 ,
                content_type=file.content_type,
                part_size=PART_SIZE)
                
            return doc_metadata


        except S3Error as e : 
            raise InternelServerError("Fail to store the document")
        
    
    def get_document (self , bucket_name : str , object_name : str):
        
        os.makedirs(STAGING_DIR, exist_ok=True)
        file_path = os.path.join(STAGING_DIR , object_name)
        try :
            minio.fget_object(bucket_name , object_name , file_path) 
            return file_path
        except Exception as e : 
            raise InternelServerError("Fail to process the document, unable to download from object storage")
    



