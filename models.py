from pydantic import BaseModel

class CreateUser(BaseModel):
    userName: str
    password: str
    email: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "userName": "KalleAnka",
                "password": "aStrongPassword",
                "email": "kalleanka@example.com",
            }
        }