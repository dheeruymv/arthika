from pydantic import BaseModel, Field



class NewUser(BaseModel):
    username: str
    password: str = Field(..., min_length=10, repr=False, example="mypassword")
    email: str


class Login(BaseModel):
    username: str
    password: str = Field(..., min_length=10, repr=False, example="mypassword")