from pydantic import BaseModel, EmailStr, Field, AnyUrl
from typing import Optional, List, Union
from uuid import uuid4, UUID
import bcrypt
import asyncpg
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class Company(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    company_name: str
    domain: AnyUrl
    admin_email: EmailStr
    users: List[UUID] = Field(default_factory=list)  # Reference to User.Id only


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


# Class for utility functions
class UserRepository:
    
    @staticmethod
    async def create_user(conn: asyncpg.Connection, user: UserWrite) -> bool:
        hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        _id = uuid4()
        await conn.execute(
            """
            INSERT INTO users (id, username, first_name, last_name, email, phone_number, hashed_pw, role)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            _id,
            user.username,
            user.first_name,
            user.last_name,
            user.email,
            user.phone_number,
            hashed_pw,
            user.role.value,
        )
        return True

    @staticmethod
    async def get_user_by_id(conn: asyncpg.Connection, user_id: UUID) -> Optional[UserRead]:
        record = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        return UserRead(**dict(record)) if record else None

    @staticmethod
    async def get_user_by_username(conn: asyncpg.Connection, username: str) -> Optional[UserRead]:
        record = await conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
        return UserRead(**dict(record)) if record else None

    # Move to companies
    @staticmethod
    async def list_users(conn: asyncpg.Connection) -> List[UserRead]:
        records = await conn.fetch("SELECT * FROM users")
        return [UserRead(**dict(r)) for r in records]

    
    # based on role mod -> names, phone number only; admin -> everything
    @staticmethod
    async def update_user(conn: asyncpg.Connection, user_id: UUID, updates: dict) -> Optional[UserRead]:
        if not updates:
            return None
        set_clause = ", ".join([f"{k} = ${i+2}" for i, k in enumerate(updates.keys())])
        query = f"UPDATE users SET {set_clause} WHERE id = $1 RETURNING *"
        record = await conn.fetchrow(query, user_id, *updates.values())
        return UserRead(**dict(record)) if record else None

    @staticmethod
    async def delete_user(conn: asyncpg.Connection, user_id: UUID) -> bool:
        result = await conn.execute("DELETE FROM users WHERE id = $1", user_id)
        return result.split(" ")[1] == "1"
