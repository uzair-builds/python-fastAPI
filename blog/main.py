from fastapi import FastAPI,Depends,status,Response,HTTPException
from .schemas import Blog,User,ShowUser
from . import models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
app= FastAPI()

models.Base.metadata.create_all(engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog",status_code=status.HTTP_201_CREATED)
def ceate_blog(blog:Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=blog.title,body=blog.content,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blogs")
def get_blogs(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}",status_code=status.HTTP_200_OK)
def get_blog(id:int,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    return blog


#response code and exception 
@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted successfully"

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    print(request)
    blog.update({
    "title": request.title,
    "body": request.content,
    })

    # blog.update(request.dict())
    # blog.update(request)
    db.commit()
    return "Blog updated successfully"




pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")
#Response Model 
@app.post('/user',response_model=ShowUser,tags=["users"])
def create_user(user:User,db:Session=Depends(get_db)):
    hashed_password=pwd_cxt.hash(user.password)
    new_user=models.User(name=user.name,email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}",response_model=ShowUser,tags=["users"])
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    return user



#Relationships

