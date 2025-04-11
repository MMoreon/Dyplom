from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .user import UserInDB

class TicketBase(BaseModel):
    title: str
    description: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TicketInDB(TicketBase):
    id: int
    status: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserInDB

    class Config:
        from_attributes = True