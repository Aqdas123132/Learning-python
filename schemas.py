from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    name: str
    email: str
    department: str
    marks: float
    status: str
    description: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    marks: Optional[float] = None
    status: Optional[str] = None
    description: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    class Config:
        from_attributes = True