import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jtw_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

# create a post of list

posts = [
    {
    "id": 1,
    "title": "penguins",
    "content": "penguins are so beautiful to the core and aquatic birds"
    },
    
    {
    "id": 2,
    "title": "Lion",
    "content": "Lions are the most dangerous animals"
    },
     {
    "id": 3,
    "title": "Elephant",
    "content": "Elephants are the most largest animals ever"
    }
]

users = []
app = FastAPI()

# create a decorator for home page
# this is get for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

# get post
@app.get("/posts",dependencies=[Depends(jwtBearer())], tags=["posts"])
def get_post():
    return {"data": posts}


# get single post by id
@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return{"error": "post with an id does not exist"}
    # check for all posts
    for post in posts:
        if post["id"] == id:
            return{"data": post}

# Post for single blog(handler for creating a post)
@app.post("/posts", tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return{"info": "Post Added"}
    
#5 User sigup [create new user]

@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)  

# To check is a user exist

def user_check(data : UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            return False

# for user login[registered users]
@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema= Body(default=None)):
    if user_check(user):
        return signJWT(user.email)
    else:
        return{
            "error" : "Invalid login details, try again."
        }