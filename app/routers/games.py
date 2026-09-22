from fastapi import APIRouter
from app.core.database import games_collection

games_router = APIRouter(prefix="/games",tags=["Busca de Jogos"])
