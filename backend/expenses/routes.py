from fastapi import APIRouter, HTTPException, status, Depends, Path, Query
from models.expense import ExpenseCreate, ExpenseResponse
from database import get_collection
from utils.jwt import get_current_user
from datetime import datetime, timezone
from bson import ObjectId
from typing import List, Optional

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

@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    user_id: str = Depends(get_current_user),
    category: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
    ):
    expenses_collection = get_collection("expenses")

    query = {"user_id": user_id}

    if category:
        query["category"]=category
    if from_date or to_date:
        query["date"] = {}
        if from_date:
            query["date"]["$gte"]=from_date
        if to_date:
            query["date"]["$lte"]=to_date
    
    cursor = expenses_collection.find(query).skip(skip).limit(limit)
    expenses = []

    async for doc in cursor:
        expenses.append(ExpenseResponse(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            title=doc["title"],
            amount=doc["amount"],
            date=doc["date"],
            category=doc["category"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"]
        ))
    
    return expenses

@router.get("/summary")
async def get_summary(
    user_id: str = Depends(get_current_user),
    category: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None)
):
    expense_collection = get_collection("expenses")

    query = {"user_id": user_id}

    if category:
        query["category"]=category
    if from_date or to_date:
        query["date"] = {}
        if from_date:
            query["date"]["$gte"]=from_date
        if to_date:
            query["date"]["$lte"]=to_date

    pipeline = [
        {"$match": query},
        {"$group":{
            "_id": None,
            "total_spent": {"$sum": "$amount"}
        }}
    ]

    result = await expense_collection.aggregate(pipeline).to_list(length=1)

    return {"total_spent": result[0]["total_spent"] if result else 0}


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str = Path(...),
    updated_expense: ExpenseCreate = Depends(), 
    user_id: str = Depends(get_current_user)
):
    expenses_collection = get_collection("expenses")

    existing = await expenses_collection.find_one(
        {"_id": ObjectId(expense_id), 
         "user_id": user_id}
    )

    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    now = datetime.now(timezone.utc)

    updated_data = {
        "$set": {
            "title": updated_expense.title,
            "amount": updated_expense.amount,
            "date": updated_expense.date,
            "category": updated_expense.category,
            "updated_at": now
        }
    }

    await expenses_collection.update_one(
        {"_id": ObjectId(expense_id), "user_id": user_id},
        updated_data
    )

    return ExpenseResponse(
        id=str(expense_id),
        user_id=user_id,
        title=updated_expense.title,
        amount=updated_expense.amount,
        date=updated_expense.date,
        category=updated_expense.category,
        created_at=existing["created_at"],
        updated_at=now
    )

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: str = Path(...),
    user_id: str = Depends(get_current_user)
):
    expense_collection = get_collection("expenses")

    result = await expense_collection.delete_one({
        "_id": ObjectId(expense_id),
        "user_id": user_id
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    return None

    
    
    
    