import asyncio
import asyncpg


async def main():
    conn = await asyncpg.connect(
        user="popcorn", password="popcorn", database="mydb", host="localhost", port=5432
    )

    # User table
    await conn.execute(
        """CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password BYTEA NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    role user_role NOT NULL,
    company_id UUID REFERENCES company(id) ON DELETE CASCADE
    );
    """
    )
    # comapny table
    await conn.execute(
        """CREATE TABLE companies (
    id UUID PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE NOT NULL,
    admin_email VARCHAR(255) UNIQUE NOT NULL
    );"""
    )
    # create index
    await conn.execute(
        """create index users_username
    on users(username);"""
    )


asyncio.run(main())
