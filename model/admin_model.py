from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional
from pydantic import BaseModel
from passlib.context import CryptContext

MONGO_URI = "mongodb+srv://admin:greenguardapp@cluster0.glmkok5.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["your_database_name"]
admin_collection = db["admin"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Admin Schema
class Authentication(BaseModel):
    password: str
    salt: str

class Admin(BaseModel):
    id: Optional[str] = None
    username: str
    authentication: Authentication
    PlaceOfService: str
    Areas: List[int]
    city: str
    state: str
    role: str


def admin_to_dict(admin):
    if admin:
        return Admin(
            id=str(admin["_id"]),
            username=admin["username"],
            authentication=Authentication(
                password=admin["authentication"]["password"],
                salt=admin["authentication"]["salt"]
            ),
            PlaceOfService=admin["PlaceOfService"],
            Areas=admin["Areas"],
            city=admin["city"],
            state=admin["state"],
            role=admin["role"]
        )
    return None

# Hash password
def hash_password(password: str) -> (str, str):
    salt = pwd_context.hash(password)
    return salt, salt