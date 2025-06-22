from sqlalchemy.orm import Session
from blog import models
from fastapi import HTTPException, status
def get_all_blogs(db:Session):
    return db.query(models.Blog).all()

def get_blog_by_id(id:int, db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    return blog


def create_blog(blog, db:Session):
    new_blog=models.Blog(title=blog.title,body=blog.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



def delete_blog_repo(id:int, db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted successfully"

def update_blog_repo(id:int, request, db:Session):
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

