from pydantic import BaseModel


class ResponseProduct(BaseModel):
    id: int
    name: str
    price: int


class PatchProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
