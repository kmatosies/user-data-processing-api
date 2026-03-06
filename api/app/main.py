from fastapi import FastAPI
from .core.config import settings
from .db.init_db import init_db
from .routes.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(users_router)

    @app.on_event("startup")
    def on_startup():
        init_db()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
