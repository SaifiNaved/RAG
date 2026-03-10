from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Local_async_session , database_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(url=database_url)
sync_session = sessionmaker(bind=engine , expire_on_commit=False)

async def get_session () :
    session : AsyncSession = Local_async_session()

    try: 
        yield session

    except Exception: 
        await session.rollback()
        raise
    finally : 
        await session.close()

def get_sync_session() : 
    with sync_session() as session : 
        
        try : 
            yield session 
        except Exception : 
            session.rollback()
        finally : 
            session.close()
            