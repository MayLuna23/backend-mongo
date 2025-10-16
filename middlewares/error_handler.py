from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from config.logger import logger
import traceback

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejo de errores de validación"""

    # 🔹 Limpia los errores para que sean serializables
    clean_errors = []
    for e in exc.errors():
        ctx = e.get("ctx")
        if ctx and "error" in ctx:
            # Convierte el ValueError en texto
            ctx["error"] = str(ctx["error"])
        clean_errors.append(e)

    logger.warning(f"Error de validación: {clean_errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": clean_errors,
        },
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Manejo general de errores"""
    logger.error(f"Error no manejado: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "message": str(exc)
        },
    )