
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.query.schema import QueryResponse

parser = PydanticOutputParser(pydantic_object=QueryResponse)

prompt = ChatPromptTemplate.from_template(
    """You are a helpful assistant. Use the following context to answer the question.
    If you don't know the answer, say you don't know.
    
    Context: {context}
    
    Question: {question}
    
    {format_instructions}""",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

