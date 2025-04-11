from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.ticket import Ticket
from ..models.screenshot import Screenshot
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/tickets/{ticket_id}/screenshots")
async def upload_screenshot(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Проверка существования тикета
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Сохранение файла
    file_location = f"{UPLOAD_DIR}/{ticket_id}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    
    # Сохранение в БД
    db_screenshot = Screenshot(
        ticket_id=ticket_id,
        file_path=file_location
    )
    db.add(db_screenshot)
    db.commit()
    db.refresh(db_screenshot)
    
    return {"filename": file.filename, "ticket_id": ticket_id}