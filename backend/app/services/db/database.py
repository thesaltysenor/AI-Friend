import pymysql
import logging
from app.core.config import settings

def get_db_connection():
    return pymysql.connect(
        host=settings.MYSQL_HOSTNAME,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DB,
        port=settings.MYSQL_PORT
    )

def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            logging.debug("Creating users table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(36) UNIQUE,
                    username VARCHAR(50) UNIQUE,
                    email VARCHAR(255) UNIQUE,
                    hashed_password VARCHAR(255),
                    is_active BOOLEAN DEFAULT true
                )
            """)

            logging.debug("Creating intent table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intent (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    intent_name VARCHAR(255),
                    description TEXT
                )
            """)

            logging.debug("Creating entity table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entity (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    entity_name VARCHAR(255),
                    intent_id INT,
                    FOREIGN KEY (intent_id) REFERENCES intent(id)
                )
            """)

            logging.debug("Creating messages table...")
            cursor.execute("""
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
            """)

            logging.debug("Creating sessions table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    start_time DATETIME,
                    end_time DATETIME,
                    status VARCHAR(50),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            logging.debug("Creating feedback table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(36),
                    session_id INT,
                    message_id VARCHAR(36),
                    rating INT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """)

            logging.debug("Creating ai_personality table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai_personality (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    description TEXT,
                    personality_traits TEXT,
                    character_type VARCHAR(50),
                    available BOOLEAN
                )
            """)

            logging.debug("Creating interaction table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interaction (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(36),
                    ai_personality_id INT,
                    interaction_type VARCHAR(255),
                    timestamp DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (ai_personality_id) REFERENCES ai_personality(id)
                )
            """)

            logging.debug("Creating user_preferences table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    preference_type VARCHAR(255),
                    preference_value VARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            logging.debug("Tables created successfully.")

        connection.commit()
    except Exception as e:
        logging.error(f"Error creating tables: {e}")
    finally:
        connection.close()
