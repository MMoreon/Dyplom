from .auth import router as auth_router
from .users import router as users_router
from .tickets import router as tickets_router
from .files import router as files_router

__all__ = ["auth_router", "users_router", "tickets_router", "files_router"]