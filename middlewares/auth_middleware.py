from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth import verify_token
from config.logger import logger

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Middleware para obtener el usuario actual desde el token JWT
    """
    try:
        token = credentials.credentials
        username = verify_token(token)
        return username
    except HTTPException as e:
        logger.warning(f"Intento de acceso no autorizado")
        raise e
    except Exception as e:
        logger.error(f"Error en middleware de autenticación: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )