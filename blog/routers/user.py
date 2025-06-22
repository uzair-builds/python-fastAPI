from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from blog.database import get_db
from blog import models
from blog.schemas import ShowUser, User
from blog.repo.user import create_user_repo,get_user_by_id

router= APIRouter(
    tags=["Users"],
    prefix="/user"
)

#Response Model 
@router.post('/',response_model=ShowUser)
def create_user(user:User,db:Session=Depends(get_db)):
    return create_user_repo(user, db)

@router.get("/{id}",response_model=ShowUser)
def get_user(id:int,db:Session=Depends(get_db)):
    return get_user_by_id(id, db)
