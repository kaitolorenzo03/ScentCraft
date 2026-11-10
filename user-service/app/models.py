
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

class WardrobeItem(BaseModel):
    perfume_id: str
    perfume_name: str
    brand: str
    category: str  # "signature", "owned", "wishlist"

class WardrobeResponse(BaseModel):
    username: str
    items: list[WardrobeItem]