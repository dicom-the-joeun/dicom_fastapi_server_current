import os
from typing import Union
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError, jwt
from starlette import status

load_dotenv("./app/.env")
ACCESS_TOKEN_EXPIRES_MIN =  os.environ.get('ACCESS_TOKEN_EXPIRES_MIN')
REFRESH_TOKEN_EXPIRES_MIN =  os.environ.get('REFRESH_TOKEN_EXPIRES_MIN')
ALGORLITHM = os.environ.get('ALGORLITHM')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_REFRESH_KEY = os.environ.get('JWT_REFRESH_KEY')

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def create_access_token(subject: Union[str, any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRES_MIN))
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORLITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_EXPIRES_MIN))
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_KEY, ALGORLITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORLITHM)
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    return id

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, JWT_REFRESH_KEY, algorithms=ALGORLITHM)
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    return id