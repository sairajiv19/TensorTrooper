from schemas import CompanyWrite, CompanyRead
from pydantic import AnyUrl, EmailStr
from uuid import uuid4
import asyncpg
import logging

class CompanyRepository:
    
    # id: UUID = Field(default_factory=uuid4)
    # company_name: str
    # domain: AnyUrl
    # admin_email: EmailStr
    # users: List[Union[UUID, None]] = Field(default_factory=list)  # Reference to User.Id only
    
    
    @staticmethod
    async def create_company(connection: asyncpg.Connection, company: CompanyWrite):
        _id = uuid4()
        try:
            await connection.execute('''INSERT INTO company (id, company_name, domain, admin_email)
                               VALUES ($1, $2, $3, $4)''', _id, company.company_name, company.domain, company.admin_email)
        except Exception:
            logging.error("Error inserting values in company!")
        pass
    
    @staticmethod
    async def add_users():
        pass