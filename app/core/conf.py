from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URL = os.getenv("MONGO_URL","mongodb://localhost:27017")
    SECRET_KEY = os.getenv("SECRET_KEY","aleatory_secret_-key")
    DATABASE_NAME = os.getenv("DATABASE_NAME","gamespot_db")
    ALGORITHM = os.getenv("ALGORITHM","HS256")
    ACESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACESS_TOKEN_EXPIRE_MINUTES","30")
settings = Settings()


