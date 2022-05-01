from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "4V1TRf69AVjXfUynSp2SO3flAZueqRvWBSG4zT1pLDG5rl9eDnqRkDKVnINWqE09"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
  to_encode = data.copy()

  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})

  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    id: str = payload.get("id")

    if id is None:
      raise credentials_exception

    token_data = schemas.TokeData(id = id)
  except JWTError:
    raise credentials_exception

  return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Beaer"}
  )

  return verify_access_token(token, credentials_exception)
