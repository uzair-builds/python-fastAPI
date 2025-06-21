from fastapi import APIRouter, Depends, HTTPException, Response,status
from sqlalchemy.orm import Session
from blog.database import get_db
from blog import models
from blog.schemas import Blog, ShowBlog
from typing import List


router= APIRouter()

@router.get("/blogs",response_model=List[ShowBlog],status_code=status.HTTP_200_OK)
def get_blogs(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@router.post("/blog",status_code=status.HTTP_201_CREATED)
def ceate_blog(blog:Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=blog.title,body=blog.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/blog/{id}",status_code=status.HTTP_200_OK,response_model=ShowBlog)
def get_blog(id:int,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    return blog

@router.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted successfully"

@router.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    print(request)
    blog.update({
    "title": request.title,
    "body": request.body,
    })

    # blog.update(request.dict())
    # blog.update(request)
    db.commit()
    return "Blog updated successfully"
