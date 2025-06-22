from passlib.context import CryptContext
from blog import models
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

def create_user_repo(user, db):
    hashed_password=pwd_cxt.hash(user.password)
    new_user=models.User(name=user.name,email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(id:int, db:Session):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    return user