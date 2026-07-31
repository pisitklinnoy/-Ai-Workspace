"""
Application Instance & Server Entrypoint (Section 1 & 8 in Report):
Configures FastAPI instance, registers routers, and starts server with Uvicorn.
"""

from fastapi import FastAPI
from app.routers import auth
from app.core.config import settings

# 1. Application Instance (PDF Page 2)
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## FastAPI Example: Login & Signin API Architecture
    
    This example demonstrates how to structure a clean, maintainable, and secure **FastAPI Authentication API**
    following the principles outlined in the project report:
    
    * **Separation of Concerns & Layer Architecture**:
      - **Presentation Layer**: `app/routers/auth.py` (Endpoints & HTTP handling)
      - **Application Layer**: `app/core/dependencies.py` & `config.py` (Dependency Injection `Depends()`, `.env`)
      - **Business Logic Layer**: `app/services/auth_service.py` (Registration & Authentication rules)
      - **Data Layer**: `app/repositories/user_repository.py` & `db/` (Data persistence queries)
    * **Data Validation & Schemas**: Request validation & Response models hiding sensitive fields (`password`).
    * **Security**: Bcrypt password hashing & JWT Access Tokens.
    * **Automatic Docs**: Interactive Swagger UI testing at `/docs`.
    """,
    version="1.0.0",
    docs_url="/docs",     # Automatic Docs (Swagger UI)
    redoc_url="/redoc"
)

# 2. Routing System (PDF Page 2) - Include Authentication Router
app.include_router(auth.router)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "message": "FastAPI Authentication API is running",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
