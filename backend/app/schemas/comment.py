from pydantic import BaseModel
from datetime import datetime
from .user import UserInDB

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    id: int
    user_id: int
    ticket_id: int
    created_at: datetime
    user: UserInDB

    class Config:
        from_attributes = True