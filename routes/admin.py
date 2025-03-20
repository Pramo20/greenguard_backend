from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from model.admin_model import Admin, admin_collection, admin_to_dict, hash_password, pwd_context
from model.issue_model import issue_collection
from typing import List

router = APIRouter()

@router.post("/create", response_model=Admin)
async def create_admin(admin: Admin):
    salt, hashed_password = hash_password(admin.authentication.password)
    admin_data = admin.dict()
    admin_data["authentication"]["password"] = hashed_password
    admin_data["authentication"]["salt"] = salt

    result = admin_collection.insert_one(admin_data)
    created_admin = admin_collection.find_one({"_id": result.inserted_id})
    return admin_to_dict(created_admin)

@router.put("/update/{id}", response_model=Admin)
async def update_admin(id: str, admin: Admin):
    updated_admin = admin_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": admin.dict()},
        return_document=True
    )
    if updated_admin:
        return admin_to_dict(updated_admin)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

@router.delete("/delete/{id}")
async def delete_admin(id: str):
    result = admin_collection.find_one_and_delete({"_id": ObjectId(id)})
    if result:
        return {"message": "Admin deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

@router.get("/get/{id}", response_model=Admin)
async def get_admin(id: str):
    admin = admin_collection.find_one({"_id": ObjectId(id)})
    if admin:
        return admin_to_dict(admin)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

@router.get("/get_by_username/{username}", response_model=Admin)
async def get_admin_by_username(username: str):
    admin = admin_collection.find_one({"username": username})
    if admin:
        return admin_to_dict(admin)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

@router.post("/login")
async def login_admin(username: str, password: str):
    admin = admin_collection.find_one({"username": username})
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")

    is_password_correct = pwd_context.verify(password, admin["authentication"]["password"])
    if not is_password_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return admin_to_dict(admin)

@router.get("/get_issues/{id}", response_model=List)
async def get_admin_area_issues(id: str):
    admin = admin_collection.find_one({"_id": ObjectId(id)})
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    issues = issue_collection.find({"IssuePincode": {"$in": admin["Areas"]}})
    return [issue for issue in issues]