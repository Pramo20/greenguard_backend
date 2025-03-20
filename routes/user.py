from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId
from model.user_model import User, user_collection, user_to_dict
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

@router.post("/create", response_model=User)
async def create_user(user: User):
    user_data = user.dict()
    user_data["authentication"]["password"] = pwd_context.hash(user_data["authentication"]["password"])
    result = user_collection.insert_one(user_data)
    created_user = user_collection.find_one({"_id": result.inserted_id})
    return user_to_dict(created_user)

@router.get("/get_by_username/{username}", response_model=User)
async def get_user_by_username(username: str):
    user = user_collection.find_one({"username": username})
    if user:
        return user_to_dict(user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.get("/get_by_email/{email}", response_model=User)
async def get_user_by_email(email: str):
    user = user_collection.find_one({"email": email})
    if user:
        return user_to_dict(user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.put("/update", response_model=User)
async def update_user(user: User):
    updated_user = user_collection.find_one_and_update(
        {"_id": ObjectId(user.id)},
        {"$set": user.dict()},
        return_document=True
    )
    if updated_user:
        return user_to_dict(updated_user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.get("/generate/{userid}", response_model=User)
async def generate_user(userid: str):
    user = user_collection.find_one({"email": userid})
    if user:
        return user_to_dict(user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/add_issue/{user_id}/{issue_id}", response_model=User)
async def add_issue(user_id: str, issue_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["Issues"].append(ObjectId(issue_id))
        updated_user = user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": {"Issues": user["Issues"]}},
            return_document=True
        )
        return user_to_dict(updated_user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/update_points/{user_id}/{points}", response_model=User)
async def update_points(user_id: str, points: int):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["GreenPoints"] += points
        updated_user = user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": {"GreenPoints": user["GreenPoints"]}},
            return_document=True
        )
        return user_to_dict(updated_user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/login")
async def login(username: str, password: str):
    user = user_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    if not pwd_context.verify(password, user["authentication"]["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return {"message": "Login successful", "user": user_to_dict(user)}