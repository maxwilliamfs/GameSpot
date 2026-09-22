from fastapi import APIRouter
from app.core.database import users_collection

auth_routers = APIRouter(prefix="/auth",tags=["Autenticacao"])

@auth_routers.post("/create_account")
async def creat_account(name : str,email : str, password : str):
    dual_user = users_collection.find_one({"email" : email})
    if dual_user is None:
        return {"mensagem" : "erro"}
    else:
        users_collection.insert_one({"name" : name,"email" : email, "password" : password, "cart" : []})
        return {"mensagem" : "sucesso!"}