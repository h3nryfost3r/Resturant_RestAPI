from pydantic import BaseModel

class Group(BaseModel):
    title: str
    description: str

class Item(BaseModel):
    title: str
    description: str
    price: float