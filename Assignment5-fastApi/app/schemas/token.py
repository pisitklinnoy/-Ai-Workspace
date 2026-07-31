from pydantic import BaseModel
from typing import Dict, Any

class TokenResponse(BaseModel):
    """Schema for login JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    user: Dict[str, Any]
