from langchain.chat_models import init_chat_model
from src.configs import llm_settings
from src.query.prompt import prompt , parser 

llm = init_chat_model(
    model=llm_settings.generation_model,
    model_provider="google_genai",
    temperature=0.7,
    max_retries=3,          # number of retries
    request_timeout=60
    
)

rag_chain = (prompt | llm | parser)

