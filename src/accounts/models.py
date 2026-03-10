from sqlalchemy import Column , Integer , String , Boolean , DateTime
from src.database import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Users(Base) : 
    __tablename__= "users"
    id = Column(UUID(as_uuid=True), primary_key=True , default=uuid.uuid4)
    email = Column(String(100), nullable=False , unique=True )
    password = Column (String(255), nullable=False)
    username = Column(String(100) , nullable=True , unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile_photo_url = Column(String , nullable=True)
    documents = relationship("Documents" , back_populates="user" , cascade="all, delete-orphan")
    #is_active = Column(Boolean , default=False)