from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())