from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import status 
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from src.accounts.account_services import UserService
from src.chroma_db import get_collection
from src.query.query_service import query_collection , format_context
from src.accounts.models import Users
from src.document.exceptions import InternelServerError
from src.query.schema import RequestQuery
from src.query.llm_connection import rag_chain

query_routes = APIRouter(prefix="/chat")

@query_routes.get("/query", status_code=status.HTTP_200_OK)
async def chat(
    request_query: RequestQuery,
    current_user: Users= Depends(UserService.get_current_user),
    collection = Depends(get_collection)):

    try: 
        query_result = await query_collection(user_id=str(current_user.id),
                                        document_id=request_query.document_id,
                                        query=request_query.query,
                                        collection=collection)
    except: 
        raise InternelServerError("Unable to query VectorDB")
    
    try:
        formated_context = format_context(query_result)
        response= rag_chain.invoke({"context": formated_context , "question" : request_query.query})
        return response
    except Exception as e: 
        raise InternelServerError("Free LLM quota is exceeded.")


