import sys
import os

# Add backend directory to sys.path so we can import core.config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings

def main():
    print("=== Testing Settings (Pydantic BaseSettings) ===")
    print(f"PROJECT_NAME         : {settings.PROJECT_NAME}")
    print(f"REDIS_HOST           : {settings.REDIS_HOST}")
    print(f"REDIS_PORT           : {settings.REDIS_PORT}")
    print(f"POSTGRES_USER        : {settings.POSTGRES_USER}")
    print(f"POSTGRES_PASSWORD    : {settings.POSTGRES_PASSWORD}")
    print(f"POSTGRES_DB          : {settings.POSTGRES_DB}")
    print(f"POSTGRES_HOST        : {settings.POSTGRES_HOST}")
    print(f"POSTGRES_PORT        : {settings.POSTGRES_PORT}")
    print(f"LABEL_STUDIO_URL     : {settings.LABEL_STUDIO_URL}")
    print(f"LABEL_STUDIO_API_KEY : {settings.LABEL_STUDIO_API_KEY}")
    print("==================================================")

if __name__ == "__main__":
    main()
