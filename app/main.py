from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.views.user import router as user_router
from app.auth.views import router as auth_router
from app.views.product import router as product_router
from app.views.category import router as category_router
from app.views.access_rule import router as access_rule_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(access_rule_router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_run_cfg.host,
        port=settings.server_run_cfg.port,
        reload=settings.server_run_cfg.reload,
    )
