from pydantic import BaseModel , EmailStr , field_validator , model_validator 
import re
class Register_User (BaseModel) : 
    email : EmailStr 
    password : str
    username : str | None = None


    @field_validator("password")
    @classmethod
    def validate_password (cls , password : str) : 

        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit")
        
        # Require at least one special character (non-alphanumeric)
        if not re.search(r"[^a-zA-Z0-9]", password):
            raise ValueError("Password must contain at least one special character")
        
        # Optional: enforce minimum length
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        return password
    
    @field_validator("username")
    @classmethod
    def validate_username (cls , username : str) : 

        if len(username) >100 : 
            raise ValueError ("Username can not be over 100 character ")

        if '@' in username : 
            raise ValueError("Username can not consist '@' ")
        return username
    
class Login_user (BaseModel) : 
    email : EmailStr | None =None
    username : str | None = None
    password : str

    @model_validator(mode="after")
    @classmethod
    def email_or_username (cls , value) : 
        if (not value.email) and (not value.username) : 
            raise ValueError("Either email or username should be present")
        return value
    

class Token(BaseModel):
    access_token: str
    token_type: str

class ResponseRegisterUser(BaseModel): 
    email : EmailStr 
    username : str 
    created_at : str
    profile_url :str