from pydantic_settings import BaseSettings
from pydantic import BaseModel


class ServerRunCfg(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True


class AuthJWT(BaseModel):
    algorithm: str = "HS256"
    key: str = "bb5c7496947f8ffef547ab2dbc12936b9bdba8f8413bfc8479373077d9880690"
    # access_token_expire_minutes: int = 2
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@localhost:5437/demo_auth"
    db_echo: bool = True
    server_run_cfg: ServerRunCfg = ServerRunCfg()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
