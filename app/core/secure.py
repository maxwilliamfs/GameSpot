from bson import ObjectId
from passlib.context import CryptContext
from app.core.database import users_collection
from app.core.conf import settings
from jose import jwt, JWTError
from app.core.enums import TokenTypesEnum
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
OAuth2Schema = OAuth2PasswordBearer(tokenUrl="/auth/loginOAuth2")

async def verify_token(token : str = Depends(OAuth2Schema)):
    try:
        dic_info = jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="ERRO: Access Blocked!!!")
    user = await users_collection.find_one({"_id" : ObjectId(dic_info.get("sub"))})
    if dic_info.get("type") != TokenTypesEnum.Access_Token.value:
        raise HTTPException(status_code=401, detail="ERRO: Invalid User!!!")
    if user is None:
        raise HTTPException(status_code=401,detail="ERRO: Invalid User!!!")
    return user

async def verify_refresh_token(token : str = Depends(OAuth2Schema)):
    try:
        dic_info = jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="ERRO: Access Blocked!!!")
    user = await users_collection.find_one({"_id" : ObjectId(dic_info.get("sub"))})
    if dic_info.get("type") != TokenTypesEnum.Refresh_Token.value:
        raise HTTPException(status_code=401, detail="ERRO: Invalid User!!!")
    if user is None:
        raise HTTPException(status_code=401,detail="ERRO: Invalid User!!!")
    return user

async def verify_admin(user : dict = Depends(verify_token)):
    if user.get("admin"):
        return user
    else:
        raise HTTPException(status_code=403,detail="ERRO: Access Blocked!!!")