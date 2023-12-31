from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import os


app = FastAPI()
model.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    id: int
    title: str
    content : str
    user_id : int

class UserBase(BaseModel):
    id: int
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dp_dependency = Annotated[Session,Depends(get_db)]

stop_words = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
    'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by',
    'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "dont", 'should', "shouldve", 'now', 'd', 'll',
    'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didnt", 'doesn', "doesnt", 'hadn', "hadnt",
    'hasn', "hasn't", 'haven', "havent", 'isn', "isnt", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "neednt", 'shan',
    "shan't", 'shouldn', "shouldnt", 'wasn', "wasnt", 'weren', "werent", 'won', "wont", 'wouldn', "wouldnt","the"
])

def remove_stop_words(input_string):
    words = input_string.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

@app.post("/users/")
def creat_user(user:UserBase, db:dp_dependency):
    response_id = db.query(model.User).filter(model.User.id==user.id).first()
    response_name = db.query(model.User).filter(model.User.username==user.username).first()
    if response_id is None:
        if response_name is None:
            db_user = model.User(**user.dict())
            db.add(db_user)
            db.commit()
            return "User Created"
        else:
            return "UserName Alredy in Use"
    else:
        return "Please use another userid"

@app.get("/user/{user_id}")
def read_user(user_id:int, db:dp_dependency):
    user = db.query(model.User).filter(model.User.id==user_id).first()
    if user is None:
        return "User Not Found!"
    return user

@app.put("/update-user-name/{user_id}")
def update_user(user_id: int, new_name:str, db:dp_dependency):
    user = db.query(model.User).filter(model.User.id==user_id).first()
    if user is None:
        return "User Not Found!"
    user.username = new_name
    db.commit()
    return "Username updated!"

@app.post("/posts/")
def create_post(post:PostBase, db:dp_dependency):
    db_post = model.Post(**post.dict())
    user = db.query(model.User).filter(model.User.id==db_post.user_id).first()
    if user is None:
        return "User does not exits!"
    db.add(db_post)
    db.commit()
    return "Post Created"

@app.delete("/user/{user_id}")
def delete_user(user_id:int, db:dp_dependency):
    db_user = db.query(model.User).filter(model.User.id==user_id).first()
    if db_user is None:
        return "User Not Found!"
    db.delete(db_user)
    db.commit()
    return "User Deleted."

@app.get("/posts/{post_id}")
def read_post(post_id:int, db:dp_dependency):
    post = db.query(model.Post).filter(model.Post.id == post_id).first()
    if post is None:
        return "Post Not Found!"
    return post


@app.delete("/delete_posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id:int,db:dp_dependency):
    db_post = db.query(model.Post).filter(model.Post.id==post_id).first()
    if db_post is None:
        return "Post Not Found!"
    db.delete(db_post)
    db.commit()
    return "Post Deleted"

@app.get("/post-cloud/")
def post_cloud(db:dp_dependency):
    # query = text("SELECT GROUP_CONCAT(CONCAT(title, ', ') SEPARATOR '') FROM posts")
    # titles_string = db.execute(query).scalar().lower()
    #
    # titles_without_stop_words = remove_stop_words(titles_string)
    #
    # return {"concatenated_titles_without_stop_words": titles_without_stop_words}

    titles = db.query(model.Post.title).all()

    # Extract titles from the result
    titles_list = [title[0] for title in titles]

    # Concatenate titles using ', ' separator
    titles_string = ', '.join(titles_list).lower()

    # Assuming remove_stop_words is a function that removes stop words
    titles_without_stop_words = remove_stop_words(titles_string)

    return {"concatenated_titles_without_stop_words": titles_without_stop_words}
