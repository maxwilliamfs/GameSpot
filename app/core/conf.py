from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URL = os.getenv("MONGO_URL","mongodb://localhost:27017")
    SECRET_KEY = os.getenv("SECRET_KEY","aleatory_secret_-key")
    DATABASE_NAME = os.getenv("DATABASE_NAME","gamespot_db")
settings = Settings()


