"""

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from src.main import app
from src.accounts.exceptions import *
from src.document.exceptions import *




@app.exception_handler(UserAlreadyAxistException)
async def user_already_exist_handler (request: Request , exc : UserAlreadyAxistException) : 
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT , 
        content={"error" : "User Already Exist" , "message" : f"User Already exist with {exc.perm}"}
    )

@app.exception_handler(UserDoesNotExistException)
async def user_doesnot_exist_handler(request : Request , exc : UserDoesNotExistException) : 
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND , 
        content={
            "error" : "User Does not Exist" , 
            "message" : f"User Does not exist with {exc.perm}"
        }
    )

@app.exception_handler(InvalidCredentialsException)
async def invalid_credential_handler( request : Request , exc : InvalidCredentialsException) : 
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST , 
        content={
            "error" : "Invalid Credentials" , 
            "message" : "Invalid Credentials"
        }
    )

@app.exception_handler(CredentialsException)
async def credentials_exception_handler ( request : Request , exc : CredentialsException) : 
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED , 
        content={
            "error" : "Could not validate credentials" , 
        } ,
        headers={"WWW-Authenticate": "Bearer"}
    )
@app.exception_handler(TokenExpire)
async def credentials_exception_handler ( request : Request , exc : TokenExpire) : 
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED , 
        content={
            "error" :"Token has expired" ,
            "message" : "Token has expired" 
        } ,
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.exception_handler(UnsupportedFileType)
async def unsupported_file_type (request : Request , exc : UnsupportedFileType):
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
        content={
            "error" : "Unsupported media type" , 
            "message" : "Unsupported file type supports only .pdf, .docx"
        }
    )

@app.exception_handler(ContentTooLarge)
async def unsupported_file_type (request : Request , exc : ContentTooLarge):
    return JSONResponse(
        status_code=status.HTTP_413_CONTENT_TOO_LARGE, 
        content={
            "error" : "File size too large" ,
            "message" : "Uploaded file is too large, should not be greater then 25Mb"
        }
    )

@app.exception_handler(ObjectStorageRelatedError)
async def internal_server_error(request : Request , exc : ObjectStorageRelatedError) : 
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , 
        content={
            "error" : "Internal server error" ,
            "message" : "Not able to upload file to object storage"
        }
    )

    """