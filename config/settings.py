import os
from dotenv import load_dotenv

load_dotenv()
default_url_db = 'mongodb://admin:admin123@mongodb_numbers_api:27017/numbers_db?authSource=admin'

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "G)Xbn=k[!gM*(0UT&_V:euwV!3]xM5")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    MONGODB_URL: str = os.getenv("MONGODB_URL", default_url_db)
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "numbers_db")
    
    # Usuario predefinido
    DEFAULT_USERNAME: str = "admin"
    DEFAULT_PASSWORD: str = "1234"

settings = Settings()