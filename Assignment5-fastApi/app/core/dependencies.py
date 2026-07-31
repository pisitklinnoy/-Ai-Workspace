"""
Application Layer (Section 2.2 in Report):
Manages Dependency Injection via FastAPI's Depends() mechanism.
Reduces code duplication across endpoints (Reusability).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.core.security import decode_access_token

# OAuth2 bearer token scheme for swagger UI integration & request parsing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_user_repository() -> UserRepository:
    """Dependency injection provider for UserRepository (Data Layer)."""
    return UserRepository()

def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    """Dependency injection provider for AuthService (Business Logic Layer)."""
    return AuthService(user_repo=user_repo)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository)
) -> dict:
    """
    Dependency Injection for protected endpoints (Page 6 in Report).
    Validates incoming JWT token and returns authenticated user object.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing user identifier.",
        )

    user = user_repo.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authenticated user account not found.",
        )
    return user
