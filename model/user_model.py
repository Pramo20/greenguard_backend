
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional
from pydantic import BaseModel, EmailStr

MONGO_URI = "mongodb+srv://admin:greenguardapp@cluster0.glmkok5.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["test"]
user_collection = db["user"]

class Authentication(BaseModel):
    password: str
    salt: str

class User(BaseModel):
    id: Optional[str] = None
    FirstName: str
    LastName: str
    email: EmailStr
    username: str
    profilePicture: Optional[str] = None
    Issues: List[str] = []
    GreenPoints: int = 0
    clientid: str
    anonymousId: str
    authentication: Authentication


def user_to_dict(user):
    if user:
        return User(
            id=str(user["_id"]),
            FirstName=user["FirstName"],
            LastName=user["LastName"],
            email=user["email"],
            username=user["username"],
            profilePicture=user.get("profilePicture"),
            Issues=[str(issue) for issue in user.get("Issues", [])],
            GreenPoints=user.get("GreenPoints", 0),
            clientid=user["clientid"],
            anonymousId=user["anonymousId"],
            authentication=user["authentication"]
        )
    return None