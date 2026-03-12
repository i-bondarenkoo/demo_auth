from pydantic_settings import BaseSettings
from pydantic import BaseModel


class ServerRunCfg(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@localhost:5437/demo_auth"
    db_echo: bool = True
    server_run_cfg: ServerRunCfg = ServerRunCfg()


settings = Settings()
