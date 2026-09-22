from app.core.conf import settings
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")