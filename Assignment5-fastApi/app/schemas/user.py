from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# --- Request Models (Input Validation - PDF Page 2 & Page 8) ---

class UserRegisterRequest(BaseModel):
    """Schema for signup / user registration request."""
    username: str = Field(..., min_length=3, max_length=50, description="Username for login", example="somchai")
    email: EmailStr = Field(..., description="Valid user email address", example="somchai@example.com")
    full_name: str = Field(..., min_length=1, max_length=100, description="Full name of user", example="Somchai Dee")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)", example="secret1234")

class UserLoginRequest(BaseModel):
    """Schema for login request."""
    username: str = Field(..., description="Username or Email", example="somchai")
    password: str = Field(..., description="Password", example="secret1234")


# --- Response Models (Masking Sensitive Data - PDF Page 2 & Page 8) ---

class UserResponse(BaseModel):
    """
    Response model controlling output structure and masking sensitive data (e.g., password / hashed_password).
    """
    id: int
    username: str
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
