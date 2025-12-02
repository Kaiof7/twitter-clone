from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime
from typing import Optional, List

# ----------------------------
# Modelos de Usuário
# ----------------------------

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="usuario@example.com")

class UserCreate(UserBase):
    name: str = Field(..., min_length=2, max_length=100, example="Fulano da Silva")
    password: str = Field(..., min_length=8, max_length=128, example="senhasegura123")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    email: Optional[EmailStr] = Field(None)

class UserOut(UserBase):
    id: int
    name: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ----------------------------
# Modelos de Tweet
# ----------------------------

class TweetBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class TweetCreate(TweetBase):
    model_config = ConfigDict(from_attributes=True)

class TweetUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)

class TweetOut(TweetBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: Optional["UserOut"] = None   # ← IMPORTANTE: evita erro no Railway
    
    model_config = ConfigDict(from_attributes=True)

class TweetSimpleOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)

# ----------------------------
# Modelos de Autenticação
# ----------------------------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

# ----------------------------
# Relacionamentos
# ----------------------------

class UserWithTweets(UserOut):
    tweets: List[TweetSimpleOut] = []

    model_config = ConfigDict(from_attributes=True)

# Resolve referência circular
TweetOut.update_forward_refs()
