from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from config.settings import settings
from config.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Obtener hash de contraseña"""
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str) -> bool:
    """Autenticar usuario predefinido"""
    if username == settings.DEFAULT_USERNAME and password == settings.DEFAULT_PASSWORD:
        logger.info(f"Usuario {username} autenticado exitosamente")
        return True
    logger.warning(f"Intento de autenticación fallido para usuario: {username}")
    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.info(f"Token creado para usuario: {data.get('sub')}")
    return encoded_jwt

def verify_token(token: str) -> str:
    """Verificar y decodificar token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token sin username")
            raise credentials_exception
        return username
    except JWTError as e:
        logger.error(f"Error verificando token: {e}")
        raise credentials_exception