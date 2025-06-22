from fastapi import APIRouter,HTTPException
from blog.schemas import Login
from blog import database,models
from fastapi import Depends
from sqlalchemy.orm import Session
from blog.hashing import Hash
from datetime import timedelta

from blog.token import create_access_token
router=APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)


@router.post("/login")
def login(request:Login ,db: Session= Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    # Here you would typically create a JWT token or session
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    