from chromadb import Knn, Rrf, Search, K
from src.chroma_db import get_collection




def create_hybrid_rank_query (query:str):
    hybrid_rank_query = Rrf(
        ranks=[
            Knn(query=query, return_rank=True),
            Knn(query=query, key="sparse_embedding", return_rank=True)
        ],
        weights=[0.5, 0.5],  # 50% semantic, 50% keyword
        k=60
    )
    return hybrid_rank_query

def get_search_query(user_id: str, document_id: str, hybrid_rank_query):
    search = (Search().where((K("user_id") == user_id) & (K("document_id") == document_id)).rank(hybrid_rank_query).limit(10).select(K.DOCUMENT, K.SCORE))
    return search

async def query_collection (user_id: str , document_id: str, query: str, collection) :
    hybrid_query = create_hybrid_rank_query(query)
    search_query = get_search_query(user_id, document_id, hybrid_query)
    result = await collection.search(search_query)
    result_rows = result.rows()[0]

    return result_rows 

def format_context(query_result):
    formatted_result = []                     
    
    for i, item in enumerate(query_result, 1): 
        formatted_result.append(f"[{i}] {item['document'].strip()}")
    
    return "\n\n".join(formatted_result)
