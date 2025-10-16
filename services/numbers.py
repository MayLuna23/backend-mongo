from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
from fastapi import HTTPException, status
from database.connection import get_database
from config.logger import logger

class NumberService:
    
    @staticmethod
    async def save_number(username: str, value: int) -> Dict:
        """Guardar un número para un usuario"""
        try:
            db = get_database()
            collection = db["numbers"]
            
            number_doc = {
                "username": username,
                "value": value,
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            
            result = await collection.insert_one(number_doc)
            logger.info(f"Número {value} guardado para usuario {username}")
            
            return {
                "id": str(result.inserted_id),
                "username": username,
                "value": value,
                "created_at": number_doc["created_at"]
            }
        except Exception as e:
            logger.error(f"Error guardando número: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error guardando el número"
            )
    
    @staticmethod
    async def get_numbers(username: str) -> Dict:
        """Obtener todos los números de un usuario"""
        try:
            db = get_database()
            collection = db["numbers"]
            
            cursor = collection.find({"username": username}).sort("created_at", -1)
            numbers = await cursor.to_list(length=None)
            
            numbers_list = [
                {
                    "id": str(num["_id"]),
                    "value": num["value"],
                    "created_at": num["created_at"]
                }
                for num in numbers
            ]
            
            logger.info(f"Obtenidos {len(numbers_list)} números para usuario {username}")
            
            return {
                "username": username,
                "numbers": numbers_list
            }
        except Exception as e:
            logger.error(f"Error obteniendo números: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error obteniendo los números"
            )
    
    @staticmethod
    async def get_number_by_id(username: str, number_id: str) -> Dict:
        """Obtener un número específico por ID"""
        try:
            db = get_database()
            collection = db["numbers"]
            
            if not ObjectId.is_valid(number_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID inválido"
                )
            
            number = await collection.find_one({
                "_id": ObjectId(number_id),
                "username": username
            })
            
            if not number:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Número no encontrado"
                )
            
            return {
                "id": str(number["_id"]),
                "value": number["value"],
                "created_at": number["created_at"]
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo número por ID: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error obteniendo el número"
            )
    
    @staticmethod
    async def update_number(username: str, number_id: str, new_value: int) -> Dict:
        """Actualizar un número existente"""
        try:
            db = get_database()
            collection = db["numbers"]
            
            if not ObjectId.is_valid(number_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID inválido"
                )
            
            result = await collection.update_one(
                {"_id": ObjectId(number_id), "username": username},
                {"$set": {"value": new_value}}
            )
            
            if result.matched_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Número no encontrado"
                )
            
            logger.info(f"Número {number_id} actualizado para usuario {username}")
            
            return await NumberService.get_number_by_id(username, number_id)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error actualizando número: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error actualizando el número"
            )
    
    @staticmethod
    async def delete_number(username: str, number_id: str) -> Dict:
        """Eliminar un número"""
        try:
            db = get_database()
            collection = db["numbers"]
            
            if not ObjectId.is_valid(number_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID inválido"
                )
            
            result = await collection.delete_one({
                "_id": ObjectId(number_id),
                "username": username
            })
            
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Número no encontrado"
                )
            
            logger.info(f"Número {number_id} eliminado para usuario {username}")
            
            return {"message": "Número eliminado exitosamente"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error eliminando número: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error eliminando el número"
            )
    
    @staticmethod
    async def get_stats(username: str) -> Dict:
        """Obtener estadísticas de los números del usuario"""
        try:
            db = get_database()
            collection = db["numbers"]
            
            cursor = collection.find({"username": username})
            numbers = await cursor.to_list(length=None)
            
            if not numbers:
                return {
                    "username": username,
                    "total_numbers": 0,
                    "average": 0,
                    "maximum": 0,
                    "minimum": 0
                }
            
            values = [num["value"] for num in numbers]
            
            stats = {
                "username": username,
                "total_numbers": len(values),
                "average": sum(values) / len(values),
                "maximum": max(values),
                "minimum": min(values)
            }
            
            logger.info(f"Estadísticas calculadas para usuario {username}")
            
            return stats
        except Exception as e:
            logger.error(f"Error calculando estadísticas: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error calculando estadísticas"
            )