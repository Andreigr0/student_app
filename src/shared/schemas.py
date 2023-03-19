from pydantic import BaseModel


class ValueSchema(BaseModel):
    id: int
    name: str


class FileSchema(BaseModel):
    name: str
    url: str
