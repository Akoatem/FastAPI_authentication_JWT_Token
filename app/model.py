from pydantic import BaseModel, EmailStr, Field

# create a class

class PostSchema(BaseModel):
    id: int= Field(default=None)
    title: str= Field(default=None)
    content: str= Field(default=None)
    # create a subclass
    class Config:
        scema_extra = {
            "post_demo":{
                "title": "some title about animals",
                "content": "some content about animals"
            }
        }

class UserSchema(BaseModel):
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    
    class Config:
        the_schema = {
            "name" : "Ako",
            "email" : "akoatem2003@gmail.com",
            "password" : "123"
        }
        
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    
    class Config:
        the_schema = {
            "email" : "akoatem2003@gmail.com",
            "password" : "123"
        }