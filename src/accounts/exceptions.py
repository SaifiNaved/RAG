from src.base_exception import AppException

class UserDoesNotExistException(AppException) : 
    def __init__(self, perm : str):
        self.perm = perm
        super().__init__(f"User does not exist with {perm}") 

class UserAlreadyAxistException(AppException) : 
    def __init__(self , perm : str) : 
        self.perm = perm
        super().__init__(f"User already exist with {perm}")

class InvalidCredentialsException(AppException) : 
    def __init__(self ) : 
        super().__init__(f"Invalid Credentails")
   
class CredentialsException (AppException) : 
    def __init__(self):
        super().__init__(f"Credential Exception : Could not validate credentials")

class TokenExpire (AppException): 
    def __init__(self):
        super().__init__("Authentication Token expired")