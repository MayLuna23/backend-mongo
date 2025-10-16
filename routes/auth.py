from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from schemas.user import LoginRequest, Token
from services.auth import authenticate_user, create_access_token
from config.settings import settings
from config.logger import logger

router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(user: LoginRequest):
    """
    Endpoint de autenticación
    
    - **username**: Nombre de usuario (admin)
    - **password**: Contraseña (1234)
    
    Retorna un token JWT válido por 15 minutos
    """
    if not authenticate_user(user.username, user.password):
        logger.warning(f"Intento de login fallido para usuario: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": "admin"}, expires_delta=access_token_expires
    )
    
    logger.info(f"Login exitoso para usuario: {user.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }