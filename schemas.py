from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: str | None = None
    description: str | None = None

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True