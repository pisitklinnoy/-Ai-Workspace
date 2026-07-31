"""
Business Logic Layer (Section 2.3 & 3.1 in Report):
Handles core application rules: signup validation, password hashing, credential verification,
and JWT token creation. Completely independent of HTTP requests and DB specifics (Loose Coupling).
"""

from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, request: UserRegisterRequest) -> dict:
        """
        Business Logic for User Registration (Signup):
        1. Check duplicate username using UserRepository.get_user_by_username
        2. Check duplicate email using UserRepository.get_user_by_email
        3. Hash raw password using bcrypt (Never store plain password)
        4. Save user via UserRepository.save_user
        """
        if self.user_repo.get_user_by_username(request.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{request.username}' is already registered."
            )

        if self.user_repo.get_user_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{request.email}' is already registered."
            )

        # 3. Hash password using bcrypt
        hashed_pwd = hash_password(request.password)

        # 4. Delegate database insertion to Data Layer
        new_user = self.user_repo.save_user(
            username=request.username,
            email=request.email,
            full_name=request.full_name,
            hashed_password=hashed_pwd
        )
        return new_user

    def authenticate_user(self, request: UserLoginRequest) -> dict:
        """
        Business Logic for User Authentication (Login / Signin):
        1. Find user by username or email
        2. Verify plain password against hashed password
        3. Check account active status
        4. Issue JWT access token
        """
        user = self.user_repo.get_user_by_username(request.username)
        if not user:
            user = self.user_repo.get_user_by_email(request.username)

        if not user or not verify_password(request.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive."
            )

        # 4. Generate JWT access token
        token_data = {"sub": str(user["id"]), "username": user["username"]}
        access_token = create_access_token(data=token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"]
            }
        }
