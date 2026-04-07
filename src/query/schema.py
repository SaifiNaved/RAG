from pydantic import BaseModel, Field
from typing import List

class RequestQuery(BaseModel):
    query: str
    document_id: str

class QueryResponse(BaseModel): 
    answer: str = Field(description="The final answer to the user's question")
    confidence_score: float = Field(description="Score from 0-1 on how sure the model is")
    sources: List[int] = Field(description="List of document IDs used to answer")