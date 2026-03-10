
from src.database import engine
from src.database import Base

async def init_db() : 
    async with engine.begin() as conn : 
        await conn.run_sync(Base.metadata.create_all)