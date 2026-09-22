from app.core.database import users_collection
from passlib.context import CryptContext

async def create(name : str, email : str, password : str):
    dual_user = await users_collection.find_one({"email": email})

    if dual_user is None:
        await users_collection.insert_one({"name": name, "email": email, "password": password, "cart": []})
        return {"mensagem": "sucesso!"}
    else:
        return {"mensagem": "erro"}