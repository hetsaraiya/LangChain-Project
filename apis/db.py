from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
from dotenv import load_dotenv
import os
from apis.logger import logger
load_dotenv(".env.local")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")


try:
    async_engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=False,
    )
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise


try:
    SessionLocal = async_sessionmaker(bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False)
    logger.info("Session maker created successfully.")
except Exception as e:
    logger.error(f"Failed to create session maker: {e}")
    raise

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with SessionLocal() as db:
            logger.info("Database session opened successfully.")
            yield db
    except Exception as e:
        logger.error(f"Error while accessing the database session: {e}")
        raise e
    finally:
        logger.info("Database session closed.")