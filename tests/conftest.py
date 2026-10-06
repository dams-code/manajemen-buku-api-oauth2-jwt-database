import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from sqlalchemy import text

from main import app

from core.database import Base, get_database
from repositories.roles import CekRole
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("USER_DB")
DB_PASSWORD = os.getenv("PASSWORD_DB")
DB_PORT = os.getenv("PORT_DB")
DB_NAME_TEST = os.getenv("DATABASE_DB_TEST")
DB_HOST = os.getenv("HOST_DB")

DB_url = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_TEST}"

engine_test = create_async_engine(DB_url, echo=False)

AsyncLocalSessionTest = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    
    yield

    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    
    await engine_test.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncLocalSessionTest() as sesi_db_test:
        yield sesi_db_test

    async with engine_test.begin() as connection:
        await connection.execute(
            text("TRUNCATE TABLE dpeminjaman, hpeminjaman, member, buku RESTART IDENTITY CASCADE;")
        )

@pytest_asyncio.fixture(scope="function")
async def client(async_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_database] = override_get_db

    async def mock_cek_role_call(self, request=None, websocket=None):
        return "test2"

    transport = ASGITransport(app=app)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(CekRole, "__call__", mock_cek_role_call)

        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()
