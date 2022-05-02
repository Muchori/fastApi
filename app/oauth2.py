from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from . import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "9512212bb10e93449c97db39129920d961470107fb703946f194f51826cd99e17f1f88a3d899cd3cdb85e2564158ad39ce1534742d1ac470e73775a53313d9c4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

##
# creating the the JWT token for  authentication
# ##
def create_access_token(data: dict):
  to_encode = data.copy()

  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})

  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

##
# decoding the tekn and
# Verying the JWT token 
# ##
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


## getting the current user that's logged in

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Beaer"}
  )

  token = verify_access_token(token, credentials_exception) ## verifying the token sent by the jwt

  user = db.query(models.User).filter(models.User.id == token.id).first()

  return user
