# This file is reponsible for signing, encoding, decoding  and returning JTWs

import time
import jwt
from decouple import config 


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# This function returns generated token
def token_response(token: str):
    return{
        "access token" : token
    }

# This function use for signing JWT string
def signJWT(userID : str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token : str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {
            
        }