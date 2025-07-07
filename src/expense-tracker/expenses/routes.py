from fastapi import APIRouter, HTTPException, status, Depends
from models.expense import ExpenseCreate, ExpenseResponse
from database import get_collection
from utils.jwt import get_current_user
from datetime import datetime, timezone
from bson import ObjectId

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/me")
async def get_my_expenses(user_id: str = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user_id": user_id
    }

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreate, user_id: str = Depends(get_current_user)):
    expenses_collection = get_collection("expenses")
    now = datetime.now(timezone.utc)

    expenses_doc = {
        "user_id": user_id,
        "title": expense.title,
        "amount": expense.amount,
        "date": expense.date,
        "category": expense.category,
        "created_at": now,
        "updated_at": now
    }

    result = await expenses_collection.insert_one(expenses_doc)

    return ExpenseResponse(
        id=str(result.inserted_id),
        user_id=user_id,
        title=expense.title,
        amount=expense.amount,
        date=expense.date,
        category=expense.category,
        created_at=now,
        updated_at=now
    )