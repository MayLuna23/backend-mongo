from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings
from config.logger import logger

class Database:
    client: AsyncIOMotorClient = None
    
db = Database()


async def connect_to_mongo():
    """Conectar a MongoDB"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)

        # Intentar un 'ping' para verificar la conexión
        await db.client.admin.command('ping')
        
        logger.info("Conexión exitosa a MongoDB")
    except Exception as e:
        logger.error(f"Error conectando a MongoDB")
        raise e


async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    try:
        db.client.close()
        logger.info("Conexión a MongoDB cerrada")
    except Exception as e:
        logger.error(f"Error cerrando conexión a MongoDB: {e}")

def get_database():
    """Obtener instancia de la base de datos"""
    return db.client[settings.DATABASE_NAME]