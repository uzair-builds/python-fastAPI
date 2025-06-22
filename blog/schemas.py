from pydantic import BaseModel
from typing import Optional,List
class BlogBase(BaseModel):
    title: str
    body: str
    
    # published: Optional[bool] = True
class Blog(BlogBase):
    class Config():
        # orm_mode = True
        from_attributes = True 

class User(BaseModel):
    name: str
    email: str 
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []  # Using forward reference for ShowBlog
    class Config():
        # orm_mode = True
        from_attributes = True 


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        # orm_mode = True
        from_attributes = True 


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # email: Optional[str] = None
    username: Optional[str] = None