from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from model.issue_model import Issue, issue_collection, issue_to_dict, Comment
from typing import List
from routes.admin import check_token  


router = APIRouter()

@router.post("/create", response_model=Issue)
async def create_issue(issue: Issue, token: str = Depends(check_token)):
    issue_data = issue.dict()
    result = issue_collection.insert_one(issue_data)
    created_issue = issue_collection.find_one({"_id": result.inserted_id})
    return issue_to_dict(created_issue)

@router.get("/all", response_model=List[Issue])
async def get_all_issues(token: str = Depends(check_token)):
    issues = issue_collection.find()
    return [issue_to_dict(issue) for issue in issues]

@router.get("/location/{location}", response_model=List[Issue])
async def get_issues_by_location(location: str, token: str = Depends(check_token)):
    issues = issue_collection.find({"IssueLocation": location})
    return [issue_to_dict(issue) for issue in issues]

@router.get("/pincode/{pincode}", response_model=List[Issue])
async def get_issues_by_pincode(pincode: str, token: str = Depends(check_token)):
    issues = issue_collection.find({"IssuePincode": pincode})
    return [issue_to_dict(issue) for issue in issues]

@router.get("/status/{status}", response_model=List[Issue])
async def get_issues_by_status(status: str, token: str = Depends(check_token)):
    issues = issue_collection.find({"IssueStatus": status})
    return [issue_to_dict(issue) for issue in issues]

@router.get("/type/{type}", response_model=List[Issue])
async def get_issues_by_type(type: str, token: str = Depends(check_token)):
    issues = issue_collection.find({"IssueType": type})
    return [issue_to_dict(issue) for issue in issues]

@router.get("/{id}", response_model=Issue)
async def get_issue_by_id(id: str, token: str = Depends(check_token)):
    issue = issue_collection.find_one({"_id": ObjectId(id)})
    if issue:
        return issue_to_dict(issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/{id}", response_model=Issue)
async def update_issue(id: str, issue: Issue, token: str = Depends(check_token)):
    updated_issue = issue_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": issue.dict()},
        return_document=True
    )
    if updated_issue:
        return issue_to_dict(updated_issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/{issueid}/{userid}/forward", response_model=Issue)
async def forward_issue(issueid: str, userid: str, token: str = Depends(check_token)):
    issue = issue_collection.find_one({"_id": ObjectId(issueid)})
    if issue:
        if userid not in issue.get("ForwardedByPeople", []):
            issue["ForwardedByPeople"].append(userid)
            updated_issue = issue_collection.find_one_and_update(
                {"_id": ObjectId(issueid)},
                {"$set": {"ForwardedByPeople": issue["ForwardedByPeople"]}},
                return_document=True
            )
            return issue_to_dict(updated_issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.get("/{userid}/use", response_model=List[Issue])
async def get_issues_by_user(userid: str, token: str = Depends(check_token)):
    issues = issue_collection.find({"createdBy": userid})
    return [issue_to_dict(issue) for issue in issues]

@router.put("/{id}/status", response_model=Issue)
async def update_status(id: str, status: str, token: str = Depends(check_token)):
    issue = issue_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"IssueStatus": status}},
        return_document=True
    )
    if issue:
        return issue_to_dict(issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/{id}/spam", response_model=Issue)
async def mark_spam(id: str, token: str = Depends(check_token)):
    issue = issue_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"isSpam": True}},
        return_document=True
    )
    if issue:
        return issue_to_dict(issue)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
