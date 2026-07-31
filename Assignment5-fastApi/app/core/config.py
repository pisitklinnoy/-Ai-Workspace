import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file (as recommended in PDF report page 6)
load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI Auth System (Best Practice Demo)")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-jwt-token-generation-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()
