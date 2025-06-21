from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from blog.database import get_db
from blog import models
from blog.schemas import ShowUser, User
from passlib.context import CryptContext


router= APIRouter()

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")
#Response Model 
@router.post('/user',response_model=ShowUser,tags=["users"])
def create_user(user:User,db:Session=Depends(get_db)):
    hashed_password=pwd_cxt.hash(user.password)
    new_user=models.User(name=user.name,email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}",response_model=ShowUser,tags=["users"])
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    return user
