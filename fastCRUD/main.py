from fastapi import FastAPI, HTTPException, status,Query,Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
from databse import db
from bson import ObjectId

app = FastAPI()

class Post(BaseModel):
    _id:Optional[ObjectId]
    title:str
    content:str
    published:bool = True
    ratings: Optional[int] = None


posts = [
    {"title":"Post 1", "content": "Hey, this is going to be the first post", "published":False,"ratings":4},
    {"title":"Post 2", "content": "Hey, this is going to be the secong post", "ratings":2}
]

@app.get('/', status_code=status.HTTP_200_OK)
async def getHome():
    return "Hey! successfully running"

@app.get('/posts', status_code=status.HTTP_200_OK)
async def getPosts(latest: bool = False):
    posts_collection = db.posts.find()
    posts_list = []

    for post in posts_collection:
        # Convert ObjectId to string for serialization
        post['_id'] = str(post['_id'])
        posts_list.append(post)

    if latest:
        return {"data": posts_list}
    else:
        return {"data": posts_list[::-1]} 
    

@app.post('/posts',status_code=status.HTTP_201_CREATED)
async def addPost(post:Post):
    postsCollection = db.posts
    post_dict = post.dict()
    post_dict['id']= randrange(0,10000)
    result = postsCollection.insert_one(post_dict)
    return {'message': 'Post created successfully', 'id': str(result.inserted_id)}


@app.patch('/posts/{id}', status_code=status.HTTP_200_OK)
async def updatePost(id: str, post: Post):
    postId = ObjectId(id)
    existing_post = db.posts.find_one({"_id": postId})

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

    # Update only the fields that are provided in the request
    updated_fields = {}

    if post.title:
        updated_fields['title'] = post.title

    if post.content:
        updated_fields['content'] = post.content

    if post.published is not None:
        updated_fields['published'] = post.published

    if post.ratings is not None:
        updated_fields['ratings'] = post.ratings

    # Perform the update in the database
    db.posts.update_one({"_id": postId}, {"$set": updated_fields})

    return {"message": "Post updated successfully"}

@app.delete('/posts/{id}', status_code=status.HTTP_200_OK)
async def deletePost(id: str):
    postId = ObjectId(id)
    res = db.posts.delete_one({"_id": postId})

    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

    return {"message": "Post deleted successfully"}
