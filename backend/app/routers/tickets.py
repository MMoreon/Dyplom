from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from ..database import get_db
from ..models.ticket import Ticket
from ..models.comment import Comment
from ..models.screenshot import Screenshot
from ..models.user import User
from ..schemas.ticket import TicketCreate, TicketUpdate, TicketInDB
from ..schemas.comment import CommentCreate, CommentInDB
from ..utils.security import get_current_user

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=TicketInDB)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = Ticket(
        user_id=current_user.id,
        title=ticket.title,
        description=ticket.description,
        status="open"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/", response_model=List[TicketInDB])
def read_tickets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "user":
        tickets = db.query(Ticket).filter(Ticket.user_id == current_user.id).offset(skip).limit(limit).all()
    else:
        tickets = db.query(Ticket).offset(skip).limit(limit).all()
    return tickets

@router.post("/{ticket_id}/comments", response_model=CommentInDB)
def add_comment(
    ticket_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = Comment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.post("/{ticket_id}/screenshots")
async def upload_screenshot(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверяем существование заявки
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Сохраняем файл
    file_location = f"{UPLOAD_DIR}/{ticket_id}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    
    # Сохраняем информацию в БД
    db_screenshot = Screenshot(
        ticket_id=ticket_id,
        file_path=file_location
    )
    db.add(db_screenshot)
    db.commit()
    db.refresh(db_screenshot)
    
    return {"filename": file.filename, "ticket_id": ticket_id}