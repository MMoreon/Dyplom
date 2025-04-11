from pydantic import BaseModel
from datetime import datetime

class ScreenshotBase(BaseModel):
    file_path: str

class ScreenshotCreate(ScreenshotBase):
    pass

class ScreenshotInDB(ScreenshotBase):
    id: int
    ticket_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True