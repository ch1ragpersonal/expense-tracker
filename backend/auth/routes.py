from fastapi import APIRouter, HTTPException, status
from models.user import UserCreate, UserResponse, UserLogin
from utils.crypto import hash_password, verify_password
from database import get_collection
from datetime import datetime
from bson import ObjectId
from utils.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    user_collection = get_collection("users")
    existing_user = await user_collection.find_one({
        "$or": [
            {"email": user.email},
            {"username": user.username}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or Email already registered")
    
    hashed_password = hash_password(user.password)

    now = datetime.now()

    user_dict = {
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "created_at": now,
        "updated_at": now
    }

    result = await user_collection.insert_one(user_dict)

    return UserResponse(
        id=str(result.inserted_id),
        name=user.name,
        username=user.username,
        email=user.email,
        created_at=now,
        updated_at=now
    )

@router.post("/login")
async def login(user: UserLogin):
    user_collection = get_collection("users")
    existing_user = await user_collection.find_one({
        "$or": [
            {"email": user.login},
            {"username": user.login}
        ]
    })
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(existing_user["_id"])})

    response_user = {
        "id": str(existing_user["_id"]),
        "name": existing_user["name"],
        "username": existing_user["username"],
        "email": existing_user["email"],
    }

    return {
        "user": response_user,
        "access_token": access_token,
    }
    



