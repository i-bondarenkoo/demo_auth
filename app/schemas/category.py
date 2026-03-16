from pydantic import BaseModel


class ResponseCategory(BaseModel):
    id: int
    category_type: str
    count_instance: int
