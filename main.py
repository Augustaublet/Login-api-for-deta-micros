from fastapi import FastAPI
from routes import router as  createUser # login,
from deta import Deta



app = FastAPI()




#app.include_router(login,tags=["login"], prefix="/login")
app.include_router(createUser,tags=["create_user"], prefix="")