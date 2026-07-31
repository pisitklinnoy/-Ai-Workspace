"""
Presentation Layer (Section 2.1 & 3.1 in Report):
Exposes HTTP endpoints using APIRouter.
Validates input requests via Pydantic Schemas, delegates execution to AuthService,
and returns JSON responses with appropriate HTTP Status Codes.
"""

from fastapi import APIRouter, Depends, status
from app.schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse
from app.schemas.token import TokenResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_auth_service, get_current_user

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication API (Login / Signin)"]
)

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User Signup / Registration",
    description="Accepts user signup details, validates schema, hashes password, and saves user without returning password."
)
def signup(
    request: UserRegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Presentation Layer Endpoint for User Signup / Register:
    - Receives HTTP POST request with JSON body (UserRegisterRequest)
    - Delegates registration rules to AuthService
    - Returns HTTP 201 Created with UserResponse schema (password masked)
    """
    created_user = auth_service.register_user(request)
    return created_user

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login / Signin",
    description="Authenticates credentials and returns a Bearer JWT Token."
)
def login(
    request: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Presentation Layer Endpoint for User Login / Signin:
    - Receives HTTP POST request with login credentials
    - Verifies user via AuthService
    - Returns HTTP 200 OK with access_token (JWT)
    """
    token_data = auth_service.authenticate_user(request)
    return token_data

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Authenticated User Profile",
    description="Protected endpoint demonstrating token verification using Dependency Injection."
)
def get_me(
    current_user: dict = Depends(get_current_user)
):
    """
    Demonstration of Protected Endpoint using JWT token verification.
    """
    return current_user
