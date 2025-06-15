from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional 
import uvicorn
app = FastAPI()

@app.get("/")
def main():
    return {"message": "Hello World"}


@app.get("/blogs/{blog_id}")
def get_blog(blog_id: int):
    return {"blog_id": blog_id, "title": "Sample Blog Title", "content": "This is a sample blog content."}


@app.get("/blogs/{blog_id}/comments")
def get_comments(blog_id: int):
    return {
        "blog_id": blog_id,
        "comments": [
            {"comment_id": 1, "content": "Great blog post!"},
            {"comment_id": 2, "content": "Thanks for sharing!"}
        ]
    }


# dynamic route should be at the end

@app.get("/blogs/")
def get_blogs(published: bool,limit: int = 10):
    if published:
        return {
            "blogs": [
                {"blog_id": 1, "title": "Published Blog 1", "content": "Content of published blog 1"},
                {"blog_id": 2, "title": "Published Blog 2", "content": "Content of published blog 2"}
            ],
            "limit": limit
        }
    return {
        "blogs": [
            {"blog_id": 1, "title": "Blog 1", "content": "Content of blog 1"},
            {"blog_id": 2, "title": "Blog 2", "content": "Content of blog 2"}
        ],
        "limit": limit
    }


#request body example
class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool] 
@app.post("/blogs/")
# def create_blog(request: Blog):
def create_blog(blog: Blog):
    return {
        "message": "Blog created successfully",
        "blog": blog
    }


# debugging
# it only works if you run the file directly and debugging is enabled
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)