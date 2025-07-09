from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ExpenseBase(BaseModel):
    title: str
    amount: float
    date: datetime
    category: str

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True