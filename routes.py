from ast import Return
from dotenv import dotenv_values
from fastapi import APIRouter, status, Request, Body
from models import CreateUser
from fastapi.encoders import jsonable_encoder
from deta import Deta

router = APIRouter()

config = dotenv_values(".env")

deta = Deta(config["projectKey"])
db = deta.Base("users")




@router.post("/create_user", response_description="Create a Create user. Requires userName, password, email", status_code=status.HTTP_201_CREATED,)
def createUser(requset: Request, CreateUser: CreateUser = Body(...)):
    checkThisName =  db.fetch(query={"userName":CreateUser.userName})
    
    if checkThisName["items"] == []: #True condition: userName is free.
        respons = db.put(CreateUser)
        return jsonable_encoder(respons["items"])
    else:
        return jsonable_encoder({"Error":"UserName occupied"})