import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
from urllib.parse import quote_plus
from app.config.logger import get_logger

logger = get_logger("database")

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
user = os.getenv("POSTGRES_USER", "myuser")
password = os.getenv("POSTGRES_PASSWORD", "")
db_name = os.getenv("POSTGRES_DB", "classicmodels")
host = os.getenv("POSTGRES_HOST", "127.0.0.1")
port = os.getenv("POSTGRES_PORT", "5432")

print(f"DEBUG: Connecting as {user} to {db_name} at {host}")

# URL encode the password in case it contains special characters
password_encoded = quote_plus(password) if password else ""

# Build the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password_encoded}@{host}:{port}/{db_name}"

logger.info(f"Connecting to PostgreSQL: {user}@{host}:{port}/{db_name}")

try:
    # Create the SQLAlchemy engine
    # Note: echo=True logs all SQL queries (disable in production)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,  # Test connections before using them
        poolclass=NullPool  # Recommended for development with Docker
    )
    
    # Test the connection
    with engine.connect() as connection:
        logger.info("✓ Successfully established database connection")
    
    # Create session factory
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # Create declarative base for models
    Base = declarative_base()
    
    logger.info("✓ Database initialization complete")

except Exception as e:
    logger.error(f"✗ Database connection failed: {e}")
    logger.error(f"  URL: {SQLALCHEMY_DATABASE_URL}")
    logger.error(f"  Host: {host}")
    logger.error(f"  Port: {port}")
    logger.error(f"  Database: {db_name}")
    logger.error(f"  User: {user}")
    raise


def get_db():
    """
    Dependency injection function for FastAPI routes.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
