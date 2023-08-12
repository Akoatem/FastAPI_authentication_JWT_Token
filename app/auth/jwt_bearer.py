# This function is to check out if the request is authorize or not

from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jtw_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)
    
    
    async  def __call__(self, request: Request):
        credentials : HTTPAuthorizationCredentials =  await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.schema == "Bearer":
                raise HTTPException(status_code= 403, detail="invalid or Expire Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code= 403, detail="invalid or Expire Token")
        
    # here is the verify if token is valid
    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False  # this is a fale flag
        payload = decodeJWT(jwtBearer)
        if payload:
            isTokenValid = True # set it to true
        return isTokenValid
         

