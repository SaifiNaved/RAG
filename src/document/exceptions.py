from src.base_exception import AppException

class UnsupportedFileType (AppException) :
    def __init__(self):
        super().__init__("Unsupported file type")  


class ContentTooLarge (AppException) : 
    def __init__(self):
        super().__init__("File size too large")

class InternelServerError(AppException) : 
    def __init__(self , param):
        self.param = param
        super().__init__(f"{param}") 

