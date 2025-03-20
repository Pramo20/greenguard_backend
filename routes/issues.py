from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId
from model.issue_model import Issue, issue_collection, issue_to_dict, Comment
from typing import List

router = APIRouter()

@router.post("/create", response_model=Issue)
async def create_issue(issue: Issue):
    issue_data = issue.dict()
    result = issue_collection.insert_one(issue_data)
    created_issue = issue_collection.find_one({"_id": result.inserted_id})
    return issue_to_dict(created_issue)

@router.get("/get_all", response_model=List[Issue])
async def get_all_issues():
    issues = issue_collection.find()
    return [issue_to_dict(issue) for issue in issues]

@router.get("/get_by_id/{id}", response_model=Issue)
async def get_issue_by_id(id: str):
    issue = issue_collection.find_one({"_id": ObjectId(id)})
    if issue:
        return issue_to_dict(issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/update/{id}", response_model=Issue)
async def update_issue(id: str, issue: Issue):
    updated_issue = issue_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": issue.dict()},
        return_document=True
    )
    if updated_issue:
        return issue_to_dict(updated_issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.delete("/delete/{id}")
async def delete_issue(id: str):
    result = issue_collection.find_one_and_delete({"_id": ObjectId(id)})
    if result:
        return {"message": "Issue deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.get("/get_by_pincode/{pincode}", response_model=List[Issue])
async def get_issues_by_pincode(pincode: str):
    issues = issue_collection.find({"IssuePincode": pincode})
    return [issue_to_dict(issue) for issue in issues]

@router.get("/get_by_location/{location}", response_model=List[Issue])
async def get_issues_by_location(location: str):
    issues = issue_collection.find({"IssueLocation": location})
    return [issue_to_dict(issue) for issue in issues]

@router.get("/get_by_type/{type}", response_model=List[Issue])
async def get_issues_by_type(type: str):
    issues = issue_collection.find({"IssueType": type})
    return [issue_to_dict(issue) for issue in issues]

@router.get("/get_by_status/{status}", response_model=List[Issue])
async def get_issues_by_status(status: str):
    issues = issue_collection.find({"IssueStatus": status})
    return [issue_to_dict(issue) for issue in issues]

@router.put("/update_status/{id}/{status}", response_model=Issue)
async def update_status(id: str, status: str):
    issue = issue_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"IssueStatus": status}},
        return_document=True
    )
    if issue:
        return issue_to_dict(issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.get("/get_by_user/{userid}", response_model=List[Issue])
async def get_issues_by_user(userid: str):
    issues = issue_collection.find({"createdBy": userid})
    return [issue_to_dict(issue) for issue in issues]

@router.post("/forward/{id}/{userid}", response_model=Issue)
async def forward_issue(id: str, userid: str):
    issue = issue_collection.find_one({"_id": ObjectId(id)})
    if issue:
        if userid not in issue["ForwardedByPeople"]:
            issue["ForwardedByPeople"].append(userid)
            updated_issue = issue_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": {"ForwardedByPeople": issue["ForwardedByPeople"]}},
                return_document=True
            )
            return issue_to_dict(updated_issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.post("/mark_spam/{id}", response_model=Issue)
async def mark_spam(id: str):
    issue = issue_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"isSpam": True}},
        return_document=True
    )
    if issue:
        return issue_to_dict(issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.post("/add_comment/{id}", response_model=Issue)
async def add_comment(id: str, comment: Comment):
    issue = issue_collection.find_one({"_id": ObjectId(id)})
    if issue:
        comment.commentDate = str(comment.commentDate or "")
        issue["comments"].append(comment.dict())
        updated_issue = issue_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {"comments": issue["comments"]}},
            return_document=True
        )
        return issue_to_dict(updated_issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")