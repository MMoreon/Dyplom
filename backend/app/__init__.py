from .database import Base, engine, SessionLocal

def init_db():
    from .models import User, Ticket, Comment, Screenshot
    Base.metadata.create_all(bind=engine)