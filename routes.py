from ast import Return
from distutils.log import Log
from http.client import HTTPException, responses
from urllib import response
from xxlimited import new
from dotenv import dotenv_values
from fastapi import APIRouter, status, Request, HTTPException
from passlib.hash import pbkdf2_sha256 

from fastapi.encoders import jsonable_encoder
from deta import Deta

from models import CreateUser, Login

router = APIRouter()

config = dotenv_values(".env")

deta = Deta(config["projectKey"])
db = deta.Base("users")




@router.post("/create_user", response_description="Create a Create user. Requires userName, password, email", status_code=status.HTTP_201_CREATED)
def createUser(requset: Request, newUser: CreateUser):
    try:
        checkThisName =  jsonable_encoder(db.fetch(query={"userName":newUser.userName}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No connection to database")

    if checkThisName["_count"] > 0:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="User already exists")
    response = jsonable_encoder(db.put({
        "userName":newUser.userName,
        "password":pbkdf2_sha256.hash(newUser.password),
        "email":newUser.email
    }))
    return {"key":response["key"],"userName":newUser.userName,"email":newUser.email}



@router.post("/login",response_description="Login with userName and password", status_code=status.HTTP_202_ACCEPTED)
def login(request:Request, credentials: Login):
    try:
        userLoginInfo =  jsonable_encoder(db.fetch(query={"userName":credentials.userName}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No connection to database")

    if userLoginInfo["_count"] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    userInfo = userLoginInfo["_items"][0]
    if pbkdf2_sha256.verify(credentials.password,userLoginInfo["_items"][0]["password"]):
        return {"login":True,"item":{"key":userInfo["key"],"userName":userInfo["userName"],"email":userInfo["email"]}}
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password incorrect")