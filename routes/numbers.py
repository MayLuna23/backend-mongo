from fastapi import APIRouter, Depends
from typing import Dict
from schemas.number import (
    NumberCreate, 
    NumbersListResponse, 
    NumberUpdate, 
    StatsResponse
)
from services.numbers import NumberService
from middlewares.auth_middleware import get_current_user

router = APIRouter(prefix="/numbers", tags=["Numbers"])

@router.post("", status_code=201)
async def save_number(
    number: NumberCreate,
    current_user: str = Depends(get_current_user)
) -> Dict:
    """
    Guardar un número para el usuario autenticado
    
    - **value**: Número entero positivo a guardar
    
    Requiere autenticación Bearer Token
    """
    
    result = await NumberService.save_number(current_user, number.value)
    return {
        "message": "Número guardado exitosamente",
        "data": result
    }

@router.get("", response_model=NumbersListResponse)
async def get_numbers(current_user: str = Depends(get_current_user)) -> Dict:
    """
    Obtener todos los números del usuario autenticado
    
    Requiere autenticación Bearer Token
    """
    return await NumberService.get_numbers(current_user)

@router.get("/stats", response_model=StatsResponse)
async def get_stats(current_user: str = Depends(get_current_user)) -> Dict:
    """
    Obtener estadísticas de los números del usuario
    
    Retorna:
    - Total de números
    - Promedio
    - Máximo
    - Mínimo
    
    Requiere autenticación Bearer Token
    """
    return await NumberService.get_stats(current_user)

@router.get("/{number_id}")
async def get_number(
    number_id: str,
    current_user: str = Depends(get_current_user)
) -> Dict:
    """
    Obtener un número específico por ID
    
    - **number_id**: ID del número a consultar
    
    Requiere autenticación Bearer Token
    """
    return await NumberService.get_number_by_id(current_user, number_id)

@router.put("/{number_id}")
async def update_number(
    number_id: str,
    number: NumberUpdate,
    current_user: str = Depends(get_current_user)
) -> Dict:
    """
    Actualizar un número existente
    
    - **number_id**: ID del número a actualizar
    - **value**: Nuevo valor del número
    
    Requiere autenticación Bearer Token
    """
    result = await NumberService.update_number(current_user, number_id, number.value)
    return {
        "message": "Número actualizado exitosamente",
        "data": result
    }

@router.delete("/{number_id}")
async def delete_number(
    number_id: str,
    current_user: str = Depends(get_current_user)
) -> Dict:
    """
    Eliminar un número
    
    - **number_id**: ID del número a eliminar
    
    Requiere autenticación Bearer Token
    """
    return await NumberService.delete_number(current_user, number_id)