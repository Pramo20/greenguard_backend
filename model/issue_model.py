from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional
from pydantic import BaseModel

MONGO_URI = "mongodb+srv://admin:greenguardapp@cluster0.glmkok5.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["test"]
issue_collection = db["issue"]


class Comment(BaseModel):
    commenterId: str
    commenterName: Optional[str] = None
    commentText: str
    commentDate: Optional[str] = None


class Issue(BaseModel):
    id: Optional[str] = None
    IssueTitle: str
    IssueDescription: str
    IssueStatus: str = "Pending"
    Views: int = 0
    IssueType: str
    IssueImage: str
    IssueDate: str
    IssueLocation: str
    IssueLatitude: float
    IssueLongitude: float
    IssueContact: Optional[str] = None
    IssuePincode: str
    createdBy: str
    ForwardedByPeople: List[str] = []
    isSpam: bool = False
    comments: List[Comment] = []


def issue_to_dict(issue):
    if issue:
        return Issue(
            id=str(issue["_id"]),
            IssueTitle=issue["IssueTitle"],
            IssueDescription=issue["IssueDescription"],
            IssueStatus=issue["IssueStatus"],
            Views=issue["Views"],
            IssueType=issue["IssueType"],
            IssueImage=issue["IssueImage"],
            IssueDate=issue["IssueDate"],
            IssueLocation=issue["IssueLocation"],
            IssueLatitude=issue["IssueLatitude"],
            IssueLongitude=issue["IssueLongitude"],
            IssueContact=issue.get("IssueContact"),
            IssuePincode=issue["IssuePincode"],
            createdBy=issue["createdBy"],
            ForwardedByPeople=issue.get("ForwardedByPeople", []),
            isSpam=issue.get("isSpam", False),
            comments=[Comment(**comment) for comment in issue.get("comments", [])]
        )
    return None