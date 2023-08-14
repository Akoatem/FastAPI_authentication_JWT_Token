from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# to get secret key run this openssl rand -hex 32


SECRET_KET = "1890cf6c075827cd5ca975a3a31a9219173e31acecafc70010e3eddd6f2b54ca"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTE = 4000


# create a database

db = {
    "Peter":{
        "username": "sam20",
        "full_name": "Ako Atem",
        "email": "akoatem@gmail.com",
        "hashed_password": "$2b$12$e/f2Cdr/r2lIX30ODJGqqeiPIdRU4REqzkHoyALUvXSucYEE.YnE6",
        "married": False
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str 
    full_name:str or None = None
    email: str or None = None
    married: bool or None = None
    
class UserInDb(User):
    hashed_password: str
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_schema = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()    

# to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# To get password hash

def get_password_hash(password):
    return pwd_context.hash(password)

# to check user in the database

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDb(**user_data) # ** takes all param in database

# to verify authenticated user
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# create our access token
def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow + expires_delta
    else:
        expire = datetime.utcnow + timedelta(minutes=4000)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KET,algorithm= ALGORITHM)
    return encoded_jwt  # this is our access token

# we write a function of getting our user from access token

async def get_current_user(token: str = Depends(oauth_2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credential", 
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KET, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)  
    except JWTError:
        raise credential_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

# for users who may not be active or disable

async def get_current_active_user(current_user: UserInDb=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code = 400, detail="Inactive user")
    
    return current_user

# we write our token root(endpoint)
# access for login token

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code =status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
        
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRES_MINUTE)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# for authenticated root
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User=Depends(get_current_active_user)):
    return current_user

# for authenticated root and items
@app.get("/users/me/items")
async def read_own_items(current_user: User=Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]


pwd = get_password_hash("monica123")
print(pwd)

       
    
    
    
    
    
    
    
    
    
# class Data(BaseModel):
#     name: str
# # using request method
# @app.post("/create/")
# async def create(data: Data):
#     return {"data": Data}


# # add endpoint
# @app.get("/test/{item_id}")
# async def test(item_id: str, query: int= 1): # we do query and path param
#     return {"hello":  item_id}