from fastapi import UploadFile , File ,  status , Depends
from fastapi.routing import APIRouter 
from src.accounts.account_services import UserService
from src.document.exceptions import *
from src.document.doc_services import DocumentServices , ALLOWED_SIZE
from src.accounts.models import Users
from sqlalchemy.ext.asyncio import AsyncSession
from src.util import get_session
from src.document.document_processing import process_doc
from fastapi.requests import Request
from src.chroma_db import get_chroma_client
from src.document.exceptions import *

doc_routes = APIRouter(prefix="/docs")

ALLOWED_SIZE = ALLOWED_SIZE
ALLOWED_TYPES = { "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain" }

@doc_routes.post("/uploadfile" , status_code=status.HTTP_201_CREATED)
async def upload_file(
    request : Request,
    file : UploadFile = File(...),
    chroma_client = Depends(get_chroma_client),
    document_services : DocumentServices= Depends(DocumentServices) ,
    current_user : Users = Depends(UserService.get_current_user) ,
    db : AsyncSession = Depends(get_session)  ) :
        try : 
            result = await document_services.create_doc(file)
            #result = await document_services.create_metadata(file , result , current_user , db=db)
            file_path = document_services.get_document(result.bucket_name , result.object_name)
            result = await document_services.create_metadata(file , result , current_user , db=db)
            await process_doc(file_path , str(current_user.id), str(result.document_name), chroma_client)
            return result
        except Exception as e : 
              raise InternelServerError("Fail to process document")
        
        