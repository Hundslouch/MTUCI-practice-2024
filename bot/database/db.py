from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
from config import (
    DB_USER as POSTGRES_USER,
    DB_PASSWORD as POSTGRES_PASSWORD,
    DB_HOST as POSTGRES_HOST,
    DB_PORT as POSTGRES_PORT,
    DB_NAME as POSTGRES_DB,
)

Base = declarative_base()

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(
    DATABASE_URL, poolclass=NullPool, echo=False, pool_pre_ping=True
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
