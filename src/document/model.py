from src.database import Base
from sqlalchemy import Column , Integer , String , DateTime , ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid , datetime
from sqlalchemy.orm import relationship


class Documents (Base) :
    __tablename__ = "documents" 
    id = Column(UUID (as_uuid=True) ,primary_key=True , default=uuid.uuid4)
    bucket_name = Column(String(256) , nullable= False)
    document_name = Column( String(256) , nullable=False)
    document_title = Column(String(256) , nullable= True)
    document_type = Column(String(30) , nullable = False)
    document_path = Column(String , nullable = False)
    status = Column(String(100) , default="Document Uploaded")
    cretaed_at = Column (DateTime , default=datetime.datetime.utcnow)
    user_id = Column(UUID (as_uuid=True) , ForeignKey("users.id") , nullable=False , index=True)
    user = relationship("Users" , back_populates="documents")