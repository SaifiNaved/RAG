
from pwdlib import PasswordHash
import os , jwt 
from dotenv import load_dotenv
from datetime import datetime , timedelta
from fastapi.security import OAuth2PasswordBearer



load_dotenv()
seret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_time = int (os.getenv("ACCESS_TOKEN_EXPIRE_TIME"))

password_hash = PasswordHash.recommended()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password (plain_password : str) -> str : 
    return password_hash.hash(plain_password)

def verify_password (plain_password : str , hash : str) : 
    return password_hash.verify(plain_password , hash)

def create_access_token (data : dict , expire_delta : timedelta | None = None ) :
    to_encode = data.copy()
    if expire_delta : 
        expire = datetime.utcnow() + expire_delta
    else : 
        expire = datetime.utcnow() + timedelta(minutes = access_token_expire_time)

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode , seret_key , algorithm )  
    return encoded_jwt

"""
async def get_current_user ( db : AsyncSession = Depends(get_session), token : str = Depends(oauth_scheme)) :  
        
    try : 
        payload = jwt.decode(token , seret_key ,algorithms= [algorithm])
        identifier : str = payload.get('sub')
        if not identifier : 
            raise CredentialsException
        
    except PyJWTError:
        raise CredentialsException

    if "@" in identifier : 
        user = await UserService.get_user_by_email(email=identifier , db=db)

    else : 
        user = await UserService.get_user_by_username(username= identifier , db = db)

    return user

"""