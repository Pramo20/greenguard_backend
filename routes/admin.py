from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId
from model.admin_model import Admin, admin_collection, admin_to_dict, hash_password, pwd_context
from model.issue_model import issue_collection
from typing import List

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

SECRET_KEY = "jsonwebhelloworld"  
ALGORITHM = "HS256"

def check_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


router = APIRouter()

@router.post("/admin", response_model=Admin)
async def create_admin(admin: Admin):
    salt, hashed_password = hash_password(admin.authentication.password)
    admin_data = admin.dict()
    admin_data["authentication"]["password"] = hashed_password
    admin_data["authentication"]["salt"] = salt

    result = admin_collection.insert_one(admin_data)
    created_admin = admin_collection.find_one({"_id": result.inserted_id})
    return admin_to_dict(created_admin)

@router.get("/admin/{id}", response_model=Admin)
async def get_admin(id: str):
    admin = admin_collection.find_one({"_id": ObjectId(id)})
    if admin:
        return admin_to_dict(admin)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")


@router.get("/admin/username/{username}", response_model=Admin)
async def get_admin_by_username(username: str):
    admin = admin_collection.find_one({"username": username})
    if admin:
        return admin_to_dict(admin)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")


@router.put("/admin/{id}", response_model=Admin)
async def update_admin(id: str, admin: Admin):
    updated_admin = admin_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": admin.dict()},
        return_document=True
    )
    if updated_admin:
        return admin_to_dict(updated_admin)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

# Admin login
@router.post("/admin/login")
async def login_admin(username: str, password: str):
    admin = admin_collection.find_one({"username": username})
    if not admin or not pwd_context.verify(password, admin["authentication"]["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return admin_to_dict(admin)

# Get issues assigned to an admin's area
@router.get("/admin/issues/{id}", response_model=List)
async def get_admin_area_issues(id: str):
    admin = admin_collection.find_one({"_id": ObjectId(id)})
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    issues = issue_collection.find({"IssuePincode": {"$in": admin["Areas"]}})
    return [issue for issue in issues]
