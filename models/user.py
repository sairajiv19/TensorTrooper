from pydantic import BaseModel, EmailStr, Field, AnyUrl
from typing import Optional, List
from uuid import uuid4, UUID
import bcrypt
import asyncpg
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class User(BaseModel): # need to define CRUD methods!
    id: UUID = Field(..., alias="_id")
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    hashed_pw: bytes
    role: Role



class Company(BaseModel):
    id: UUID
    company_name: str
    domain: AnyUrl
    users: List[UUID] = Field(default_factory=list) # Reference to User.Id only
