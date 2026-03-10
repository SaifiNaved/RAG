from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
import os 
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
load_dotenv()

database_url = os.getenv("DATABASE_URL")

class Base (DeclarativeBase) : 
    pass 


engine = create_async_engine(database_url , echo=True)


Local_async_session = sessionmaker(bind=engine , class_=AsyncSession , expire_on_commit=False)



