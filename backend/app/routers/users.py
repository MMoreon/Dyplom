from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils.security import get_current_active_user, get_password_hash
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserInDB

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка существования пользователя
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Создание пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/me/", response_model=UserInDB)
def read_current_user(
    current_user: User = Depends(get_current_active_user)
):
    # Убедимся, что все обязательные поля присутствуют
    if not hasattr(current_user, 'is_active'):
        current_user.is_active = True
    if not hasattr(current_user, 'role'):
        current_user.role = "user"
    
    return current_user