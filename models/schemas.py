from pydantic import BaseModel, EmailStr, Field, AnyUrl
from typing import Optional, List, Union
from uuid import uuid4, UUID
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

# API Request Schema
class CompanyWrite(BaseModel):
    company_name: str
    domain: AnyUrl
    admin_email: EmailStr

    
# DB/API Response Schema
class CompanyRead(BaseModel):
    _id: UUID
    company_name: str
    domain: AnyUrl
    admin_email: EmailStr
    users: List[Union[UUID, None]] = Field(default_factory=list)



# API + DB Response
class UserRead(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: Role


# API + DB Write Schema
class UserWrite(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    role: Role = Role.user
