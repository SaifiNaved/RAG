from sqlalchemy.ext.asyncio import AsyncSession
from src.accounts.schemas import Register_User , Login_user
from sqlalchemy import select
from fastapi import Depends
from src.util import get_session
from src.accounts.models import Users
from src.accounts.exceptions import *
from src.accounts.utilities import hash_password , verify_password , create_access_token , access_token_expire_time , seret_key , algorithm
from datetime import datetime , timedelta , timezone
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError , ExpiredSignatureError
import jwt


class UserService () :
    
    oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
    
    @staticmethod
    async def register_user(db : AsyncSession , user : Register_User) :

        result =await db.execute(select(Users).where(Users.email == user.email))

        if result.scalar_one_or_none() : 
            raise UserAlreadyAxistException(user.email)
        
        if not user.username : 
            username = user.email.split('@')
            user.username = username[0]
        result = await db.execute(select(Users).where(Users.username == user.username))

        if result.scalar_one_or_none() : 
            raise UserAlreadyAxistException(user.username)
        

        hashed_password = hash_password(user.password)

        new_user = Users(email=user.email , password= hashed_password , username = user.username)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    
    @staticmethod
    async def login_user(db : AsyncSession , user : Login_user):

        if user.email: 
            result =await db.execute(select(Users).where(Users.email == user.email))
            found_user = result.scalar_one_or_none()
            if not found_user : 
                raise UserDoesNotExistException(user.email)

            if not verify_password (user.password ,found_user.password) : 
                raise InvalidCredentialsException()
            
            access_token = create_access_token( 
                data= {"sub" : found_user.email} , 
                expire_delta= timedelta(minutes = access_token_expire_time) )
            
            return {"access_token" : access_token ,
                    "token_type" : "bearer"}
        
        else : 
            result =await db.execute(select(Users).where(Users.username == user.username))
            found_user= result.scalar_one_or_none()

            if not found_user : 
                raise UserDoesNotExistException(user.username)
            
            if not verify_password (user.password ,found_user.password) : 
                raise InvalidCredentialsException()
            
            access_token = create_access_token( 
                data= {"sub" : found_user.username} , 
                expire_delta= timedelta(minutes = access_token_expire_time) )
            
            return {"access_token" : access_token ,
                    "token_type" : "bearer"}
            
        
    @staticmethod
    async def get_user_by_email (email : str , db : AsyncSession) :

        user = await db.execute(select(Users).where(Users.email == email))
        
        found_user = user.scalar_one_or_none()

        if not found_user : 
            raise UserDoesNotExistException(f"email : {email}")
        return found_user
    
    @staticmethod
    async def get_user_by_username (username : str , db : AsyncSession) :

        user = await db.execute(select(Users).where(Users.username == username))
        
        found_user = user.scalar_one_or_none()

        if not found_user : 
            raise UserDoesNotExistException(f"username : {username}")
        return found_user
    
    @staticmethod
    async def get_current_user ( db : AsyncSession = Depends(get_session), token : str = Depends(oauth_scheme)) :  
        
        try : 
            payload = jwt.decode(token , seret_key ,algorithms= [algorithm])
            identifier : str = payload.get('sub')
            exp: int = payload.get("exp")
            if not identifier : 
                raise InvalidCredentialsException
        except ExpiredSignatureError : 
                raise TokenExpire
        except InvalidTokenError:
            raise CredentialsException

        if "@" in identifier : 
            user = await UserService.get_user_by_email(email=identifier , db=db)

        else : 
            user = await UserService.get_user_by_username(username= identifier , db = db)
        print (user)
        return user