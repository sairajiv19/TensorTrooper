from schemas import CompanyWrite, CompanyRead, UserWrite, UserRead
from user import UserRepository
from pydantic import AnyUrl, EmailStr
from uuid import uuid4, UUID
from typing import List
import asyncpg
import logging

class CompanyRepository:
    
    
    @staticmethod
    async def create_company(connection: asyncpg.Connection, company: CompanyWrite):
        _id = uuid4()
        try:
            await connection.execute('''INSERT INTO company (id, company_name, domain, admin_email)
                               VALUES ($1, $2, $3, $4)''', _id, company.company_name, company.domain, company.admin_email)
        except Exception:
            logging.error("Error inserting values in company.")
        
    @staticmethod
    async def list_users(conn: asyncpg.Connection) -> List[UserRead]:
        records = await conn.fetch(
            "SELECT (id, username, first_name, last_name, email, phone_number, role) FROM users"
        )
        return [UserRead(**dict(r)) for r in records]
    
    
    @staticmethod
    async def add_user(connection: asyncpg.Connection, user: UserWrite):
        try:
            f = await UserRepository.create_user(connection, user)
        except Exception:
            logging.error("Error creating a new user.")
            f = False
        return f
        
    @staticmethod
    async def remove_user(connection: asyncpg.Connection, username: str = None, _id: str = None):
        try:
            if username:
                await UserRepository.delete_user_by_username(connection, username)
            else:
                _id = UUID(_id)
                await UserRepository.delete_user_by_id(connection, _id)
        except Exception:
            logging.error("Error removing the user.")
    
    @staticmethod
    async def update_user_modedrator():
        pass
    
    @staticmethod
    async def update_user_administrator():
        pass
    # id: UUID = Field(default_factory=uuid4)
    # company_name: str
    # domain: AnyUrl
    # admin_email: EmailStr
    # users: List[Union[UUID, None]] = Field(default_factory=list)  # Reference to User.Id only
    