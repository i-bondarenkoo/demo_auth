from pydantic import BaseModel


class ResponseTokenSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"
