from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from database.connection import connect_to_mongo, close_mongo_connection
from routes import auth, numbers
from middlewares.error_handler import validation_exception_handler, general_exception_handler
from config.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    # Startup
    logger.info("Iniciando aplicación...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("Cerrando aplicación...")
    await close_mongo_connection()

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Números con JWT",
    description="API REST para autenticación JWT y gestión de números",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar manejadores de errores
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Incluir rutas
app.include_router(auth.router)
app.include_router(numbers.router)

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud de la API"""
    return {
        "message": "API de Números con JWT",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Verificación de salud del servicio"""
    return {
        "status": "healthy",
        "service": "numbers-api"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor en puerto 8080")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_excludes=["logs/*", "logs/**", "*.log", "__pycache__/*", "*.pyc"]
    )