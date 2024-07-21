import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:example@localhost:5432/postgres')

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


try:
    session = get_async_session()
    print('Database connection successful')
    session.aclose()
except Exception as e:
    print(f'Database connection error: {e}')
