from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.get("/")
async def autenticar():
    return {"message": "Voce está autenticado", "autenticado": False}
