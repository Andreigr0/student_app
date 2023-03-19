from pydantic import BaseModel


class ValueSchema(BaseModel):
    id: int
    name: str
