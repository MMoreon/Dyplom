from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from .database import engine, Base
from .routers import auth_router, users_router, tickets_router, files_router

# Сначала инициализируем oauth2_scheme (должен быть доступен для роутеров)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Ticket System API",
    description="API для системы учета заявок",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
    # Настройки безопасности для Swagger UI
    swagger_ui_init_oauth={
        "clientId": "swagger-ui",
        "usePkceWithAuthorizationCodeGrant": True,
        "scopes": ""
    }
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Импорт моделей для создания таблиц
from .models import user, ticket, comment, screenshot  # noqa: F401
Base.metadata.create_all(bind=engine)

# Подключение роутеров
app.include_router(
    auth_router,
    tags=["Authentication"]
)
app.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(oauth2_scheme)]  # Защищаем все endpoints в роутере
)
app.include_router(
    tickets_router,
    prefix="/tickets",
    tags=["Tickets"],
    dependencies=[Depends(oauth2_scheme)]
)
app.include_router(
    files_router,
    prefix="/files",
    tags=["Files"],
    dependencies=[Depends(oauth2_scheme)]
)

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Приветствую в системе учета заявок"}