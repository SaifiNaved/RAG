from fastapi import APIRouter, status , Depends
from src.accounts.schemas import Register_User , Login_user , Token , ResponseRegisterUser
from sqlalchemy.ext.asyncio import AsyncSession
from src.util import get_session
from src.accounts.models import Users
from src.accounts.account_services import UserService

user_router = APIRouter(prefix="/users" , tags=["User ferature"])

@user_router.post('/register' , status_code=status.HTTP_201_CREATED , response_model=ResponseRegisterUser)
async def user_register(user : Register_User , session :AsyncSession = Depends(get_session) ) :
    new_user = await UserService.register_user(session , user= user)
    resp = ResponseRegisterUser(
        email = new_user.email ,
        username=new_user.username ,
        created_at= new_user.created_at ,
        profile_url = new_user.profile_photo_url)
    return resp


@user_router.post("/login" , status_code=status.HTTP_200_OK , response_model=Token)
async def user_login(user :Login_user , session : AsyncSession = Depends(get_session)) :

    token = await UserService.login_user(session , user)
    return token 

@user_router.get("/me")
async def get_profile(current_user: Users = Depends(UserService.get_current_user)):
    return current_user
