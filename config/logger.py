import logging
import os
from datetime import datetime

# Crear carpeta de logs si no existe
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configurar el logger
# Solo usar archivo en producción, en desarrollo solo consola
USE_FILE_LOGGING = os.getenv("USE_FILE_LOGGING", "False").lower() == "true"

handlers = [logging.StreamHandler()]

if USE_FILE_LOGGING:
    log_filename = f"logs/api_{datetime.now().strftime('%Y%m%d')}.log"
    handlers.append(logging.FileHandler(log_filename))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger("FastAPI_App")