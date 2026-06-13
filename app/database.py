import logging
import re

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

logger = logging.getLogger(__name__)

# Ensure the asyncpg dialect is used. Railway's DATABASE_URL is typically
# postgresql:// (psycopg2), which is incompatible with SQLAlchemy's async
# extension. Replace the scheme so asyncpg is always the driver.
database_url = settings.DATABASE_URL

# Log the raw DATABASE_URL with the password masked so we can verify the
# value Railway is injecting without leaking credentials to the log stream.
_masked_original = re.sub(r"(?<=:\/\/[^:]+:)[^@]+(?=@)", "****", database_url)
logger.info("DATABASE_URL (original): %s", _masked_original)

if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)

_masked_transformed = re.sub(r"(?<=:\/\/[^:]+:)[^@]+(?=@)", "****", database_url)
logger.info("DATABASE_URL (transformed): %s", _masked_transformed)

try:
    engine = create_async_engine(database_url, echo=False, future=True)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error("Failed to create database engine: %s", e, exc_info=True)
    raise
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
