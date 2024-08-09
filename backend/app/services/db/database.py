import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# Update the DATABASE_URL to include the character set
DATABASE_URL = f"{settings.DATABASE_URL}?charset=utf8mb4"

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    echo=False  # Set to True for SQL query logging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables() -> None:
    """
    Create database tables if they don't exist.
    """
    with engine.connect() as connection:
        try:
            # Create users table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(36) UNIQUE,
                    username VARCHAR(50) UNIQUE,
                    email VARCHAR(255) UNIQUE,
                    hashed_password VARCHAR(255),
                    is_active BOOLEAN DEFAULT true
                )
            """))

            # Create intent table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS intent (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    intent_name VARCHAR(255),
                    description TEXT
                )
            """))

            # Create entity table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS entity (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    entity_name VARCHAR(255),
                    intent_id INT,
                    FOREIGN KEY (intent_id) REFERENCES intent(id)
                )
            """))

            # Create messages table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    role VARCHAR(50),
                    content VARCHAR(2000),
                    timestamp FLOAT,
                    relevance FLOAT,
                    user_id VARCHAR(36),
                    adaptive_traits JSON,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """))

            # Create sessions table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    start_time DATETIME,
                    end_time DATETIME,
                    status VARCHAR(50),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))

            # Create feedback table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(36),
                    session_id INT,
                    message_id VARCHAR(36),
                    rating INT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """))

            # Create ai_personalities table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS ai_personalities (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    description TEXT,
                    personality_traits TEXT,
                    character_type VARCHAR(50),
                    available BOOLEAN
                )
            """))

            # Create interaction table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS interaction (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(36),
                    ai_personality_id INT,
                    interaction_type VARCHAR(255),
                    timestamp DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (ai_personality_id) REFERENCES ai_personalities(id)
                )
            """))

            # Create user_preferences table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    preference_type VARCHAR(255),
                    preference_value VARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))

            # Create generated_images table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS generated_images (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    prompt VARCHAR(255),
                    prompt_id VARCHAR(255) UNIQUE,
                    image_url VARCHAR(255),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id INT,
                    ai_personality_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (ai_personality_id) REFERENCES ai_personalities(id),
                    INDEX (prompt),
                    INDEX (prompt_id)
                )
            """))

            logging.debug("Tables created successfully.")

        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            raise
