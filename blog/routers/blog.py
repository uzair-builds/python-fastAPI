from fastapi import APIRouter, Depends, HTTPException, Response,status
from sqlalchemy.orm import Session
from blog.database import get_db
from blog import models
from blog.schemas import Blog, ShowBlog
from typing import List
from blog.repo.blog import get_all_blogs,get_blog_by_id,create_blog,delete_blog_repo,update_blog_repo

router= APIRouter(
    tags=["Blogs"],
    prefix="/blog"
)

@router.get("/",response_model=List[ShowBlog],status_code=status.HTTP_200_OK)
def get_blogs(db:Session=Depends(get_db)):
    return get_all_blogs(db)

@router.post("/",status_code=status.HTTP_201_CREATED)
def ceate_blog(blog:Blog,db:Session=Depends(get_db)):
    return create_blog(blog, db)

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=ShowBlog)
def get_blog(id:int,response:Response,db:Session=Depends(get_db)):
    return get_blog_by_id(id, db)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session=Depends(get_db)):
   return delete_blog_repo(id, db)

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:Blog,db:Session=Depends(get_db)):
    return update_blog_repo(id, request, db)
