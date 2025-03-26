from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from model.user_model import User, user_collection, user_to_dict
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Route to create a user
@router.post("/user", response_model=User)
async def create_user(user: User):
    user_data = user.dict()
    user_data["authentication"]["password"] = pwd_context.hash(user_data["authentication"]["password"])
    result = user_collection.insert_one(user_data)
    created_user = user_collection.find_one({"_id": result.inserted_id})
    return user_to_dict(created_user)

# Route to log in and generate a JWT (for now, returns a success message)
@router.post("/login")
async def login(username: str, password: str):
    user = user_collection.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["authentication"]["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return {"message": "Login successful", "user": user_to_dict(user)}

# Route to get a user by username (authentication check can be added later)
@router.get("/user/{username}", response_model=User)
async def get_user(username: str):
    user = user_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_to_dict(user)

# Route to update a user (authentication check can be added later)
@router.put("/user", response_model=User)
async def update_user(user: User):
    updated_user = user_collection.find_one_and_update(
        {"_id": ObjectId(user.id)},
        {"$set": user.dict()},
        return_document=True
    )
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_to_dict(updated_user)
